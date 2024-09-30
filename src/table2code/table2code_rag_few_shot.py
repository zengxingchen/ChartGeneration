import os
import json
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import random
from table2code_echart import generate_diversified_echart_code
from table2code_python import generate_diversified_python_code
from table2code_vega import generate_diversified_vega_lite_code

def get_generator_function(method):
    generator_mapping = {
        "vega-lite": generate_diversified_vega_lite_code,
        "echart": generate_diversified_echart_code,
        "matplot": generate_diversified_python_code,
        "seaborn": generate_diversified_python_code,
    }
    return generator_mapping.get(method, None)

def load_closest_features_info(json_file_path):
    """Load precomputed closest feature file information from a JSON file."""
    with open(json_file_path, 'r') as f:
        closest_features_info = json.load(f)
    return closest_features_info

def find_closest_features_from_precomputed(closest_features_info, target_feature_name):
    """Find the closest three feature file names from precomputed information based on the target feature filename."""
    # Get the value (closest three filenames) corresponding to the target feature filename from the loaded info (dictionary)
    closest_features = closest_features_info.get(target_feature_name, [])
    return closest_features

def main(data_table_dir, seed_dir, save_dir, chart_type, method, max_workers):
    os.makedirs(save_dir, exist_ok=True)

    csv_file_paths = [os.path.join(data_table_dir, f) for f in os.listdir(data_table_dir) if f.endswith('.csv')]
    all_json_files = [os.path.join(seed_dir, f) for f in os.listdir(seed_dir) if f.endswith('.json')]
    json_dir = os.path.join("..", f"{method}_generation", chart_type)
    precomputed_json_path = [os.path.join(json_dir, f) for f in os.listdir(json_dir) if f.endswith('.json')]
    closest_features_info = load_closest_features_info(precomputed_json_path)
    generate_function = get_generator_function(method)

    if len(all_json_files) > 3:
        args_list = []
        for csv_file_path in csv_file_paths[:]:
            print('Processing file:', csv_file_path)
            target_feature_name = os.path.basename(csv_file_path).replace('.csv', '.json')
            closest_feature_files = find_closest_features_from_precomputed(closest_features_info, target_feature_name)
            closest_json_files = [os.path.join(seed_dir, feature_file) for feature_file in closest_feature_files]
            random_json_file = random.choice(all_json_files)
            random_json_file_2 = random.choice(all_json_files)
            closest_json_files.append(random_json_file)
            closest_json_files.append(random_json_file_2)
            args_list.append((closest_json_files, csv_file_path, save_dir, chart_type))
    else:
        args_list = []
        for csv_file_path in csv_file_paths[:]:
            print('Processing file:', csv_file_path)
            target_feature_name = os.path.basename(csv_file_path).replace('.csv', '.json')
            closest_json_files = all_json_files
            args_list.append((closest_json_files, csv_file_path, save_dir, chart_type))

    # Use ThreadPoolExecutor instead of Pool
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks using the submit method
        futures = [executor.submit(generate_function, args) for args in args_list]
        # Wait for all tasks to complete using the as_completed method
        for future in tqdm(as_completed(futures), total=len(args_list), desc='Processing files'):
            try:
                # Get the result of the task; if there's an exception, it will be raised
                future.result()
            except Exception as exc:
                print(f'Generated exception: {exc}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Vega-Lite code from CSV data using OpenAI API.")
    parser.add_argument('--method', type=str, required=True,
                    help='Type of method (e.g., matplot, echart, seaborn, etc.)')
    parser.add_argument('--chart_type', type=str, required=True,
                    help='Type of chart to generate (e.g., bar_chart, line_chart, pie_chart, etc.)')
    
    parser.add_argument('--data_table_dir', type=str, default=r"table",
                        help='Directory path containing CSV tables')

    parser.add_argument('--seed_dir', type=str, default=r"seed\code",
                        help='Directory path containing CSV tables')

    parser.add_argument('--save_dir', type=str, default=r'expanded_seed',
                        help='Directory path to save generated Vega-Lite JSON files')

    parser.add_argument('--max_workers', type=int, default=1000,
                        help='Maximum number of processes to use for concurrent requests. Defaults to number of CPUs')
    parser.add_argument('--multiprocessing', type=bool, default=True)

    args = parser.parse_args()
    args.data_table_dir = os.path.join("..", f"{args.method}_generation", args.chart_type, args.data_table_dir)
    args.save_dir = os.path.join("..", f"{args.method}_generation", args.chart_type, args.save_dir)
    args.seed_dir = os.path.join("..", f"{args.method}_generation", args.chart_type, args.seed_dir)

    os.makedirs(args.save_dir, exist_ok=True)
    main(data_table_dir=args.data_table_dir, seed_dir=args.seed_dir, save_dir=args.save_dir, chart_type=args.chart_type, method=args.method,
         max_workers=args.max_workers)

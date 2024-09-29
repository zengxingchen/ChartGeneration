import os
import json
import re
import argparse
import pandas as pd
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import csv
import random
topics_pool = [
    "Future Technologies & Society", "Art & Design", "Science & Nature",
    "Health & Psychology", "Culture & Society", "Economics & Finance",
    "Education & Learning", "Entertainment & Leisure", "Environment & Climate Change",
    "Food & Nutrition", "Travel & Adventure", "Fashion & Beauty",
    "Politics & Governance", "Sports & Fitness", "History & Archaeology",
    "Philosophy & Ethics", "Music & Performing Arts", "Literature & Writing",
    "Business & Entrepreneurship", "Astronomy & Space Exploration"
]

def load_matplotlib_code(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def extract_and_save_data(plot_code, csv_path):
    """
    Extracts data from the Matplotlib code and saves it to a CSV file.
    """
    # Assuming the data is provided in the Matplotlib code as a list of dictionaries
    data_match = re.search(r'data\s*=\s*(\[[^\]]+\])', plot_code)
    if data_match:
        data_str = data_match.group(1)
        data = json.loads(data_str.replace("'", '"'))
        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False)
        print(f'Saved data to {csv_path}')
    else:
        print(f"No data found in the Matplotlib code for {csv_path}")

def generate_diversified_vega_lite_code(args):
    # client = OpenAI(base_url='',
    #     api_key='')
    client = OpenAI(base_url='',
        api_key='')
    file_path, save_dir = args
    original_vl_code = load_matplotlib_code(file_path)
    # with open(file_path, 'r') as json_file:
    #     original_vl_code = json.load(json_file)
        
    # original_vl_code = remove_data_property(original_vl_code)

    filename = os.path.basename(file_path)
    print(filename)
    random.shuffle(topics_pool)
    # Constructing the prompt for GPT-4 to diversify the given Vega-Lite code
    # 6. Add text labels (or remove) in reasonable positions, but avoid give text label in stacked bar to prevent clutter.\
    prompt_messages = [
        {"role": "system", "content": "You are a highly intelligent AI familiar with data visualization and seaborn."},
        {"role": "user", "content": "Given the following seaborn code of a line chart: " + original_vl_code +
         " Please generate a diversified version of this seaborn code of line chart. Here are some options you should follow:\
            1. Generate data points that fit the chart type, but you should not skip any data point in your code. Do not add any comment in your code\
            2. Add or change some data point with new corresponding values to enrich the visualization.\
            print the final table data you use in the code within triple backticks (```), and don't include things like csv, plaintext in the triple backticks (```).\
            3. Modify the color scheme using specific color codes (e.g., #RRGGBB) for better clarity or visual appeal. Avoid using color categories.\
            4. change width and height of the chart reasonably\
            5. change the trend of data (down/up/cross)\
            6. change the topic,headline and data type (which fit the topic) of the chart,put the headline in appropriate place that does not overlap with other things (make sure the headline does not overlap with legend! put these two things away), you can refer and choose one (not all) of the topic from: " +str(topics_pool) + " but reduce using global...topic \
            7. assign annotation/label in the chart\
            Do not use random data\
            You should choose some of these options not all of them to diversfy the visualization\
            different data points should have different values\
            You should give FULL code with ALL datapoints and don't miss any detail\
            print table data first, the table data format should be able to directly write in csv file, then print your code\
            Include the code with ``` ``` format."}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=prompt_messages
    )
    print(response)
    try:
        # Attempt to extract the Vega-Lite code from the response
        assistant_reply = response.choices[0].message.content

        
        vega_lite_code_blocks = re.findall(
            r'```(.*?)```', assistant_reply, re.DOTALL)
        assert vega_lite_code_blocks[0] != ''
        # code for table
        table = vega_lite_code_blocks[0]
        print(table)
        # csv_data = re.findall(r'```(.*?)```', table, re.DOTALL)
        csv_data = table
        if csv_data and isinstance(csv_data[0], str):
            # csv_data = csv_data[0].strip()
            if csv_data.startswith('json'):
                csv_data = csv_data.lstrip('json')
            if csv_data.startswith('csv'):
                csv_data = csv_data.lstrip('csv')
            if csv_data.startswith('plaintext'):
                csv_data = csv_data.lstrip('plaintext')
            csv_lines = csv_data.split('\n')

            # 提取实体数量
            filename_pre = filename.split('.')[0]
            file_path = os.path.join(save_dir, f'_15_{filename_pre}.csv')

            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for line in csv_lines:
                    writer.writerow(line.replace('"', '').split(','))

            print(f"table data saved to {file_path}")
        # code for code
        vega_lite_code = vega_lite_code_blocks[1].strip()


        if vega_lite_code.startswith('python'):
            vega_lite_code = vega_lite_code.lstrip('python')
        if vega_lite_code.startswith('json'):
            vega_lite_code = vega_lite_code.lstrip('json')
        # vega_lite_code = json.loads(vega_lite_code)

        # Save the diversified Vega-Lite code as a JSON file
        diversified_json_path = os.path.join(save_dir, f"_15_{filename}")
        with open(diversified_json_path, 'w', encoding='utf-8') as file:
            file.write(vega_lite_code)
        print(f'Saved diversified python code to {diversified_json_path}')
    except Exception as e:
        print(f"Failed to generate diversified code for {filename}: {e}")



def main(data_dir, save_dir, max_workers):
    os.makedirs(save_dir, exist_ok=True)
    file_paths = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.py')]
    
    args_list = [(file_path, save_dir) for file_path in file_paths]
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(generate_diversified_vega_lite_code, args) for args in args_list]
        for future in tqdm(as_completed(futures), total=len(args_list), desc='Processing files'):
            try:
                future.result()
            except Exception as exc:
                print(f'Generated exception: {exc}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Vega-Lite code from CSV data using OpenAI API.")
    parser.add_argument('--data_dir', type=str, default=r"enriched_charts",
                        help='Directory path containing CSV tables')
    parser.add_argument('--save_dir', type=str, default=r'enriched_charts',
                        help='Directory path to save generated Vega-Lite JSON files')

    parser.add_argument('--max_workers', type=int, default=100,
                        help='Maximum number of processes to use for concurrent requests. Defaults to number of CPUs')
    parser.add_argument('--multiprocessing', type=bool, default=True)

    args = parser.parse_args()
    os.makedirs(args.save_dir, exist_ok=True)
    main(data_dir=args.data_dir, save_dir=args.save_dir, max_workers=args.max_workers)
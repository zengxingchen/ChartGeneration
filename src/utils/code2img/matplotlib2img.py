import os
import matplotlib.pyplot as plt
import numpy as np
import concurrent.futures

# Set file paths
matplotlib_code_folder_path = r''  # Replace with the folder path containing Matplotlib code files
output_folder_path = r''  # Replace with the folder path to store output images

# Ensure the output folder exists
os.makedirs(output_folder_path, exist_ok=True)

def process_file(filename):
    if not filename.endswith('.py'):
        return

    file_path = os.path.join(matplotlib_code_folder_path, filename)
    output_file_path = os.path.join(output_folder_path, filename.replace('.py', '.png'))

    # Check if the target file already exists
    if os.path.exists(output_file_path):
        print(f"{output_file_path} already exists, skipping.")
        return

    # Read the content of the Matplotlib code file
    with open(file_path, 'r') as file:
        code = file.read()

    # Replace plt.show() with nothing to prevent plt.show() from clearing the image
    code = code.replace('plt.show()', '')  # Remove plt.show()

    # Execute the Matplotlib code
    try:
        exec(code, {'plt': plt, 'np': np})
        
        # Save the generated chart as an image
        plt.savefig(output_file_path)
        plt.close()
        print(f"{filename} has been successfully converted to an image and saved.")
    except Exception as e:
        print(f"Error executing {filename}: {e}")

if __name__ == '__main__':
    # Specify the number of processes
    num_processes = 10

    # Use multiprocessing to handle files
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        executor.map(process_file, os.listdir(matplotlib_code_folder_path))

    print("All Matplotlib code files have been converted to images and saved.")

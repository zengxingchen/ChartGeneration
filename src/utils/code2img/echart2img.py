import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from http.server import SimpleHTTPRequestHandler
import socketserver
import threading
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

# Set file paths
html_folder_path = r''  # Replace with the folder path where HTML files are stored
output_folder_path = r''  # Replace with the folder path where output images will be stored

# Ensure the output folder exists
os.makedirs(output_folder_path, exist_ok=True)

# Start the local HTTP server
PORT = 8000
Handler = SimpleHTTPRequestHandler

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

httpd = ThreadedTCPServer(("", PORT), Handler)

def start_server():
    os.chdir(html_folder_path)
    httpd.serve_forever()

thread = threading.Thread(target=start_server)
thread.daemon = True
thread.start()

time.sleep(2)  # Ensure the server has started

# Start the local HTTP server
server_url = f'http://localhost:{PORT}/'

def process_html_file(filename):
    # Set Chrome browser options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # Headless mode
    chrome_options.add_argument('--disable-gpu')
    
    # Start Chrome browser
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        screenshot_path = os.path.join(output_folder_path, filename.replace('.html', '.png'))
        
        # Skip if the target file already exists
        if os.path.exists(screenshot_path):
            print(f"{screenshot_path} already exists, skipping...")
            return

        file_url = server_url + urllib.parse.quote(filename)
        
        # Open HTML file
        driver.get(file_url)
        
        # Find the chart container
        chart = driver.find_element(By.ID, 'container')
        
        # Wait for the chart to fully render
        time.sleep(2)  # Adjust the wait time as needed
        
        # Get chart dimensions
        chart_location = chart.location
        chart_size = chart.size
        
        # Set window size
        window_width = chart_location['x'] + chart_size['width']
        window_height = chart_location['y'] + chart_size['height']
        driver.set_window_size(window_width, window_height)
        
        # Screenshot
        chart.screenshot(screenshot_path)
        
        # Crop the image to remove extra borders (optional)
        image = Image.open(screenshot_path)
        cropped_image = image.crop((chart_location['x'], chart_location['y'], chart_location['x'] + chart_size['width'], chart_location['y'] + chart_size['height']))
        cropped_image.save(screenshot_path)
    except Exception as e:
        print(f"Error processing file {filename}: {e}")
    finally:
        # Close the browser
        driver.quit()

# Create a thread pool
with ThreadPoolExecutor(max_workers=100) as executor:
    html_files = [f for f in os.listdir(html_folder_path) if f.endswith('.html')]
    executor.map(process_html_file, html_files)

# Shutdown the HTTP server
httpd.shutdown()
httpd.server_close()

print("All HTML files have been converted to images and saved.")

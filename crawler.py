import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time

urls_file_path = "urls_prova.txt"
base_dir = 'master_courses_html'
os.makedirs(base_dir, exist_ok=True)

# Function to download HTML and save it to a file

def download_and_save_html(url_index_tuple):

    index, url = url_index_tuple
    page_number = (index // 15) + 1
    page_dir = os.path.join(base_dir, f'page_{page_number}')
    filename = f'course_{index % 15 + 1}.html'
    file_path = os.path.join(page_dir, filename)

    if os.path.exists(file_path):
        print(f"Already downloaded: {url}")
        return

    while True:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                html_content = response.text
                page_number = (index // 15) + 1
                page_dir = os.path.join(base_dir, f'page_{page_number}')
                os.makedirs(page_dir, exist_ok=True)
                filename = f'course_{index % 15 + 1}.html'
                filepath = os.path.join(page_dir, filename)
                with open(filepath, 'w', encoding='utf-8') as html_file:
                    html_file.write(html_content)
                return f'Saved HTML content from {url} to {filepath}'

            elif response.status_code == 429:

                print(f"Rate limit hit. Waiting to retry for URL: {url}")
                time.sleep(5)
                continue

        except requests.exceptions.RequestException as e:
            return f'An error occurred while trying to retrieve content from {url}: {e}'


with open(urls_file_path, 'r') as file:
    urls = [line.strip() for line in file]

max_threads = 10

with ThreadPoolExecutor(max_threads) as executor:
    tasks = {executor.submit(download_and_save_html, (i, url)): url for i, url in enumerate(urls)}
    for future in tqdm(as_completed(tasks)):
        print(future.result())
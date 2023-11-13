import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def fetch_course_urls(start_page, end_page, output_file):

    base_url = 'https://www.findamasters.com'
    all_urls = []

    for page in tqdm(range(start_page, end_page + 1)):
        url = f"{base_url}/masters-degrees/msc-degrees/?PG={page}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            a_tags = soup.find_all('a', {'class': 'courseLink'})
            curr_urls = [a.get('href') for a in a_tags]
            print(len(curr_urls))
            all_urls.extend(curr_urls)
        else:
            print(response.status_code)

    with open(output_file, "w") as urls:
        for row in all_urls:
            urls.write(f"{base_url}{str(row)}\n")

fetch_course_urls(1, 400, "urls_prova.txt")

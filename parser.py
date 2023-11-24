import os
import glob
import csv
from bs4 import BeautifulSoup

base_dir = "/Users/c.perrone/PycharmProjects/ADM_HW3/master_courses_html"
output_dir = "/Users/c.perrone/PycharmProjects/ADM_HW3/tsv_output"

def extract_msc_page(base_dir, output_dir):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    counter = 1

    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)

        for html_file in glob.glob(os.path.join(folder_path, '*.html')):
            with open(html_file, 'r', encoding='utf-8') as file:
                html_content = file.read()

            contents = {}

            page_soup = BeautifulSoup(html_content, 'html.parser')

            # course name

            name = page_soup.find('h1', {'class': 'course-header__course-title'})
            if name:
                contents['courseName'] = name.get_text(strip=True)
            else:
                contents['courseName'] = None

            # university name

            university = page_soup.find_all('a', {'class': 'course-header__institution'})
            if university:
                contents['universityName'] = university[0].contents[0]
            else:
                contents['universityName'] = None

            # faculty name

            faculty = page_soup.find_all('a', {'class': 'course-header__department'})
            if faculty:
                contents['facultyName'] = faculty[0].contents[0]
            else:
                contents['facultyName'] = None

            # full/part time

            FullTime_links = page_soup.find_all('a', {'class': 'concealLink'})
            FullTime = False
            for item in FullTime_links:
                if item['href'] == "/masters-degrees/full-time/":
                    FullTime = True
                    break
            contents['isItFullTime'] = FullTime

            # description

            description = page_soup.find('div', {'class': 'course-sections__content'})
            if description:
                paragraphs = description.find_all('p')
                contents['courseDescription'] = ' '.join([p.get_text(strip=True) for p in paragraphs])
            else:
                contents['courseDescription'] = None

            # start date

            start_date = page_soup.find('span', {'class': "key-info__content key-info__start-date py-2 pr-md-3 text-nowrap d-block d-md-inline-block"})
            if start_date:
                contents['startDate'] = start_date.get_text(strip=True)
            else:
                contents['startDate'] = None

            # fees

            fees = page_soup.find('h2', string='Fees')
            if fees:
                fees_content = fees.find_next_sibling('div')
                if fees_content:
                    # Find the <a> tag within this section and extract the text
                    link_element = fees_content.find(['a', 'p'])

                    if link_element:
                        contents['fees'] = link_element.get_text()
                    else:
                        contents['fees'] = None

            # modality

            modality = page_soup.find('span', {'class': 'key-info__content key-info__qualification py-2 pr-md-3 text-nowrap d-block d-md-inline-block'})
            if modality:
                modality_content = modality.find('a')
                if modality_content:
                    contents['modality'] = modality_content.get_text()
                else:
                    contents['modality'] = None

            # duration

            duration = page_soup.find('span', {'class': 'key-info__content key-info__duration py-2 pr-md-3 d-block d-md-inline-block'})
            if duration:
                contents['duration'] = duration.get_text()
            else:
                contents['duration'] = None

            # city

            city = page_soup.find('a', {'class': 'course-data__city'})
            if city:
                contents['city'] = city.get_text()
            else:
                contents['city'] = None

            # country

            country = page_soup.find('a', {'class': 'course-data__country'})
            if country:
                contents['country'] = country.get_text()
            else:
                contents['country'] = None

            # presence

            administration = page_soup.find('a', class_=["course-data__on-campus", "course-data__online"])
            if administration:
                contents['administration'] = administration.get_text()
            else:
                contents['administration'] = None

            url = page_soup.find('link', rel='canonical')
            if url:
                contents['url'] = url['href']
            else:
                contents['url'] = None

            tsv_filename = os.path.join(output_dir, f'course_{counter}.tsv')

            # Write the data to the TSV file
            with open(tsv_filename, 'wt', newline='', encoding='utf-8') as tsv_file:
                writer = csv.DictWriter(tsv_file, fieldnames=contents.keys(), delimiter='\t')
                writer.writeheader()
                writer.writerow(contents)

            print(f"Created {tsv_filename}")

            # Increment the counter for the next file
            counter += 1

extract_msc_page("/Users/c.perrone/PycharmProjects/ADM_HW3/master_courses_html", "/Users/c.perrone/PycharmProjects/ADM_HW3/tsv_output")

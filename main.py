import os.path
import datetime

import requests
import yaml
from bs4 import BeautifulSoup
from linkedin_api import Linkedin

from linkedin_api.utils.helpers import get_id_from_urn

with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)


filepath = data['save_path_local']

user = data['user']
password = data['password']
username = data['username']

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
]




def retrieve_cousera_logo(certification):
    try:

        headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        url = certification['url']
        url = url.replace("/certificate/", "/verify/")
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        image = soup.find('a', {'data-e2e': 'partner-logo-link'}).findNext()['src']
        return image
    except:
        print("Error retrieving image for" + certification['name'])
        return None

def calculate_values():

    api = Linkedin(user, password)
    certifications = api.get_profile_certifications(username)
    for certification in certifications:
        if certification['displaySource'] == 'coursera.org':


                date = datetime.datetime(certification['timePeriod']['startDate']['year'], certification['timePeriod']['startDate']['month'], 1)
                date = date.strftime('%Y-%m-%d %H:%M:%S')
                formatted_date = date + ' -0400'

                image = retrieve_cousera_logo(certification)
                if image is not None:
                    certification['image'] = image


                title = certification['name']
                title_quotes = f'"{title}"'
                title = title.replace(" ", "_")
                full_name = os.path.join(filepath, title + ".md")

                with open(full_name, 'w', encoding='utf-8') as file:

                    file.write("---")
                    file.write('\n')
                    file.write("title: " + title_quotes)
                    file.write('\n')
                    file.write("university: " + certification['authority'])
                    file.write('\n')
                    if 'image' in certification:
                        file.write("background: " + certification['image'])
                        file.write('\n')
                    file.write("description: " + certification['url'])
                    file.write('\n')
                    file.write("date: " + formatted_date)
                    file.write('\n')
                    file.write("---")
                    file.write('\n')

                    file.close()

if __name__ == '__main__':
    calculate_values()


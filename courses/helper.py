# imports
import argparse
import os
import requests
from bs4 import BeautifulSoup

# set up arguments
parser = argparse.ArgumentParser(description='Create base files')
parser.add_argument('folder')
parser.add_argument('url')
args = parser.parse_args()
folder = args.folder
url = args.url

# make folders
os.mkdir(folder)
os.mkdir(folder + '/data')

# request page and make soup
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

# extract info
title = soup.title.string.split('|')[0].strip()

chapters = soup.find_all('h4', {'class': 'chapter__title'})
clean_chapters = []
for c in chapters:
    clean_chapters.append(c.text.strip())

datasets = soup.find_all('li', {'class': 'course__dataset'})
dataset_links = []
for d in datasets:
    dataset_links.append(d.find('a', href=True)['href'])

# download files
for file in dataset_links:
    req = requests.get(file)
    filename = file.split('/')[-1]
    open(folder + '/data/' + filename, 'wb').write(req.content)

# make README
with open(folder + '/README.md', 'w') as file:
    file.write('# [' + title + '](' + url + ')\n\n')
    file.write('## Chapters\n\n')
    for i in range(len(clean_chapters)):
        ch_num = i + 1
        file.write(str(ch_num) + '. ' + clean_chapters[i] + '\n')

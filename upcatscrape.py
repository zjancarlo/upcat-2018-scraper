import requests
import os
from bs4 import BeautifulSoup
import csv

results_directory = 'results'

def process_pagenum(i):
    if i < 10:
        page_num = '00{}'.format(i)
    elif i < 100:
        page_num = '0{}'.format(i)
    else:
        page_num = '{}'.format(i)
    return page_num

def download_results(min=1, max=259):
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)
    for i in range(min, max+1):
        page_num = process_pagenum(i)
        page_url = 'https://upcat.up.edu.ph/results/page-{}.html'.format(page_num)
        page_result = requests.get(page_url)
        with open('{}/{}.html'.format(results_directory, 'page-{}'.format(page_num)), 'w+') as resultsfile:
            resultsfile.write(page_result.text.encode('utf-8'))
            print("Saved page-{}".format(page_num))

def process_page(min, max):
    with open('upcat_results.csv', 'w+') as csvfile:
        csvwriter = csv.writer(csvfile, dialect=csv.excel)
        for i in range(min, max + 1):
            page_num = process_pagenum(i)
            with open('{}/page-{}.html'.format(results_directory, page_num), 'r') as current_page:
                soup = BeautifulSoup(current_page, 'html.parser')
                tables = soup.find_all('table')
                results_table = tables[2]
                for row in results_table.find_all('tr'):
                    columns = row.find_all('td')
                    csvwriter.writerow([column.text.encode('utf-8') for column in columns])
                print("Processed page {}".format(page_num))

def main():
    download_results(1, 259)
    process_page(1, 259)

main()
import requests
import re
from bs4 import BeautifulSoup
import validators
import csv  

n=20
url="https://en.wikipedia.org/wiki/Toronto_Raptors"


def scrape_url(url):
    '''Scrapes the specified URL'''
    if validators.url(url):
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        return soup
    else:
        print('URL is Invalid:')

def iterate_through(url,n):
    '''Gets all links from URL, once the links are scrape it iterates through the first N items and gets all URLS from said items.'''
    urls = []
    scrape=scrape_url(url)
    for link in scrape.find_all('a',attrs={'href': re.compile("^https://")}):
        url=link.get('href')
        urls.append(url)

    for i in range(n):
        url=urls[i]
        if validators.url(url):
            scrape=scrape_url(url)
            for link in scrape.find_all('a',attrs={'href': re.compile("^https://")}):
                if url in urls:
                    pass
                else:
                    url=link.get('href')
                    urls.append(url)
        else:
            print('URL is Invalid:')
        return urls


def COUNT(urls):
    '''Counts both amount of items scraped and unique items.'''
    l1 = []
    UNIQUE_COUNT = 0
    COUNT  = len(urls)
    for item in urls:
        if item not in l1:
            UNIQUE_COUNT += 1
            l1.append(item)
    return COUNT , UNIQUE_COUNT

def ADD_TO_CSV(urls,COUNT):
    '''Appends items to a CSV file.'''
    with open('output.csv', 'w+') as f:
        writer = csv.writer(f)
        for item in urls:
            writer.writerow([item])
        writer.writerow(COUNT)


def main():
    output = iterate_through(url,n)
    output1 = COUNT(output)
    ADD_TO_CSV(output,output1)

if __name__ == "__main__":
    main()

from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re

# a queue of urls to be crawled
new_urls = deque(['https://www.entrepreneur.com/page/271758/'])

# a set of urls that we have already crawled
processed_urls = set()

# a set of crawled emails
emails = set()

# process urls one by one until we exhaust the queue
while len(new_urls):
    # move next url from the queue to the set of processed urls
    url = new_urls.popleft()
    processed_urls.add(url)

#extract base url and path to resolve relative links
parts = urlsplit(url)
base_url = "{0.scheme}://{0.netloc}".format(parts)
path = url[:url.rfind('/')+1] if '/' in parts.path else url

# get url's content
print("Processing %s" % url)
try:
    response = requests.get(url)
    #response.text
except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
    # ignore pages with errors
    pass

# extract all email addresses and add them into the resulting set
new_emails = set(re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', response.text, re.I))
emails.update(new_emails)

# create a beutiful soup for the html document
soup = BeautifulSoup(response.text)

# find and process all the anchors in the document
for anchor in soup.find_all('a'):
    print (anchor)

# extract link url from the anchor
link = anchor.attrs["href"] if "href" in anchor.attrs else ''


# add base url to relative links
if link.startswith('/'):
    link = base_url + link

# add the new url to the queue if it's of HTTP protocol, not enqueued and not processed yet
if link.startswith('http') and not link in new_urls and not link in processed_urls:
    new_urls.append(link)
    print (emails)

import csv
fname = 'output.csv'
with open(fname, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(emails)

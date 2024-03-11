#!/usr/bin/env python

import requests
import configparser
from bs4 import BeautifulSoup
import json
import sys
import os

session = requests.Session()

if os.path.exists('./config.ini'):
    config = configparser.RawConfigParser()
    config.read_file(open('./config.ini'))
else:
    sys.exit()

url = "https://syndication.twitter.com/srv/timeline-profile/screen-name/%s?dnt=false&embedId=&frame=false" % str(config.get('twitter', 'user'))
print(url)
headers = {
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/jxl,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://platform.twitter.com",
    "Host": "syndication.twitter.com",
    "Connection": "keep-alive",
    "Referer": "https://platform.twitter.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers",
    "DNT": "1",
    "Cookie": "auth-token=%s;" % (str(config.get('twitter', 'auth-token')))
}
response = session.get(
    url,
    headers=headers
)

page_soup = BeautifulSoup(response.text, 'lxml')
data = str(page_soup.select("[type='application/json']")[0].contents[0])
data = data.replace("['", "").replace("']", "")
oJson = json.loads(data)
print(oJson['props']['pageProps']['timeline']['entries'])

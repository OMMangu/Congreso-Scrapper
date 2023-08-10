#!/usr/bin/python3

import requests
from fake_useragent import UserAgent

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


def form_url(day, legislatura, main_url):
    fday = f"{day:%d}"
    fmonth = f"{day:%m}"
    return main_url.format(LEGISLATURA=legislatura, DD=fday, MM=fmonth, YY=day.year)


def get_download_link(url, scrap_url):
    soup = get_soup(url)
    results = soup.find("a", download=True)
    if results is None:
        return ""
    return scrap_url.format(zip_url=results["href"])


def get_soup(url):
    ua = UserAgent()
    req = get_request_with_headers(url)
    return BeautifulSoup(req.text, "lxml")


def get_request_with_headers(url: str):
    session = requests.session()
    s_result = session.get(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'referer': url,
        'Cookie': str(requests.utils.dict_from_cookiejar(s_result.cookies))}
    req = requests.get(url, headers=headers)
    return req

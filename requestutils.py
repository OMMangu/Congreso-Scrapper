#!/usr/bin/python3
import requests

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


def form_url(day, main_url):
    fday = f"{day:%d}"
    fmonth = f"{day:%m}"
    return main_url.format(DD=fday, MM=fmonth, YY=day.year)


def get_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, "lxml")


def get_download_link(url, scrap_url):
    soup = get_soup(url)
    results = soup.find("a", download=True)
    if results is None:
        print("No session today, Skipping")
        return ""
    return scrap_url.format(zip_url=results["href"])

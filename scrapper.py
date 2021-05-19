#!/usr/bin/python3
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
import datetime
import re
import requests
import os
import os.path
import zipfile

folder = "files"
os.chdir(".")
SCRAP_URL = "https://www.congreso.es{zip_url}"
MAIN_URL = "https://www.congreso.es/opendata/votaciones?p_p_id=votaciones&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&targetLegislatura=XIV&targetDate={DD}/{MM}/{YY}"


def form_url(day):
    fday = f"{day:%d}"
    fmonth = f"{day:%m}"
    return MAIN_URL.format(DD=fday, MM=fmonth, YY=day.year)


def get_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, "lxml")


def get_download_link(url):
    soup = get_soup(url)
    results = soup.find("a", download=True)
    if results is None:
        print("No session today, Skipping")
        return ""
    return SCRAP_URL.format(zip_url=results["href"])


def get_zip(url, day):
    r = requests.get(url)
    name = "{folder}/{DD}-{MM}-{YY}".format(folder=folder, DD=day.day, MM=day.month, YY=day.year)
    if os.path.isfile(name):
        print("Skipping {name}, already downloaded".format(name=name))
    else:
        print("Saving {name}".format(name=name))
        with open(name + ".zip", 'wb') as f:
            f.write(r.content)
    return name


def create_download_folder():
    if os.path.isdir(folder):
        print("Skipping download folder creation")
    else:
        print("Creating download folder")
        os.mkdir(folder)


def unzip_file(filename):
    with zipfile.ZipFile(filename, "r") as zip_ref:
        for info in zip_ref.infolist():
            if re.match(r'.+\.json', info.filename):
                zip_ref.extract(info, "files/")


def is_final_date(d):
    if d.day == 1 and d.month == 1 and d.year == 2019:
        return True
    return False


def delete_zip(name):
    if os.path.isfile(name):
        os.remove(name)


def main():
    create_download_folder()
    day = datetime.datetime.today() - datetime.timedelta(days=1)
    final_date = False
    while not final_date:
        url = form_url(day)
        zip_link = get_download_link(url)
        if zip_link:
            name = get_zip(zip_link, day)
            unzip_file("{name}.zip".format(name=name))
            delete_zip("{name}.zip".format(name=name))

        day = day - datetime.timedelta(days=1)
        final_date = is_final_date(day)


if __name__ == "__main__":
    main()

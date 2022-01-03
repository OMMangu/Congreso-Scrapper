#!/usr/bin/python3
from dateutils import update_dates
from fileutils import create_download_folder, get_zip, unzip_file, delete_zip
from requestutils import form_url, get_download_link


import datetime
import os.path

folder = "files"
os.chdir(".")
SCRAP_URL = "https://www.congreso.es{zip_url}"
MAIN_URL = "https://www.congreso.es/opendata/votaciones?p_p_id=votaciones&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&targetLegislatura=XIV&targetDate={DD}/{MM}/{YY}"


def main():
    create_download_folder(folder)
    day = datetime.datetime.today() - datetime.timedelta(days=1)
    final_date = False
    while not final_date:
        url = form_url(day, MAIN_URL)
        zip_link = get_download_link(url, SCRAP_URL)
        if zip_link:
            name = get_zip(zip_link, day, folder)
            unzip_file("{name}.zip".format(name=name))
            delete_zip("{name}.zip".format(name=name))

        day, final_date = update_dates(day)


if __name__ == "__main__":
    main()

#!/usr/bin/python3
import datetime
import os.path

from dateutils import update_dates
from db import PostgreDB
from fileutils import create_download_folder, get_zip, unzip_file, delete_zip
from requestutils import form_url, get_download_link

folder = "files_{LEGISLATURA}"
os.chdir(".")
SCRAP_URL = "https://www.congreso.es{zip_url}"
MAIN_URL = "https://www.congreso.es/opendata/votaciones?p_p_id=votaciones&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&targetLegislatura={LEGISLATURA}&targetDate={DD}/{MM}/{YY}"
DEFAULT_LEGISLATURA = "XIV"


def main():
    db = PostgreDB("localhost", "postgres", "postgres", "test1")
    legislaturas = db.get_legislaturas()
    for legislatura in legislaturas:
        current_legislatura = legislatura[1]
        folder_legislatura = folder.format(LEGISLATURA=current_legislatura)
        print(f"Doing legislatura {current_legislatura}")
        create_download_folder(folder_legislatura)
        last_day = legislatura[3]
        day = datetime.datetime.today() - datetime.timedelta(days=1) if last_day is None else last_day
        final_date = False
        first_day = legislatura[2]
        while not final_date:
            url = form_url(day, current_legislatura, MAIN_URL)
            zip_link = get_download_link(url, SCRAP_URL)
            if zip_link:
                name = get_zip(zip_link, day, folder_legislatura)
                unzip_file("{name}.zip".format(name=name), folder_legislatura)
                delete_zip("{name}.zip".format(name=name))
            else:
                print(f"No session in {day}, skipping ")

            day, final_date = update_dates(day, first_day)


if __name__ == "__main__":
    main()

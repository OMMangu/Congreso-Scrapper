#!/usr/bin/python3


from dateutils import get_date
from db import MongoDb
from fileutils import get_json_list, read_json
from votesutils import get_title, get_votos, get_subtitle


def main():
    name_list = get_json_list()
    db = MongoDb("localhost", "votes-db", "test", "test1")
    for file in name_list:
        json_file = read_json(file)
        title = get_title(json_file)
        subtitle = get_subtitle(json_file)
        date = get_date(json_file)
        groups = get_votos(json_file)
        if db.title_is_present(title, subtitle, date):
            print("Skipping insert, votes for {title} are present".format(title=title))
            continue
        db.insert(title, subtitle, date, groups)
        print("Inserted votes for {title}".format(title=title))


if __name__ == '__main__':
    main()

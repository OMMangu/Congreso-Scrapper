#!/usr/bin/python3


from dateutils import get_date
from fileutils import get_json_list, read_json
from mongoutils import insert, title_is_present
from votesutils import get_title, get_votos, get_subtitle


def main():
    name_list = get_json_list()
    for file in name_list:
        json_file = read_json(file)
        title = get_title(json_file)
        subtitle = get_subtitle(json_file)
        date = get_date(json_file)
        groups = get_votos(json_file)
        if title_is_present(title, subtitle, date):
            print("Skipping insert, votes for {title} are present".format(title=title))
            continue
        insert(title, subtitle, date, groups)
        print("Inserted votes for {title}".format(title=title))


if __name__ == '__main__':
    main()

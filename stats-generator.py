#!/usr/bin/python3


from db import PostgreDB
from fileutils import get_json_list, read_json
from vote import create


def main():
    name_list = get_json_list()
    db = PostgreDB("localhost", "postgres", "postgres", "test1")
    for file in name_list:
        json_file = read_json(file)
        vote = create(json_file)
        if db.title_is_present(vote):
            print("Skipping insert, votes for {title} are present".format(title=vote.title))
            continue
        db.insert(vote)
        print("Inserted votes for {title} from session {session}, date {date}".format(title=vote.title,
                                                                                      session=vote.session,
                                                                                      date=vote.date))


if __name__ == '__main__':
    main()

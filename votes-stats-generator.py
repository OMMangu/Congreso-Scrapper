#!/usr/bin/python3
from math import isclose

from db import PostgreDB


def voted_together(votes_a, votes_b):
    total_a = sum(votes_a)
    total_b = sum(votes_b)
    together = total_b + total_a

    return isclose(votes_a[0] + votes_b[0], together, abs_tol=10) or isclose(votes_a[1] + votes_b[1], together,
                                                                             abs_tol=10) or (
                   votes_a[2] > 10 and votes_b[2] > 10 and isclose(votes_a[2] + votes_b[2], together, abs_tol=10))


def main():
    db = PostgreDB("localhost", "postgres", "postgres", "test1")
    group_a = "GVOX"
    group_b = "GP"
    group_c = "GS"
    rst = db.get_similar_votes(group_a, group_b, group_c)
    session_map = {}
    for record in rst:
        session_id = record[0]
        if session_id not in session_map:
            session_map.update({session_id: [record]})
        else:
            session_map[session_id].append(record)
    session_together = []
    for key_session in session_map.keys():
        votes_a = tuple(int(elem) for elem in session_map[key_session][0][4:])
        votes_b = tuple(int(elem) for elem in session_map[key_session][1][4:])
        votes_c = tuple(int(elem) for elem in session_map[key_session][2][4:])
        if voted_together(votes_a, votes_b) and voted_together(votes_b, votes_c):
            print("Votaron juntos %s, %s y %s el dia %s en %s" % (
                group_a, group_b, group_c, session_map[key_session][0][1], session_map[key_session][0][2]))
            session_together.append(session_map[key_session])
    print("Votaron juntos en %d ocasiones" % len(session_together))
    # pprint.pprint(session_together)


if __name__ == '__main__':
    main()

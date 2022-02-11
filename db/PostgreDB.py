#!/usr/bin/python3

import psycopg2
from psycopg2.extras import execute_values

from db.DbConnection import DbConnection
from vote import Vote

SUMMARISED_VOTE_QUERY = """
INSERT INTO public.votos_resumido
(votacion_id, grupo, a_favor, en_contra, abstencion, nsnc)
VALUES %s;
"""
DETAILED_VOTE_QUERY = """
INSERT INTO public.votos_detallado
(votacion_id, asiento, diputado, grupo, voto)
VALUES %s;

"""
VOTING_QUERY = """
INSERT INTO public.votacion
(sesion_id, votacion_number, fecha, titulo, textoexpediente, titulosubgrupo, textosubgrupo)
VALUES(%s, %s, to_date(%s, 'DD-MM-YY'), %s, %s, %s, %s) RETURNING id;
"""
SESSION_QUERY = """
INSERT INTO public.sesion
(sesion_number)
VALUES(%s) RETURNING id;
"""
PRESENT_QUERY = """
SELECT COUNT(*) FROM public.sesion s, public.votacion v 
where s.sesion_number = %s and v.votacion_number = %s and v.titulo = %s;
"""


def insert_summarised(cursor, vote: Vote, votacion_id: int) -> bool:
    summarised = vote.votes
    execute_values(cursor, SUMMARISED_VOTE_QUERY,
                   [(votacion_id, group, votes[0], votes[1], votes[2], votes[3]) for group, votes in
                    summarised.items()])
    return True


def insert_detailed(cursor, vote: Vote, votacion_id: int) -> bool:
    detailed = vote.detailed_vote
    execute_values(cursor, DETAILED_VOTE_QUERY,
                   [(votacion_id, member['asiento'], member['diputado'], member['grupo'], member['voto']) for member
                    in detailed])
    return True


class PostgreDB(DbConnection):
    def get_connection(self):
        try:
            print('Connecting to the PostgreSQL database...')
            return psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.pwd)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def title_is_present(self, vote):
        with self.conn.cursor() as cursor:
            cursor.execute(PRESENT_QUERY, (vote.session, vote.num_vote, vote.title))
            row = cursor.fetchone()
            if row[0] == 0:
                return False
            return True
        # cursor.execute("select * from public.votes votes where votes.title = %s and votes.subtitle = %s and "
        #                "votes.date_vote = %s;", (vote.title, vote.sub_title, vote.date))
        # row = cursor.fetchone()
        # if row is not None:
        #     return True

    def insert(self, vote: Vote):
        with self.conn.cursor() as cursor:
            cursor.execute(SESSION_QUERY, [vote.session])
            session_id = cursor.fetchone()[0]
            cursor.execute(VOTING_QUERY,
                           [session_id, vote.num_vote, vote.date, vote.title, vote.record_text, vote.sub_title,
                            vote.sub_group])
            vote_id = cursor.fetchone()[0]
            insert_summarised(cursor, vote, vote_id)
            insert_detailed(cursor, vote, vote_id)
            self.conn.commit()
        return True

    def check_db_exists(self):
        return True

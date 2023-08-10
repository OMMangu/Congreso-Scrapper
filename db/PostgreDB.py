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
(sesion_id, votacion_number, legislatura, fecha, titulo, textoexpediente, titulosubgrupo, textosubgrupo)
VALUES(%s, %s, %s, to_date(%s, 'DD-MM-YY'), %s, %s, %s, %s) RETURNING id;
"""
SESSION_QUERY = """
INSERT INTO public.sesion
(sesion_number, legislatura)
VALUES(%s, %s)
ON CONFLICT(sesion_number, legislatura) DO NOTHING
;
"""
PRESENT_QUERY = """SELECT COUNT(*) FROM public.sesion s, public.votacion v where s.sesion_number = %s and 
s.legislatura = %s and v.votacion_number = %s and v.titulo = %s and v.votacion_number = %s and v.fecha = to_date(%s, 
'DD-MM-YY'); """
SIMILAR_QUERY = """
select vot.id , vot.fecha, vot.titulo , vr.grupo, vr.a_favor, vr.en_contra , vr.abstencion , 
vr.nsnc from public.votos_resumido vr inner join public.votacion vot on vr.votacion_id = vot.id where vr.grupo = %s 
or vr.grupo = %s or vr.grupo = %s; 
"""
LEGISLATURA_QUERY = """
SELECT id, nombre, inicio, fin FROM public.legislatura order by inicio desc;
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
            cursor.execute(PRESENT_QUERY,
                           (vote.session, vote.legislatura, vote.num_vote, vote.title, vote.num_vote, vote.date))
            row = cursor.fetchone()
            if row[0] == 0:
                return False
            return True

    def insert(self, vote: Vote):
        with self.conn.cursor() as cursor:
            cursor.execute(SESSION_QUERY, [vote.session, vote.legislatura])
            cursor.execute(VOTING_QUERY,
                           [vote.session, vote.num_vote, vote.legislatura, vote.date, vote.title, vote.record_text,
                            vote.sub_title,
                            vote.sub_group])
            vote_id = cursor.fetchone()[0]
            insert_summarised(cursor, vote, vote_id)
            insert_detailed(cursor, vote, vote_id)
            self.conn.commit()
        return True

    def get_similar_votes(self, group_a, group_b, group_c):
        with self.conn.cursor() as cursor:
            cursor.execute(SIMILAR_QUERY, (group_a, group_b, group_c))
            # vot.id, vot.date, vot.title, vot.group, vot.favor, vot.against, vot.abst, vot.nsnc
            return cursor.fetchall()

    def get_legislaturas(self):
        with self.conn.cursor() as cursor:
            cursor.execute(LEGISLATURA_QUERY)
            return cursor.fetchall()

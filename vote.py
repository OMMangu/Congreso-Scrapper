from dateutils import get_date
from votesutils import get_sesion, get_num_votacion, get_title, get_subtitle, get_votos, get_record_text, get_subgroup, \
    get_detailed_vote, get_legislatura


class Vote(object):
    def __init__(self, session: int, num_vote: int, date: str, title: str, record_text: str, sub_title: str,
                 sub_group: str, votes, detailed_vote, legislatura: str):
        self.votes = votes
        self.sub_group = sub_group
        self.sub_title = sub_title
        self.record_text = record_text
        self.title = title
        self.date = date
        self.num_vote = num_vote
        self.session = session
        self.detailed_vote = detailed_vote
        self.legislatura = legislatura


def create(json_data: dict, filename: str) -> Vote:
    return Vote(
        session=get_sesion(json_data),
        num_vote=get_num_votacion(json_data),
        date=get_date(json_data),
        title=get_title(json_data),
        sub_title=get_subtitle(json_data),
        votes=get_votos(json_data),
        record_text=get_record_text(json_data),
        sub_group=get_subgroup(json_data),
        detailed_vote=get_detailed_vote(json_data),
        legislatura=get_legislatura(filename)
    )

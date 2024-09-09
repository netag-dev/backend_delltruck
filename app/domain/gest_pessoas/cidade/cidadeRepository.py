# cidadeRepository.py

from app.extensions import db

from app.utils import BaseRepository

from .cidade import Cidade


class CidadeRepository(BaseRepository):
    def __init__(self):
        super().__init__(Cidade)

    def find_by_nome(self, nome):
        cidade = db.session.query(Cidade).filter_by(nome=nome).first()
        return cidade

# encomendaRepository.py

from app.extensions import db

from app.utils import BaseRepository

from .encomenda import Encomenda


class EncomendaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Encomenda)

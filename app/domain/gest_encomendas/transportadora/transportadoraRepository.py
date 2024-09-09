# transportadoraRepository.py

from app.extensions import db

from app.utils import BaseRepository

from .transportadora import Transportadora


class TransportadoraRepository(BaseRepository):
    def __init__(self):
        super().__init__(Transportadora)

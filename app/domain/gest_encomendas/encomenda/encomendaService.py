# encomendaService.py

import logging

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions import EntityUniqueViolationException, EntityNotFoundException
from app.utils import SingletonMeta

from .encomenda import Encomenda
from .encomendaRepository import EncomendaRepository


class EncomendaService(metaclass=SingletonMeta):

    def __init__(self):
        self.encomenda_repository = EncomendaRepository()

    def create(self, encomenda: Encomenda):
        try:
            encomenda_criado = self.encomenda_repository.save(encomenda)
            logging.info("1: EncomendaService.create(): %s", encomenda)
            return encomenda_criado

        except IntegrityError as ex:
            if "unique constraint" in str(ex.orig):
                logging.error("IntegrityError %s", ex.orig)
                raise EntityUniqueViolationException(ex.orig)

        except Exception as ex:
            logging.error("%s", ex)

    def get_all(self):
        return self.encomenda_repository.find_all()

# transportadoraService.py

import logging

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions import EntityUniqueViolationException, EntityNotFoundException
from app.utils import SingletonMeta

from .transportadora import Transportadora
from .transportadoraRepository import TransportadoraRepository


class TransportadoraService(metaclass=SingletonMeta):

    def __init__(self):
        self.transportadora_repository = TransportadoraRepository()

    def create(self, transportadora: Transportadora):
        try:
            transportadora_criado = self.transportadora_repository.save(transportadora)
            logging.info("1: TransportadoraService.create(): %s", transportadora)
            return transportadora_criado

        except IntegrityError as ex:
            if "unique constraint" in str(ex.orig):
                logging.error("IntegrityError %s", ex.orig)
                raise EntityUniqueViolationException(ex.orig)

        except Exception as ex:
            logging.error("%s", ex)

    def get_all(self):
        return self.transportadora_repository.find_all()

    def get_by_id(self, transp_id):
        transportadora = self.transportadora_repository.find_by_id(transp_id)
        if transportadora is None:
            raise EntityNotFoundException(
                f"Transportadora com id {transp_id} não encontrado."
            )
        return transportadora

    def delete(self, transp_id):
        try:
            logging.info("0: TransportadoraService.delete()")
            self.transportadora_repository.delete(transp_id)

        except SQLAlchemyError as e:
            logging.info("TransportadoraService.delete(). error %s", e)
            raise EntityNotFoundException(
                f"Transportadora com id {transp_id} não encontrado."
            )

    def update(self, nova_transp, transp_id):
        updated = self.transportadora_repository.update(nova_transp, transp_id)
        if updated is None:
            raise EntityNotFoundException(
                f"Transportadora com id {transp_id} não encontrado."
            )
        return updated

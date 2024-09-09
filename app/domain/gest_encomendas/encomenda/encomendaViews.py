# encomendaViews.py

import logging

from flask import request, jsonify, json

from app.utils import BaseProtectedView, SchemaUtils, HateoasLinkGenerator

from app.domain.gest_encomendas.encomenda import EncomendaService
from app.domain.gest_encomendas.encomenda.schemas import (
    EncomendaCreateSchema,
    EncomendaResponseSchema,
)


class EncomendaApi(BaseProtectedView):
    def __init__(self):
        super().__init__()
        self.encomenda_service = EncomendaService()
        self.hateos_link_generator = HateoasLinkGenerator(
            {
                "self": "encomenda_api",
            },
            resource_id="encomenda_id",
        )

    def post(self):
        encomenda_data = request.get_json()

        encomenda = SchemaUtils.deserialize(EncomendaCreateSchema(), encomenda_data)

        logging.debug("0: EncomendaApi.post")

        encomenda_criado = self.encomenda_service.create(encomenda)

        logging.info("1: EncomendaApi.post")

        # retorna uma resposta com status 201 (CREATED) e corpo contendo os dados da encomenda.
        return (
            jsonify(SchemaUtils.serialize(EncomendaResponseSchema(), encomenda_criado)),
            201,
        )

    def get(self, encomenda_id=None):
        if encomenda_id is None:
            return self._get_all()
        else:
            return self._get_encomenda(encomenda_id)

    def _get_all(self):
        """ """
        encomendas = self.encomenda_service.get_all()
        # Retorna uma resposta com status 200 (OK) e corpo contendo a lista de encomendas
        return (
            jsonify(SchemaUtils.serialize(EncomendaResponseSchema(), encomendas)),
            200,
        )

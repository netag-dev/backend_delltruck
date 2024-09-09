#  transportadoraApi.py

import logging

from flask import request, jsonify, json

from app.utils import BaseProtectedView, SchemaUtils, HateoasLinkGenerator

from app.domain.gest_encomendas.transportadora import TransportadoraService
from app.domain.gest_encomendas.transportadora.shemas import (
    TransportadoraCreateSchema,
    TransportadoraResponseSchema,
    TransportadoraEditSchema,
)


class TransportadoraApi(BaseProtectedView):
    def __init__(self):
        super().__init__()
        self.transportadora_service = TransportadoraService()
        self.hateos_link_generator = HateoasLinkGenerator(
            {
                "self": "transportadora_api",
            },
            resource_id="transp_id",
        )

    def post(self):
        transportadora_data = request.get_json()

        transportadora = SchemaUtils.deserialize(
            TransportadoraCreateSchema(), transportadora_data
        )

        logging.debug("0: TransportadoraApi.post")

        transportadora_criado = self.transportadora_service.create(transportadora)

        logging.info("1: TransportadoraApi.post")

        # retorna uma resposta com status 201 (CREATED) e corpo contendo os dados da transportadora.
        return (
            jsonify(
                SchemaUtils.serialize(
                    TransportadoraResponseSchema(), transportadora_criado
                )
            ),
            201,
        )

    def get(self, transp_id=None):
        if transp_id is None:
            return self._get_all()
        else:
            return self._get_transportadora(transp_id)

    def _get_all(self):
        """ """
        transportadoras = self.transportadora_service.get_all()
        # Retorna uma resposta com status 200 (OK) e corpo contendo a lista de transportadoras
        return (
            jsonify(
                SchemaUtils.serialize(TransportadoraResponseSchema(), transportadoras)
            ),
            200,
        )

    def _get_transportadora(self, transp_id):
        """ """
        transportadora = self.transportadora_service.get_by_id(transp_id)

        logging.info("0: TransportadoraApi._get_transportadora(): %s", transportadora)

        # Retorna uma resposta com status 200 (OK) e corpo contendo a transportadora.
        return (
            jsonify(SchemaUtils.serialize(TransportadoraEditSchema(), transportadora)),
            200,
        )

    def put(self, transp_id):
        """
        Atualiza um recurso existente com todos os campos fornecidos.

        Recomendações para o uso do método PUT:
            - Inclua todos os campos do recurso, mesmo aqueles que não serão modificados.
            - Use valores mascarados para campos sensíveis que não devem ser alterados.
        """
        transp_data = request.get_json()

        nova_transp = SchemaUtils.deserialize(TransportadoraEditSchema(), transp_data)

        logging.info("0: TransportadoraApi.put()")

        self.transportadora_service.update(nova_transp, transp_id)

        logging.info("1: TransportadoraApi.put()")
        # gera a resposta HATEOAS.
        hateoas_response_data = self.hateos_link_generator.generate_response(transp_id)

        # Retorna uma resposta com status 200 (OK) e corpo contendo os links HATEOAS.
        return jsonify(hateoas_response_data), 200

    def delete(self, transp_id):

        logging.info("0: TransportadoraApi.delete()")

        self.transportadora_service.delete(transp_id)

        # Retorna uma resposta com status 204 (No Contect) indicando que o usuário foi
        # excluído com sucesso.
        return "", 204

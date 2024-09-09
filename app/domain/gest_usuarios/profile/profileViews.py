# profileViews.py

import logging

from flask import request, jsonify, json

from app.utils import BaseProtectedView, SchemaUtils, HateoasLinkGenerator
from app.domain.gest_usuarios.user import UserService
from .schemas import ProfileEditSchema


class ProfileApi(BaseProtectedView):
    def __init__(self):
        super().__init__()
        self.user_service = UserService()
        # self.hateos_link_generator = HateoasLinkGenerator(
        #     {
        #         "self": "profile_api",
        #     },
        #     resource_id="user_id",
        # )

    def get(self, user_id):
        """ """
        user = self.user_service.get_by_id(user_id)

        # Retorna uma resposta com status 200 (OK) e corpo contendo dados do perfil.
        return jsonify(SchemaUtils.serialize(ProfileEditSchema(), user)), 200

    # 888888888888888
    def put(self, user_id):
        """
        Atualiza um recurso existente com todos os campos fornecidos.

        Recomendações para o uso do método PUT:
            - Inclua todos os campos do recurso, mesmo aqueles que não serão modificados.
            - Use valores mascarados para campos sensíveis que não devem ser alterados.
        """

        user_data = request.get_json()

        novo_user = SchemaUtils.deserialize(ProfileEditSchema(), user_data)

        logging.info("0: ProfileApi.PUT: %s ", novo_user)
        logging.info("1: ProfileApi.PUT: %s ", novo_user.pessoa)
        logging.info("2: ProfileApi.PUT: %s ", novo_user.pessoa.contacto.telefone_1)

        # Actualiza o usuário no banco de dados, junto com a nova pessoa associada
        self.user_service.update(novo_user, user_id)

        # gera a resposta HATEOAS.
        # hateoas_response_data = self.hateos_link_generator.generate_response(user_id)

        # Retorna uma resposta com status 200 (OK) e corpo contendo os links HATEOAS.
        # return jsonify(hateoas_response_data), 200

        return "", 200

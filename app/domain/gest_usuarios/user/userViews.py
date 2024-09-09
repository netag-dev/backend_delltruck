# userViews.py

import logging

from flask import request, jsonify, json

from app.utils import BaseProtectedView, SchemaUtils, HateoasLinkGenerator
from app.security.authz import Authorization as authorization

from app.domain.gest_usuarios.user import UserService
from app.domain.gest_usuarios.user.schemas import (
    UserCreateSchema,
    UserResponseSchema,
    UserEditScheme,
    UserEditPasswordSchema,
    FinalUserCreateSchema,
)

from app.domain.gest_pessoas.pessoa import PessoaService
from app.domain.gest_usuarios.role import RoleService
from app.domain.gest_pessoas.pessoa.schemas import PessoaCreateSchema
from flask_jwt_extended import jwt_required


class UsersApi(BaseProtectedView):
    def __init__(self):
        super().__init__()
        self.user_service = UserService()
        self.role_service = RoleService()
        self.pessoa_service = PessoaService()
        self.hateos_link_generator = HateoasLinkGenerator(
            {
                "self": "users_api",
            },
            resource_id="user_id",
        )

    def post(self):
        if request.path.endswith("/final"):
            return self._post_user_final()
        else:
            return self._post_user()

    def _post_user(self):
        user_data = request.get_json()
        pessoa_data = user_data.pop("pessoa", None)

        pessoa = SchemaUtils.deserialize(PessoaCreateSchema(), pessoa_data)

        user = SchemaUtils.deserialize(UserCreateSchema(), user_data)

        # Associa a instância de Pessoa ao usuário
        # user.pessoa = pessoa

        # Cria o usuário no banco de dados, junto com a nova pessoa associada
        # user_criado = self.user_service.create(user)

        pessoa_criado = self.pessoa_service.create_pessoa_with_initial_details(pessoa)

        user.pessoa = pessoa_criado

        user_criado = self.user_service.create(user)

        logging.info("1: UsersApi.post")

        # retorna uma resposta com status 201 (CREATED) e corpo contendo os dados do usuário.
        return jsonify(SchemaUtils.serialize(UserResponseSchema(), user_criado)), 201

    def _post_user_final(self):
        user_data = request.get_json()
        pessoa_data = user_data.pop("pessoa", None)

        pessoa = SchemaUtils.deserialize(PessoaCreateSchema(), pessoa_data)

        user = SchemaUtils.deserialize(FinalUserCreateSchema(), user_data)

        logging.info("0: UsersApi()._post_user_final:")

        user.role = self.role_service.get_by_name("USER")
        user.pessoa = pessoa

        # Cria o usuário no banco de dados, junto com a nova pessoa associada
        user_criado = self.user_service.create(user)

        # retorna uma resposta com status 201 (CREATED) e corpo contendo os dados do usuário.
        return jsonify(SchemaUtils.serialize(UserResponseSchema(), user_criado)), 201

    def get(self, user_id=None):
        if user_id is None:
            return self._get_all()
        else:
            return self._get_user(user_id)

    def _get_all(self):
        """ """
        users = self.user_service.get_all_except_role_user_and_root()
        # Retorna uma resposta com status 200 (OK) e corpo contendo a lista de usuários
        return jsonify(SchemaUtils.serialize(UserResponseSchema(), users)), 200

    def _get_user(self, user_id):
        """ """
        user = self.user_service.get_by_id(user_id)

        # Retorna uma resposta com status 200 (OK) e corpo contendo o usuário.
        return jsonify(SchemaUtils.serialize(UserEditScheme(), user)), 200

    def put(self, user_id):
        """
        Atualiza um recurso existente com todos os campos fornecidos.

        Recomendações para o uso do método PUT:
            - Inclua todos os campos do recurso, mesmo aqueles que não serão modificados.
            - Use valores mascarados para campos sensíveis que não devem ser alterados.
        """

        user_data = request.get_json()

        novo_user = SchemaUtils.deserialize(UserEditScheme(), user_data)

        logging.info("0: UsersApi.PUT: %s ", novo_user)
        logging.info("1: UsersApi.PUT: %s ", novo_user.pessoa)

        # Actualiza o usuário no banco de dados, junto com a nova pessoa associada
        self.user_service.update(novo_user, user_id)

        # gera a resposta HATEOAS.
        hateoas_response_data = self.hateos_link_generator.generate_response(user_id)

        # Retorna uma resposta com status 200 (OK) e corpo contendo os links HATEOAS.
        return jsonify(hateoas_response_data), 200

    def patch(self, user_id):
        """
        Método PATCH: Actualiza parcialmente um recurso existente.
        Recomenda-se:
            - Obter apenas os campos que precisam ser atualizados (e não a representação completa do recurso).
            - Modificar apenas os campos especificados na solicitação.
            - Enviar a requisição PATCH com os campos atualizados para o servidor.
            - Implementar lógica para atualizar apenas os campos fornecidos, evitando a sobrescrição dos campos não mencionados.
        """

        if request.path.endswith("/update-password"):
            return self._patch_update_password(user_id)

        if request.path.endswith("/archived"):
            return self._patch_archive(user_id)

    def _patch_update_password(self, user_id):
        user_data = request.get_json()

        novo_user = SchemaUtils.deserialize(UserEditPasswordSchema(), user_data)

        self.user_service.update_partial(novo_user, user_id)

        # Retorna uma resposta com status 204 (No Contect) indicando que o usuário foi
        # actualizado com sucesso.
        return "", 204

    def _patch_archive(self, user_id):
        archived_status = request.args.get("archived")

        archived = archived_status.lower() in [
            "true",
            "yes",
            "1",
        ]  # Retorna 'True' se 'archived_status' for 'true', 'yes' ou '1'; caso contrário, retorna 'False'

        archived_field = {"archived": archived}

        self.user_service.update_partial(
            archived_field,
            user_id,
        )

        # Retorna uma resposta com status 204 (No Contect) indicando que o usuário foi
        # excluído com sucesso.
        return "", 204

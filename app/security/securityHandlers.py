# handlers/securityHandlers.py

import logging
import secrets

from flask import g, request, jsonify
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError


class SecurityHandlers:
    def __init__(self, app):
        self.app = app
        self._register_before_requests()
        self._register_after_requests()

    def _register_before_requests(self):
        """Registra o manipulador before_equest."""

        @self.app.before_request
        def generate_nonce():
            """Gera um nonce e o armazena no objeto 'g' para uso posterior nas requisição."""
            g.csp_nonce = self._generate_nonce()
            nonce = getattr(g, "csp_nonce", None)
            logging.info(
                "SecurityHandlers._register_before_requests.generate_nonce() %s", nonce
            )

        @self.app.before_request
        def check_jwt():
            """Verifica se o token JWT está presente, exceto para as rotas públicas."""

            open_routes = ["/login", "/users/final", "/roles", "/sexos", "/cidades"]

            if not any(request.path.endswith(route) for route in open_routes):
                try:
                    verify_jwt_in_request()
                except NoAuthorizationError as e:
                    return jsonify({"msg": str(e)}), 401

    def _register_after_requests(self):
        """Registra o manipulador after_request."""

        @self.app.after_request
        def set_nonce(response):
            """Atualiza o cabeçalho 'Content-Security-Policy' com o nonce gerado.

             Após cada requisição HTTP, este método:

             1. Obtém o nonce armazenado no objeto 'g' (gerado anteriormente).
             2. Atualiza o cabeçalho 'Content-Security-Policy' da resposta com o nonce gerado.

             A política de segurança de conteúdo (CSP) padrão foi configurada usando 'Talisman'
             na classe 'SecurityConfig'.

            O cliente, com configurações CORS apropriadas, deve obter o nonce do cabeçalho
            Content-Security-Policy da resposta HTTP e aplicá-lo aos elementos inline
            '<style nonce={nonce}></style>' e '<script nonce={nonce}></script>', garantindo que
            apenas scripts e estilos autorizados sejam executados.

             :param response: A resposta HTTP que será enviada ao cliente.
             :return: A resposta atualizada com o nonce no cabeçalho 'Content-Security-Policy'.
            """
            nonce = getattr(g, "csp_nonce", None)

            logging.info(
                "0: SecurityHandlers._register_after_requests.set_nonce(): %s", nonce
            )

            if request.path.startswith("/apidocs/"):  # Verifica se a rota é do Swagger
                response = self._set_swagger_csp_policy(response, nonce)
            else:
                response.headers["Content-Security-Policy"] = response.headers.get(
                    "Content-Security-Policy", ""
                ).replace("{nonce}", nonce)
            return response

    def _set_swagger_csp_policy(self, response, nonce):
        """
        Configura a Política de Segurança de Conteúdo específica para o Swagger.

        :param response: A resposta HTTP que será enviada ao cliente.
        :param nonce: O nonce gerado para a política CSP.
        :return: A resposta atualizada com a política CSP para o Swagger.
        """
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'nonce-{nonce}' 'unsafe-inline' https://cdnjs.cloudflare.com https://code.jquery.com; "
            "style-src 'self' 'nonce-{nonce}' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
            "style-src-elem 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "script-src-elem 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
            "style-src-attr 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self' data: https://fonts.googleapis.com https://fonts.gstatic.com; "
            "connect-src 'self';"
        ).format(nonce=nonce)

        return response

    def _generate_nonce(self):
        """Gera um nonce aleatório de forma segura."""
        return secrets.token_urlsafe(
            16
        )  # Gera um nonce seguro com 16 bytes de segurança

# exceptions/apiHandlerException.py

import logging
import re
from flask import Flask, jsonify
from flask_jwt_extended.exceptions import NoAuthorizationError
from werkzeug.exceptions import Forbidden
from sqlalchemy.exc import IntegrityError
from jwt.exceptions import InvalidTokenError

from . import EntityNotFoundException, EntityUniqueViolationException
from ..security.auth.exceptions.invalidPasswordException import InvalidPasswordException

from marshmallow import ValidationError


class ApiHandlerException:
    def __init__(self, app):
        self.app = app
        self._register_error_handlers()

    def _register_error_handlers(self):
        """Registra manipuladores de erros personalizados.

        Captura e manipula exceções que ocorrem em qualquer parte da aplicação,
        fornecendo uma resposta consistente para erros específicos.
        """

        @self.app.errorhandler(ValidationError)
        def handle_marshmallow_validation_error(error):
            """Handle Marshmallow validation errors."""
            logging.error("Api Error - %s", error)
            return jsonify({"errors": str(error.messages)}), 400

        @self.app.errorhandler(NoAuthorizationError)
        def handle_missing_authorization_header(error):
            """Manipula a falta de cabeçalho de autorização"""
            logging.error("Api Error - %s", error)
            return (
                jsonify({"msg": str(error)}),
                401,
            )

        @self.app.errorhandler(InvalidTokenError)
        def handle_invalid_token(error):
            """Manipula erros de token inválido ou expirado."""
            logging.error("Token inválido ou expirado: %s", error)
            return jsonify({"message": str(error)}), 401

        @self.app.errorhandler(InvalidPasswordException)
        def handle_invalid_password_exception(error):
            """Manipula a exceção quando a senha é inválida."""
            logging.error("Api Error - %s", error)
            return jsonify({"msg": str(error)}), 401

        @self.app.errorhandler(Forbidden)
        def handle_forbidden_error(error):
            """Manipula erros 403 Forbidden"""
            response = {"error": "Acesso negado",
                        "message": str(error.description)}
            return jsonify(response), 403

        @self.app.errorhandler(EntityNotFoundException)
        def handle_entity_not_found(error):
            """Manipula a exceção quando uma entidade solicitada não é encontrada."""
            logging.error("Api Error - %s", error)
            return jsonify({"msg": str(error)}), 404

        @self.app.errorhandler(EntityUniqueViolationException)
        def handle_entity_unique_violation(error):
            """Handles exceptions when a uniqueness violation occurs."""
            logging.error("Api Error - %s", error)

            # Extract the field name from the error message
            field = extract_field_from_message(str(error))

            response = {
                "msg": f"Este {field} já existe. Experimente outro.",
                "field": field,
            }

            return jsonify(response), 409

        def extract_field_from_message(error_message):
            """Extracts the field name from the error message."""
            # Regex pattern to match the field name in the error message
            pattern = re.compile(r"Key \((\w+)\)")
            match = pattern.search(error_message)
            return match.group(1) if match else "campo desconhecido"

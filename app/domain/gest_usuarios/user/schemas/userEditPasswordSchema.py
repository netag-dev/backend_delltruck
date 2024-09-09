# userEditPasswordSchema.py
import logging

from marshmallow import Schema, fields, validate, ValidationError, validates_schema, post_load

from app.utils import ValidationUtils
from app.security.securityConfig import SecurityConfig

from ..user import User


class UserEditPasswordSchema(Schema):

    new_password = fields.Str(
        required=True,
        validate=[ValidationUtils.password()],)
    confirm_password = fields.Str(
        required=True,
        validate=[ValidationUtils.password()],)

    @validates_schema
    def validate_passwords_match(self, data, **kwargs):
        """Verifiqua se 'new_password' e 'confirm_password' correspondem."""
        if data.get("new_password") != data.get("confirm_password"):
            raise ValidationError(
                "A senha de confirmação deve coincidir com a nova senha.",
                field_names=["confirm_password"],
            )

    @post_load
    def make_dic(self, data, **kwargs):
        """Cria um dicionário com apenas o campo password."""
        # Cria um dicionário contendo o campo password
        # Criptografar a password
        new_password = SecurityConfig.hash_password(data.get('new_password'))
        password_dict = {'password': new_password}

        return password_dict

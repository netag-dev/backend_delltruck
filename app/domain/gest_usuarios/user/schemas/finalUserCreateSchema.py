# finalUserCreationSchema.py.py

from marshmallow import Schema, fields, validate, post_load
from app.domain.gest_pessoas.pessoa.schemas import PessoaCreateSchema
from app.utils import ValidationUtils

from ..user import User


class FinalUserCreateSchema(Schema):
    user_email = fields.Str(
        required=True,
        validate=[ValidationUtils.email()],
    )
    password = fields.Str(
        required=True,
        validate=[ValidationUtils.password()],
    )
    # id_role = fields.Int()
    pessoa = fields.Nested(PessoaCreateSchema)

    @post_load
    def make_user(self, data, **kwargs):
        """Desserializar dados para uma instância User"""
        return User(**data)

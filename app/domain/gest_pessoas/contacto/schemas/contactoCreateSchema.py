# contactoCreateSchema.py

from marshmallow import Schema, fields, post_load
from ..contacto import Contacto


class ContactoCreateSchema(Schema):
    # id = fields.Int()
    telefone_1 = fields.Int()
    telefone_2 = fields.Int()

    @post_load
    def make_user(self, data, **kwargs):
        """Desserializar dados para uma instância User"""
        return Contacto(**data)

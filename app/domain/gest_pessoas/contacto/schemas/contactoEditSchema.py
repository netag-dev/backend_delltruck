# contactoEditSchema.py

from marshmallow import Schema, fields, post_load

from ..contacto import Contacto


class ContactoEditSchema(Schema):
    id = fields.Int()
    telefone_1 = fields.Int(missing=None)
    telefone_2 = fields.Int(missing=None)

    @post_load
    def make_user(self, data, **kwargs):
        return Contacto(**data)

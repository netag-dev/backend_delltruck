# encomendaCreateSchema.py

from marshmallow import Schema, fields, post_load
from ..encomenda import Encomenda


class EncomendaCreateSchema(Schema):
    id_pessoa_cliente_final = fields.Int(required=True)
    id_transportadora = fields.Int(required=True)

    @post_load
    def make_encomenda(self, data, **kwargs):
        return Encomenda(**data)

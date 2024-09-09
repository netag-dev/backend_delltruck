# transportadoraCreateSchema.py


from marshmallow import Schema, fields, post_load


from app.domain.gest_pessoas.contacto.schemas import ContactoCreateSchema
from app.domain.gest_pessoas.endereco.schemas import EnderecoCreateSchema

from ..transportadora import Transportadora


class TransportadoraCreateSchema(Schema):
    # id = fields.Int()
    nome = fields.Str(required=True)
    contacto = fields.Nested(ContactoCreateSchema)
    endereco = fields.Nested(EnderecoCreateSchema)

    @post_load
    def make_transportadora(self, data, **kwargs):
        """Deserialize data into a Transportadora instance"""
        return Transportadora(**data)

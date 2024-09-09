# transportadoraEditSchema.py.py


from marshmallow import Schema, fields, post_load


from app.domain.gest_pessoas.contacto.schemas import ContactoEditSchema
from app.domain.gest_pessoas.endereco.schemas import EnderecoEditSchema

from ..transportadora import Transportadora


class TransportadoraEditSchema(Schema):
    """"""

    id = fields.Int()
    nome = fields.Str(required=True)
    contacto = fields.Nested(ContactoEditSchema)
    endereco = fields.Nested(EnderecoEditSchema)

    @post_load
    def make_transportadora(self, data, **kwargs):
        """Deserialize data into a Transportadora instance"""
        return Transportadora(**data)

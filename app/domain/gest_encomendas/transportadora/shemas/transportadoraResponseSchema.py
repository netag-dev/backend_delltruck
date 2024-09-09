# transportadoraResponseSchema.py

from marshmallow import Schema, fields
from app.domain.gest_pessoas.contacto.schemas import ContactoResponseSchema
from app.domain.gest_pessoas.endereco.schemas import EnderecoResponseSchema


class TransportadoraResponseSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    contacto = fields.Nested(ContactoResponseSchema)
    endereco = fields.Nested(EnderecoResponseSchema)

# enderecoCreateSchema.py

from marshmallow import Schema, fields, post_load

from ..endereco import Endereco


class EnderecoCreateSchema(Schema):
    # id = fields.Int()
    linha_1 = fields.Str()
    linha_2 = fields.Str()
    bairro = fields.Str()
    id_cidade = fields.Int()

    @post_load
    def make_user(self, data, **kwargs):
        """Desserializar dados para uma instância User"""
        return Endereco(**data)

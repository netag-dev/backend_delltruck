# schemaUtils.py

import logging

from marshmallow import Schema, ValidationError


class SchemaUtils:
    """Utilitários para serialização e desserialização usando marshmallow."""

    @staticmethod
    def serialize(schema: Schema, obj):
        """
        Serializa um objeto ou uma lista de objetos usando o esquema fornecido.

        Args:
        - schema (Schema): Instância do esquema de marshmallow usada para serialização.
        - obj: Objeto ou lista de objetos a ser serializado.

        Returns:
        - Dados serializados no formato JSON.
        """
        if isinstance(obj, list):
            return [schema.dump(item) for item in obj]
        return schema.dump(obj)

    @staticmethod
    def deserialize(schema: Schema, data):
        """
        Desserializa dados (por exemplo, JSON) usando o esquema fornecido.

        Args:
        - schema (Schema): Instância do esquema de marshmallow usada para desserialização.
        - data: Dados a serem desserializados.

        Returns:
        - dict: Dados desserializados como um dicionário por padrão.
        - obj: Pode retornar um objeto se o método de callback @post_load estiver configurado no esquema.

        Raises:
        - ValidationError: Se os dados não forem válidos de acordo com o esquema.
        """
        try:
            return schema.load(data)
        except ValidationError as err:
            print(f"Erro de validação: {err.messages}")
            raise

    @staticmethod
    def schema_to_dict(schema_cls):
        """Converte um schema Marshmallow em um dicionário Swagger."""
        schema = schema_cls()
        return {
            "type": "object",
            "properties": {
                field_name: {"type": field_info.__class__.__name__.lower()}
                for field_name, field_info in schema.fields.items()
            },
            "required": [
                field_name
                for field_name, field_info in schema.fields.items()
                if field_info.required
            ],
        }

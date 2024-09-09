# authResponseSchema.py

from marshmallow import Schema, fields


class AuthResponseSchema(Schema):
    user_email = fields.Str()
    access_token = fields.Str()
    role_name = fields.Str()

# sexoViews.py

from flask import request, jsonify, json

from app.utils import BaseProtectedView, SchemaUtils
from . import SexoService
from .schemas import SexoResponseSchema


class SexoApi(BaseProtectedView):
    def __init__(self):
        super().__init__()
        self.sexo_service = SexoService()

    def get(self, sexo_id=None):
        if sexo_id is None:
            return self._get_all()

    def _get_all(self):
        """ """
        sexos = self.sexo_service.get_all()
        # Retorna uma resposta com status 200 (OK) e corpo contendo a lista de sexos
        return jsonify(SchemaUtils.serialize(SexoResponseSchema(), sexos)), 200

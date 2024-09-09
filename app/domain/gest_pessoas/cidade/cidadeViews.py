# cidadeViews.py

from flask import request, jsonify, json

from app.utils import BaseProtectedView, SchemaUtils
from . import CidadeService
from .schemas import CidadeResponseSchema


class CidadeApi(BaseProtectedView):
    def __init__(self):
        super().__init__()
        self.cidade_service = CidadeService()

    def get(self, cidade_id=None):
        if cidade_id is None:
            return self._get_all()

    def _get_all(self):
        """ """
        cidades = self.cidade_service.get_all()
        # Retorna uma resposta com status 200 (OK) e corpo contendo a lista de cidades
        return jsonify(SchemaUtils.serialize(CidadeResponseSchema(), cidades)), 200

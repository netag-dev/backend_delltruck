# cidade/__init__.py

from .cidade import Cidade
from .cidadeCache import CidadeCache
from .cidadeRepository import CidadeRepository
from .cidadeService import CidadeService
from .cidadeViews import *
from .schemas import *


def cidade_blueprints(app, BASE_API_URL):
    cidade_views = CidadeApi.as_view("cidade_api")

    app.add_url_rule(
        f"{BASE_API_URL}/cidades",
        view_func=cidade_views,
        methods=["GET"],
    )

# encomenda/__init__.py

from .encomenda import Encomenda
from .encomendaRepository import EncomendaRepository
from .encomendaService import EncomendaService
from .schemas import *
from .encomendaViews import EncomendaApi


def encomenda_blueprints(app, BASE_API_URL):
    encomenda_views = EncomendaApi.as_view("encomenda_api")

    app.add_url_rule(
        f"{BASE_API_URL}/encomendas",
        view_func=encomenda_views,
        methods=["GET", "POST"],
    )

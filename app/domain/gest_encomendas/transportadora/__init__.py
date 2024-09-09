# transportadora/__init__.py

from .transportadora import Transportadora
from .transportadoraRepository import TransportadoraRepository
from .transportadoraService import TransportadoraService
from .transportadoraViews import *
from .shemas import *


def transportadora_blueprints(app, BASE_API_URL):
    transp_views = TransportadoraApi.as_view("transportadora_api")

    app.add_url_rule(
        f"{BASE_API_URL}/transportadora",
        view_func=transp_views,
        methods=["GET", "POST"],
    )

    app.add_url_rule(
        f"{BASE_API_URL}/transportadora/<int:transp_id>",
        view_func=transp_views,
        methods=["GET", "PUT", "DELETE"],
    )

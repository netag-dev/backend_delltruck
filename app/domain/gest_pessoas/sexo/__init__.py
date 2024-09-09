# sexo/__init__.py

from .sexo import Sexo
from .sexoRepository import SexoRepository
from .sexoService import SexoService
from .sexoCache import SexoCache
from .sexoViews import *
from .schemas import *


def sexo_blueprints(app, BASE_API_URL):
    sexo_views = SexoApi.as_view("sexo_api")

    app.add_url_rule(
        f"{BASE_API_URL}/sexos",
        view_func=sexo_views,
        methods=["GET"],
    )

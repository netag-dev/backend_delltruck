# role/__init__.py

from .role import Role
from .roleRepository import RoleRepository
from .roleService import RoleService
from .roleCache import RoleCache
from .roleViews import *
from .schemas import *


def role_blueprints(app, BASE_API_URL):
    roles_views = RolesApi.as_view("roles_api")

    app.add_url_rule(
        f"{BASE_API_URL}/roles",
        view_func=roles_views,
        methods=["GET"],
    )

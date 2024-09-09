# profile/__init__.py

from .schemas import *
from .profileViews import *


def users_profile_blueprints(app, BASE_API_URL):
    profile_views = ProfileApi.as_view("profile_api")

    app.add_url_rule(
        f"{BASE_API_URL}/users/<int:user_id>/profile",
        view_func=profile_views,
        methods=["GET", "PUT"],
    )

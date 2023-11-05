"""Views in dangerdine app."""

from collections.abc import Callable
from typing import TYPE_CHECKING

from django.contrib import auth
from django.views.generic.base import TemplateView

if TYPE_CHECKING:
    from dangerdine.models import User

# NOTE: Adding external package functions to the global scope for frequent usage
get_user_model: Callable[[], "User"] = auth.get_user_model  # type: ignore[assignment]


class HomeView(TemplateView):
    template_name = "dangerdine/home.html"
    http_method_names = ["get"]  # noqa: RUF012

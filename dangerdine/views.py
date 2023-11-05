"""Views in dangerdine app."""

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from django.contrib import auth
from django.views.generic.base import TemplateView

import dangerdine.utils

if TYPE_CHECKING:
    from dangerdine.models import User

# NOTE: Adding external package functions to the global scope for frequent usage
get_user_model: Callable[[], "User"] = auth.get_user_model  # type: ignore[assignment]


class HomeView(TemplateView):
    template_name = "dangerdine/home.html"
    http_method_names = ["get"]  # noqa: RUF012

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        original_points: list[tuple[float, float]] = [
            (52.955102, -1.176063),
            (52.956178, -1.185526),
            (52.954766, -1.181988),
            (52.956252340447975, -1.189677385249408)
        ]
        context["original_points"] = [list(point) for point in original_points]
        context["route_points"] = dangerdine.utils.getPolyLinePoints(original_points)  # type: ignore[attr-defined]
        return context

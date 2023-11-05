"""Views in dangerdine app."""

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from django import shortcuts
from django.contrib import auth
from django.http import HttpRequest, HttpResponseRedirect
from django.views import View
from django.views.generic.base import TemplateView

import dangerdine.utils

if TYPE_CHECKING:
    from dangerdine.models import LocationRoute, User

# NOTE: Adding external package functions to the global scope for frequent usage
get_user_model: Callable[[], "User"] = auth.get_user_model  # type: ignore[assignment]


class HomeView(TemplateView):
    template_name = "dangerdine/home.html"
    http_method_names = ["get"]  # noqa: RUF012


class AddRouteView(View):
    http_method_names = ["post"]  # noqa: RUF012

    def post(self, _: HttpRequest, *__: Any, **___: Any) -> HttpResponseRedirect:
        return shortcuts.redirect("/my-routes")


class UserView(TemplateView):
    template_name = "dangerdine/userpage.html"
    http_method_names = ["get"]  # noqa: RUF012

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_authenticated:
            return context

        user: User = self.request.user
        context["full_routes"] = []
        route: LocationRoute
        for route in user.location_routes.all():
            original_points: list[tuple[float, float]] = [
                (business_location.location.x, business_location.location.y)
                for business_location
                in route.business_rating_locations.all()
            ]
            context["full_routes"].append(
                {
                    "id": route.id,
                    "original_points": [list(point) for point in original_points],
                    "route_points": dangerdine.utils.getPolyLinePoints(original_points)  # type: ignore[attr-defined]
                }
            )
        return context

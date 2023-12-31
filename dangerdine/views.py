"""Views in dangerdine app."""

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from django import shortcuts
from django.contrib import auth
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.http import HttpRequest, HttpResponseRedirect
from django.views import View
from django.views.generic.base import TemplateView

import dangerdine.utils
from dangerdine.models import BusinessRatingLocation, LocationRoute

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from dangerdine.models import User

# NOTE: Adding external package functions to the global scope for frequent usage
get_user_model: Callable[[], "User"] = auth.get_user_model  # type: ignore[assignment]


class HomeView(TemplateView):
    template_name = "dangerdine/home.html"
    http_method_names = ["get"]  # noqa: RUF012


class AddRouteView(View):
    http_method_names = ["post"]  # noqa: RUF012

    # noinspection PyMethodMayBeStatic
    def post(self, request: HttpRequest, *_: Any, **__: Any) -> HttpResponseRedirect:
        user: User = self.request.user  # type: ignore[assignment]
        if user.is_authenticated:
            anchor: tuple[float, float] = float(
                str(request.POST["startCoords"]).split(",")[0]
            ), float(str(request.POST["startCoords"]).split(",")[1])
            user.location_routes.all().delete()
            route = LocationRoute.objects.create(
                user=user,
                anchor=Point(anchor, srid=4326)
            )
            rating: int = int(request.POST["rating"])
            all_businesses: QuerySet[BusinessRatingLocation] = BusinessRatingLocation.objects.filter(food_hygiene_rating=rating).annotate(  # noqa: E501
                distance=Distance("location", Point(anchor, srid=4326))
            ).order_by("distance")[:int(request.POST["locationRange"])]
            for business in all_businesses:
                route.business_rating_locations.add(business)
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
            original_points: list[tuple[float, float, str]] = [
                (
                    business_location.location.x,
                    business_location.location.y,
                    f"{business_location.name} - {business_location.food_hygiene_rating}★"
                )
                for business_location
                in route.business_rating_locations.all().order_by("-id")
            ]

            if not original_points:
                continue

            context["full_routes"].append(
                {
                    "id": route.id,
                    "original_points": [
                        [point[1], point[0], point[2]] for point in original_points
                    ],
                    "route_points": dangerdine.utils.getPolyLinePoints(  # type: ignore[attr-defined]
                        [tuple(route.anchor), *original_points]
                    )
                }
            )
        return context

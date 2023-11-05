from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db import models
from django.db.models import Model, QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import NumericRangeFilter

from dangerdine.models import BusinessRatingLocation

if TYPE_CHECKING:
    from dangerdine.models import User


class UserIsStaffListFilter(admin.SimpleListFilter):
    """Admin filter to limit the :model:`dangerdine.user` objects by staff member or not."""

    title = _("Staff Member Status")
    parameter_name = "is_staff"

    def lookups(self, request: HttpRequest, model_admin: "ModelAdmin[User]") -> Sequence[tuple[str, Any]]:  # noqa: E501,ARG002
        """Return the sequence of url & verbose filter names of the possible lookups."""
        return ("1", _("Is Staff Member")), ("0", _("Is Not Staff Member"))

    def queryset(self, request: HttpRequest, queryset: QuerySet["User"]) -> QuerySet["User"]:  # noqa: ARG002
        """Return the filtered queryset according to the given url lookup."""
        if self.value() == "1":
            return queryset.filter(is_staff=True)
        if self.value() == "0":
            return queryset.filter(is_staff=False)
        return queryset


class UserIsActiveListFilter(admin.SimpleListFilter):
    """Admin filter to limit the :model:`dangerdine.user` objects by the active status."""

    title = _("Is Active Status")
    parameter_name = "is_active"

    def lookups(self, request: HttpRequest, model_admin: "ModelAdmin[User]") -> Sequence[tuple[str, Any]]:  # noqa: E501,ARG002
        """Return the sequence of url & verbose filter names of the possible lookups."""
        return ("1", _("Is Active")), ("0", _("Is Not Active"))

    def queryset(self, request: HttpRequest, queryset: QuerySet["User"]) -> QuerySet["User"]:  # noqa: ARG002
        """Return the filtered queryset according to the given url lookup."""
        if self.value() == "1":
            return queryset.filter(is_active=True)
        if self.value() == "0":
            return queryset.filter(is_active=False)
        return queryset


class UserLocationRouteCountListFilter(admin.ListFilter):
    # noinspection SpellCheckingInspection
    """
    Admin filter to limit :model:`dangerdine.user` objects.

    They are limited by the number of location routes they own.
    """

    def __new__(cls, request: HttpRequest, params: dict[str, str], model: type[Model], model_admin: ModelAdmin) -> admin.ListFilter:  # type: ignore[type-arg,misc] # noqa: E501
        return NumericRangeFilter(  # type: ignore[no-any-return]
            models.PositiveIntegerField(verbose_name=_("Number of owned Location Routes")),
            request,
            params,
            model,
            model_admin,
            field_path="location_route_count",
        )


class BusinessRatingLocationLocationRouteCountListFilter(admin.ListFilter):
    # noinspection SpellCheckingInspection
    """
    Admin filter to limit :model:`dangerdine.businessratinglocation` objects.

    They are limited by the number of location routes they are in.
    """

    def __new__(cls, request: HttpRequest, params: dict[str, str], model: type[Model], model_admin: ModelAdmin) -> admin.ListFilter:  # type: ignore[type-arg,misc] # noqa: E501
        return NumericRangeFilter(  # type: ignore[no-any-return]
            models.PositiveIntegerField(verbose_name=_("Number of Location Routes")),
            request,
            params,
            model,
            model_admin,
            field_path="location_route_count",
        )


class BusinessRatingLocationFoodHygieneRatingListFilter(admin.SimpleListFilter):
    # noinspection SpellCheckingInspection
    """
    Admin filter to limit the :model:`dangerdine.businessratinglocation` objects.

    They are limited by their food hygiene rating.
    """

    title = _("Food Hygiene Rating")
    parameter_name = "food_hygiene_rating"

    def lookups(self, request: HttpRequest, model_admin: "ModelAdmin[BusinessRatingLocation]") -> Sequence[tuple[str, Any]]:  # noqa: E501,ARG002
        """Return the sequence of url & verbose filter names of the possible lookups."""
        return [
            (str(parameter), verbose_parameter)
            for parameter, verbose_parameter
            in BusinessRatingLocation.FoodHygieneRating.choices
        ]

    def queryset(self, request: HttpRequest, queryset: QuerySet["BusinessRatingLocation"]) -> QuerySet["BusinessRatingLocation"]:  # noqa: E501,ARG002
        """Return the filtered queryset according to the given url lookup."""
        value: str | None
        if not (value := self.value()):
            return queryset

        return queryset.filter(
            food_hygiene_rating=BusinessRatingLocation.FoodHygieneRating(value)
        )


class LocationRouteBusinessRatingLocationCountListFilter(admin.ListFilter):
    # noinspection SpellCheckingInspection
    """
    Admin filter to limit :model:`dangerdine.locationroute` objects.

    They are limited by the number of Business Rating Locations within this Location Route.
    """

    def __new__(cls, request: HttpRequest, params: dict[str, str], model: type[Model], model_admin: ModelAdmin) -> admin.ListFilter:  # type: ignore[type-arg,misc] # noqa: E501
        return NumericRangeFilter(  # type: ignore[no-any-return]
            models.PositiveIntegerField(verbose_name=_("Number of Business Rating Locations")),
            request,
            params,
            model,
            model_admin,
            field_path="business_rating_location_count",
        )

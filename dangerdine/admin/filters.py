from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from dangerdine.models import User

if TYPE_CHECKING:
    from django.contrib.admin import ModelAdmin


class UserIsStaffListFilter(admin.SimpleListFilter):
    """Admin filter to limit the :model:`dangerdine.user` objects by staff member or not."""

    title = _("Staff Member Status")
    parameter_name = "is_staff"

    def lookups(self, request: HttpRequest, model_admin: "ModelAdmin[User]") -> Sequence[tuple[str, Any]]:  # noqa: E501,ARG002
        """Return the sequence of url & verbose filter names of the possible lookups."""
        return ("1", _("Is Staff Member")), ("0", _("Is Not Staff Member"))

    def queryset(self, request: HttpRequest, queryset: QuerySet[User]) -> QuerySet[User]:  # noqa: ARG002
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

    def queryset(self, request: HttpRequest, queryset: QuerySet[User]) -> QuerySet[User]:  # noqa: ARG002
        """Return the filtered queryset according to the given url lookup."""
        if self.value() == "1":
            return queryset.filter(is_active=True)
        if self.value() == "0":
            return queryset.filter(is_active=False)
        return queryset

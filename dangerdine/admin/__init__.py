"""Admin configurations for models in dangerdine app."""

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from django.contrib import admin, auth
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.db import models
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import DateTimeRangeFilterBuilder

from dangerdine.models import BusinessRatingLocation, LocationRoute

from .filters import (
    BusinessRatingLocationFoodHygieneRatingListFilter,
    BusinessRatingLocationLocationRouteCountListFilter,
    LocationRouteBusinessRatingLocationCountListFilter,
    UserIsActiveListFilter,
    UserIsStaffListFilter,
    UserLocationRouteCountListFilter,
)
from .inlines import BusinessRatingLocationLocationRoutesInline, UserLocationRoutesInline

if TYPE_CHECKING:
    from django.forms import ModelForm

    from dangerdine.models import User

# NOTE: Adding external package functions to the global scope for frequent usage
get_user_model: Callable[[], "User"] = auth.get_user_model  # type: ignore[assignment]

admin.site.site_header = f"""DangerDine {_("Administration")}"""
admin.site.site_title = f"""DangerDine {_("Admin")}"""
admin.site.index_title = _("Overview")
admin.site.empty_value_display = "- - - - -"

admin.site.unregister(Group)


@admin.register(get_user_model())  # type: ignore[arg-type]
class UserAdmin(DjangoUserAdmin):
    """
    Admin display configuration for :model:`dangerdine.user` models.

    This adds the functionality to provide custom display configurations on the
    list, create & update pages.
    """

    filter_horizontal = ("user_permissions",)
    fieldsets = (
        (None, {"fields": ("email", "is_active", "location_route_count")}),
        ("Authentication", {"fields": ("last_login", "password"), "classes": ("collapse",)}),
        ("Permissions", {
            "fields": ("user_permissions", "is_staff", "is_superuser"),
            "classes": ("collapse",)
        })
    )
    add_fieldsets = (
        (None, {"fields": (("email",), ("password1", "password2"))}),
        ("Extra", {"fields": ("is_active",), "classes": ("collapse",)}),
        ("Permissions", {
            "fields": ("user_permissions", "is_staff", "is_superuser"),
            "classes": ("collapse",)
        })
    )
    list_display = ("id", "email", "is_staff", "is_active", "location_route_count")
    list_display_links = ("id", "email")
    list_editable = ("is_staff", "is_active")
    list_filter = (
        UserIsStaffListFilter,
        UserIsActiveListFilter,
        UserLocationRouteCountListFilter,
        ("last_login", DateTimeRangeFilterBuilder(title=_("Last Login")))
    )
    inlines = (UserLocationRoutesInline,)
    readonly_fields = ("password", "last_login", "location_route_count")
    search_fields = ("email",)
    ordering = ("email",)
    search_help_text = _("Search for a user's Email Address")

    @admin.display(description="Last Login", ordering="last_login")
    def last_login(self, obj: "User | None") -> str:
        """Return the custom formatted string representation of the last_login field."""
        if not obj or not obj.last_login:
            return admin.site.empty_value_display

        return obj.last_login.strftime("%d %b %Y %I:%M:%S %p")

    def get_form(self, *args: Any, **kwargs: Any) -> type["ModelForm[auth.models.User]"]:
        """
        Return a Form class for use in the admin add view.

        This is used by add_view and change_view.
        """
        kwargs.update(  # NOTE: Change the labels on the form to remove unnecessary clutter
            {
                "labels": {"password": _("Hashed password string")},
                "help_texts": {
                    "user_permissions": None,
                    "is_staff": None,
                    "is_superuser": None,
                    "is_active": None
                }
            }
        )
        return super().get_form(*args, **kwargs)

    def get_queryset(self, request: HttpRequest) -> QuerySet["User"]:  # type: ignore[override]
        # noinspection SpellCheckingInspection
        """
        Return a QuerySet of all :model:`dangerdine.user` model instances.

        These are the instances that can be edited by the admin site. This is used by
        changelist_view.
        """
        return super().get_queryset(request).annotate(  # type: ignore[return-value]
            location_route_count=models.Count("location_routes", distinct=True)
        )

    @admin.display(description=_("Number of Location Routes"), ordering="location_route_count")
    def location_route_count(self, obj: "User | None") -> int | str:
        """Return the number of location routes that this User owns."""
        if not obj:
            return admin.site.empty_value_display

        return obj.location_route_count  # type: ignore[no-any-return,attr-defined]


@admin.register(BusinessRatingLocation)
class BusinessRatingLocationAdmin(ModelAdmin):  # type: ignore[type-arg]
    # noinspection SpellCheckingInspection
    """
    Admin display configuration for :model:`dangerdine.businessratinglocation` models.

    This adds the functionality to provide custom display configurations on the
    list, create & update pages.
    """

    fields = (
        "name",
        "food_hygiene_rating",
        ("raw_location", "location"),
        "location_route_count"
    )
    list_display = (
        "name",
        "food_hygiene_rating",
        "location_route_count",
        "raw_location",
        "location"
    )
    list_display_links = ("name",)
    list_editable = ("food_hygiene_rating", "location")
    list_filter = (
        BusinessRatingLocationFoodHygieneRatingListFilter,
        BusinessRatingLocationLocationRouteCountListFilter
    )
    inlines = (BusinessRatingLocationLocationRoutesInline,)
    readonly_fields = ("raw_location", "location_route_count")
    search_fields = ("name",)
    ordering = ("food_hygiene_rating", "name")
    search_help_text = _("Search for a Business Rating Location's name")

    def get_queryset(self, request: HttpRequest) -> QuerySet[BusinessRatingLocation]:
        # noinspection SpellCheckingInspection
        """
        Return a QuerySet of all :model:`dangerdine.businessratinglocation` model instances.

        These are the instances that can be edited by the admin site. This is used by
        changelist_view.
        """
        return super().get_queryset(request).annotate(  # type: ignore[no-any-return]
            location_route_count=models.Count("location_routes", distinct=True)
        )

    @admin.display(description=_("Raw Location Coordinated"))
    def raw_location(self, obj: BusinessRatingLocation | None) -> str:
        """Return the location coordinated of this BusinessRatingLocation."""
        if not obj:
            return admin.site.empty_value_display

        return f"({obj.location.x}, {obj.location.y})"

    @admin.display(description=_("Number of Location Routes"), ordering="location_route_count")
    def location_route_count(self, obj: BusinessRatingLocation | None) -> int | str:
        """Return the number of location routes this BusinessRatingLocation is a part of."""
        if not obj:
            return admin.site.empty_value_display

        return obj.location_route_count  # type: ignore[no-any-return,attr-defined]


@admin.register(LocationRoute)
class LocationRouteAdmin(ModelAdmin):  # type: ignore[type-arg]
    # noinspection SpellCheckingInspection
    """
    Admin display configuration for :model:`dangerdine.locationroute` models.

    This adds the functionality to provide custom display configurations on the
    list, create & update pages.
    """

    fields = ("user", ("business_rating_locations", "business_rating_location_count"))
    list_display = ("id", "user", "business_rating_location_count")
    list_display_links = ("id", "user", "business_rating_location_count")
    list_filter = (LocationRouteBusinessRatingLocationCountListFilter,)
    autocomplete_fields = ("business_rating_locations",)
    readonly_fields = ("business_rating_location_count",)
    search_fields = ("user__email", "business_rating_location__name")
    search_help_text = _(
        "Search for a user's Email Address or a Business Rating Location's name"
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[LocationRoute]:
        # noinspection SpellCheckingInspection
        """
        Return a QuerySet of all :model:`dangerdine.locationroute` model instances.

        These are the instances that can be edited by the admin site. This is used by
        changelist_view.
        """
        return super().get_queryset(request).annotate(  # type: ignore[no-any-return]
            business_rating_location_count=models.Count(
                "business_rating_locations",
                distinct=True
            )
        )

    @admin.display(
        description=_("Number of Business Rating Locations"),
        ordering="business_rating_location_count"
    )
    def business_rating_location_count(self, obj: LocationRoute | None) -> int | str:
        """Return the number of Business Rating Locations within this Location Route."""
        if not obj:
            return admin.site.empty_value_display

        return obj.business_rating_location_count  # type: ignore[no-any-return,attr-defined]

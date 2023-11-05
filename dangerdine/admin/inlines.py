from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from dangerdine.models import LocationRoute


class UserLocationRoutesInline(admin.StackedInline):  # type: ignore[type-arg]
    extra = 0
    model = LocationRoute
    verbose_name_plural = _("Location Routes")
    autocomplete_fields = ("business_rating_locations",)


class BusinessRatingLocationLocationRoutesInline(admin.StackedInline):  # type: ignore[type-arg]
    extra = 0
    model = LocationRoute.business_rating_locations.through
    verbose_name_plural = _("Location Routes")

"""Admin configurations for models in dangerdine app."""

from typing import TYPE_CHECKING, Any

from django.contrib import admin, auth
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import DateTimeRangeFilterBuilder

from dangerdine.models import User

from .filters import UserIsActiveListFilter, UserIsStaffListFilter

if TYPE_CHECKING:
    from django.forms import ModelForm

admin.site.site_header = f"""DangerDine {_("Administration")}"""
admin.site.site_title = f"""DangerDine {_("Admin")}"""
admin.site.index_title = _("Overview")
admin.site.empty_value_display = "- - - - -"

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """
    Admin display configuration for :model:`dangerdine.user` models.

    This adds the functionality to provide custom display configurations on the
    list, create & update pages.
    """

    filter_horizontal = ("user_permissions",)
    fieldsets = (
        (None, {"fields": ("email", "is_active")}),
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
    list_display = ("id", "email", "is_staff", "is_active")
    list_display_links = ("id", "email")
    list_editable = ("is_staff", "is_active")
    list_filter = (
        UserIsStaffListFilter,
        UserIsActiveListFilter,
        ("last_login", DateTimeRangeFilterBuilder(title=_("Last Login")))
    )
    readonly_fields = ("password", "last_login")
    search_fields = ("email",)
    ordering = ("email",)
    search_help_text = _("Search for a user's Email Address")

    @admin.display(description="Last Login", ordering="last_login")
    def last_login(self, obj: User | None) -> str:
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

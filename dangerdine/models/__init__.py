from typing import TYPE_CHECKING, Any, Final

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from .utils import AttributeDeleter, CustomBaseModel
from .validators import (
    ConfusableEmailValidator,
    ExampleEmailValidator,
    FreeEmailValidator,
    HTML5EmailValidator,
    PreexistingEmailTLDValidator,
)

if TYPE_CHECKING:
    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.db.models import ForeignObjectRel


class User(CustomBaseModel, AbstractBaseUser, PermissionsMixin):
    normalize_username = AttributeDeleter(  # type: ignore[assignment]
        object_name="User",
        attribute_name="normalize_username"
    )
    groups = AttributeDeleter(  # type: ignore[assignment]
        object_name="User",
        attribute_name="groups"
    )
    get_group_permissions = AttributeDeleter(  # type: ignore[assignment]
        object_name="User",
        attribute_name="get_group_permissions"
    )


    email = models.EmailField(
        verbose_name=_("Email Address"),
        max_length=255,
        unique=True,
        validators=[
            HTML5EmailValidator(),
            FreeEmailValidator(),
            ConfusableEmailValidator(),
            PreexistingEmailTLDValidator(),
            ExampleEmailValidator()
        ],
        error_messages={
            "unique": _("A user with that Email Address already exists."),
            "max_length": _("The Email Address must be at most 255 digits.")
        }
    )
    is_staff = models.BooleanField(
        _("Is Admin?"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("Is Active?"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()

    USERNAME_FIELD: Final[str] = "email"
    EMAIL_FIELD: Final[str] = "email"

    class Meta:
        verbose_name = _("User")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        password_field: models.Field[Any, Any] | ForeignObjectRel | GenericForeignKey = (
            self._meta.get_field("password")
        )
        if isinstance(password_field, models.Field):
            password_field.error_messages = {
                "null": _("Password is a required field."),
                "blank": _("Password is a required field.")
            }
        is_superuser_field: models.Field[Any, Any] | ForeignObjectRel | GenericForeignKey = (
            self._meta.get_field("is_superuser")
        )
        if isinstance(is_superuser_field, models.Field):
            is_superuser_field.verbose_name = _("Is Superuser?")

    def __str__(self) -> str:
        return self.email

    def clean(self) -> None:
        if self.is_superuser:
            self.is_staff = True


class BusinessRatingLocation(CustomBaseModel):
    class FoodHygieneRating(models.IntegerChoices):
        """Enum of food hygiene rating number."""

        ZERO = 0, _("0")
        ONE = 1, _("1")

    name = models.CharField(
        _("Name"),
        max_length=100,
        validators=[
            RegexValidator(r"^(?![\s'-])(?!.*[\s'-]{2})[A-Za-z '-]+(?<![\s'-])\Z"),
            MinLengthValidator(2)
        ]
    )
    food_hygiene_rating = models.PositiveIntegerField(
        _("Food Hygiene Rating"),
        choices=FoodHygieneRating.choices
    )

    class Meta:
        verbose_name = _("Restaurant")

    def __str__(self) -> str:
        return self.name


class LocationRoute(CustomBaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="location_routes",
        verbose_name=_("User"),
        help_text=_("The user that owns this route."),
        blank=False,
        null=False
    )
    business_rating_locations = models.ManyToManyField(
        BusinessRatingLocation,
        related_name="location_routes",
        verbose_name=_("Business Rating Locations"),
        help_text=_("The set of business rating locations in this route."),
        blank=False
    )

    class Meta:
        verbose_name = _("Location Route")

    def __str__(self) -> str:
        return f"{self.user} - {self.business_rating_locations.count()} locations"

"""Utility classes & functions provided for all models within dangerdine app."""

from typing import Any, Final, Self

from django.core.exceptions import FieldDoesNotExist
from django.db.models import Model


class AttributeDeleter:
    def __init__(self, object_name: str, attribute_name: str) -> None:
        self.object_name: str = object_name
        self.attribute_name: str = attribute_name

    # noinspection PyTypeChecker
    def __get__(self, instance: object, owner: object) -> Self:
        NO_ATTRIBUTE_MESSAGE: Final[str] = (
            f"type object {self.object_name!r} has no attribute {self.attribute_name!r}"
        )
        raise AttributeError(NO_ATTRIBUTE_MESSAGE)


class CustomBaseModel(Model):
    """
    Base model that provides extra utility methods for all other models to use.

    This class is abstract so should not be instantiated or have a table made for it in
    the database (see https://docs.djangoproject.com/en/stable/topics/db/models/#abstract-base-classes).
    """

    class Meta:
        """Metadata options about this model."""

        abstract = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize a new model instance, capturing any proxy field values."""
        proxy_fields: dict[str, Any] = {
            field_name: kwargs.pop(field_name)
            for field_name
            in set(kwargs.keys()) & self.get_proxy_field_names()
        }

        super().__init__(*args, **kwargs)

        proxy_field_name: str
        value: Any
        for proxy_field_name, value in proxy_fields.items():
            setattr(self, proxy_field_name, value)

    def save(self, *args: Any, **kwargs: Any) -> None:  # noqa: DJ012
        """
        Save the current instance to the database, only after the model has been cleaned.

        Cleaning the model ensures all data in the database is valid, even if the data was not
        added via a ModelForm (E.g. data is added using the ORM API).

        Uses django's argument structure, which cannot be changed (see https://docs.djangoproject.com/en/stable/ref/models/instances/#django.db.models.Model.save).
        """
        self.full_clean()

        super().save(*args, **kwargs)

    def update(self, *, commit: bool = True, using: str | None = None, **kwargs: Any) -> None:
        """
        Change an in-memory object's values, then save it to the database.

        This simplifies the two steps into a single operation
        (based on Django's Queryset.bulk_update method).

        Uses django's argument structure, which cannot be changed (see https://docs.djangoproject.com/en/stable/ref/models/instances/#django.db.models.Model.save).
        """
        unexpected_kwargs: set[str] = set()

        field_name: str
        for field_name in set(kwargs.keys()) - self.get_proxy_field_names():
            try:
                # noinspection PyUnresolvedReferences
                self._meta.get_field(field_name)
            except FieldDoesNotExist:
                unexpected_kwargs.add(field_name)

        if unexpected_kwargs:
            UNEXPECTED_KWARGS_MESSAGE: Final[str] = (
                f"{self._meta.model.__name__} got unexpected keyword arguments:"
                f" {tuple(unexpected_kwargs)}"
            )
            raise TypeError(UNEXPECTED_KWARGS_MESSAGE)

        value: Any
        for field_name, value in kwargs.items():
            setattr(self, field_name, value)

        if commit:
            self.save(using)

    update.alters_data = True  # type: ignore[attr-defined]

    @classmethod
    def get_proxy_field_names(cls) -> set[str]:
        """
        Return the set of extra names of properties that can be saved to the database.

        These are proxy fields because their values are not stored as object attributes,
        however, they can be used as a reference to a real attribute when saving objects to the
        database.
        """
        return set()

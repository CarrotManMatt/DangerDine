from typing import TYPE_CHECKING, Any, Final

from django.contrib.auth.models import UserManager as DjangoUserManager

if TYPE_CHECKING:
    from dangerdine.models import User


class UserManager(DjangoUserManager["User"]):
    use_in_migrations: bool = True

    def _create_user(self, email: str, password: str | None = None, **extra_fields: Any) -> "User":  # noqa: E501
        if not email:
            EMPTY_EMAIL_MESSAGE: Final[str] = "Users must have an email address."
            raise ValueError(EMPTY_EMAIL_MESSAGE)

        user: "User" = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields: Any) -> "User":  # type: ignore[override] # noqa: E501
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None = None, **extra_fields: Any) -> "User":  # type: ignore[override] # noqa: E501
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            INVALID_IS_STAFF_MESSAGE: Final[str] = "Superuser must have is_superuser=True."
            raise ValueError(INVALID_IS_STAFF_MESSAGE)
        if extra_fields.get("is_superuser") is not True:
            INVALID_IS_SUPERUSER_MESSAGE: Final[str] = "Superuser must have is_superuser=True."
            raise ValueError(INVALID_IS_SUPERUSER_MESSAGE)

        return self._create_user(email, password, **extra_fields)

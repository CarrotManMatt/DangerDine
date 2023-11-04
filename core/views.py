"""Views for direct use in core app."""

from collections.abc import Callable, Sequence
from typing import Any, TypeAlias

from django import urls as django_urls
from django.views.generic import RedirectView

RedirectURLArgs: TypeAlias = str | Sequence | dict[str, Any] | None | Callable


class AdminDocsRedirectView(RedirectView):
    """Helper redirect view for the docs/ url to doc/ (with any included subpath)."""

    def get_redirect_url(self, *args: RedirectURLArgs, **kwargs: RedirectURLArgs) -> str:
        """
        Return the URL redirect to.

        Keyword arguments from the URL pattern match, that is generating the redirect request,
        are provided as kwargs to this method. Also adds a possible subpath
        to the end of the redirected URL.
        """
        subpath: str = ""
        if "subpath" in self.kwargs:
            subpath = self.kwargs.pop("subpath")
            kwargs.pop("subpath")

        # noinspection SpellCheckingInspection
        url: str = django_urls.reverse(
            "django-admindocs-docroot",
            args=args,
            kwargs=kwargs
        ) + subpath

        url_args: str = self.request.META.get("QUERY_STRING", "")
        if url_args and self.query_string:
            url = f"{url}?{url_args}"

        return url

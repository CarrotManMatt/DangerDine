"""Root URL conf for DangerDine project."""

import django
from django.contrib import admin
from django.urls import URLPattern, URLResolver
from django.views.generic import RedirectView

from core.views import AdminDocsRedirectView

urlpatterns: list[URLResolver | URLPattern] = [
    django.urls.path(
        r"admin/doc/",
        django.urls.include("django.contrib.admindocs.urls")
    ),
    django.urls.path(r"admin/docs/", AdminDocsRedirectView.as_view()),
    django.urls.path(
        r"admin/docs/<path:subpath>",
        AdminDocsRedirectView.as_view()
    ),
    django.urls.path(r"admin/", admin.site.urls),
    django.urls.path("", django.urls.include("dangerdine.urls")),
    django.urls.path(
        "",
        RedirectView.as_view(pattern_name="dangerdine:home"),
        name="default"
    )
]

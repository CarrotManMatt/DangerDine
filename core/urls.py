"""
Root URL conf for DangerDine project.
"""

import django
from django.contrib import admin
from django.urls import URLResolver, URLPattern

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
    django.urls.path(r"admin/", admin.site.urls)
]

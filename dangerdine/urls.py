"""URL conf for dangerdine app."""

import django
from django.urls import URLPattern, URLResolver

from dangerdine import views

urlpatterns: list[URLResolver | URLPattern] = [
    django.urls.path("", views.HomeView.as_view(), name="home"),
    django.urls.path("my-routes/", views.UserView.as_view(), name="routes")
]

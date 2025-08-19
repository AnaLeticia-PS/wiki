from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("error", views.error, name="error"),
    path("entry", views.entry, name = "entry"),
    path("new", views.new_entry, name="new_entry"),
    path("random_page", views.random_page, name="random_page"),
    path("<str:title>", views.entry, name="entry"),
    path("<str:title>/delete", views.delete, name="delete"),
    path("search/", views.search, name="search"),
    path("<str:title>/edit", views.edit, name="edit")
]

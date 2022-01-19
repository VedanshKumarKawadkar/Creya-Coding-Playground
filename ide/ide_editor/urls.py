from django.contrib import admin
from django.urls import path, include
from graphviz import view
from ide_editor import views


urlpatterns = [
    path("", view=views.home, name="home"),
    path("editor", view=views.editor, name="run"),
    path("login", view=views.login, name="login"),
]

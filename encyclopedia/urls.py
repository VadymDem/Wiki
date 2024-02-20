from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("create/", views.create_page, name="create_page"),
    # Додайте інші URL, які вам потрібно
]



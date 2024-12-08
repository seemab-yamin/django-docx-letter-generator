from django.urls import path
from . import views

urlpatterns = [
    path("form/", views.render_form, name="render_form"),
    path("download/<str:encoded_path>/", views.download_file, name="download_file"),
]

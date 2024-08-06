from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path(
        "registrar-nuevo-anticipo/",
        views.registrar_anticipos,
        name="registrar_anticipos",
    ),
    path("lista-de-anticipos/", views.listar_anticipos, name="listar_anticipos"),
    path(
        "detalles-del-anticipo/<str:id>/",
        views.detalles_anticipos,
        name="detalles_anticipos",
    ),
    path(
        "formulario-para-actualizar-anticipo/<str:id>/",
        views.view_form_update_anticipo,
        name="view_form_update_anticipo",
    ),
    path(
        "actualizar-anticipo/<str:id>/",
        views.actualizar_anticipo,
        name="actualizar_anticipo",
    ),
    path("eliminar-anticipo/", views.eliminar_anticipo, name="eliminar_anticipo"),
    path(
        "descargar-informe-anticipos", views.informe_anticipo, name="informe_anticipo"
    ),
    path(
        "formulario-para-la-carga-masiva-de-anticipos",
        views.view_form_carga_masiva,
        name="view_form_carga_masiva",
    ),
    path("subir-data-xlsx", views.cargar_archivo, name="cargar_archivo"),
]

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.urls import path
from . import views


urlpatterns = [
    # favicon
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('main/images/favicon.ico'))),
    
    # formulario para alertas
    path('alert', views.alertForm, name="form_alert"),
]
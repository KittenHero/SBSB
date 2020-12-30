from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.blank),
    path('contact', views.contact),
    path('purchase', views.purchase),
]

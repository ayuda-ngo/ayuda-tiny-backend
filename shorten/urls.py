from django.urls import path
from . import views

urlpatterns = [
    path('api/shorten-url/', views.url_shortener_api, name='url_shortener_api'),
    path('<slug:slug>/', views.redirect),
]

from django.urls import path
from . import views

urlpatterns = [
    path('authorize/', views.Authorize.as_view(), name='authorize'),
    path('token/', views.TokenView.as_view(), name='token'),
]
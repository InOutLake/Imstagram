from django.urls import path
from . import views

app_name = 'imstagram'
urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('add_new_image/', views.AddNewImage.as_view(), name='add_new_image')
]
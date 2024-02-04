from django.urls import path
from . import views

app_name = 'dataprovider'
urlpatterns = [
    path('provide_images_info/', views.ProvideImagesInfo.as_view(), name='provide_images_info'),
    path('provide_images/', views.ProvideImages.as_view(), name='provide_images'),
    path('save_image_instance/', views.SaveImageInstance.as_view(), name='save_image_instance')
]
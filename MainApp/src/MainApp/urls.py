from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
      openapi.Info(
         title="Project API",
         default_version='v1',
         description="API description",
         terms_of_service="https://www.yourproject.com/policies/terms/",
         contact=openapi.Contact(email="contact@yourproject.local"),
         license=openapi.License(name="BSD License"),
      ),
      public=True,
   )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('imstagram/', include('Imstagram.urls')),
    path('oauth/', include('oauthprovider.urls')),
    path('dataprovider/', include('dataprovider.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]

from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Api pour la documentation avec swagger
schema_view = get_schema_view(
    openapi.Info(title="API Documentation", default_version="v1"),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"), # API swagger pour la documentation de l'api
    path('auth_app/', include('auth_app.urls')),
    path('messaging/', include('messaging.urls')),
    path('offers/', include('offers.urls')),
]

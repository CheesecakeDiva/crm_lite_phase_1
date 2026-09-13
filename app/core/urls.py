from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from crm.views import CompanyViewSet, StorageViewSet

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="CRM Lite API",
        default_version='v1',
        description="Документация для 1 этапа CRM Lite",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'storages', StorageViewSet, basename='storage')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Авторизация по JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Эндпоинты CRM
    path('api/', include(router.urls)),

    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]





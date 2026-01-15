from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from mi_app import views
from rest_framework.authtoken import views as drf_views  # Para TokenAuth
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # Para JWT

# Configuración del router de DRF
router = routers.DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'productos', views.ProductoViewSet)
router.register(r'clientes', views.ClienteViewSet)
router.register(r'pedidos', views.PedidoViewSet)
router.register(r'detalles', views.DetallePedidoViewSet)
router.register(r'proveedores', views.ProveedorViewSet)
router.register(r'producto-proveedor', views.ProductoProveedorViewSet)
router.register(r'movimientos', views.MovimientoInventarioViewSet)

urlpatterns = [
    path('', RedirectView.as_view(url='admin/', permanent=True)),

    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    path('api/auth/login/', views.CustomAuthToken.as_view(), name='api_login'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('api/auth/registro/', views.registro_usuario, name='registro_usuario'),
    path('api/auth/registro_cliente/', views.registro_usuario_cliente, name='registro_usuario_cliente'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


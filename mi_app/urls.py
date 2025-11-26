from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('categorias', CategoriaViewSet)
router.register('productos', ProductoViewSet)
router.register('clientes', ClienteViewSet)
router.register('pedidos', PedidoViewSet)
router.register('detalles', DetallePedidoViewSet)
router.register('proveedores', ProveedorViewSet)
router.register('producto-proveedor', ProductoProveedorViewSet)
router.register('movimientos', MovimientoInventarioViewSet)

urlpatterns = router.urls

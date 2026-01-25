from mi_app.serializers.usuario_serializer import UserSerializer
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .serializers.categoria_serializer import CategoriaSerializer
from .serializers.cliente_serializer import ClienteSerializer
from .serializers.detallepedido_serializer import DetallePedidoSerializer
from .serializers.movimientoinventario_serializer import MovimientoInventarioSerializer
from .serializers.pedido_serializer import PedidoSerializer
from .serializers.producto_serializer import ProductoSerializer, ProductoProveedorSerializer
from .serializers.proveedor_serializer import ProveedorSerializer
from .models import *
from .serializers import *

class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly()]


class CategoriaViewSet(BaseViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    search_fields = ['nombre']
    permission_classes = [AllowAny]


class ProductoViewSet(BaseViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    search_fields = ['nombre']
    permission_classes = [AllowAny]

    # NUEVO ENDPOINT: productos con stock bajo
    @action(detail=False, methods=['get'])
    def stock_bajo(self, request):
        productos = Producto.objects.filter(stock__lt=models.F('cantidad_minima'))
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)


class ClienteViewSet(BaseViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    search_fields = ['nombre', 'email']


class PedidoViewSet(BaseViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    search_fields = ['cliente__nombre']


class DetallePedidoViewSet(BaseViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer
    search_fields = ['producto__nombre']


class ProveedorViewSet(BaseViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    search_fields = ['nombre']
    permission_classes = [AllowAny]


class ProductoProveedorViewSet(BaseViewSet):
    queryset = ProductoProveedor.objects.all()
    serializer_class = ProductoProveedorSerializer


class MovimientoInventarioViewSet(BaseViewSet):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer
    search_fields = ['producto__nombre']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([AllowAny]) 
def registro_usuario(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not all([username, email, password]):
        return Response({"error": "Faltan campos"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    return Response({"message": "Usuario creado"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def registro_usuario_cliente(request):
    username = request.data.get('username')
    email = request.data.get('email')
    telefono = request.data.get('telefono')
    password = request.data.get('password')

    # Validación
    if not all([username, email, telefono, password]):
        return Response({"error": "Faltan campos"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)

    cliente = Cliente.objects.create(
        user=user,
        nombre=username,  
        email=email,
        telefono=telefono
    )

    return Response({
        "message": "Usuario y cliente creados",
        "user_id": user.id,
        "cliente_id": cliente.id,
        "cliente": {
            "nombre": cliente.nombre,
            "email": cliente.email,
            "telefono": cliente.telefono
        }
    }, status=status.HTTP_201_CREATED)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_staff': user.is_staff,  # 👈 Esto es lo que nos falta
            'email': user.email
        })

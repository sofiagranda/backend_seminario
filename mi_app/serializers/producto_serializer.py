from rest_framework import serializers
from mi_app.models import Producto
from mi_app.serializers.productoproveedor_serializer import ProductoProveedorSerializer

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')

    class Meta:
        model = Producto
        fields = '__all__'
        

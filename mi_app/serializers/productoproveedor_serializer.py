from rest_framework import serializers
from mi_app.models import ProductoProveedor


class ProductoProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoProveedor
        fields = '__all__'
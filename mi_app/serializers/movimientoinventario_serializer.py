from rest_framework import serializers
from mi_app.models import MovimientoInventario


class MovimientoInventarioSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')

    class Meta:
        model = MovimientoInventario
        fields = '__all__'
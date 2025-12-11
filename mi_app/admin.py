# mi_app/admin.py

from django.contrib import admin
from .models import (
    Categoria, Producto, Cliente, Pedido, 
    DetallePedido, Proveedor, ProductoProveedor, MovimientoInventario
)

# -----------------------------------------------------------------
# 1. Registros Sencillos (Recomendado para la mayoría de los modelos)
# -----------------------------------------------------------------

admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(ProductoProveedor)


# -----------------------------------------------------------------
# 2. Registros con Personalización (Recomendado para modelos complejos)
# -----------------------------------------------------------------

# Personalización de DetallePedido para mostrarlo DENTRO del Pedido
class DetallePedidoInline(admin.TabularInline):
    """Permite añadir DetallePedido directamente en el formulario de Pedido."""
    model = DetallePedido
    extra = 1 # Muestra un campo vacío para añadir un detalle nuevo por defecto
    fields = ('producto', 'cantidad', 'subtotal')
    readonly_fields = ('subtotal',) # El subtotal debe calcularse, no editarse manualmente

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha')
    list_filter = ('fecha', 'cliente')
    inlines = [DetallePedidoInline] # Añade los detalles del pedido

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'stock', 'precio', 'cantidad_minima')
    list_filter = ('categoria', 'unidad')
    search_fields = ('nombre', 'categoria__nombre')
    list_editable = ('stock', 'precio', 'cantidad_minima') # Permite editar estos campos desde la vista de lista

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'producto', 'tipo', 'cantidad', 'observaciones')
    list_filter = ('tipo', 'fecha')
    readonly_fields = ('fecha',)
    # Los movimientos se registran, pero generalmente no se editan después
    fields = ('producto', 'tipo', 'cantidad', 'observaciones')

from django.contrib import admin
from .models import Cart, Customer, OrderPlaced, Payment, Product, Wishlist, ContactMessage
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Registro del modelo Product en el panel de administración
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de administración de productos
    list_display = ['id', 'titulo_producto', 'precio_venta', 'precio_con_descuento', 'categoria', 'imagen_producto']

# Registro del modelo Customer en el panel de administración
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de administración de clientes
    list_display = ['id_cliente', 'user', 'nombre', 'direccion', 'telefono', 'departamento', 'identificacion', 'ciudad']

# Registro del modelo Cart en el panel de administración
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de administración del carrito
    list_display = ['id', 'user', 'productos', 'cantidad']
    
    # Método personalizado para mostrar productos como enlaces
    def productos(self, obj):
        # Genera un enlace al modelo Product relacionado
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.titulo_producto)

# Registro del modelo Payment en el panel de administración
@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de administración de pagos
    list_display = ['id', 'user', 'amount', 'razorpay_order_id', 'razorpay_payment_status', 'razorpay_payment_id', 'paid']

# Registro del modelo OrderPlaced en el panel de administración
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de administración de órdenes
    list_display = ['id', 'user', 'administradores', 'productos', 'cantidad', 'fecha_orden', 'pagos']
    
    # Método personalizado para mostrar el cliente relacionado como enlace
    def administradores(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.nombre)

    # Método personalizado para mostrar el producto relacionado como enlace
    def productos(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.titulo_producto)

    # Método personalizado para mostrar el pago relacionado como enlace
    def pagos(self, obj):
        link = reverse("admin:app_payment_change", args=[obj.payment.pk])
        return format_html('<a href="{}">{}</a>', link, obj.payment.razorpay_payment_id)

# Registro del modelo Wishlist en el panel de administración
@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de administración de listas de deseos
    list_display = ['id', 'user', 'productos']
    
    # Método personalizado para mostrar productos como enlaces
    def productos(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.titulo_producto)

# Registro del modelo ContactMessage en el panel de administración
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de administración de mensajes de contacto
    list_display = ['nombre', 'apellidos', 'telefono', 'celular', 'identificacion', 'tipo_caso', 'asunto', 'numero_factura', 'descripcion']

# Personalización del administrador de usuarios de Django para mostrar el ID
class CustomUserAdmin(BaseUserAdmin):
    # Campos a mostrar en la lista de administración de usuarios
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')

# Eliminación del grupo predeterminado de Django del panel de administración
admin.site.unregister(Group)

# Eliminación del administrador original de usuarios
admin.site.unregister(User)

# Registro del modelo User con la nueva configuración que incluye el ID
admin.site.register(User, CustomUserAdmin)

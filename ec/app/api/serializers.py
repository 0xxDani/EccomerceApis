# En serializers.py, voy a crear serializadores para convertir los modelos (por ejemplo, Product, Category, etc.) en JSON.

from rest_framework import serializers
from app.models import Product, Wishlist  # Importamos los modelos Product y Wishlist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from app.models import Cart
from app.models import OrderPlaced
from app.models import Payment

# Serializers.ModelSerializer es una clase especial que automáticamente crea 
# un serializer basado en el modelo Django existente.

# Serializador para el modelo Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # Todos los campos del modelo Product


# Serializador para registrar un usuario
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    # Validamos que las contraseñas coincidan
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Las contraseñas no coinciden'})
        return attrs

    # Creamos el usuario en la base de datos
    def create(self, validated_data):
        validated_data.pop('password2')  # Eliminamos password2 ya que no se almacena
        user = User.objects.create_user(**validated_data)  # Usamos create_user para manejar el hash de la contraseña
        return user


# Serializador para login de usuario
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    # Validamos las credenciales del usuario
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)  # Usamos authenticate para verificar las credenciales
        if not user:
            raise serializers.ValidationError('Credenciales incorrectas')
        attrs['user'] = user  # Guardamos el usuario autenticado
        return attrs


# Serializador para listar, actualizar y administrar usuarios
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active']  # Campos básicos del usuario


#Serializador para la lista de favoritos
class WishlistSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)  # Mostrar el nombre del producto
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)  # Precio del producto

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'product_name', 'product_price']


#Serializador para el carrito de compras
class CartSerializer(serializers.ModelSerializer):
    # Mostramos los detalles del producto en el carrito, no solo el ID.
    product = serializers.StringRelatedField()  # O podrías usar un ProductSerializer si lo prefieres

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'cantidad', 'total_cost']  # Incluye el campo total_cost como propiedad
        read_only_fields = ['total_cost']  # Este campo es solo lectura, no lo podremos modificar directamente

#Serializador para las órdenes
class OrderPlacedSerializer(serializers.ModelSerializer):
    total_cost = serializers.ReadOnlyField()

    class Meta:
        model = OrderPlaced
        fields = '__all__'

# Serializador para el modelo Payment
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'razorpay_order_id', 'razorpay_payment_status', 'razorpay_payment_id', 'paid']

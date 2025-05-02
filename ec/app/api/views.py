from rest_framework import generics
from app.models import Product, Cart
from .serializers import ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ProductSerializer, UserRegistrationSerializer, UserLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .serializers import WishlistSerializer
from app.models import Wishlist
from rest_framework.decorators import api_view
from .serializers import CartSerializer
from .serializers import UserSerializer
from app.models import OrderPlaced
from .serializers import OrderPlacedSerializer
from .serializers import PaymentSerializer
from app.models import Payment
from rest_framework import generics, permissions



# Vista para listar todos los productos
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()  # Consultar todos los productos
    serializer_class = ProductSerializer  # Usar el serializer de Product

# Vista para obtener los detalles de un solo producto
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()  # Consultar todos los productos
    serializer_class = ProductSerializer  # Usar el serializer de Product
    lookup_field = 'pk'  # Establecer que el campo para buscar será el 'id' (primary key)

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Vista para actualizar un producto
class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()          # Consultar todos los productos
    serializer_class = ProductSerializer      # Usar el serializer de Product
    lookup_field = 'pk'                       # Establecer que el campo para buscar será el 'id' (primary key)

# Vista para eliminar un producto
class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()          # Consultar todos los productos
    serializer_class = ProductSerializer      # Usar el serializer de Product
    lookup_field = 'pk'                       # Establecer que el campo para buscar será el 'id' (primary key)


# -------------------------------
#   USUARIOS
# -------------------------------

# Vista para registrar un usuario
class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

# Vista para login de un usuario
class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_200_OK)


# Vista para listar todos los usuarios
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()    # Traer todos los usuarios
    serializer_class = UserSerializer   # Usar el serializador que sí trae el id


# Vista para obtener y actualizar un usuario específico
class UserUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()           # Traer todos los usuarios
    serializer_class = UserRegistrationSerializer  # Usar el serializador de registro
    lookup_field = 'pk'                     # Buscar usuario por id (primary key)

# Vista para eliminar un usuario
class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()           # Consultar todos los usuarios
    serializer_class = UserRegistrationSerializer   # Usar el serializer de usuario
    lookup_field = 'pk'                      # Buscar usuario por id (primary key)


# Vista para agregar un producto a la lista de deseos
class AddToWishlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product_id')  # ID del producto que se quiere agregar

        if not product_id:
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)  # Buscar el producto en la base de datos
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        # Crear el objeto Wishlist
        wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)

        if created:
            return Response({"message": "Product added to wishlist."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Product is already in wishlist."}, status=status.HTTP_200_OK)


# Vista para eliminar un producto de la lista de deseos
class RemoveFromWishlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product_id')  # ID del producto que se quiere eliminar

        if not product_id:
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)  # Buscar el producto
            wishlist_item = Wishlist.objects.get(user=user, product=product)  # Buscar el ítem en la lista de deseos
        except (Product.DoesNotExist, Wishlist.DoesNotExist):
            return Response({"error": "Product not found in wishlist."}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item.delete()  # Eliminar el producto de la lista de deseos
        return Response({"message": "Product removed from wishlist."}, status=status.HTTP_200_OK)


# Vista para obtener todos los productos de la lista de deseos de un usuario
class WishlistListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)  # Filtrar por el usuario actual


# Vista para actualizar los detalles de la lista de deseos (por ejemplo, cambiar el producto)
class WishlistUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer
    queryset = Wishlist.objects.all()
    lookup_field = 'pk'  # Aquí utilizamos el campo ID de la wishlist


# Ver el carrito de compras de un usuario (GET)
@api_view(['GET'])
def view_cart(request):
    try:
        # Obtén el carrito de compras del usuario logueado
        cart = Cart.objects.filter(user=request.user)  # Filtramos por el usuario actual
        if cart.exists():
            serializer = CartSerializer(cart, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "El carrito está vacío."}, status=status.HTTP_404_NOT_FOUND)
    except Cart.DoesNotExist:
        return Response({"detail": "Carrito no encontrado."}, status=status.HTTP_404_NOT_FOUND)

#Agregar productos a carrito de un cliente en específico
@api_view(['POST'])
def add_to_cart(request):
    # Verificamos si los datos son correctos
    if 'user_id' not in request.data or 'product_id' not in request.data or 'cantidad' not in request.data:
        return Response({"detail": "user_id, product_id y cantidad son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.data['user_id']
    product_id = request.data['product_id']
    cantidad = request.data['cantidad']
    
    # Verificamos si el producto existe
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"detail": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
    # Verificamos si el usuario existe
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    # Creamos el carrito
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    
    # Actualizamos la cantidad si el producto ya existe en el carrito
    if not created:
        cart_item.cantidad += cantidad
        cart_item.save()

    # Si el producto no existía, asignamos la cantidad
    else:
        cart_item.cantidad = cantidad
        cart_item.save()

    # Serializamos y devolvemos la respuesta
    serializer = CartSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# Actualizar la cantidad de un producto en el carrito (PUT o PATCH)
@api_view(['PUT', 'PATCH'])
def update_cart_item(request, pk):
    try:
        # Obtiene el item del carrito por su ID (pk)
        cart_item = Cart.objects.get(id=pk, user=request.user)

        # Actualiza la cantidad
        cart_item.cantidad = request.data.get("cantidad", cart_item.cantidad)
        cart_item.save()
        return Response(CartSerializer(cart_item).data, status=status.HTTP_200_OK)

    except Cart.DoesNotExist:
        return Response({"detail": "El producto no se encuentra en el carrito."}, status=status.HTTP_404_NOT_FOUND)

# Eliminar un producto del carrito (DELETE)
@api_view(['DELETE'])
def remove_from_cart(request, pk):
    try:
        cart_item = Cart.objects.get(id=pk, user=request.user)
        cart_item.delete()
        return Response({"detail": "Producto eliminado del carrito."}, status=status.HTTP_204_NO_CONTENT)
    
    except Cart.DoesNotExist:
        return Response({"detail": "Producto no encontrado en el carrito."}, status=status.HTTP_404_NOT_FOUND)

#vistas para las apis de las órdenes
class OrderPlacedListAPIView(generics.ListAPIView):
    queryset = OrderPlaced.objects.all()
    serializer_class = OrderPlacedSerializer

class OrderPlacedDetailAPIView(generics.RetrieveAPIView):
    queryset = OrderPlaced.objects.all()
    serializer_class = OrderPlacedSerializer

class OrderPlacedCreateAPIView(generics.CreateAPIView):
    queryset = OrderPlaced.objects.all()
    serializer_class = OrderPlacedSerializer

class OrderPlacedUpdateAPIView(generics.UpdateAPIView):
    queryset = OrderPlaced.objects.all()
    serializer_class = OrderPlacedSerializer

class OrderPlacedDeleteAPIView(generics.DestroyAPIView):
    queryset = OrderPlaced.objects.all()
    serializer_class = OrderPlacedSerializer

# Vista para listar todos los pagos
class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()  # Traer todos los pagos
    serializer_class = PaymentSerializer  # Usar el serializador Payment

# Vista para obtener los detalles de un solo pago
class PaymentDetailAPIView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()  # Traer todos los pagos
    serializer_class = PaymentSerializer  # Usar el serializador Payment
    lookup_field = 'pk'  # Buscar por ID (primary key)

class PaymentUpdateAPIView(generics.UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = 'pk'  # ¡clave!

class PaymentDeleteAPIView(generics.DestroyAPIView):
    queryset = Payment.objects.all()  # Consultamos todos los pagos
    serializer_class = PaymentSerializer  # Usamos el serializador del pago
    lookup_field = 'pk'  # Buscamos por el ID (primary key)
#ARCHIVO CON URLS DE LAS APIS DEL PROYECTO

from django.urls import path
from . import views
from .views import (
    ProductListAPIView, ProductDetailAPIView, ProductCreateAPIView,
    ProductUpdateAPIView, ProductDeleteAPIView, UserRegistrationAPIView,
    UserLoginAPIView, UserListAPIView, UserUpdateAPIView,
    UserDeleteAPIView, AddToWishlistAPIView, RemoveFromWishlistAPIView,
    WishlistListAPIView, WishlistUpdateAPIView, OrderPlacedListAPIView,
    OrderPlacedDetailAPIView, OrderPlacedCreateAPIView, OrderPlacedUpdateAPIView,
    OrderPlacedDeleteAPIView, PaymentListAPIView, PaymentDetailAPIView, 
    PaymentUpdateAPIView,  PaymentDeleteAPIView
)
urlpatterns = [
    # Productos
    path('products/', ProductListAPIView.as_view(), name='api-product-list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='api-product-detail'),
    path('products/create/', ProductCreateAPIView.as_view(), name='api-product-create'),
    path('products/<int:pk>/update/', ProductUpdateAPIView.as_view(), name='api-product-update'),
    path('products/<int:pk>/delete/', ProductDeleteAPIView.as_view(), name='api-product-delete'),
    # Usuarios
    path('users/register/', UserRegistrationAPIView.as_view(), name='api-user-register'),
    path('users/login/', UserLoginAPIView.as_view(), name='api-user-login'),
    path('users/', UserListAPIView.as_view(), name='api-user-list'),                     
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='api-user-update'), 
    path('users/<int:pk>/delete/', UserDeleteAPIView.as_view(), name='user-delete'),
    #Lista de favoritos
    path('wishlist/add/', AddToWishlistAPIView.as_view(), name='add_to_wishlist'),
    path('wishlist/remove/', RemoveFromWishlistAPIView.as_view(), name='remove_from_wishlist'),
    path('wishlist/', WishlistListAPIView.as_view(), name='wishlist_list'),
    path('wishlist/update/<int:pk>/', WishlistUpdateAPIView.as_view(), name='update_wishlist'),
    #Carrito de compras
    path('cart/', views.view_cart, name='view_cart'),  
    path('cart/add/', views.add_to_cart, name='add_to_cart'),  
    path('cart/<int:pk>/update/', views.update_cart_item, name='update_cart_item'),  
    path('cart/<int:pk>/delete/', views.remove_from_cart, name='remove_from_cart'),  
    #Órdenes
    path('orders/', OrderPlacedListAPIView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderPlacedDetailAPIView.as_view(), name='order-detail'),
    path('orders/<int:pk>/update/', OrderPlacedUpdateAPIView.as_view(), name='order-update'),
    path('orders/<int:pk>/delete/', OrderPlacedDeleteAPIView.as_view(), name='order-delete'),
    #Pagos
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    path('payments/<int:pk>/', PaymentDetailAPIView.as_view(), name='payment-detail'),
    path('payments/<int:pk>/update/', PaymentUpdateAPIView.as_view(), name='update_payment'),
    path('payments/<int:pk>/delete/', PaymentDeleteAPIView.as_view(), name='payment-delete'),
]

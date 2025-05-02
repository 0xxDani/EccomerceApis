# Importamos el módulo necesario para la administración de Django
from django.contrib import admin
# Importamos el módulo de rutas de Django
from django.urls import path, include
# Importamos el objeto HttpResponseNotFound para manejar respuestas HTTP no encontradas
from django.http import HttpResponseNotFound

# Definimos las rutas de las URL del proyecto
urlpatterns = [
    # Ruta para acceder a la administración de Django (admin)
    path('admin/', admin.site.urls),  # Ruta que enlaza con la interfaz de administración de Django

    # Ruta para la aplicación principal del proyecto
    path('', include('app.urls')),  # Redirige a las URLs definidas dentro de la aplicación 'app'

    # Ruta para integrar las URLs de PayPal para procesar IPN (Instant Payment Notification)
    path('paypal/', include('paypal.standard.ipn.urls')),  # Permite que las notificaciones de PayPal se manejen en esta ruta

    # La siguiente ruta está comentada, pero es útil para evitar que se muestre el favicon.ico
    # path('favicon.ico', lambda x: HttpResponseNotFound()),  # Devuelve un error 404 si se solicita el favicon.ico (para evitar solicitudes no encontradas)
]

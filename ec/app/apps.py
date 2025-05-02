from django.apps import AppConfig

# Configuración de la aplicación en Django
class AppConfig(AppConfig):
    # Especifica el tipo de campo de auto-incremento predeterminado para los modelos
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nombre de la aplicación que se utiliza como identificador interno
    name = 'app'

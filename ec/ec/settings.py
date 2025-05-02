# ARCHIVO DE CONFIGURACIONES ESPECIALES DE ESTE CHICHARRÓNNN

# Importamos Path para manejar rutas de archivos de manera más eficiente y flexible
from pathlib import Path

# Definimos el directorio base del proyecto (donde está el archivo manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta para la seguridad del proyecto. Debe mantenerse privada.
SECRET_KEY = 'django-insecure-)orag=7+8z@-lf)9t_*wqcl94m^&y9y&%x43@dt^6$_zij(s-!'

# Si está en modo desarrollo, el debug se establece en True. En producción, debe estar en False.
DEBUG = True

# Especificamos qué hosts están permitidos para acceder al proyecto. El asterisco '*' permite todos los hosts.
# Se usa * para usar Ngrok con PayPal y permitir que cualquier host pueda acceder.
ALLOWED_HOSTS = ['*']

# Configuración de Django REST Framework
REST_FRAMEWORK = {
    # Esto asegura que la vista acepta solicitudes en formato JSON
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',  # Parser para JSON
    ],
    # Esto asegura que la respuesta será en formato JSON
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # Renderer para JSON
    ],
}


# Lista de aplicaciones instaladas en el proyecto Django
INSTALLED_APPS = [
    'django.contrib.admin',  # Aplicación para la administración del proyecto
    'django.contrib.auth',  # Sistema de autenticación de usuarios
    'django.contrib.contenttypes',  # Sistema de tipos de contenido (modelos)
    'django.contrib.sessions',  # Manejo de sesiones de usuario
    'django.contrib.messages',  # Sistema de mensajes (alertas, notificaciones)
    'django.contrib.staticfiles',  # Gestión de archivos estáticos
    'app',  # La aplicación principal del proyecto
    'paypal.standard.ipn',  # Integración con PayPal (IPN - Instant Payment Notification)
    'django_extensions',  # Extensiones útiles para el entorno de desarrollo de Django
    'rest_framework', # Extención para la creación de las apis
    'rest_framework.authtoken',
]

# Middleware que define cómo se gestionan las solicitudes y respuestas del servidor
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Middleware de seguridad
    'django.contrib.sessions.middleware.SessionMiddleware',  # Middleware de sesiones
    'django.middleware.common.CommonMiddleware',  # Middleware común
    'django.middleware.csrf.CsrfViewMiddleware',  # Protección contra ataques CSRF (Cross-Site Request Forgery)
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Middleware de autenticación
    'django.contrib.messages.middleware.MessageMiddleware',  # Middleware de mensajes
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Prevención de clickjacking
]

# Configuración de las URLs principales del proyecto
ROOT_URLCONF = 'ec.urls'

# Configuración de las plantillas (HTML) que usa el proyecto
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Backend de plantillas de Django
        'DIRS': [],  # Aquí se podrían especificar directorios adicionales de plantillas, si los hubiera
        'APP_DIRS': True,  # Permite cargar plantillas desde directorios de aplicaciones
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Contexto de depuración
                'django.template.context_processors.request',  # Contexto de la solicitud
                'django.contrib.auth.context_processors.auth',  # Contexto de autenticación de usuario
                'django.contrib.messages.context_processors.messages',  # Contexto de mensajes
            ],
        },
    },
]

# Definimos la aplicación WSGI para el proyecto
WSGI_APPLICATION = 'ec.wsgi.application'

# Configuración de la base de datos. En este caso, se está usando SQLite.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Usamos la base de datos SQLite
        'NAME': BASE_DIR / 'db.sqlite3',  # Definimos la ruta del archivo de base de datos
    }
}

# Definimos los validadores de contraseñas, asegurando que las contraseñas cumplan ciertos requisitos de seguridad
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Verifica similitud con el nombre de usuario
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Verifica la longitud mínima de la contraseña
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Verifica si la contraseña es común
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Verifica si la contraseña es numérica
    },
]

# Definimos el código de lenguaje. Aquí se está utilizando español de España.
LANGUAGE_CODE = 'es-es'

# Definimos la zona horaria. En este caso se está usando UTC.
TIME_ZONE = 'UTC'

# Habilitamos la internacionalización (i18n) y la zona horaria (tz)
USE_I18N = True
USE_TZ = True

# Configuración de archivos estáticos (CSS, JS, etc.)
STATIC_URL = '/static/'  # URL base para archivos estáticos

# Configuración de archivos multimedia (imágenes, videos, etc.)
MEDIA_URL = '/media/'  # URL base para archivos multimedia
MEDIA_ROOT = BASE_DIR / 'media'  # Directorio donde se guardarán los archivos multimedia

# Redirige al usuario a la página de perfil después de iniciar sesión correctamente
LOGIN_REDIRECT_URL = '/profile/'

# Configuración para usar identificadores automáticos grandes (BigAutoField) para nuevas tablas
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración para el backend de correo electrónico. En este caso, estamos usando un backend de consola
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Configuración para el servicio de pagos
# Configuración de Razorpay
RAZOR_KEY_ID = 'rzp_test_V3NdXPh72wKeN8'  # Clave pública de Razorpay
RAZOR_KEY_SECRET = 'VBaWeeL4qat7tGO9Dg6Wk9PF'  # Clave secreta de Razorpay


# Configuración de PayPal
PAYPAL_TEST = True  # Usamos el entorno de pruebas de PayPal
PAYPAL_RECEIVER_EMAIL = 'sb-0plnt29007470@business.example.com'  # Correo electrónico del receptor de pagos de PayPal



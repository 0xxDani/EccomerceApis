#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

Este archivo `manage.py` es una herramienta de línea de comandos proporcionada por Django que permite interactuar con la aplicación web. 
Se utiliza para ejecutar diversas tareas administrativas, como ejecutar el servidor de desarrollo, crear bases de datos, migrar esquemas, entre otras funciones de gestión.

Uso típico:
- `python manage.py runserver`: Inicia el servidor de desarrollo.
- `python manage.py migrate`: Aplica las migraciones de la base de datos.
- `python manage.py makemigrations`: Crea nuevas migraciones basadas en cambios en los modelos.

Este archivo facilita la administración de proyectos Django.
"""

import os
import sys

def main():
    """Ejecuta tareas administrativas."""
    # Establece el módulo de configuración predeterminado de Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ec.settings')
    try:
        # Intenta importar y ejecutar la línea de comandos de Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Estás seguro de que está instalado y "
            "disponible en la variable de entorno PYTHONPATH? ¿Olvidaste activar un entorno virtual?"
        ) from exc
    # Ejecuta el comando de línea de comandos con los argumentos pasados
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

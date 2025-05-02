# Nombre del Proyecto

Descripción corta del proyecto.

## Requisitos previos

- Python >= 3.6
- Node.js >= 10
- npm (Node Package Manager)

## Instalación

1. Descomprime el proyecto en tu directorio preferido.

2. Abre una consola y navega a la carpeta principal del proyecto:

    ```bash
    cd ruta/del/proyecto/ec
    ```

3. Crea y activa un entorno virtual:

    ```bash
    python -m venv env
    env\Scripts\activate  # Para Windows
    source env/bin/activate  # Para Linux/Mac
    ```

4. Instala las librerías necesarias:

    ```bash
    pip install -r requirements.txt
    ```

5. Compila los estilos Sass:

    ```bash
    sass app/static/app/sass/index.scss app/static/src/bundle.css
    ```

6. Ejecuta Rollup para los archivos JS:

    ```bash
    npm install
    npm run build
    ```

7. Levanta el servidor:

    ```bash
    python manage.py runserver
    ```

8. Accede a la página en tu navegador:

    ```
    http://localhost:8000/
    ```

## Administrador

- URL del administrador: `http://localhost:8000/admin`
- Usuario: `daniel`
- Contraseña: `12345Dani..-`

## Configuración de Pagos

1. Crea una cuenta en Razor Pay y obtén las claves.

2. Coloca las claves en el archivo `settings.py`.

3. En la ventana de pago, elige "Pay using UPI" y escribe `success@razorpay` donde se requiere el UPI.

## Funcionalidades

- **Ordenes:**
  - Marcar como pagada, entregada, en camino, etc.

- **Secciones en el Administrador:**
  - Carrito, productos, clientes, administradores, etc.
  - Eliminar, actualizar, agregar y ver funcionalidades disponibles.

- **Búsqueda:**
  - Usa la lupa de búsqueda escribiendo cualquier indicativo de producto.

- **Favoritos:**
  - Agrega productos a la lista de favoritos.

Para cualquier consulta, ¡contáctame! 3017753925

---

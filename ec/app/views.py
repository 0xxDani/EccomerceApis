# Importación de librerías y módulos necesarios para la funcionalidad
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
import razorpay
from .models import Cart, Customer, OrderPlaced, Payment, Product, Wishlist, ContactMessage
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

import uuid
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.template.defaultfilters import stringformat

# Función para calcular el número de imagen a partir del contenido del comentario
def calculate_image_number(comment_content):
    return sum(ord(char) for char in comment_content)

# Vista para la página de inicio
def home(request):
    totalitem = 0  # Inicializa el contador de productos en el carrito
    wishitem = 0  # Inicializa el contador de productos en la lista de deseos
    felicitaciones = ContactMessage.objects.filter(tipo_caso='felicitaciones')  # Filtra mensajes de felicitaciones
    productos_recientes = Product.objects.order_by('-id')[:3]  # Obtiene los 3 productos más recientes

    if request.user.is_authenticated:  # Si el usuario está autenticado
        totalitem = len(Cart.objects.filter(user=request.user))  # Cuenta los productos en el carrito
        wishitem = len(Wishlist.objects.filter(user=request.user))  # Cuenta los productos en la lista de deseos

    # Pasa los datos al contexto para ser renderizados en la plantilla
    context = {
        'felicitaciones': felicitaciones,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'productos_recientes': productos_recientes,
    }

    return render(request, "app/home.html", context)  # Renderiza la plantilla de inicio

# Vista para la página "Acerca de"
def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/about.html", locals())  # Renderiza la plantilla "about.html"

# Vista para la página de contacto
def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/contact.html", locals())  # Renderiza la plantilla "contact.html"

# Vista para la categoría de productos
class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(categoria=val)  # Filtra los productos por categoría
        titulo_producto = Product.objects.filter(categoria=val).values('titulo_producto')  # Obtiene los títulos de productos de la categoría
        
        # Pasar una bandera al template si no hay productos
        categoria_vacia = not product.exists()
        
        return render(request, "app/category.html", locals())


# Vista para la categoría de productos por título
class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(titulo_producto=val)  # Filtra los productos por título
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        titulo_producto = Product.objects.filter(categoria=product[0].categoria).values('titulo_producto')  # Filtra por productos con la misma categoría
        return render(request, "app/category.html", locals())  # Renderiza la plantilla de categoría

# Vista para los detalles de un producto
class ProductDetail(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)  # Obtiene el producto por su ID o devuelve un error 404
        wishlist = []  # Inicializa la lista de deseos
        totalitem = 0
        wishitem = 0

        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))  # Verifica si el producto está en la lista de deseos del usuario
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))

        return render(request, "app/productdetail.html", locals())  # Renderiza los detalles del producto

# Vista para la registración del cliente
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()  # Crea un formulario vacío de registro de cliente
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, "app/customerregistration.html", locals())  # Renderiza la página de registro

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)  # Recibe los datos del formulario
        if form.is_valid():  # Si el formulario es válido
            form.save()  # Guarda el cliente en la base de datos
            messages.success(request, "Usuario registrado exitosamente!")  # Muestra un mensaje de éxito
        else:
            messages.warning(request, "Información inválida")  # Muestra un mensaje de advertencia si hay errores
        return render(request, 'app/customerregistration.html', locals())  # Vuelve a renderizar la página con el mensaje correspondiente

# Vista para ver y editar el perfil del cliente
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()  # Crea un formulario vacío para el perfil
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/profile.html', locals())  # Renderiza la plantilla del perfil

    def post(self, request):
        form = CustomerProfileForm(request.POST)  # Recibe los datos del formulario
        if form.is_valid():  # Si el formulario es válido
            # Crea o actualiza el perfil del cliente con los datos recibidos
            user = request.user
            nombre = form.cleaned_data['nombre']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']
            departamento = form.cleaned_data['departamento']
            ciudad = form.cleaned_data['ciudad']
            identificacion = form.cleaned_data['identificacion']
            reg = Customer(user=user, nombre=nombre, direccion=direccion, telefono=telefono, departamento=departamento, ciudad=ciudad, identificacion=identificacion)
            reg.save()  # Guarda los datos del perfil
            messages.success(request, 'Felicitaciones, perfil guardado con éxito')  # Mensaje de éxito
        else:
            messages.warning(request, 'Revise la información en los campos')  # Mensaje de advertencia
        return render(request, 'app/profile.html', locals())  # Vuelve a renderizar la plantilla del perfil

# Vista para mostrar la dirección del cliente
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)  # Filtra las direcciones del usuario autenticado
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/address.html', locals())  # Renderiza la plantilla de direcciones

# Vista para actualizar la dirección del cliente
@method_decorator(login_required, name='dispatch')
class UpdateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)  # Obtiene la dirección del cliente por ID
        form = CustomerProfileForm(instance=add)  # Carga el formulario con los datos actuales de la dirección
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/updateAddress.html', locals())  # Renderiza la plantilla para actualizar la dirección

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)  # Recibe los datos del formulario de actualización
        if form.is_valid():  # Si el formulario es válido
            add = Customer.objects.get(pk=pk)  # Obtiene la dirección actualizada
            # Actualiza los campos con los datos del formulario
            add.nombre = form.cleaned_data['nombre']
            add.direccion = form.cleaned_data['direccion']
            add.telefono = form.cleaned_data['telefono']
            add.departamento = form.cleaned_data['departamento']
            add.ciudad = form.cleaned_data['ciudad']
            add.identificacion = form.cleaned_data['identificacion']
            add.save()  # Guarda la dirección actualizada
            messages.success(request, 'Felicitaciones, perfil actualizado correctamente')  # Mensaje de éxito
        else:
            messages.warning(request, 'Revisa bien todos los campos!')  # Mensaje de advertencia si hay errores
        return redirect('address')  # Redirige a la página de direcciones

# Vista para agregar un producto al carrito
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    try:
        product = Product.objects.get(id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.cantidad += 1
            cart_item.save()
    except Product.DoesNotExist:
        raise Http404("El producto no existe.")
    return redirect("/cart")


# Vista para mostrar el carrito del usuario
@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)  # Obtiene los productos en el carrito del usuario
    amount = 0
    for p in cart:
        value = p.cantidad * p.product.precio_con_descuento  # Calcula el valor del producto con descuento
        amount = amount + value  # Suma el valor de todos los productos
    totalamount = amount + 2  # Agrega un costo adicional (probablemente envío)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html', locals())  # Renderiza la plantilla del carrito

# Vista para mostrar la lista de deseos del usuario
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)  # Obtiene los productos de la lista de deseos
    return render(request, "app/wishlist.html", locals())  # Renderiza la plantilla de lista de deseos

@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.cantidad * p.product.precio_con_descuento
            famount = famount + value
        totalamount = famount + 2
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = { "amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12" }
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()

        # Crear un nuevo formulario de PayPal con librería paypal-django
        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': str(totalamount),
            'item_name': 'Producto',
            'invoice': str(uuid.uuid4()),
            'currency_code': 'USD',
            'notify_url': f'http://{host}{reverse("paypal-ipn")}',
            'return_url': f'http://{host}{reverse("paypal-return")}',
            'cancel_return': f'http://{host}{reverse("paypal-cancel")}',
        }
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request, 'app/checkout.html',locals())

def paypal_return(request):
    return redirect('orders')  

def paypal_cancel(request):
    messages.error(request, 'Tu pago no se realizó')
    return redirect('checkout')  

@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')

    user = request.user
    customer = Customer.objects.get(id=cust_id)

    try:
        payment = Payment.objects.get(razorpay_order_id=order_id)
    except Payment.DoesNotExist:
        raise Http404("El pago no existe para el order_id recibido")

    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()

    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, cantidad=c.cantidad, payment=payment).save()
        c.delete()

    return redirect("orders")

@login_required
def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',locals())


# Función para incrementar la cantidad de un producto en el carrito
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))  # Obtenemos el producto del carrito
        c.cantidad += 1  # Aumentamos la cantidad del producto
        c.save()

        # Calculamos el monto total actualizado
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.cantidad * p.product.precio_con_descuento
            amount += value
        totalamount = amount + 2

        data = {
            'cantidad': c.cantidad,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

# Función para decrementar la cantidad de un producto en el carrito
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))  # Obtenemos el producto del carrito
        c.cantidad -= 1  # Disminuimos la cantidad del producto
        c.save()

        # Calculamos el monto total actualizado
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.cantidad * p.product.precio_con_descuento
            amount += value
        totalamount = amount + 2

        data = {
            'cantidad': c.cantidad,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

# Función para eliminar un producto del carrito
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))  # Obtenemos el producto del carrito
        c.delete()  # Eliminamos el producto

        # Calculamos el monto total actualizado
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.cantidad * p.product.precio_con_descuento
            amount += value
        totalamount = amount + 2

        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

# Función para agregar un producto a la lista de deseos
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)  # Obtenemos el producto
        user = request.user
        Wishlist(user=user, product=product).save()  # Añadimos el producto a la lista de deseos

        data = {
            'message': 'Añadido a la lista de favoritos',
        }
        return JsonResponse(data)

# Función para eliminar un producto de la lista de deseos
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)  # Obtenemos el producto
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()  # Eliminamos el producto de la lista de deseos

        data = {
            'message': 'Eliminado de la lista de favoritos',
        }
        return JsonResponse(data)

# Función para realizar una búsqueda de productos
def search(request):
    query = request.GET['search']  # Obtenemos la consulta de búsqueda
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    # Filtramos los productos que coinciden con la consulta
    product = Product.objects.filter(Q(titulo_producto__icontains=query))
    return render(request,"app/search.html", locals())

# Función para manejar los mensajes de contacto
def contact(request):
    if request.method == 'POST':
        # Recuperamos los datos del formulario de contacto
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        telefono = request.POST.get('telefono')
        celular = f"{request.POST.get('indicativo')}{request.POST.get('celular')}"
        identificacion = request.POST.get('identificacion')
        tipo_caso = request.POST.get('tipo-caso')
        asunto = request.POST.get('asunto')
        numero_factura = request.POST.get('numero-factura')
        descripcion = request.POST.get('descripcion')

        # Guardamos el mensaje en la base de datos
        mensaje = ContactMessage(
            nombre=nombre,
            apellidos=apellidos,
            telefono=telefono,
            celular=celular,
            identificacion=identificacion,
            tipo_caso=tipo_caso,
            asunto=asunto,
            numero_factura=numero_factura,
            descripcion=descripcion
        )
        mensaje.save()

        # Devolvemos una respuesta JSON de éxito
        return JsonResponse({'status': 'success'})

    # Si no es una solicitud POST, renderizamos la página de contacto
    return render(request, 'app/contact.html')

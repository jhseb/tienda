#from django.shortcuts import render
from .models import  producto,cliente,carrito
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .form import productoForm,carrritoForm,clienteForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.db import IntegrityError
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden


def restringir(request, username):
    nombre_grupo = 'admin'
    nombre_grupo1 = 'usuario'
    rol =(cliente.objects.get(username=username)).rol
    grupo = Group.objects.filter(name=nombre_grupo).first()
    # Verificar si el grupo 'usuario' existe
    grupo1 = Group.objects.filter(name=nombre_grupo1).first()
    if not grupo:
        grupo = Group.objects.create(name=nombre_grupo)  
        print(f'El grupo "{nombre_grupo}" ha sido creado.')
    else:
        print(f'El grupo "{nombre_grupo}" ya existe.')
    
    if not grupo1:
        grupo1 = Group.objects.create(name=nombre_grupo1)  
        print(f'El grupo "{nombre_grupo1}" ha sido creado.')
    else:
        print(f'El grupo "{nombre_grupo1}" ya existe.')

    try:
        usuario = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f'El usuario con nombre de usuario "{username}" no existe.')
        return

    if rol == 2 :
        usuario.groups.add(grupo)
    
    else:
        usuario.groups.add(grupo1)    

def index(request):
    #return HttpResponse("HOLA")
    title = 'PAGINA'
    return render(request,'inicio.html',{
        'title':title
    })

def obtener_cliente(request):
    if request.user.is_authenticated:
        username = request.user.username
        cliente1 = cliente.objects.get(username=username)
        return cliente1
    return None  # Si el usuario no está autenticado, retorna None

def inicio(request):
    cliente0 = obtener_cliente(request)
    productos = producto.objects.all()
    return render(request, 'inicio.html',{'productos':productos,'cliente':cliente0})

def hello(request, username):
    print(username)
    return HttpResponse("<h1>hola %s</h1>"% username)

def buscar_cantidad(request):
    cliente0 = obtener_cliente(request)
    car = carrito.objects.filter(cedula=cliente0.cedula, estado="por comprar")
    resultados = len(car)
    return resultados

def about(request):
    return render(request,'about.html')
"""
def projects(request):
    #projects = list(Project.objects.values())
    #return JsonResponse(projects, safe=False)
    projects= Project.objects.all()
    return render(request,'projects.html',{
        'projects': projects
    })

def tasks(request):
    tasks=Tak.objects.all()
    return render(request,'tasks.html',{
        'tasks': tasks
    })
"""
#@login_required
#@login_required
def is_admin(user):
    return user.groups.filter(name='admin').exists()

def is_usuario(user):
    return user.groups.filter(name='usuario').exists()

def denied_access(request):
    return HttpResponse("Acceso denegado", status=403)

@user_passes_test(is_admin, login_url='denied_access')
def producto_view(request):
    cliente0 = obtener_cliente(request)
    productos = producto.objects.all()
    return render(request, 'Producto/index.html',{'productos':productos,'cliente':cliente0})

def crear_producto(request):
    cliente0 = obtener_cliente(request)
    formulario = productoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('producto')
    return render(request, 'Producto/crear.html',{'formulario': formulario,'cliente': cliente0 })


def editar_producto(request, id):
    cliente0 = obtener_cliente(request)
    producto1 = producto.objects.get(id=id)
    formulario = productoForm(request.POST or None, request.FILES or None, instance=producto1)
    if formulario.is_valid() and  request.POST:
        formulario.save()
        return redirect('producto')
    return render(request,'Producto/editar.html',{'formulario': formulario,'cliente': cliente0 })


def eliminar(request,id):
    producto1 = producto.objects.get(id=id)
    producto1.delete()
    return redirect('producto')


def signup(request):
    if request.method=='GET':
        return render(request,'signup.html',{ 'form': UserCreationForm})
    else:
        cedula = request.POST['cedula']
        try:
            cedulabase = cliente.objects.get(cedula=cedula)
            return render(request,'signup.html',{ 'form': UserCreationForm, 'error': 'La cedula ya esta registrada'})
        except cliente.DoesNotExist:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                    nombre = request.POST['nombre']
                    apellido = request.POST['apellido']
                    email = request.POST['email']
                    telefono = request.POST.get('telefono', '') 
                    direccion = request.POST.get('direccion', '')
                    rol = 1
                    username=request.POST['username']
                    cliente1 = cliente.objects.create(
                        cedula=cedula,nombre=nombre,apellido=apellido,email=email,telefono=telefono,
                        direccion=direccion,rol=rol,username=username
                    )
                    cliente1.save()
                    user.save()
                    login(request, user)
                    clien=(cliente.objects.get(username=(request.POST['username']))).rol
                    restringir(request,request.POST['username'])
                    login(request,user)
                    if clien == 2 :
                        return redirect('producto')
                    else:
                        return redirect('agregarcarrito')

                    return redirect('producto')
                except IntegrityError:
                    return render(request,'signup.html',{ 'form': UserCreationForm, 'error': 'El usuario ya existe'})
            return render(request,'signup.html',{ 'form': UserCreationForm, 'error': 'Las contraseñas no conciden'})


def signout(request):
    logout(request)
    return redirect('signin')

def signin(request):
    if request.method=='GET':
        return render(request,'signin.html',{ 'form': AuthenticationForm})
    else:
        user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
        if user is None:
             return render(request,'signin.html',{ 'form': AuthenticationForm,'error':'Contraseña incorrecta o usuario inexistente'})
        else:
            clien=(cliente.objects.get(username=(request.POST['username']))).rol
            login(request,user)
            if clien == 2 :
                return redirect('producto')
            else:
                return redirect('agregarcarrito')
       

"""
def signin(request):

    if request.method=='GET':
        return render(request,'signin.html',{ 'form': AuthenticationForm})
    else:
        user = authenticate(request,request.POST['username'], request.POST['password'])
        if user is None:
             return render(request,'signin.html',{ 'form': AuthenticationForm,'error':'Contraseña incorrecta o usuario inexistente'})
        else:
            clien=(cliente.objects.get(username=(request.POST['username']))).rol
            login(request,user)
            if clien == 2 :
                return redirect('agregarcarrito')
            else:
                return redirect('producto')"""

def productostienda(request):
    productos1= producto.objects.all()
    return render(request,'Producto/productostienda.html',{'productos':productos1})

@user_passes_test(is_usuario, login_url='denied_access')
def agregarcarrito(request):
    cantidad_car = buscar_cantidad(request)
    cliente0 = obtener_cliente(request)
    productos = producto.objects.all()
    return render(request, 'Producto/agregarcarrito.html',{'productos':productos,'cliente':cliente0,'cantidad_car':cantidad_car})

def productosgenerales(request):
    cliente0 = obtener_cliente(request)
    productos = producto.objects.all()
    return render(request, 'Producto/productosgenerales.html',{'productos':productos,'cliente':cliente0})

@user_passes_test(is_usuario, login_url='denied_access')
def crear_carrito(request,username,id):
    cliente0 = obtener_cliente(request)
    productos = producto.objects.all()
    cliente1 = cliente.objects.get(username=username)
    cedula = cliente1.cedula
    producto1 = producto.objects.get(id=id)
    cant = int(request.POST['cantidad'])
    precio=(producto1.precio)*cant
    producto1=producto1.id
    carrito1 = carrito.objects.create(idproducto=producto1,precio=precio,cedula=cliente1,estado="por comprar",car_cantidad=cant)
    product = producto.objects.get(id=id)
    cantidad = product.cantidad
    product.cantidad = cantidad-cant
    cantidad_rango = list(range(1, cantidad))
    if cantidad == 0:
        return render(request,'Producto/agregarcarrito.html',{'error':'Ya no hay productos de este tipo'})
    
    product.save()
    carrito1.save()
    return render(request, 'Producto/agregarcarrito.html',{'productos':productos,'cliente':cliente0, 'cantidad_rango': cantidad_rango})

def cantidadproducto(request,username,id):
    cliente0 = obtener_cliente(request)
    productos = producto.objects.all()
    cliente1 = cliente.objects.get(username=username)
    cedula = cliente1.cedula
    producto1 = producto.objects.get(id=id)
    precio=producto1.precio
    producto1=producto1.id
    carrito1 = carrito.objects.create(idproducto=producto1,precio=precio,cedula=cliente1,estado="por comprar")
    product = producto.objects.get(id=id)
    cantidad = product.cantidad
    product.cantidad = cantidad-1
    cantidad_rango = list(range(1, cantidad))
    if cantidad == 0:
        return render(request,'Producto/agregarcarrito.html',{'error':'Ya no hay productos de este tipo'})
    #product.save()
    #carrito1.save()
    return HttpResponse(cantidad_rango)
    return render(request, 'Producto/agregarcarrito.html',{'productos':productos,'cliente':cliente0, 'cantidad_rango': cantidad_rango})


@user_passes_test(is_usuario, login_url='denied_access')
def mostrarcarrito(request, username):
    cliente0 = obtener_cliente(request)
    cantidad_car = buscar_cantidad(request)
    try:
        cliente1 = cliente.objects.get(username=username)
    except cliente.DoesNotExist:
        return render(request, 'Producto/carrito.html', {'error': 'Cliente no encontrado'})
    productos = carrito.objects.filter(cedula=cliente1.cedula, estado="por comprar")
    producto_ids = productos.values_list('idproducto', flat=True) 
    productos1 = producto.objects.filter(id__in=producto_ids)
    cantidad_list = productos.values_list('car_cantidad',flat=True)

    stop = carrito.objects.filter(cedula__in=producto_ids)
    ids_productos = productos.values_list('idproducto', flat=True)
    ids_list = list(ids_productos)
    cant_list =list(cantidad_list)
    
    #conteo_por_id = stop.values('id').annotate(conteo=Count('id'))
    #conteo_dict = {item['id']: item['conteo'] for item in conteo_por_id}
    total=0
    if ids_list:
        for iteracion,iteracion1 in zip(ids_list, cant_list):
            try:
                product = producto.objects.get(id=iteracion)
                total += product.precio * iteracion1
            except producto.DoesNotExist:
                print(f"Producto con id {iteracion} no encontrado.")

    return render(request, 'Producto/carrito.html', {
        'productos': productos,'productos1': productos1 ,'cliente':cliente0,'total': total,'cantidad_car':cantidad_car
    })

@user_passes_test(is_admin, login_url='denied_access')   
def comprastotales(request):
    cliente0 = obtener_cliente(request)
    productos = carrito.objects.all()
    
    return render(request, 'Producto/comprastotales.html', {
        'productos': productos,
        'cliente': cliente0
    })

@user_passes_test(is_usuario, login_url='denied_access')
def mostrarcompra(request, username):
    cantidad_car = buscar_cantidad(request)
    cliente0 = obtener_cliente(request)
    try:
        cliente1 = cliente.objects.get(username=username)
    except cliente.DoesNotExist:
        return render(request, 'Producto/carrito.html', {'error': 'Cliente no encontrado'})
    productos = carrito.objects.filter(cedula=cliente1.cedula, estado="comprado")
    carritos_ids = productos.values_list('id', flat=True)
    producto_ids = productos.values_list('idproducto', flat=True) 
    productos1 = producto.objects.filter(id__in=producto_ids)

    #stop = carrito.objects.filter(cedula__in=producto_ids)
    ids_productos = productos.values_list('idproducto', flat=True)
    ids_list = list(carritos_ids)
    
    #conteo_por_id = stop.values('id').annotate(conteo=Count('id'))
    #conteo_dict = {item['id']: item['conteo'] for item in conteo_por_id}
    
    total=0
    return render(request, 'Producto/mostrarcompra.html', {
        'productos': productos,'productos1': productos1 ,'cliente':cliente0,'total': total,'cantidad_car':cantidad_car
    })


def compra(request, username):
    cliente0 = obtener_cliente(request)
    try:
        cliente1 = cliente.objects.get(username=username)
    except cliente.DoesNotExist:
        return render(request, 'Producto/carrito.html', {'error': 'Cliente no encontrado'})
    productos = carrito.objects.filter(cedula=cliente1.cedula, estado="por comprar")
    carritos_ids = productos.values_list('id', flat=True)
    producto_ids = productos.values_list('idproducto', flat=True) 
    productos1 = producto.objects.filter(id__in=producto_ids)

    #stop = carrito.objects.filter(cedula__in=producto_ids)
    ids_productos = productos.values_list('idproducto', flat=True)
    ids_list = list(carritos_ids)
    
    #conteo_por_id = stop.values('id').annotate(conteo=Count('id'))
    #conteo_dict = {item['id']: item['conteo'] for item in conteo_por_id}
    
    total=0
    for iteracion in ids_list:
        product = carrito.objects.get(id=iteracion)  
        product.estado="comprado"
        product.save()
        total=total+1

    return render(request, 'Producto/carrito.html', {
        'productos': productos,'productos1': productos1 ,'cliente':cliente0,'total': total
    })




def sumar_carrito(request,username,id):
    carrito1 = (carrito.objects.get(id=id)).idproducto
    car = carrito.objects.get(id=id)
    cantidad_agregar = request.POST['cantidad']

    product = producto.objects.get(id=carrito1)

    resta= (product.cantidad)-int(cantidad_agregar)
    suma = (car.car_cantidad)+int(cantidad_agregar)
    product.cantidad= resta
    car.car_cantidad=suma
    product.save()
    car.save()
    return mostrarcarrito(request,username)


def restar_carrito(request,username,id):
    carrito1 = (carrito.objects.get(id=id)).idproducto
    car = carrito.objects.get(id=id)
    cantidad_agregar = request.POST['cantidad']

    product = producto.objects.get(id=carrito1)

    resta= (product.cantidad)+int(cantidad_agregar)
    suma = (car.car_cantidad)-int(cantidad_agregar)
    product.cantidad= resta
    car.car_cantidad=suma
    product.save()
    car.save()
    return mostrarcarrito(request,username)
    

def eliminar_carrito(request,username,id):
    carrito1 = carrito.objects.get(id=id)
    cantidad_borrar = carrito1.car_cantidad
    product = producto.objects.get(id=(carrito1.idproducto))
    cantidad = product.cantidad
    product.cantidad = cantidad+cantidad_borrar
    carrito1.delete()
    product.save()
    return mostrarcarrito(request,username)


#cliente

@user_passes_test(is_admin, login_url='denied_access')   
def cliente_view(request):
    cliente0 = obtener_cliente(request)
    clientes = cliente.objects.all()
    return render(request, 'cliente/index.html',{'productos':clientes,'cliente':cliente0})

@user_passes_test(is_admin, login_url='denied_access')   
def crear_cliente(request):
    cliente0 = obtener_cliente(request)
    formulario = clienteForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('cliente')
    return render(request, 'cliente/crear.html',{'formulario': formulario,'cliente':cliente0})

@user_passes_test(is_admin, login_url='denied_access')   
def editar_cliente(request, id):
    cliente0 = obtener_cliente(request)
    producto1 = cliente.objects.get(cedula=id)
    formulario = clienteForm(request.POST or None, request.FILES or None, instance=producto1)
    nombre_grupo = 'admin'
    nombre_grupo1 = 'usuario'
    grupo = Group.objects.filter(name=nombre_grupo).first()
    grupo1 = Group.objects.filter(name=nombre_grupo1).first()

    if formulario.is_valid() and  request.POST:
        formulario.save()
        userb = User.objects.get(username=formulario.cleaned_data['username'])
        userb.groups.clear()   
        if formulario.cleaned_data['rol'] == 1:
            userb.groups.add(grupo1)
        else:
            userb.groups.add(grupo)

        return redirect('cliente')
    return render(request,'cliente/editar.html',{'formulario': formulario,'cliente':cliente0})

@user_passes_test(is_admin, login_url='denied_access')   
def modificaruser(request,id):
    username1 = request.user.username
    username=request.POST['username']
    password= request.POST['password']
    usuario = cliente.objects.get(cedula=id)
    usuario1= usuario.username
    user= User.objects.get(username=usuario1)
    user.username = username
    user.set_password(password)
    user.save()
    usuario.username=username
    usuario.save()
    if usuario1 == username1:
        return render(request,'signin.html')
    else:
        return redirect('cliente')

@user_passes_test(is_admin, login_url='denied_access')      
def crear_usuario(request):
    user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
    nombre_grupo = 'admin'
    nombre_grupo1 = 'usuario'
    grupo = Group.objects.filter(name=nombre_grupo).first()
    grupo1 = Group.objects.filter(name=nombre_grupo1).first()

    userb = User.objects.get(username=request.POST['username'])
    user1= (cliente.objects.get(username=request.POST['username'])).rol
    if user1 == 1:
            userb.groups.add(grupo1)
    else:
            userb.groups.add(grupo)

    user.save()
    return redirect('cliente')

@user_passes_test(is_admin, login_url='denied_access')   
def eliminar_cliente(request,id):
    cliente1 = cliente.objects.get(cedula=id)
    username1 = cliente1.username
    user = User.objects.get(username=username1)
    user.delete()
    cliente1.delete()
    return redirect('cliente') 
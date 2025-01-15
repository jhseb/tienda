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
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
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
    return render(request, 'inicio.html',{'cliente':  cliente0} )

def hello(request, username):
    print(username)
    return HttpResponse("<h1>hola %s</h1>"% username)

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
                    return redirect('producto')
                except IntegrityError:
                    return render(request,'signup.html',{ 'form': UserCreationForm, 'error': 'El usuario ya existe'})
            return render(request,'signup.html',{ 'form': UserCreationForm, 'error': 'Las contraseñas no conciden'})


def signout(request):
    logout(request)
    return redirect('signup')

def signin(request):
    if request.method=='GET':
        return render(request,'signin.html',{ 'form': AuthenticationForm})
    else:
        user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
        if user is None:
             return render(request,'signin.html',{ 'form': AuthenticationForm,'error':'Contraseña incorrecta o usuario inexistente'})
        else:
            login(request,user)
            return agregarcarrito(request)
       

def productostienda(request):
    productos1= producto.objects.all()
    return render(request,'Producto/productostienda.html',{'productos':productos1})

def agregarcarrito(request):
    cliente0 = obtener_cliente(request)
    productos = producto.objects.all()
    return render(request, 'Producto/agregarcarrito.html',{'productos':productos,'cliente':cliente0})


def crear_carrito(request,username,id):
    cliente0 = obtener_cliente(request)
    productos = producto.objects.all()
    cliente1 = cliente.objects.get(username=username)
    cedula = cliente1.cedula
    producto1 = producto.objects.get(id=id)
    precio=producto1.precio
    producto1=producto1.id
    carrito1 = carrito.objects.create(idproducto=producto1,precio=precio,cedula=cliente1)
    carrito1.save()
    return render(request, 'Producto/agregarcarrito.html',{'productos':productos,'cliente':cliente0})

def mostrarcarrito(request, username):
    cliente0 = obtener_cliente(request)
    try:
        cliente1 = cliente.objects.get(username=username)
    except cliente.DoesNotExist:
        return render(request, 'Producto/carrito.html', {'error': 'Cliente no encontrado'})
    productos = carrito.objects.filter(cedula=cliente1)
    producto_ids = productos.values_list('idproducto', flat=True)
    productos1 = producto.objects.filter(id__in=producto_ids)
    return render(request, 'Producto/carrito.html', {
        'productos': productos,'productos1': productos1 ,'cliente':cliente0
    })

def editar_carrito(request, id):
    producto1 = producto.objects.get(id=id)
    formulario = productoForm(request.POST or None, request.FILES or None, instance=producto1)
    if formulario.is_valid() and  request.POST:
        formulario.save()
        return redirect('producto')
    return render(request,'Producto/editar.html',{'formulario': formulario})

def eliminar_carrito(request,username,id):
    carrito1 = carrito.objects.get(id=id)
    carrito1.delete()
    return mostrarcarrito(request,username)


#cliente

    
def cliente_view(request):
    cliente0 = obtener_cliente(request)
    clientes = cliente.objects.all()
    return render(request, 'cliente/index.html',{'productos':clientes,'cliente':cliente0})

def crear_cliente(request):
    cliente0 = obtener_cliente(request)
    formulario = clienteForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('cliente')
    return render(request, 'cliente/crear.html',{'formulario': formulario,'cliente':cliente0})


def editar_cliente(request, id):
    cliente0 = obtener_cliente(request)
    producto1 = cliente.objects.get(cedula=id)
    formulario = clienteForm(request.POST or None, request.FILES or None, instance=producto1)
    if formulario.is_valid() and  request.POST:
        formulario.save()
        return redirect('cliente')
    return render(request,'cliente/editar.html',{'formulario': formulario,'cliente':cliente0})

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
    
def crear_usuario(request):
    user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
    user.save()
    return redirect('cliente')

def eliminar_cliente(request,id):
    cliente1 = cliente.objects.get(cedula=id)
    cliente1.delete()
    return redirect('cliente') 

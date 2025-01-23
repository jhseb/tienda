from django.urls import path
from . import views
from django.shortcuts import get_list_or_404
from django.conf import settings
from django.contrib.staticfiles.urls import static
urlpatterns=[
    path('',views.index),
    path('inicio',views.inicio,name="inicio"),
    path('about/',views.about),
    path('hello/<str:username>',views.hello),
    #path('projects/',views.projects),
    #path('tasks/<int:id>',views.tasks),
    #path('tasks/',views.tasks),
    path('producto/',views.producto_view, name='producto'),
    path('producto/crear',views.crear_producto, name='crear_producto'),
    path('producto/editar',views.editar_producto, name='editar_producto'),
    path('eliminar/<int:id>',views.eliminar, name='eliminar'),
    path('producto/editar/<int:id>',views.editar_producto, name='editar_producto'),
    
    path('cliente/',views.cliente_view, name='cliente'),
    path('cliente/crear',views.crear_cliente, name='crear_cliente'),
    path('cliente/editar',views.editar_cliente, name='editar_cliente'),
    path('eliminar_cliente/<int:id>',views.eliminar_cliente, name='eliminar_cliente'),
    path('editar_cliente/editar/<int:id>',views.editar_cliente, name='editar_cliente'),
    
    path('cliente/modificaruser/<int:id>',views.modificaruser, name='modificaruser'),
    path('cliente/user/',views.crear_usuario, name='crear_usuario'),
    
    
    
    path('signup/',views.signup,name='signup'),
    path('logout/',views.signout,name='logout'),
    path('signin/',views.signin,name='signin'),
    path('productostienda/',views.productostienda,name='productostienda'),
    path('accesodenegado/',views.denied_access,name='denied_access'),
    
    
    path('agregarcarrito', views.agregarcarrito, name='agregarcarrito'),
    path('productosgenerales', views.productosgenerales, name='productosgenerales'),
    path('comprastotales', views.comprastotales, name='comprastotales'),

    path('crearcarrito/<str:username>/<int:id>', views.crear_carrito, name='crearcarrito'),
    path('cantidadproducto/<str:username>/<int:id>', views.cantidadproducto, name='cantidadproducto'),
    path('mostrarcarrito/<str:username>', views.mostrarcarrito, name='mostrarcarrito'),
    path('sumarcarrito/<str:username>/<int:id>',views.sumar_carrito, name='sumarcarrito'),
    path('restarcarrito/<str:username>/<int:id>',views.restar_carrito, name='restarcarrito'),
    path('eliminarcarrito/<str:username>/<int:id>',views.eliminar_carrito, name='eliminarcarrito'),
    path('compra/<str:username>',views.compra, name='compra'),
    path('mostrarcompra/<str:username>',views.mostrarcompra, name='mostrarcompra'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





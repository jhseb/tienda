from django.contrib import admin
from .models import producto,cliente,carrito

# Register your models here.
admin.site.register(producto)
admin.site.register(cliente)
admin.site.register(carrito)

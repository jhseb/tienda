from django.db import models # type: ignore

# Create your models here.
        
class producto(models.Model):
    id =models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, verbose_name='titulo producto')
    imagen = models.ImageField(upload_to='myapp/static/imagenes/',verbose_name='imagen producto',null=True)
    descripcion=models.TextField(verbose_name='descripcion producto',null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='precio producto')
    
    def __str__(self):
        fila ="Nombre del producto"+ self.titulo + "____" + "Descripción:"+self.descripcion
        return fila
    
    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()

class cliente(models.Model):
    cedula = models.IntegerField(max_length=20, primary_key=True, verbose_name="Cédula")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    email = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    rol = models.IntegerField(verbose_name="Rol")
    username = models.CharField(max_length=50, unique=True, verbose_name="Nombre de Usuario")

class carrito(models.Model):
    id =models.AutoField(primary_key=True)
    idproducto = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    cedula = models.ForeignKey(cliente, on_delete=models.CASCADE, verbose_name="Cliente")

"""

class Project(models.Model):
    name = models.CharField(max_length=200)


    def __str__(self):
        return self.name

class Tak(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    done =models.BooleanField(default=False)

    def __str__(self):
        return self.title + ' - '+ self.project.name
"""


from django import forms
from .models import producto,carrito,cliente

class productoForm(forms.ModelForm):
    class Meta:
        model = producto
        fields ='__all__'

class carrritoForm(forms.ModelForm):
    class Meta:
        model = carrito
        fields ='__all__'

class clienteForm(forms.ModelForm):
    class Meta:
        model = cliente
        fields ='__all__'


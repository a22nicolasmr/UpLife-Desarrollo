from django import forms
from .models import Usuarios

class RexistroForm(forms.ModelForm):
    class Meta:
      model=Usuarios
      fields=['nome','email','nome_usuario','contrasinal']
      labels={
          "nome":"Nome Completo",
          "email":"Email",
          "nome_usuario":"Nome de Usuario",
          "contrasinal":"Contrasinal"
      }
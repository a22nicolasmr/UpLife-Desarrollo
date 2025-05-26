from django.db import models
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
import os
from django.contrib.auth.hashers import check_password
from cloudinary.uploader import destroy
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_save
# opcions modo_aplicacion
MODO_CHOICES = [
    ('C', 'Claro'),
    ('E', 'Escuro'),
]
class Usuarios(models.Model):
    id_usuario = models.BigAutoField(primary_key=True)
    nome=models.CharField(max_length=100)
    nome_usuario=models.CharField(max_length=100,unique=True)
    email=models.EmailField(max_length=255, unique=True)
    contrasinal=models.CharField(max_length=100)
    imaxe_perfil= CloudinaryField('image', blank=True, null=True)
    xenero=models.CharField(max_length=7, null=True, blank=True)
    altura=models.IntegerField(null=True, blank=True)
    peso=models.IntegerField(null=True, blank=True)
    obxectivo=models.CharField(max_length=30, null=True, blank=True)
    actividade=models.CharField(max_length=30,null=True, blank=True)
    idade=models.IntegerField(null=True, blank=True)
    calorias_diarias=models.IntegerField(null=True, blank=True)
    auga_diaria=models.IntegerField(null=True, blank=True)
    modo_aplicacion=models.CharField(max_length=1,choices=MODO_CHOICES)
    
    def set_password(self, raw_password):
        self.contrasinal = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.contrasinal)
    
# class Usuarios(models.Model):
#     id_usuario = models.BigAutoField(primary_key=True)
#     nome=models.CharField(max_length=100)
#     nome_usuario=models.CharField(max_length=100,unique=True)
#     email=models.EmailField(max_length=255, unique=True)
#     contrasinal=models.CharField(max_length=100)
#     imaxe_perfil= CloudinaryField('image', blank=True, null=True)
#     xenero=models.CharField(max_length=7, null=True, blank=True)
#     altura=models.IntegerField(null=True, blank=True)
#     peso=models.IntegerField(null=True, blank=True)
#     obxectivo=models.CharField(max_length=30, null=True, blank=True)
#     actividade=models.CharField(max_length=30,null=True, blank=True)
#     idade=models.IntegerField(null=True, blank=True)
#     calorias_diarias=models.IntegerField(null=True, blank=True)
#     auga_diaria=models.IntegerField(null=True, blank=True)
#     modo_aplicacion=models.CharField(max_length=1,choices=MODO_CHOICES)

#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.contrasinal = make_password(self.contrasinal)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"nome={self.nome}, nome_usuario={self.nome_usuario}, email={self.email}, contrasinal={self.contrasinal}, imaxe_perfil={self.imaxe_perfil}, altura={self.altura}, peso={self.peso}, obxectivo={self.obxectivo}, actividade={self.actividade}, idade={self.idade}, calorias_diarias={self.calorias_diarias}, auga_diaria={self.auga_diaria}, modo_aplicacion={self.modo_aplicacion}"

# cando se actualiza a imaxe de perfil , borrase a existente e actualizase ca nova
# @receiver(models.signals.pre_save, sender=Usuarios)
# def auto_delete_old_file_on_change(sender, instance, **kwargs):
#     if not instance.pk:
#         return

#     try:
#         old_file = sender.objects.get(pk=instance.pk).imaxe_perfil
#     except sender.DoesNotExist:
#         return

#     new_file = instance.imaxe_perfil

#     if old_file and old_file != new_file:
#         try:
#             old_file.delete(save=False)  # ✅ Esto funciona con Cloudinary
#         except Exception as e:
#             print(f"Error eliminando archivo anterior: {e}")


# BORRAR ARCHIVO CLOUDINARY
# @receiver(pre_save, sender=Usuarios)
# def auto_delete_old_file_on_change(sender, instance, **kwargs):
#     if not instance.pk:
#         return

#     try:
#         old_file = sender.objects.get(pk=instance.pk).imaxe_perfil
#     except sender.DoesNotExist:
#         return

#     new_file = instance.imaxe_perfil

#     if old_file and old_file != new_file:
#         try:
#             destroy(old_file.public_id)
#         except Exception as e:
#             print(f"Error eliminando archivo anterior: {e}")
            

            
class Auga(models.Model):
    id_auga=models.BigAutoField(primary_key=True)
    cantidade=models.IntegerField()
    hora=models.TimeField()
    usuario=models.ForeignKey(Usuarios,on_delete=models.CASCADE)
    data=models.DateField(null=True, blank=True)
    

    def __str__(self):
        return f"cantidade={self.cantidade}, hora={self.hora}, usuario={self.usuario}"

class Medallas(models.Model):
    id_medalla=models.BigAutoField(primary_key=True)
    nome=models.CharField(max_length=50,unique=True)
    descripcion=models.CharField(max_length=200,unique=True)
    completado=models.BooleanField()
    icona=CloudinaryField('image', blank=True, null=True)
    usuarios=models.ManyToManyField(Usuarios)
    def __str__(self):
        return f"nome={self.nome}, descripcion={self.descripcion}, completado={self.completado}, icona={self.icona}"

class Tarefas(models.Model):
    id_tarefa=models.BigAutoField(primary_key=True)
    hora=models.TimeField(blank=True,null=True)
    titulo=models.CharField(max_length=255)
    data=models.DateField()
    completado=models.BooleanField()
    data=models.DateField(null=True, blank=True)
    usuario=models.ForeignKey(Usuarios,on_delete=models.CASCADE)

    def __str__(self):
        return f"titulo={self.titulo}, hora={self.hora}, data={self.data}, completado={self.completado}, usuario={self.usuario}"

class Categorias(models.Model):
    id_categoria=models.BigAutoField(primary_key=True)
    nome=models.CharField(max_length=10)

    def __str__(self):
        return f"nome={self.nome}"

class Exercicios(models.Model):
    id_exercicio=models.BigAutoField(primary_key=True)
    nome=models.CharField(max_length=255)
    repeticions=models.CharField(max_length=10)
    peso=models.FloatField()
    data=models.DateField(null=True, blank=True)
    usuario=models.ForeignKey(Usuarios,on_delete=models.CASCADE)
    categoria=models.ForeignKey(Categorias,on_delete=models.CASCADE)

    def __str__(self):
        return f"nome={self.nome}, repeticions={self.repeticions}, peso={self.peso}, usuario={self.usuario}, categoria={self.categoria}"

class Plantillas(models.Model):
    id_plantilla = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    icona = models.CharField(max_length=255)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, null=True, blank=True)
    exercicios = models.ManyToManyField('Exercicios', blank=True)

    def __str__(self):
        return f"nome={self.nome}, icona={self.icona}, exercicios={[e.nome for e in self.exercicios.all()]}"
    
class UsoPlantilla(models.Model):
    id = models.BigAutoField(primary_key=True)
    plantilla = models.ForeignKey(Plantillas, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    data = models.DateField()

    def __str__(self):
        return f"{self.plantilla.nome} usada o {self.data} por {self.usuario.nome_usuario}"


class Comidas(models.Model):
    id_comida=models.BigAutoField(primary_key=True)
    nome=models.CharField(max_length=255)
    peso=models.FloatField()
    graxas=models.FloatField()
    carbohidratos=models.FloatField()
    proteinas=models.FloatField()
    calorias=models.FloatField()
    data=models.DateField(null=True, blank=True)
    usuario=models.ForeignKey(Usuarios,on_delete=models.CASCADE)

    def __str__(self):
        return f"nome={self.nome}, peso={self.peso}, graxas={self.graxas}, carbohidratos={self.carbohidratos}, proteinas={self.proteinas}, calorias={self.calorias}, usuario={self.usuario}"

class Grupos(models.Model):
    id_grupo=models.BigAutoField(primary_key=True)
    nome=models.CharField(max_length=255)
    icona= models.CharField(max_length=255)
    comidas=models.ManyToManyField(Comidas)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return self.nome


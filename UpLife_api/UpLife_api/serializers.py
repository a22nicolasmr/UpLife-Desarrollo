from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Usuarios, Auga, Medallas, Tarefas, Categorias, Exercicios, Plantillas, Comidas, Grupos

# facer apis con todos os campos de todos os modelos
class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'

    def update(self, instance, validated_data):
        # Se se actualiza a contrasinal, cifrala antes de gardar
        if 'contrasinal' in validated_data:
            validated_data['contrasinal'] = make_password(validated_data['contrasinal'])
        return super().update(instance, validated_data)

class AugaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auga
        fields = '__all__'

class MedallasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medallas
        fields = '__all__'

class TarefasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefas
        fields = '__all__'

class CategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorias
        fields = '__all__'

class ExerciciosSerializer(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categorias.objects.all())
    class Meta:
        model = Exercicios
        fields = '__all__'

# necesario para que ao facer PATCH nas plantillas acepte unha lista de ids de exercicios
class PlantillasSerializer(serializers.ModelSerializer):
    exercicios = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Exercicios.objects.all(),
        required=False,  # Esto asegura que no sea obligatorio
        allow_null=True,  # Esto permite que pueda ser null
        default=[]  # Esto asigna un array vacío si no se envía ningún valor
    )

    class Meta:
        model = Plantillas
        fields = '__all__'


# necesario para listar os exercicios
class PlantillasDetailSerializer(serializers.ModelSerializer):
    exercicios = ExerciciosSerializer(many=True, read_only=True)

    class Meta:
        model = Plantillas
        fields = '__all__'


class ComidasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comidas
        fields = '__all__'

# Serializer básico con solo las claves primarias de comidas
class GruposSerializer(serializers.ModelSerializer):
    comidas = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Comidas.objects.all(),
        required=False,
        allow_null=True,
        default=[]
    )

    class Meta:
        model = Grupos
        fields = '__all__'


# Serializer detallado con los datos completos de comidas
class GruposDetailSerializer(serializers.ModelSerializer):
    comidas = ComidasSerializer(many=True, read_only=True)
    class Meta:
        model = Grupos
        fields = '__all__'


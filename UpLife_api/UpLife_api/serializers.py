from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Usuarios, Auga, Medallas, Tarefas, Categorias, Exercicios, Plantillas, Comidas, Grupos,UsoPlantilla

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'

    def update(self, instance, validated_data):
        
        if 'contrasinal' in validated_data:
            validated_data['contrasinal'] = make_password(validated_data['contrasinal'])
        return super().update(instance, validated_data)
    
    def create(self, validated_data):
        if 'contrasinal' in validated_data:
            validated_data['contrasinal'] = make_password(validated_data['contrasinal'])
        return super().create(validated_data)


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

class PlantillasSerializer(serializers.ModelSerializer):
    exercicios = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Exercicios.objects.all(),
        required=False,  
        allow_null=True,  
        default=[] 
    )

    class Meta:
        model = Plantillas
        fields = '__all__'


class PlantillasDetailSerializer(serializers.ModelSerializer):
    exercicios = ExerciciosSerializer(many=True, read_only=True)

    class Meta:
        model = Plantillas
        fields = ['id_plantilla','usuario', 'nome', 'icona', 'exercicios']


class ComidasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comidas
        fields = '__all__'

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


class GruposDetailSerializer(serializers.ModelSerializer):
    comidas = ComidasSerializer(many=True, read_only=True)
    class Meta:
        model = Grupos
        fields='__all__'

class PlantillasMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plantillas
        fields = ['id_plantilla','usuario', 'nome', 'icona']

class UsoPlantillaSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.nome_usuario', read_only=True)
    plantilla = serializers.PrimaryKeyRelatedField(queryset=Plantillas.objects.all())

    class Meta:
        model = UsoPlantilla
        fields = ['id', 'plantilla', 'usuario', 'usuario_nome', 'data']



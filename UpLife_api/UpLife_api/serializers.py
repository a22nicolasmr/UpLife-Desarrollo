from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Usuarios, Auga, Medallas, Tarefas, Categorias, Exercicios, Plantillas, Comidas, Grupos,UsoPlantilla
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['nome_usuario'] = user.nome_usuario
#         return token

#     def validate(self, attrs):
#         attrs['username'] = attrs.get('nome_usuario')  # mapeamos nome_usuario → username
#         return super().validate(attrs)

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
        fields = ['id_plantilla','usuario', 'nome', 'icona', 'exercicios']


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
        fields='__all__'

class PlantillasMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plantillas
        fields = ['id_plantilla','usuario', 'nome', 'icona']

# class UsoPlantillaSerializer(serializers.ModelSerializer):
#     plantilla = PlantillasDetailSerializer(read_only=True)
#     plantilla_id = serializers.PrimaryKeyRelatedField(
#         queryset=Plantillas.objects.all(), source='plantilla', write_only=True
#     )
#     usuario = serializers.PrimaryKeyRelatedField(queryset=Usuarios.objects.all())
#     usuario_nome = serializers.CharField(source='usuario.nome_usuario', read_only=True)

#     class Meta:
#         model = UsoPlantilla
#         fields = ['id', 'plantilla', 'plantilla_id', 'usuario', 'usuario_nome', 'data']

# class UsoPlantillaSerializer(serializers.ModelSerializer):
#     usuario_nome = serializers.CharField(source='usuario.nome_usuario', read_only=True)

#     class Meta:
#         model = UsoPlantilla
#         fields = ['id', 'plantilla', 'usuario', 'usuario_nome', 'data']

class UsoPlantillaSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.nome_usuario', read_only=True)
    plantilla = serializers.PrimaryKeyRelatedField(queryset=Plantillas.objects.all())

    class Meta:
        model = UsoPlantilla
        fields = ['id', 'plantilla', 'usuario', 'usuario_nome', 'data']

    # def get_plantilla(self, obj):
    #     return {
    #         'id_plantilla': obj.plantilla.id_plantilla,
    #         'nome': obj.plantilla.nome,
    #         'icona': obj.plantilla.icona
    #     }


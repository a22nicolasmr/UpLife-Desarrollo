from .models import Usuarios, Auga, Medallas, Tarefas, Categorias, Exercicios, Plantillas, Comidas, Grupos
from .serializers import UsuariosSerializer, AugaSerializer, MedallasSerializer, TarefasSerializer, CategoriasSerializer, ExerciciosSerializer, PlantillasSerializer, ComidasSerializer, GruposSerializer,PlantillasDetailSerializer,GruposDetailSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework import viewsets

# validacion de campos de inicio de sesión
@api_view(['POST'])
def login_usuario(request):
    identificador = request.data.get('identificador')  # pode ser email ou nome_usuario
    contrasinal = request.data.get('contrasinal')

    if not identificador or not contrasinal:
        return Response({'erro': 'Faltan campos obrigatorios'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if '@' in identificador:
            usuario = Usuarios.objects.get(email=identificador)
        else:
            usuario = Usuarios.objects.get(nome_usuario=identificador)

        if check_password(contrasinal, usuario.contrasinal):
            return Response({'mensaxe': 'Login correcto'}, status=status.HTTP_200_OK)
        else:
            return Response({'erro': 'Contrasinal incorrecto'}, status=status.HTTP_401_UNAUTHORIZED)

    except Usuarios.DoesNotExist:
        return Response({'erro': 'Usuario non existe'}, status=status.HTTP_404_NOT_FOUND)
    
# creación de endpoint automáticamente para todos os modelos definidos de forma que aceptarán todo tipo de peticións
class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer

class AugaViewSet(viewsets.ModelViewSet):
    queryset = Auga.objects.all()
    serializer_class = AugaSerializer

class MedallasViewSet(viewsets.ModelViewSet):
    queryset = Medallas.objects.all()
    serializer_class = MedallasSerializer

class TarefasViewSet(viewsets.ModelViewSet):
    queryset = Tarefas.objects.all()
    serializer_class = TarefasSerializer

class CategoriasViewSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.all()
    serializer_class = CategoriasSerializer

class ExerciciosViewSet(viewsets.ModelViewSet):
    queryset = Exercicios.objects.all()
    serializer_class = ExerciciosSerializer

class PlantillasViewSet(viewsets.ModelViewSet):
    queryset = Plantillas.objects.all()
    serializer_class = PlantillasSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return PlantillasDetailSerializer
        return PlantillasSerializer


class ComidasViewSet(viewsets.ModelViewSet):
    queryset = Comidas.objects.all()
    serializer_class = ComidasSerializer

class GruposViewSet(viewsets.ModelViewSet):
    queryset = Grupos.objects.all()
    serializer_class = GruposSerializer
    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return GruposDetailSerializer
        return GruposSerializer

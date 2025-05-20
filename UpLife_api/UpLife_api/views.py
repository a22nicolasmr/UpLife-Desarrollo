from .models import Usuarios, Auga, Medallas, Tarefas, Categorias, Exercicios, Plantillas, Comidas, Grupos,UsoPlantilla
from .serializers import UsuariosSerializer, AugaSerializer, MedallasSerializer, TarefasSerializer, CategoriasSerializer, ExerciciosSerializer, PlantillasSerializer, ComidasSerializer, GruposSerializer,PlantillasDetailSerializer,GruposDetailSerializer,UsoPlantillaSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework import viewsets
from django.core.mail import send_mail
import logging
import json
from django.http import JsonResponse
logger = logging.getLogger(__name__)
from django.views.decorators.csrf import csrf_exempt

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

class UsoPlantillaViewSet(viewsets.ModelViewSet):
    queryset = UsoPlantilla.objects.all()
    serializer_class = UsoPlantillaSerializer

    def get_queryset(self):
        """
        Permite filtrar por usuario si se pasa como query param.
        Ej: /api/plantillas-uso/?usuario=3
        """
        queryset = super().get_queryset()
        usuario_id = self.request.query_params.get('usuario')
        if usuario_id:
            queryset = queryset.filter(usuario=usuario_id)
        return queryset
    
from rest_framework.decorators import api_view
from rest_framework.response import Response

# @api_view(["POST"])
# def enviar_codigo_confirmacion(request):
#     email = request.data.get("email")
#     codigo = request.data.get("codigo")

#     if not email or not codigo:
#         return Response({"error": "Datos incompletos"}, status=400)

#     try:
#         send_mail(
#             subject="Código de confirmación - UpLife",
#             message=f"Tu código de confirmación es: {codigo}",
#             from_email="uplifedaw@gmail.com",
#             recipient_list=[email],
#             fail_silently=False,
#         )
#         return Response({"mensaje": "Correo enviado correctamente"})
#     except Exception as e:
#         print("ERROR AL ENVIAR EMAIL:", e)  # 👈 te mostrará el motivo real
#         return Response({"error": str(e)}, status=500)

@csrf_exempt
def enviar_codigo_confirmacion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # <-- aquí se procesa el JSON manualmente
            email = data.get('email')
            codigo = data.get('codigo')
            
            send_mail(
                subject="Código de confirmación - UpLife",
                message=f"Tu código de confirmación es: {codigo}",
                from_email="uplifedaw@gmail.com",
                recipient_list=[email],
                fail_silently=False,
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
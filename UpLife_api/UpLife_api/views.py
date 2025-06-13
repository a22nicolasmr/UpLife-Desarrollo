from .models import Usuarios, Auga, Medallas, Tarefas, Categorias, Exercicios, Plantillas, Comidas, Grupos,UsoPlantilla
from .serializers import UsuariosSerializer, AugaSerializer, MedallasSerializer, TarefasSerializer, CategoriasSerializer, ExerciciosSerializer, PlantillasSerializer, ComidasSerializer, GruposSerializer,PlantillasDetailSerializer,GruposDetailSerializer,UsoPlantillaSerializer
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework import viewsets
from django.core.mail import send_mail
import logging
import json
from django.http import JsonResponse
logger = logging.getLogger(__name__)
from django.views.decorators.csrf import csrf_exempt
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .auth import CustomJWTAuthentication
from django.core.mail import EmailMessage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated

# comprobar se un email existe sen necesidade de acceder a api
@api_view(['POST'])
@permission_classes([AllowAny])
def comprobar_email_existente(request):
    email = request.data.get("email")
    if not email:
        return Response({"error": "Email requerido"}, status=status.HTTP_400_BAD_REQUEST)

    existe = Usuarios.objects.filter(email=email).exists()
    return Response({"existe": existe})


# obter un usuario específico sen necesidade de acceder a api
@api_view(['POST'])
@permission_classes([AllowAny])
def obter_usuario_por_email(request):
    email = request.data.get("email")
    if not email:
        return Response({"error": "Email requerido"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        usuario = Usuarios.objects.get(email=email)
        return Response({"id_usuario": usuario.id_usuario})
    except Usuarios.DoesNotExist:
        return Response({"error": "Usuario non atopado"}, status=status.HTTP_404_NOT_FOUND)

class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"detail": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Usuarios.objects.get(nome_usuario=username)
        except Usuarios.DoesNotExist:
            return Response({"detail": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"detail": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


        payload = {
            "user_id": user.id_usuario,
            "username": user.nome_usuario,
            "exp": datetime.utcnow() + timedelta(hours=24),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return Response({
            "access": token,
        })
        
        
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

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]

        # Permitir PATCH si solo se envía contraseña e email
        if self.request.method == "PATCH":
            email = self.request.data.get("email")
            contrasinal = self.request.data.get("contrasinal")
            if email and contrasinal:
                return [AllowAny()]

        return [IsAuthenticated()]


class AugaViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Auga.objects.all()
    serializer_class = AugaSerializer

class MedallasViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Medallas.objects.all()
    serializer_class = MedallasSerializer

class TarefasViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Tarefas.objects.all()
    serializer_class = TarefasSerializer

class CategoriasViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Categorias.objects.all()
    serializer_class = CategoriasSerializer

class ExerciciosViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Exercicios.objects.all()
    serializer_class = ExerciciosSerializer

class PlantillasViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Plantillas.objects.all()  

    def get_queryset(self):
        return Plantillas.objects.prefetch_related("exercicios")

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return PlantillasDetailSerializer
        return PlantillasSerializer

class ComidasViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Comidas.objects.all()
    serializer_class = ComidasSerializer

class GruposViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Grupos.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["GET", "HEAD", "OPTIONS"]:
            return GruposDetailSerializer
        return GruposSerializer

    def get_queryset(self):
        return Grupos.objects.select_related("usuario").prefetch_related("comidas")


class UsoPlantillaViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
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
    
# enviar código de de cambio de contrasinal
@api_view(["POST"])
@permission_classes([AllowAny])
def enviar_codigo_confirmacion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  
            email = data.get('email')
            codigo = data.get('codigo')

            asunto = "🔐 Código de confirmación - UpLife"
            corpo_html = f"""
                <html>
                  <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #4CAF50;">Código de Confirmación</h2>
                    <p>O teu código de confirmación é:</p>
                    <div style="font-size: 24px; font-weight: bold; color: #2196F3; margin: 20px 0;">
                      {codigo}
                    </div>
                    <p>Introduce este código na aplicación para continuar co rexistro.</p>
                    <hr />
                    <p style="font-size: 0.9em; color: #888;">UpLife - Xestiona o teu día con éxito 🚀</p>
                  </body>
                </html>
            """

            email_msg = EmailMessage(
                subject=asunto,
                body=corpo_html,
                from_email="uplifedaw@gmail.com",
                to=[email],
            )
            email_msg.content_subtype = "html"  
            email_msg.send(fail_silently=False)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


# enviar un correo electrónico de alerta
@api_view(["POST"])
@permission_classes([AllowAny])
def enviar_recordatorio(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            tarefa_nome = data.get('tarefa')
            hora = data.get('hora')

            asunto = "🔔 Lembranza de tarefa - UpLife"
            corpo_html = f"""
                <html>
                  <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                    <h2 style="color: #4CAF50;">🔔 Recordatorio de tarefa</h2>
                    <p><strong>Tarefa:</strong> {tarefa_nome}</p>
                    <p><strong>Hora:</strong> {hora}</p>
                    <p style="color: #ff5722;"><strong>⚠️ Faltan só 2 minutos!</strong></p>
                    <hr/>
                    <p style="font-size: 0.9em; color: #777;">UpLife - Xestiona o teu día con éxito 🚀</p>
                  </body>
                </html>
            """

            email_msg = EmailMessage(
                subject=asunto,
                body=corpo_html,
                from_email="uplifedaw@gmail.com",
                to=[email],
            )
            email_msg.content_subtype = "html"  # Importante: indicar que é HTML

            email_msg.send(fail_silently=False)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error(f"Erro enviando recordatorio: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

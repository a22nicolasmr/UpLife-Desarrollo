# api/auth.py
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from .models import Usuarios  

# customización de auntenticación con token
class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expirado")
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed("Token inválido")

        try:
            user_id = payload.get("user_id")
            user = Usuarios.objects.get(id_usuario=user_id)
        except Usuarios.DoesNotExist:
            raise AuthenticationFailed("Usuario non atopado")

        return (user, token)

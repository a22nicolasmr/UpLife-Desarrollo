# api/auth.py
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from .models import Usuarios  # ou o teu modelo real
import logging
logger = logging.getLogger(__name__)
logger.warning("⚠️ Aquí estamos dentro de CustomJWTAuthentication")

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        print("🟡 Authorization header recibido:", auth_header)

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        print("🔐 Token extraído:", token)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print("✅ Payload decodificado:", payload)
        except jwt.ExpiredSignatureError:
            print("❌ Token expirado")
            raise AuthenticationFailed("Token expirado")
        except jwt.InvalidTokenError as e:
            print("❌ Token inválido:", str(e))
            raise AuthenticationFailed("Token inválido")

        try:
            user = Usuarios.objects.get(id_usuario=payload["user_id"])
            print("✅ Usuario atopado:", user)
        except Usuarios.DoesNotExist:
            raise AuthenticationFailed("Usuario non atopado")

        # 💥 FALTABA ISTO
        
        return (user, token)



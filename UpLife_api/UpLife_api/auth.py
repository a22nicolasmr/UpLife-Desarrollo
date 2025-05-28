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
        logger.warning("⚠️ Dentro de CustomJWTAuthentication")

        auth_header = request.headers.get("Authorization")
        logger.warning(f"🔍 Header recibido: {auth_header}")

        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("⛔ Header vacío ou mal formado")
            return None

        token = auth_header.split(" ")[1]
        logger.warning(f"🔐 Token extraído: {token}")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            logger.warning(f"✅ Token decodificado: {payload}")
        except jwt.ExpiredSignatureError:
            logger.warning("❌ Token expirado")
            raise AuthenticationFailed("Token expirado")
        except jwt.InvalidTokenError as e:
            logger.warning(f"❌ Token inválido: {str(e)}")
            raise AuthenticationFailed("Token inválido")

        try:
            user_id = payload.get("user_id")
            logger.warning(f"🔎 Buscando usuario con ID: {user_id}")
            user = Usuarios.objects.get(id_usuario=user_id)
            logger.warning(f"✅ Usuario encontrado: {user}")
        except Usuarios.DoesNotExist:
            logger.warning(f"❌ Usuario non atopado con ID: {user_id}")
            raise AuthenticationFailed("Usuario non atopado")

        logger.warning("🟢 Autenticación completada correctamente")
        return (user, token)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import login_usuario
from .views import enviar_codigo_confirmacion
from django.urls import path
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()
router.register(r'usuarios', views.UsuariosViewSet)
router.register(r'auga', views.AugaViewSet)
router.register(r'medallas', views.MedallasViewSet)
router.register(r'tarefas', views.TarefasViewSet)
router.register(r'categorias', views.CategoriasViewSet)
router.register(r'exercicios', views.ExerciciosViewSet)
router.register(r'plantillas', views.PlantillasViewSet)
router.register(r'comidas', views.ComidasViewSet)
router.register(r'grupos', views.GruposViewSet)
router.register(r'plantillas-uso', views.UsoPlantillaViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', login_usuario),
    path("enviar-codigo/", enviar_codigo_confirmacion),
    path('token/', CustomTokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),
]

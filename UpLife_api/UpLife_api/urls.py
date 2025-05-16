from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import login_usuario
from .views import enviar_codigo_confirmacion
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
]

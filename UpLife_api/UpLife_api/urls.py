from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import enviar_codigo_confirmacion,login_usuario,CustomLoginView
from django.urls import path

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
    path('api/login/', CustomLoginView.as_view(), name='custom-login'),
    path('enviar-recordatorio/', views.enviar_recordatorio),
    path("comprobar-email/", views.comprobar_email_existente),
    path("obter-usuario-id/", views.obter_usuario_por_email),
]
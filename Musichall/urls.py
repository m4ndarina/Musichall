"""
URL configuration for Musichall project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from Modulos.Principal.views import *
from Modulos.Academico.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('landing_page/', landing_page),
    path('login/', user_login, name='login'),
    path('404/', error_404, name='error_404'),
    path('test/', test, name="test"),
    path('iniciotutor/', iniciotutor, name="iniciotutor"),
    path('inicioestudiante/', inicioestudiante, name="inicioestudiante"),
    path('metronomo/', metronomo, name='metronomo'),
    path('afinador/', afinador, name='afinador'),
    path('acordes/', acordes, name='acordes'),
    
    path('agregarcolegio/', agregar_colegio, name="agregar_colegio"),
    path('listacolegio/', listado_colegio, name='listadocolegio'),
    path('colegio/', buscar_colegio, name='colegio'),
    path('modificarcolegio/<codigo>/', modificar_colegio, name="modificar_colegio"),
    path('eliminar-colegio/<codigo>/', eliminar_colegio, name="eliminar_colegio"),
    
    path('agregarano/', agregar_ano, name="agregar_ano"),
    path('listaanos/', listado_anos, name='listadoanos'),
    path('anolectivo/', buscar_ano, name='ano'),
    path('modificarano/<codigo>/', modificar_ano, name="modificar_ano"),
    path('eliminar-ano/<codigo>/', eliminar_ano, name="eliminar_ano"),

    path('agregargrado/', agregar_grado, name="agregar_grado"),
    path('listagrado/', listado_grados, name='listadogrados'),
    path('grado/', buscar_grado, name='grado'),
    path('modificargrado/<codigo>/', modificar_grado, name="modificar_grado"),
    path('eliminar-grado/<codigo>/', eliminar_grado, name="eliminar_grado"),

    path('agregaracudiente/', agregar_acudiente, name="agregar_acudiente"),
    path('listaacudiente/', listado_acudiente, name='listadoacudiente'),
    path('acudiente/', buscar_acudiente, name='acudiente'),
    path('modificaracudiente/<codigo>/', modificar_acudiente, name="modificar_acudiente"),
    path('eliminar-acudiente/<codigo>/', eliminar_acudiente, name="eliminar_acudiente"),

    path('agregarestudiante/', agregar_estudiante, name="agregar_estudiante"),
    path('listaestudiantes/', listado_estudiantes, name='listadoestudiantes'),
    path('estudiante/', buscar_estudiante, name='estudiante'),
    path('modificarestudiante/<codigo>/', modificar_estudiante, name="modificar_estudiante"),
    path('eliminar-estudiante/<codigo>/', eliminar_estudiante, name="eliminar_estudiante"),
    path('perfil-estudiante/<codigo>/', perfil_estudiante, name="perfil_estudiante"),
    path('perfil-estudiante/', perfil_estudiante2, name="perfil_estudiante2"),
    path('listaest_pdf/', estudiante_pdf, name='crear_pdf'),

    path('agregartutor/', agregar_tutor, name="agregar_tutor"),
    path('listatutor/', listado_tutor, name='listadotutor'),
    path('tutor/', buscar_tutor, name='tutor'),
    path('modificartutor/<codigo>/', modificar_tutor, name="modificar_tutor"),
    path('eliminar-tutor/<codigo>/', eliminar_tutor, name="eliminar_tutor"),
    path('perfil-tutor/<codigo>/', perfil_tutor, name="perfil_tutor"),
    path('perfil-tutor/', perfil_tutor2, name="perfil_tutor2"),

    path('agregarcurso/<r>/', agregar_curso, name="agregar_curso"),
    path('listacurso/', listado_curso, name='listadocurso'),
    path('listacurso_est/', listado_curso_estudiantes, name='listadocurso_estudiantes'),
    path('listacurso_tut/', listado_curso_tutores, name='listadocurso_tutores'),
    path('curso/', buscar_curso, name='curso'),
    path('curso_tutor/', buscar_curso_tutor, name='curso_tutor'),
    path('curso_estudiante/', buscar_curso_estudiante, name='curso_estudiante'),
    path('modificarcurso/<codigo>/', modificar_curso, name="modificar_curso"),
    path('eliminar-curso/<codigo>/', eliminar_curso, name="eliminar_curso"),

    path('agregarmatricula/', agregar_matricula, name="agregar_matricula"),
    path('listamatricula/', listado_matricula, name='listadomatricula'),
    path('matricula/', buscar_matricula, name='matricula'),
    path('modificarmatricula/<codigo>/', modificar_matricula, name="modificar_matricula"),
    path('eliminar-matricula/<codigo>/', eliminar_matricula, name="eliminar_matricula"),

    path('agregardesempeno/<curso>/', agregar_desempeno, name="agregar_desempeno"),
    path('cursos/<codigo>/desempenos/', listado_desempeno, name='listadodesempeno'),
    path('info-desempeno/<codigo>/', ampliar_desempeno, name='ampliar_desempeno'),
    path('desempeno/', buscar_desempeno, name='desempeno'),
    path('modificardesempeno/<codigo>/', modificar_desempeno, name="modificar_desempeno"),
    path('eliminar-desempeno/<codigo>/', eliminar_desempeno, name="eliminar_desempeno"),

    path('agregarmaterial/<desempeno>/', agregar_material, name="agregar_material"),
    path('mod-material/<codigo>/<r>', mod_material, name="mod_material"),
    path('eliminar-material2/<desempeno>/<codigo>/', eliminar_material2, name="eliminar_material2"),
    path('info-material/<codigo>/', ampliar_material, name='ampliar_material'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
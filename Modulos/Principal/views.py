from django.shortcuts import render, redirect
from Modulos.Academico.models import Estudiante, Tutor, Admin
from django.contrib import messages


# Create your views here.
def landing_page(request):
	return render(request, "landing_page.html", {})

def error_404(request):
	return render(request, "404.html", {})

def user_login(request):
    if request.method == 'POST':
        nombre_usu = request.POST['nombre_usu']
        contrasena = request.POST['contrasena']

        try:
            estudiante = Estudiante.objects.get(nombre_usu=nombre_usu)
            if estudiante.contrasena == contrasena:
                # Iniciar sesión del estudiante
                request.session['identificacion'] = estudiante.dni_estudiante
                request.session['nombre'] = estudiante.nombreCompleto()
                request.session['rol'] = estudiante.rol
                # ...
                return redirect('listadocurso_estudiantes')
        except Estudiante.DoesNotExist:
            pass  # Manejar la excepción de estudiante no encontrado

        try:
            tutor = Tutor.objects.get(nombre_usu=nombre_usu)
            if tutor.contrasena == contrasena:
                # Iniciar sesión del docente
                request.session['identificacion'] = tutor.dni_tutor
                request.session['nombre'] = tutor.nombreCompleto()
                request.session['rol'] = tutor.rol
                # ...
                return redirect('listadocurso_tutores')
        except Tutor.DoesNotExist:
            pass  # Manejar la excepción de docente no encontrado

        try:
            admin = Admin.objects.get(nombre_usu=nombre_usu)
            if admin.contrasena == contrasena:
                # Iniciar sesión del personal administrativo
                request.session['identificacion'] = admin.dni_admin
                request.session['nombre'] = admin.nombreCompleto()
                request.session['rol'] = admin.rol
                # ...
                return redirect('listadocurso')
        except Admin.DoesNotExist:
            pass  # Manejar la excepción de personal administrativo no encontrado

        # Si no se encuentra el usuario en ninguna tabla, mostrar mensaje de error
        messages.error(request, 'Usuario no encontrado.')

    return render(request, 'login.html')
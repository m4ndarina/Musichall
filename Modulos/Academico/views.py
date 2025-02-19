from django.http import  HttpResponse
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.template import Template, Context
from django.template import loader
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View
from django.shortcuts import HttpResponseRedirect


#Models/Forms
from .forms import ColegioForm, anoLectivoForm, GradosForm, AcudienteForm, EstudianteForm, TutorForm, CursoForm, MatriculaForm, DesempenoForm, MaterialForm
from .models import Colegio, anoLectivo
from .models import Grados, Acudiente
from .models import Estudiante, Tutor
from .models import Curso, Matricula
from .models import Desempeno, Material

#Buscar
from django.db.models import Q

#Pdf
from .utils import render_to_pdf
from io import BytesIO
from django.template import context
from django.template.loader import get_template
from xhtml2pdf import pisa


# Create your views here.

def base_template_selector(request):
    rol_usuario = request.session.get('rol')

    base_template = 'index.html'

    if rol_usuario == 'Administrador':
        base_template = 'index.html'
    elif rol_usuario == 'Tutor':
        base_template = 'indextutor.html'
    elif rol_usuario == 'Estudiante':
        base_template = 'indexestudiante.html'

    return {'base_template': base_template}

def test(request):
    if not request.session.has_key('identificacion'):
        return redirect('login')

    rol_usuario = request.session['rol']
    rol_permitido = 'Administrador'  # Reemplaza con el rol deseado

    if rol_usuario != rol_permitido:
        return redirect('error_404')
    
    return render(request, "test.html", {})

def iniciotutor(request):
    if not request.session.has_key('identificacion'):
        return redirect('login')

    rol_usuario = request.session['rol']
    rol_permitido = 'Tutor'  # Reemplaza con el rol deseado

    if rol_usuario != rol_permitido:
        return redirect('error_404')
    
    return render(request, "iniciotutor.html", {})

def inicioestudiante(request):
    if not request.session.has_key('identificacion'):
        return redirect('login')

    rol_usuario = request.session['rol']
    rol_permitido = 'Estudiante'  # Reemplaza con el rol deseado

    if rol_usuario != rol_permitido:
        return redirect('error_404')
    
    return render(request, "inicioestudiante.html", {})

def metronomo(request):
    if not request.session.has_key('identificacion'):
        return redirect('login')
    
    return render(request, "metronomo.html", {})

def afinador(request):
    if not request.session.has_key('identificacion'):
        return redirect('login')
    
    return render(request, "afinador.html", {})

def acordes(request):
    if not request.session.has_key('identificacion'):
        return redirect('login')
    
    return render(request, "acordes.html", {})



#Colegio

def agregar_colegio(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'  # Reemplaza con el rol deseado

	if rol_usuario != rol_permitido:
		return redirect('error_404')
    
	data={
		'form': ColegioForm(),
		'titulo': "Agregar nuevo colegio"
	}

	if request.method =='POST':
		formulario = ColegioForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			data["mensaje"]="Guardado correctamente."
		else:
			data["form"]=formulario
			data["mensaje"]="El colegio ya existe."

	data['form'].fields['codigo_colegio'].label = 'Código del colegio'
	data['form'].fields['nombre_colegio'].label = 'Nombre del colegio'
	data['form'].fields['razonsocial_colegio'].label = 'Razón social del colegio'
	data['form'].fields['direccion_colegio'].label = 'Dirección del colegio'
	data['form'].fields['telefono_colegio'].label = 'Teléfono del colegio'
	data['form'].fields['email_colegio'].label = 'Correo eléctronico del colegio'
	data['form'].fields['tipo_colegio'].label = 'Tipo del colegio'
	data['form'].fields['calendario_colegio'].label = 'Calendario'

	return render(request, 'agregarcolegio.html', data)

def buscar_colegio(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	busqueda=request.GET.get("buscar")
	colegio=Colegio.objects.all()
	if busqueda:
		colegio = Colegio.objects.filter(
			Q(nombre_colegio__icontains = busqueda) | #or (o)
			Q(razonsocial_colegio__icontains = busqueda) #__icontains para que no sea exacto
			).distinct()

	return render(request, "listacolegio.html", {"colegio":colegio})

def listado_colegio(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	listadocolegio=Colegio.objects.all()
	return render(request, "listacolegio.html",{"colegio":listadocolegio})

def eliminar_colegio(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	colegio = get_object_or_404(Colegio, codigo_colegio=codigo)
	colegio.delete()
	messages.success(request, "Eliminado correctamente.")
	return redirect("listadocolegio")

def modificar_colegio(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	colegio=get_object_or_404(Colegio, codigo_colegio=codigo)#busca un elemento

	data={
		'form':ColegioForm(instance=colegio)
	}

	if request.method=='POST':
		formulario=ColegioForm(data=request.POST, instance=colegio, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Modificado correctamente")
			#data["mensaje"]="Archivo Modificado"
		#else:
			#data["form"]=formulario
			#data["mensaje"]="El archivo no existe"
			return redirect(to='listadocolegio')
		data["form"]=formulario

	data['form'].fields['codigo_colegio'].label = 'Código del colegio'
	data['form'].fields['nombre_colegio'].label = 'Nombre del colegio'
	data['form'].fields['razonsocial_colegio'].label = 'Razón social del colegio'
	data['form'].fields['direccion_colegio'].label = 'Dirección del colegio'
	data['form'].fields['telefono_colegio'].label = 'Teléfono del colegio'
	data['form'].fields['email_colegio'].label = 'Correo eléctronico del colegio'
	data['form'].fields['tipo_colegio'].label = 'Tipo del colegio'
	data['form'].fields['calendario_colegio'].label = 'Calendario'

	return render(request, 'modificar_colegio.html', data)


#Año lectivo

def agregar_ano(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	data={
		'form': anoLectivoForm(),
		'titulo': "Agregar nuevo año lectivo"
	}

	if request.method =='POST':
		formulario = anoLectivoForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			data["mensaje"]="Guardado correctamente."
		else:
			data["form"]=formulario
			data["mensaje"]="Este año lectivo ya existe."

	data['form'].fields['codigo_ano'].label = 'Código del año lectivo'
	data['form'].fields['fecha_inicio'].label = 'Fecha de inicio'
	data['form'].fields['fecha_finalizacion'].label = 'Fecha de finalización'
	data['form'].fields['colegio'].label = 'Colegio al que pertenece'

	return render(request, 'agregaranolectivo.html', data)

def buscar_ano(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	busqueda=request.GET.get("buscar")
	ano=anoLectivo.objects.all()
	if busqueda:
		ano = anoLectivo.objects.filter(
			Q(codigo_ano__icontains = busqueda) | #or (o)
			Q(fecha_inicio__icontains = busqueda) | #__icontains para que no sea exacto
			Q(fecha_finalizacion__icontains = busqueda) |
			Q(colegio__nombre_colegio__icontains = busqueda) 
			).distinct()

	return render(request, "listaanoslectivos.html", {"ano":ano})

def listado_anos(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	listadoanos=anoLectivo.objects.all()
	return render(request, "listaanoslectivos.html",{"ano":listadoanos})

def eliminar_ano(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	ano = get_object_or_404(anoLectivo, codigo_ano=codigo)
	ano.delete()
	messages.success(request, "Eliminado correctamente.")
	return redirect("listadoanos")

def modificar_ano(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	ano=get_object_or_404(anoLectivo, codigo_ano=codigo)#busca un elemento

	data={
		'form':anoLectivoForm(instance=ano)
	}

	if request.method=='POST':
		formulario=anoLectivoForm(data=request.POST, instance=ano, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Modificado correctamente")
			#data["mensaje"]="Archivo Modificado"
		#else:
			#data["form"]=formulario
			#data["mensaje"]="El archivo no existe"
			return redirect(to='listadoanos')
		data["form"]=formulario

	data['form'].fields['codigo_ano'].label = 'Código del año lectivo'
	data['form'].fields['fecha_inicio'].label = 'Fecha de inicio'
	data['form'].fields['fecha_finalizacion'].label = 'Fecha de finalización'
	data['form'].fields['colegio'].label = 'Colegio al que pertenece'

	return render(request, 'modificar_ano.html', data)

#Grado

def agregar_grado(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	data={
		'form': GradosForm(),
		'titulo': "Agregar nuevo grado"
	}

	if request.method =='POST':
		formulario = GradosForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			data["mensaje"]="Guardado correctamente."
		else:
			data["form"]=formulario
			data["mensaje"]="El grado ya existe."

	data['form'].fields['codigo_grado'].label = 'Código del grado'
	data['form'].fields['nivel_educativo'].label = 'Nivel Académico'
	data['form'].fields['anolectivo'].label = 'Año lectivo al que pertenece'

	return render(request, 'agregargrado.html', data)

def buscar_grado(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	busqueda=request.GET.get("buscar")
	grado=Grados.objects.all()
	if busqueda:
		grado = Grados.objects.filter(
			Q(codigo_grado__icontains = busqueda) | #or (o)
			Q(nivel_educativo__icontains = busqueda) #__icontains para que no sea exacto
			).distinct()

	return render(request, "listagrados.html", {"grado":grado})

def listado_grados(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	listadogrados=Grados.objects.all()
	return render(request, "listagrados.html",{"grado":listadogrados})

def eliminar_grado(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	grado = get_object_or_404(Grados, codigo_grado=codigo)
	grado.delete()
	messages.success(request, "Eliminado correctamente.")
	return redirect("listadogrados")

def modificar_grado(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	grado=get_object_or_404(Grados, codigo_grado=codigo)#busca un elemento

	data={
		'form':GradosForm(instance=grado)
	}

	if request.method=='POST':
		formulario=GradosForm(data=request.POST, instance=grado, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Modificado correctamente")
			#data["mensaje"]="Archivo Modificado"
		#else:
			#data["form"]=formulario
			#data["mensaje"]="El archivo no existe"
			return redirect(to='listadogrados')
		data["form"]=formulario

	data['form'].fields['codigo_grado'].label = 'Código del grado'
	data['form'].fields['nivel_educativo'].label = 'Nivel Académico'
	data['form'].fields['anolectivo'].label = 'Año lectivo al que pertenece'

	return render(request, 'modificar_grado.html', data)

#Acudiente

def agregar_acudiente(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol_usuario not in roles_permitidos:
		return redirect('error_404')

	data={
		'form': AcudienteForm(),
		'titulo': "Agregar nuevo acudiente"
	}

	if request.method =='POST':
		formulario = AcudienteForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			data["mensaje"]="Guardado correctamente."
		else:
			data["form"]=formulario
			data["mensaje"]="El acudiente ya existe."

	data['form'].fields['dni_acudiente'].label = 'Número de identificación del acudiente'
	data['form'].fields['nombres_acudiente'].label = 'Nombres'
	data['form'].fields['apellidos_acudiente'].label = 'Apellidos'
	data['form'].fields['fecha_nacimiento_acudiente'].label = 'Fecha de nacimiento'
	data['form'].fields['sexo_acudiente'].label = 'Sexo'
	data['form'].fields['telefono_acudiente'].label = 'Teléfono'
	data['form'].fields['email_acudiente'].label = 'Correo electrónico'
	data['form'].fields['direccion'].label = 'Dirección'
	data['form'].fields['parentesco'].label = 'Parentesco con el estudiante'

	return render(request, 'agregaracudiente.html', data)

def buscar_acudiente(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol_usuario not in roles_permitidos:
		return redirect('error_404')

	busqueda=request.GET.get("buscar")
	acudiente=Acudiente.objects.all()
	if busqueda:
		acudiente = Acudiente.objects.filter(
			Q(dni_acudiente__icontains = busqueda) | #or (o)
			Q(nombres_acudiente__icontains = busqueda) | #__icontains para que no sea exacto
			Q(apellidos_acudiente__icontains = busqueda) |
			Q(telefono_acudiente__icontains = busqueda) |
			Q(email_acudiente__icontains = busqueda) |
			Q(direccion__icontains = busqueda)
			).distinct()

	return render(request, "listaacudientes.html", {"acudiente":acudiente})

def listado_acudiente(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol_usuario not in roles_permitidos:
		return redirect('error_404')

	listadoacudientes=Acudiente.objects.all()
	return render(request, "listaacudientes.html",{"acudiente":listadoacudientes})

def eliminar_acudiente(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol_usuario not in roles_permitidos:
		return redirect('error_404')

	acudiente = get_object_or_404(Acudiente, dni_acudiente=codigo)
	acudiente.delete()
	messages.success(request, "Eliminado correctamente.")
	return redirect("listadoacudientes")

def modificar_acudiente(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol_usuario not in roles_permitidos:
		return redirect('error_404')

	acudiente=get_object_or_404(Acudiente, dni_acudiente=codigo)#busca un elemento

	data={
		'form':AcudienteForm(instance=acudiente)
	}

	if request.method=='POST':
		formulario=AcudienteForm(data=request.POST, instance=acudiente, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Modificado correctamente")
			#data["mensaje"]="Archivo Modificado"
		#else:
			#data["form"]=formulario
			#data["mensaje"]="El archivo no existe"
			return redirect(to='listadoacudientes')
		data["form"]=formulario

	data['form'].fields['dni_acudiente'].label = 'Número de identificación del acudiente'
	data['form'].fields['nombres_acudiente'].label = 'Nombres'
	data['form'].fields['apellidos_acudiente'].label = 'Apellidos'
	data['form'].fields['fecha_nacimiento_acudiente'].label = 'Fecha de nacimiento'
	data['form'].fields['sexo_acudiente'].label = 'Sexo'
	data['form'].fields['telefono_acudiente'].label = 'Teléfono'
	data['form'].fields['email_acudiente'].label = 'Correo electrónico'
	data['form'].fields['direccion'].label = 'Dirección'
	data['form'].fields['parentesco'].label = 'Parentesco con el estudiante'
	
	return render(request, 'modificar_acudiente.html', data)

#Estudiante

def agregar_estudiante(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol_usuario not in roles_permitidos:
		return redirect('error_404')

	data={
		'form': EstudianteForm(),
		'titulo': "Agregar nuevo estudiante"
	}

	if request.method =='POST':
		formulario = EstudianteForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			data["mensaje"]="Guardado correctamente."
		else:
			data["form"]=formulario
			data["mensaje"]="El estudiante ya existe."

	data['form'].fields['dni_estudiante'].label = 'Número de identificación del estudiante'
	data['form'].fields['dni_estudiante'].label = 'Número de identificación del estudiante'

	return render(request, 'agregarestudiante.html', data)

def buscar_estudiante(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol_usuario not in roles_permitidos:
		return redirect('error_404')

	busqueda=request.GET.get("buscar")
	estudiante=Estudiante.objects.all()
	if busqueda:
		estudiante = Estudiante.objects.filter(
			Q(dni_estudiante__icontains = busqueda) | #or (o)
			Q(nombres_estudiante__icontains = busqueda) #__icontains para que no sea exacto
			).distinct()

	return render(request, "estudiantes.html", {"estudiante":estudiante})

def listado_estudiantes(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol_usuario not in roles_permitidos:
		return redirect('error_404')

	listadoestudiantes=Estudiante.objects.all()
	return render(request, "estudiantes.html",{"estudiante":listadoestudiantes})

def eliminar_estudiante(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol_usuario not in roles_permitidos:
		return redirect('error_404')

	estudiante = get_object_or_404(Estudiante, dni_estudiante=codigo)
	estudiante.delete()
	messages.success(request, "Eliminado correctamente.")
	return redirect("listadoestudiantes")

def modificar_estudiante(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol_usuario not in roles_permitidos:
		return redirect('error_404')

	estudiante=get_object_or_404(Estudiante, dni_estudiante=codigo)#busca un elemento

	data={
		'form':EstudianteForm(instance=estudiante)
	}

	if request.method=='POST':
		formulario=EstudianteForm(data=request.POST, instance=estudiante, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Modificado correctamente")
			#data["mensaje"]="Archivo Modificado"
		#else:
			#data["form"]=formulario
			#data["mensaje"]="El archivo no existe"
			return redirect(to='listadoestudiantes')
		data["form"]=formulario
	return render(request, 'modificar.html', data)

def estudiante_pdf(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol_usuario not in roles_permitidos:
		return redirect('error_404')

	estudiante=Estudiante.objects.all()
	template_path="pdf_estudiante.html"
	context ={'estudiante':estudiante,
		'comp':{'name':'COSFA', 'rut':'8003488-5', 'address':'Calle 52 #14-44'}
		}
	response=HttpResponse(content_type='application/pdf')
	response['Content-Disposition']='attachment; filename="lista_de_estudiantes.pdf"'
	template=get_template('pdf_estudiante.html')
	html=template.render(context)
	pisa_status=pisa.CreatePDF(
		html, dest=response)
	if pisa_status.err:
		return HttpResponse('Se presentaron algunos problemas <pre>' + html + '</pre>')
	return response

def perfil_estudiante(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol_usuario not in roles_permitidos:
		return redirect('error_404')

	estudiante = get_object_or_404(Estudiante, dni_estudiante=codigo)
	
	context = {
        'estudiante': estudiante,
    }
	return render(request, 'perfil_estudiante.html', context)

def perfil_estudiante2(request):
    if not request.session.has_key('identificacion'):
        return redirect('login')

    codigo = request.session['identificacion']

    # Recuperar la información del usuario
    try:
        estudiante = Estudiante.objects.get(dni_estudiante=codigo)
    except Estudiante.DoesNotExist:
        # Manejar la excepción de usuario no encontrado
        pass

    # Renderizar la plantilla con la información del usuario
    context = {
        'estudiante': estudiante,
    }
    return render(request, 'perfil_estudiante.html', context)

#Tutor

def agregar_tutor(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	data={
		'form': TutorForm(),
		'titulo': "Agregar nuevo tutor"
	}

	if request.method =='POST':
		formulario = TutorForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			data["mensaje"]="Guardado correctamente."
		else:
			data["form"]=formulario
			data["mensaje"]="El tutor ya existe."

	data['form'].fields['dni_tutor'].label = 'Número de identificación del tutor'
	data['form'].fields['nombres_tutor'].label = 'Nombre del tutor'
	data['form'].fields['apellidos_tutor'].label = 'Apellidos del tutor'
	data['form'].fields['fecha_nacimiento_tutor'].label = 'Fecha de nacimiento del tutor'
	data['form'].fields['sexo_tutor'].label = 'Sexo del tutor'
	data['form'].fields['telefono_tutor'].label = 'Teléfono del tutor'
	data['form'].fields['email_tutor'].label = 'Correo electrónico del tutor'

	return render(request, 'agregartutor.html', data)

def buscar_tutor(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	busqueda=request.GET.get("buscar")
	tutor=Tutor.objects.all()
	if busqueda:
		tutor = Tutor.objects.filter(
			Q(dni_tutor__icontains = busqueda) | #or (o)
			Q(nombres_tutor__icontains = busqueda) | #__icontains para que no sea exacto
			Q(apellidos_tutor__icontains = busqueda) |
			Q(telefono_tutor__icontains = busqueda) |
			Q(email_tutor__icontains = busqueda) 
			).distinct()

	return render(request, "tutores.html", {"tutor":tutor})

def listado_tutor(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	listadotutor=Tutor.objects.all()
	return render(request, "tutores.html",{"tutor":listadotutor})

def eliminar_tutor(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	tutor = get_object_or_404(Tutor, dni_tutor=codigo)
	tutor.delete()
	messages.success(request, "Eliminado correctamente.")
	return redirect("listadotutor")

def modificar_tutor(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	tutor=get_object_or_404(Tutor, dni_tutor=codigo)#busca un elemento

	data={
		'form':TutorForm(instance=tutor)
	}

	if request.method=='POST':
		formulario=TutorForm(data=request.POST, instance=tutor, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Modificado correctamente")
			#data["mensaje"]="Archivo Modificado"
		#else:
			#data["form"]=formulario
			#data["mensaje"]="El archivo no existe"
			return redirect(to='listadotutor')
		data["form"]=formulario

	data['form'].fields['dni_tutor'].label = 'Número de identificación del tutor'
	data['form'].fields['nombres_tutor'].label = 'Nombre del tutor'
	data['form'].fields['apellidos_tutor'].label = 'Apellidos del tutor'
	data['form'].fields['fecha_nacimiento_tutor'].label = 'Fecha de nacimiento del tutor'
	data['form'].fields['sexo_tutor'].label = 'Sexo del tutor'
	data['form'].fields['telefono_tutor'].label = 'Teléfono del tutor'
	data['form'].fields['email_tutor'].label = 'Correo electrónico del tutor'

	return render(request, 'modificar_tutor.html', data)

def perfil_tutor(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	tutor = get_object_or_404(Tutor, dni_tutor=codigo)

	context = {
        'tutor': tutor,
    }
	return render(request, 'perfil_tutor.html', context)

def perfil_tutor2(request):
    if not request.session.has_key('identificacion'):
        return redirect('login')

    codigo = request.session['identificacion']

    try:
        tutor = Tutor.objects.get(dni_tutor=codigo)
    except Tutor.DoesNotExist:
        pass

    context = {
        'tutor': tutor,
    }
    return render(request, 'perfil_tutor.html', context)

#Curso

def buscar_curso(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Administrador'

	if rol_usuario != rol_permitido:
		return redirect('error_404')

	busqueda=request.GET.get("buscar")
	curso=Curso.objects.all()
	if busqueda:
		curso = Curso.objects.filter(
			Q(codigo_curso__icontains = busqueda) | #or (o)
			Q(nombre_curso__icontains = busqueda) #__icontains para que no sea exacto 
			).distinct()

	return render(request, "cursos.html", {"curso":curso})

def buscar_curso_tutor(request):
    if not request.session.has_key('identificacion'):
        return redirect('login')

    rol_usuario = request.session['rol']
    rol_permitido = 'Tutor'

    if rol_usuario != rol_permitido:
        return redirect('error_404')

    tutor_id = request.session.get('identificacion')
    cursos = [] 

    try:
        tutor = Tutor.objects.get(dni_tutor=tutor_id)

        cursos = Curso.objects.filter(tutor=tutor).filter(
            Q(codigo_curso__icontains=request.GET.get("buscar")) |
            Q(nombre_curso__icontains=request.GET.get("buscar"))
        ).distinct()
    except Tutor.DoesNotExist:
        pass

    context = {'cursos': cursos}
    return render(request, "cursos_tutor.html", context)

def buscar_curso_estudiante(request):
    if not request.session.has_key('identificacion'):
        return redirect('login')

    rol_usuario = request.session['rol']
    rol_permitido = 'Estudiante'

    if rol_usuario != rol_permitido:
        return redirect('error_404')

    estudiante_id = request.session.get('identificacion')

    matriculas = Matricula.objects.filter(estudiante__dni_estudiante=estudiante_id)
    cursos_matriculados = [matricula.curso for matricula in matriculas]

    busqueda = request.GET.get("buscar")
    cursos = Curso.objects.all()
    if busqueda:
        cursos = cursos.filter(
            Q(codigo_curso__icontains=busqueda) |
            Q(nombre_curso__icontains=busqueda)
        ).distinct()

    cursos_filtrados = []
    for curso in cursos:
        if curso in cursos_matriculados:
            cursos_filtrados.append(curso)

    context = {
        "curso": cursos_filtrados
    }
    return render(request, "cursos.html", context)

def agregar_curso(request, r):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol_usuario not in roles_permitidos:
		return redirect('error_404')

	data={
		'form': CursoForm(),
		'titulo': "Agregar nuevo curso"
	}

	if request.method =='POST':
		formulario = CursoForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			data["mensaje"]="Guardado correctamen, tutor)te."

			if r=='Tutor':
				return redirect('listadocurso_tutores')
			if r=='Administrador':
				return redirect('listadocurso')
			
		else:
			data["form"]=formulario
			data["mensaje"]="El curso ya existe."

	data['form'].fields['codigo_curso'].label = 'Código del curso'
	data['form'].fields['nombre_curso'].label = 'Nombre del curso'
	data['form'].fields['descripcion_curso'].label = 'Descripción del curso'
	data['form'].fields['imagen_curso'].label = 'Imagen del curso'
	data['form'].fields['grado'].label = 'Grado al que pertenecerá el curso'
	data['form'].fields['tutor'].label = 'Tutor del curso'

	return render(request, 'agregarcurso.html', data)

def listado_curso(request):
    if not request.session.has_key('identificacion'):
        return redirect('login')

    rol_usuario = request.session['rol']
    rol_permitido = 'Administrador'

    if rol_usuario != rol_permitido:
        return redirect('error_404')
    
    listadocurso=Curso.objects.all()
    return render(request, "cursos.html",{"curso":listadocurso})

def listado_curso_estudiantes(request):
    if not request.session.has_key('identificacion'):
        return redirect('login')

    rol_usuario = request.session['rol']
    rol_permitido = 'Estudiante'

    if rol_usuario != rol_permitido:
        return redirect('error_404')
    
    estudiante_id = request.session.get('identificacion')

    matriculas = Matricula.objects.filter(estudiante__dni_estudiante=estudiante_id)
    cursos_matriculados = [matricula.curso for matricula in matriculas]

    context = {
        "curso": cursos_matriculados
    }
    return render(request, "cursos.html", context)

def listado_curso_tutores(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol_usuario = request.session['rol']
	rol_permitido = 'Tutor'

	if rol_usuario != rol_permitido:
		return redirect('error_404')
    
	tutor_id = request.session.get('identificacion')

	try:
		tutor = Tutor.objects.get(dni_tutor=tutor_id)
		cursos = Curso.objects.filter(tutor=tutor)
	except Tutor.DoesNotExist:
		pass

	context = {
		'cursos': cursos,
		'tutor': tutor_id,
	}
	return render(request, 'cursos_tutor.html', context)

def eliminar_curso(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol not in roles_permitidos:
		return redirect('error_404')

	curso = get_object_or_404(Curso, codigo_curso=codigo)
	curso.delete()
	messages.success(request, "Eliminado correctamente.")
 
	if rol == 'Administrador':
		return redirect('listadocurso')
	elif rol == 'Tutor':
		return redirect('listadocurso_tutores')

def modificar_curso(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol not in roles_permitidos:
		return redirect('error_404')

	curso=get_object_or_404(Curso, codigo_curso=codigo)#busca un elemento

	data={
		'form':CursoForm(instance=curso)
	}

	if request.method=='POST':
		formulario=CursoForm(data=request.POST, instance=curso, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Modificado correctamente")

		rol = request.session.get('rol')
			
		if rol == 'Administrador':
			return redirect('listadocurso')
		elif rol == 'Tutor':
			return redirect('listadocurso_tutores')

		data["form"]=formulario

	data['form'].fields['codigo_curso'].label = 'Código del curso'
	data['form'].fields['nombre_curso'].label = 'Nombre del curso'
	data['form'].fields['descripcion_curso'].label = 'Descripción del curso'
	data['form'].fields['imagen_curso'].label = 'Imagen del curso'
	data['form'].fields['grado'].label = 'Grado al que pertenecerá el curso'
	data['form'].fields['tutor'].label = 'Tutor del curso'

	return render(request, 'modificar_curso.html', data)

#Matricula

def agregar_matricula(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol not in roles_permitidos:
		return redirect('error_404')

	data={
		'form': MatriculaForm(),
		'titulo': "Matricular un estudiante"
	}

	if request.method =='POST':
		formulario = MatriculaForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			data["mensaje"]="Guardado correctamente."
		else:
			data["form"]=formulario
			data["mensaje"]="El estudiante ya está matriculado."

	data['form'].fields['estudiante'].label = 'Estudiante a matricular'
	data['form'].fields['curso'].label = 'Curso'

	return render(request, 'agregarmatricula.html', data)

def buscar_matricula(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol not in roles_permitidos:
		return redirect('error_404')

	busqueda=request.GET.get("buscar")
	matricula=Matricula.objects.all()
	if busqueda:
		matricula = Matricula.objects.filter(
			Q(id_matricula__icontains = busqueda) | #or (o)
			Q(fechaMatricula__icontains = busqueda) #__icontains para que no sea exacto 
			).distinct()

	return render(request, "listamatricula.html", {"matricula":matricula})

def listado_matricula(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol not in roles_permitidos:
		return redirect('error_404')

	listadomatricula=Matricula.objects.all()
	return render(request, "listamatricula.html",{"matricula":listadomatricula})

def eliminar_matricula(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol not in roles_permitidos:
		return redirect('error_404')

	matricula = get_object_or_404(Matricula, id_matricula=codigo)
	matricula.delete()
	messages.success(request, "Eliminado correctamente.")
	return redirect("listadomatricula")

def modificar_matricula(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol not in roles_permitidos:
		return redirect('error_404')

	matricula=get_object_or_404(Matricula, id_matricula=codigo)#busca un elemento

	data={
		'form':MatriculaForm(instance=matricula)
	}

	if request.method=='POST':
		formulario=MatriculaForm(data=request.POST, instance=matricula, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Modificado correctamente")
			#data["mensaje"]="Archivo Modificado"
		#else:
			#data["form"]=formulario
			#data["mensaje"]="El archivo no existe"
			return redirect(to='listadomatricula')
		data["form"]=formulario

	data['form'].fields['estudiante'].label = 'Estudiante a matricular'
	data['form'].fields['curso'].label = 'Curso'

	return render(request, 'modificar_matricula.html', data)

#Desempeno

def agregar_desempeno(request, curso):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol not in roles_permitidos:
		return redirect('error_404')

	data={
		'form': DesempenoForm(),
		'titulo': "Agregar un desempeño"
	}

	if request.method =='POST':
		formulario = DesempenoForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			data["mensaje"]="Guardado correctamente."
			return redirect('listadodesempeno', codigo=curso)
		else:
			data["form"]=formulario
			data["mensaje"]="El desempeño ya existe."

	data['form'].fields['nombre_desempeno'].label = 'Nombre del desempeño'
	data['form'].fields['descripcion_desempeno'].label = 'Descripción del desempeño'
	data['form'].fields['imagen_desempeno'].label = 'Imagen del desempeño'
	data['form'].fields['curso'].label = 'Curso al que pertenecerá'

	return render(request, 'agregardesempeno.html', data)

def buscar_desempeno(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	busqueda=request.GET.get("buscar")
	codigo_curso = request.GET.get("desempeno")
	
	if busqueda:
		desempeno = Desempeno.objects.filter(
			Q(codigo_desempeno__icontains = busqueda) | #or (o)
			Q(nombre_desempeno__icontains = busqueda) | #__icontains para que no sea exacto
			Q(descripcion_desempeno__icontains = busqueda)
			).distinct()

	#return HttpResponse(f"hola"+codigo_curso)
	return render(request, "desempenos.html", {"desempeno":desempeno})

def buscar_desempeno2(request):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	codigo_curso = request.GET.get("curso")  # Get curso ID from request parameter
	busqueda = request.GET.get("buscar")  # Get search term (optional)

	desempeno = desempeno.filter(curso=codigo_curso)

	if codigo_curso:
		desempeno = desempeno.filter(curso=codigo_curso)  # Filter by curso ID
	if busqueda:
		desempeno = desempeno.filter(
			Q(codigo_desempeno__icontains=busqueda) |
			Q(nombre_desempeno__icontains=busqueda) |
			Q(descripcion_desempeno__icontains=busqueda)
		).distinct()
	else:
		busqueda = None
	
	#return HttpResponse(f'hola')
	return render(request, "desempenos.html", {"desempeno": desempeno})

def listado_desempeno(request, codigo):
    if not request.session.has_key('identificacion'):
        return redirect('login')

    if codigo:
        listadodesempeno = Desempeno.objects.filter(curso=codigo)

    context = {
		'desempeno': listadodesempeno,
		'curso': codigo,
		}
    return render(request, "desempenos.html", context)

def eliminar_desempeno(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol not in roles_permitidos:
		return redirect('error_404')

	desempeno = get_object_or_404(Desempeno, codigo_desempeno=codigo)
	desempeno.delete()
	messages.success(request, "Eliminado correctamente.")
	return redirect("listadodesempeno", codigo=desempeno.curso.codigo_curso)

def modificar_desempeno(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol not in roles_permitidos:
		return redirect('error_404')

	desempeno=get_object_or_404(Desempeno, codigo_desempeno=codigo)#busca un elemento

	data={
		'form':DesempenoForm(instance=desempeno)
	}

	if request.method=='POST':
		formulario=DesempenoForm(data=request.POST, instance=desempeno, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Modificado correctamente")
			#data["mensaje"]="Archivo Modificado"
		#else:
			#data["form"]=formulario
			#data["mensaje"]="El archivo no existe"
			return redirect(to='listadodesempeno', codigo=desempeno.curso.codigo_curso)
		data["form"]=formulario

	data['form'].fields['nombre_desempeno'].label = 'Nombre del desempeño'
	data['form'].fields['descripcion_desempeno'].label = 'Descripción del desempeño'
	data['form'].fields['imagen_desempeno'].label = 'Imagen del desempeño'
	data['form'].fields['curso'].label = 'Curso al que pertenecerá'

	return render(request, 'modificar_desempeno.html', data)

def ampliar_desempeno(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	desempeno = get_object_or_404(Desempeno, codigo_desempeno=codigo) 
	materials = Material.objects.filter(desempeno=codigo)

	context = {
		'desempeno': desempeno,
		'materials': materials,
	}
	return render(request, 'infodesempeno.html', context)

#Material

def agregar_material(request, desempeno):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol not in roles_permitidos:
		return redirect('error_404')

	data={
		'form': MaterialForm(),
		'titulo': "Agregar material de estudio"
	}

	if request.method =='POST':
		formulario = MaterialForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			data["mensaje"]="Guardado correctamente."
			return redirect('ampliar_desempeno', codigo=desempeno)
		else:
			data["form"]=formulario
			data["mensaje"]="El material ya existe."

	data['form'].fields['nombre_material'].label = 'Nombre del material'
	data['form'].fields['descripcion_material'].label = 'Descripción del material'
	data['form'].fields['url_material'].label = 'URL del material'
	data['form'].fields['desempeno'].label = 'Desempeño al que pertenecerá'

	return render(request, 'agregarmaterial.html', data)

def eliminar_material2(request, desempeno, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol not in roles_permitidos:
		return redirect('error_404')

	material = get_object_or_404(Material, codigo_material=codigo)
	material.delete()
	messages.success(request, "Eliminado correctamente.")
	return redirect('ampliar_desempeno', codigo=desempeno)

def mod_material(request, codigo, r):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	rol = request.session['rol']
	roles_permitidos = ['Administrador', 'Tutor']

	if rol not in roles_permitidos:
		return redirect('error_404')

	material=get_object_or_404(Material, codigo_material=codigo)#busca un elemento

	data={
		'form':MaterialForm(instance=material)
	}

	if request.method=='POST':
		formulario=MaterialForm(data=request.POST, instance=material, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Modificado correctamente")
			#data["mensaje"]="Archivo Modificado"
		#else:
			#data["form"]=formulario
			#data["mensaje"]="El archivo no existe"
			if r=='2':
				material = Material.objects.get(codigo_material=codigo)
				material = material.desempeno_id
				return redirect('ampliar_desempeno', codigo=material)
			else:
				return redirect(to='listadomaterial')
			#request.META.get('HTTP_REFERER', '/')			
		data["form"]=formulario


	data['form'].fields['nombre_material'].label = 'Nombre del material'
	data['form'].fields['descripcion_material'].label = 'Descripción del material'
	data['form'].fields['url_material'].label = 'URL del material'
	data['form'].fields['desempeno'].label = 'Desempeño al que pertenecerá'

	return render(request, 'modificar_material1.html', data)

def ampliar_material(request, codigo):
	if not request.session.has_key('identificacion'):
		return redirect('login')

	material = get_object_or_404(Material, codigo_material=codigo)

	ctx = {
		'material': material
	}

	return render(request, 'infomaterial.html', ctx)

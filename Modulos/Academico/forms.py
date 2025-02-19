from django import forms
from .models import Colegio, anoLectivo, Grados, Acudiente, Estudiante, Tutor, Curso, Matricula, Desempeno, Material

class ColegioForm(forms.ModelForm):

	class Meta:
		model = Colegio
		fields = "__all__"
  
class anoLectivoForm(forms.ModelForm):

	class Meta:
		model = anoLectivo
		fields = "__all__"

class GradosForm(forms.ModelForm):

	class Meta:
		model = Grados
		fields = "__all__"

class AcudienteForm(forms.ModelForm):

	class Meta:
		model = Acudiente
		fields = "__all__"

class EstudianteForm(forms.ModelForm):

	class Meta:
		model = Estudiante
		fields = '__all__'

class TutorForm(forms.ModelForm):

	class Meta:
		model = Tutor
		fields = "__all__"

class CursoForm(forms.ModelForm):

	class Meta:
		model = Curso
		fields = "__all__"

class MatriculaForm(forms.ModelForm):

	class Meta:
		model = Matricula
		fields = "__all__"

class DesempenoForm(forms.ModelForm):

	class Meta:
		model = Desempeno
		fields = "__all__"

class MaterialForm(forms.ModelForm):

	class Meta:
		model = Material
		fields = "__all__"


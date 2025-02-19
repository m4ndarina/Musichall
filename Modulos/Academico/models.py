from django.db import models

# Create your models here.

class Colegio(models.Model):
    codigo_colegio=models.CharField(max_length=3, primary_key=True)
    nombre_colegio = models.CharField(max_length=60)
    razonsocial_colegio = models.CharField(max_length=35)
    direccion_colegio = models.CharField(max_length=35)
    telefono_colegio = models.CharField(max_length=35)
    email_colegio = models.CharField(max_length=100)
    seleccion1 = [ 
        ('A', 'Publico'),
        ('B', 'Privado'),
    ]
    tipo_colegio = models.CharField(max_length=1, choices=seleccion1, default='A')
    seleccion2 = [ 
        ('A', 'Calendario A'),
        ('B', 'Calendario B'),
    ]
    calendario_colegio = models.CharField(max_length=1, choices=seleccion2, default='A')
    
    def __str__(self):
        txt = "{0} / {1}".format(self.codigo_colegio, self.nombre_colegio)
        return txt

class anoLectivo(models.Model):
    codigo_ano=models.CharField(max_length=3, primary_key=True)
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()
    colegio = models.ForeignKey(Colegio, null=True, blank=False, on_delete=models.CASCADE)
    
    def __str__(self):
        txt = "{0} / {1} / {2}".format(self.fecha_inicio, self.fecha_finalizacion, self.colegio.nombre_colegio)
        return txt

class Grados(models.Model):
    codigo_grado=models.CharField(max_length=3, primary_key=True)
    niveles = [ 
        ('A', 'Preescolar'),
        ('B', 'Primaria'),
        ('C', 'Secundaria'),
        ('D', 'Bachillerato')
    ]
    nivel_educativo = models.CharField(max_length=1, choices=niveles, default='A')
    anolectivo = models.ForeignKey(anoLectivo, null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        txt = "Grado: {0} / Nivel: {1}".format(self.codigo_grado, self.nivel_educativo)
        return txt

class Acudiente(models.Model):
    dni_acudiente = models.CharField(max_length=15, primary_key=True)
    nombres_acudiente = models.CharField(max_length=35)
    apellidos_acudiente = models.CharField(max_length=35)
    fecha_nacimiento_acudiente = models.DateField()
    sexos = [ 
        ('F', 'Femenino'),
        ('M', 'Masculino'),
        ('O', 'Otros')
    ]
    sexo_acudiente = models.CharField(max_length=1, choices=sexos, default='F')
    telefono_acudiente = models.IntegerField(null=True)
    email_acudiente = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    parentesco = models.CharField(max_length=100)

    def nombreCompleto(self):
        txt = "{0} {1}".format(self.nombres_acudiente, self.apellidos_acudiente)
        return txt

    def __str__(self):
        txt = "{0}"
        return txt.format(self.nombreCompleto())

class Estudiante(models.Model):
    dni_estudiante = models.CharField(max_length=15, primary_key=True)
    nombres_estudiante = models.CharField(max_length=35)
    apellidos_estudiante = models.CharField(max_length=35)
    fecha_nacimiento_estudiante = models.DateField()
    sexos = [ 
        ('F', 'Femenino'),
        ('M', 'Masculino'),
        ('O', 'Otros')
    ]
    sexo_estudiante = models.CharField(max_length=1, choices=sexos, default='F')
    telefono_estudiante = models.IntegerField(null=True)
    email_estudiante = models.CharField(max_length=100)
    grado = models.ForeignKey(Grados, null=True, blank=False, on_delete=models.CASCADE)
    nombres_madre = models.CharField(max_length=35, null=True)
    apellidos_madre = models.CharField(max_length=35, null=True)
    fecha_nacimiento_madre = models.DateField(null=True)
    sexo_madre = models.CharField(max_length=1, choices=sexos, default='F')
    telefono_madre = models.IntegerField(null=True)
    email_madre = models.CharField(max_length=100, null=True)
    direccion_madre = models.CharField(max_length=100, null=True)
    ocupacion_madre = models.CharField(max_length=100, null=True)
    nombres_padre = models.CharField(max_length=35, null=True)
    apellidos_padre = models.CharField(max_length=35, null=True)
    fecha_nacimiento_padre = models.DateField(null=True)
    sexo_padre= models.CharField(max_length=1, choices=sexos, default='F')
    telefono_padre = models.IntegerField(null=True)
    email_padre = models.CharField(max_length=100, null=True)
    direccion_padre = models.CharField(max_length=100, null=True)
    ocupacion_padre = models.CharField(max_length=100, null=True)
    acudiente = models.ForeignKey(Acudiente, null=True, blank=False, on_delete=models.CASCADE)
    nombre_usu = models.CharField(max_length=20, null=True)
    contrasena = models.CharField(max_length=25, null=True)
    imagen = models.FileField(upload_to='imagen_estudiante/', verbose_name='Foto de perfil del estudiante', null=True)
    rol = models.CharField(max_length=25, default="Estudiante", editable=False, null=True)

    def nombreCompleto(self):
        txt = "{0} {1}".format(self.nombres_estudiante, self.apellidos_estudiante)
        return txt

    def __str__(self):
        txt = "{0}"
        return txt.format(self.nombreCompleto())

class Tutor(models.Model):
    dni_tutor = models.CharField(max_length=15, primary_key=True)
    nombres_tutor = models.CharField(max_length=35)
    apellidos_tutor = models.CharField(max_length=35)
    fecha_nacimiento_tutor = models.DateField()
    sexos = [ 
        ('F', 'Femenino'),
        ('M', 'Masculino'),
        ('O', 'Otros')
    ]
    sexo_tutor = models.CharField(max_length=1, choices=sexos, default='F')
    telefono_tutor = models.IntegerField(null=True)
    email_tutor = models.CharField(max_length=100)
    nombre_usu = models.CharField(max_length=20, null=True)
    contrasena = models.CharField(max_length=25, null=True)
    imagen = models.FileField(upload_to='imagen_tutor/', verbose_name='Foto de perfil del tutor', null=True)
    rol = models.CharField(max_length=25, default="Tutor", editable=False, null=True)

    def nombreCompleto(self):
        txt = "{0} {1}".format(self.nombres_tutor, self.apellidos_tutor)
        return txt

    def __str__(self):
        txt = "{0}"
        return txt.format(self.nombreCompleto())

class Curso(models.Model):
    codigo_curso = models.CharField(max_length=4, primary_key=True)
    nombre_curso = models.CharField(max_length=35)
    descripcion_curso = models.TextField()
    imagen_curso = models.FileField(upload_to='curso_imagen/', verbose_name='Imagen del curso', null=True)
    grado = models.ForeignKey(Grados, null=True, blank=True, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        txt = "{0} ({1}) / Docente: {2}".format(self.codigo_curso, self.nombre_curso, self.tutor)
        return txt

class Matricula(models.Model):
    id_matricula = models.AutoField(primary_key=True)
    estudiante = models.ForeignKey(Estudiante, null=False, blank=False, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, null=False, blank=False, on_delete=models.CASCADE)
    fechaMatricula = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.estudiante.sexo_estudiante == "F":
            letraSexo = "a"
        elif self.estudiante.sexo_estudiante == "M":
            letraSexo="o"
        else:
            letraSexo="@"
        fecMat=self.fechaMatricula.strftime("%A %d %m %Y %H %M %S")
        txt = "{0} matriculad{1} en el curso {2} / Fecha: {3}".format(self.estudiante.nombreCompleto(), letraSexo, self.curso, fecMat)
        return txt

class Desempeno(models.Model):
    codigo_desempeno = models.AutoField(primary_key=True)
    nombre_desempeno = models.CharField(max_length=35)
    descripcion_desempeno = models.TextField()
    imagen_desempeno = models.FileField(upload_to='desempeno_imagen/', verbose_name='Imagen del curso', null=True)
    fecha_creacion = models.DateField(null=True)
    curso = models.ForeignKey(Curso, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        txt = "Desempeño: '{0}' / Curso: {1}.".format(self.nombre_desempeno, self.curso.nombre_curso)
        return txt

class Material(models.Model):
    codigo_material = models.AutoField(primary_key=True)
    nombre_material = models.CharField(max_length=35)
    descripcion_material = models.TextField()
    url_material = models.CharField(max_length=150)
    imagen_material = models.FileField(upload_to='material_imagen/', verbose_name='Imagen del material', null=True)
    fecha_creacion = models.DateField(null=True)
    desempeno = models.ForeignKey(Desempeno, null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        txt = "Material: '{0}' / Desempeño: {1}.".format(self.nombre_material, self.desempeno.nombre_desempeno)
        return txt

class Publicacion(models.Model):
    id_publicacion = models.AutoField(primary_key=True)
    titulo_publicacion = models.CharField(max_length=100)
    contenido_publicacion = models.TextField() 
    fecha_publicacion = models.DateField()
    autor = models.ForeignKey(Estudiante, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        txt = "Publicación: {0} / Autor: {1}".format(self.titulo_publicacion, self.autor.nombreCompleto())
        return txt

class Comentario(models.Model):
    id_comentario = models.AutoField(primary_key=True)
    fecha_comentario = models.DateField()
    contenido_comentario = models.TextField()
    autor = models.ForeignKey(Estudiante, null=False, blank=False, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        txt = "{0} comentó en la publicación {1}".format(self.autor.nombreCompleto(), self.publicacion.titulo_publicacion)
        return txt

class Admin(models.Model):
    dni_admin = models.CharField(max_length=15, primary_key=True)
    nombres_admin = models.CharField(max_length=35)
    apellidos_admin = models.CharField(max_length=35)
    nombre_usu = models.CharField(max_length=20)
    contrasena = models.CharField(max_length=25)
    rol = models.CharField(max_length=25, default="Administrador", editable=False)

    def nombreCompleto(self):
        txt = "{0} {1}".format(self.nombres_admin, self.apellidos_admin)
        return txt

    def str(self):
        txt = "{0}"
        return txt.format(self.nombreCompleto())
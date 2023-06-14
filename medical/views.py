from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .forms import LoginForm
from .models import Paciente, Antecedentes, Medico, PadecimientoActual, ExploracionFisica, Consulta
from datetime import datetime, date
from django.contrib import messages


# Create your views here.

def login_view(request):
    error_message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        error_message = 'Completa todos los campos'

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
                
            else:
                error_message = 'Usuario y/o contraseña incorrectos'
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form, 'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    pacientes = Paciente.objects.all()
    
    for paciente in pacientes:
        try:
            paciente.antecedentes = Antecedentes.objects.get(paciente=paciente)
        except Antecedentes.DoesNotExist:
            paciente.antecedentes = None
    
    return render(request, 'home.html', {'pacientes': pacientes})

@login_required
def createExp_view(request):
    return render(request, 'expedientes/create.html' )

def validar_campos_requeridos(request, campos_requeridos):
    for campo in campos_requeridos:
        if campo not in request.POST or not request.POST[campo]:
            msg = f"Falta el campo requerido: {campo}"
            return msg
    return None

def validar_datos(datos):
    try:
        datos.full_clean()
    except ValidationError as e:
        error_messages = [f"{field}: {str(error).strip('[]')}" for field, error_list in e.error_dict.items() for error in error_list]
        error_message = '\n'.join(error_messages)
        return error_message
    return None

@login_required
def guarda_ficha_identificacion_view(request):
    if request.method == 'POST':
        campos_requeridos = ['nombre', 'apellido_pat', 'apellido_mat', 'fecha_nacimiento', 'genero', 'grupo_rh', 'alergias']

        nombre = request.POST.get('nombre').upper()
        apellido_pat = request.POST.get('apellido_pat').upper()
        apellido_mat = request.POST.get('apellido_mat').upper()
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        genero = request.POST.get('genero')
        estado_civil = request.POST.get('estado_civil').upper()
        grupo_rh = request.POST.get('grupo_rh').upper()
        alergias = request.POST.get('alergias').upper()
        curp = request.POST.get('curp').upper()
        nacionalidad = request.POST.get('nacionalidad').upper()
        escolaridad = request.POST.get('escolaridad').upper()
        religion = request.POST.get('religion').upper()
        direccion = request.POST.get('direccion').upper()
        ocupacion = request.POST.get('ocupacion').upper()
        empleador = request.POST.get('empleador').upper()
        telefono_personal = ''.join(filter(str.isdigit, request.POST.get('telefono_personal')))
        nombre_contacto_emergencia = request.POST.get('nombre_contacto_emergencia').upper()
        telefono_contacto_emergencia = ''.join(filter(str.isdigit, request.POST.get('telefono_contacto_emergencia')))
        notas = request.POST.get('notas').upper()

        ficha = Paciente(
            nombre=nombre,
            apellido_pat=apellido_pat,
            apellido_mat=apellido_mat,
            fecha_nacimiento=fecha_nacimiento,
            genero=genero,
            estado_civil=estado_civil,
            grupo_rh=grupo_rh,
            alergias=alergias,
            curp=curp,
            nacionalidad=nacionalidad,
            escolaridad=escolaridad,
            religion=religion,
            direccion=direccion,
            ocupacion=ocupacion,
            empleador=empleador,
            telefono_personal=telefono_personal,
            nombre_contacto_emergencia=nombre_contacto_emergencia,
            telefono_contacto_emergencia=telefono_contacto_emergencia,
            notas=notas,
            fecha_alta=date.today(),
        )

        error_msg = validar_campos_requeridos(request, campos_requeridos)
        if error_msg:
            return render(request, 'expedientes/create.html', {'error_msg_ficha': error_msg})

        error_msg = validar_datos(ficha)
        if error_msg:
            return render(request, 'expedientes/create.html', {'error_msg_ficha': error_msg})

        ficha.save()
        # Obtener el ID del paciente
        paciente = ficha
        #messages.success(request, 'Datos guardados con éxito')
        return render(request, 'expedientes/create.html', {'paciente': paciente, 'success_msg_ficha': 'Paciente guardado con éxito'})
    
    return render(request, 'expedientes/create.html')

@login_required
def guarda_antecedentes_view(request):
    if request.method == 'POST':
        campos_requeridos = ['paciente_id','ahf', 'apnp', 'app']

        paciente_id = request.POST.get('paciente_id')
        ahf = request.POST.get('ahf').upper()
        apnp = request.POST.get('apnp').upper()
        app = request.POST.get('app').upper()
        ago = request.POST.get('ago').upper()

        antecedentes = Antecedentes(
            paciente_id=paciente_id,
            medico=request.user.medico,
            fecha=date.today(),
            ahf=ahf,
            apnp=apnp,
            app=app,
            ago=ago
        )

        if not paciente_id:
            error_msg = "No se ha inicializado ningun paciente"
            return render(request, 'expedientes/create.html', {'error_msg_antecedentes': error_msg})

        paciente = get_object_or_404(Paciente, id=paciente_id)

        error_msg = validar_campos_requeridos(request, campos_requeridos)
        if error_msg:
            return render(request, 'expedientes/create.html', {'paciente': paciente,'error_msg_antecedentes': error_msg})

        error_msg = validar_datos(antecedentes)
        if error_msg:
            return render(request, 'expedientes/create.html', {'paciente': paciente,'error_msg_antecedentes': error_msg})

        antecedentes.save()
        #messages.success(request, 'Datos guardados con éxito')
        return render(request, 'expedientes/create.html', {'paciente': paciente, 'success_msg_antecedentes': 'Antecedentes guardados con éxito'})
        #return render(request, 'expedientes/create.html', {'success_msg_antecedentes': 'Antecedentes guardados con éxito'})

    return render(request, 'expedientes/create.html')

@login_required
def guarda_padecimiento_view(request):
    if request.method == 'POST':
        campos_requeridos = ['paciente_id','padecimiento_actual','piel_tegumentos','cabeza_cuello','torax','abdomen','genitourinario','musculo_extremidades','neurologico',]

        paciente_id = request.POST.get('paciente_id')
        padecimiento_actual = request.POST.get('padecimiento_actual').upper()
        piel_tegumentos = request.POST.get('piel_tegumentos').upper()
        cabeza_cuello = request.POST.get('cabeza_cuello').upper()
        torax = request.POST.get('torax').upper()
        abdomen = request.POST.get('abdomen').upper()
        genitourinario = request.POST.get('genitourinario').upper()
        musculo_extremidades = request.POST.get('musculo_extremidades').upper()
        neurologico = request.POST.get('neurologico').upper()
        notas = request.POST.get('notas').upper()

        padecimiento = PadecimientoActual(
            paciente_id=paciente_id,
            medico=request.user.medico,
            fecha=datetime.now(),
            padecimiento_actual=padecimiento_actual,
            piel_tegumentos=piel_tegumentos,
            cabeza_cuello=cabeza_cuello,
            torax=torax,
            abdomen=abdomen,
            genitourinario=genitourinario,
            musculo_extremidades=musculo_extremidades,
            neurologico=neurologico,
            notas=notas
        )
        if not paciente_id:
            error_msg = "No se ha inicializado ningun paciente"
            return render(request, 'expedientes/create.html', {'error_msg_padecimiento': error_msg})
        paciente = get_object_or_404(Paciente, id=paciente_id)

        error_msg = validar_campos_requeridos(request, campos_requeridos)
        if error_msg:
            return render(request, 'expedientes/create.html', {'paciente': paciente,'error_msg_padecimiento': error_msg})

        error_msg = validar_datos(padecimiento)
        if error_msg:
            return render(request, 'expedientes/create.html', {'paciente': paciente,'error_msg_padecimiento': error_msg})

        # Guardar el objeto PadecimientoActual en la base de datos
        padecimiento.save()
        return render(request, 'expedientes/create.html', {'paciente': paciente,'success_msg_padecimiento': 'Padecimiento actual guardado con éxito'})
    
    return render(request, 'expedientes/create.html')

@login_required
def guarda_exploracion_view(request):
    if request.method == 'POST':
        campos_requeridos = ['paciente_id','temperatura','presion_arterial','frecuencia_cardiaca','frecuencia_respiratoria','descripcion_exploracion']

        paciente_id = request.POST.get('paciente_id')
        peso = request.POST.get('peso')
        talla = request.POST.get('talla')
        temperatura = request.POST.get('temperatura')
        presion_arterial = request.POST.get('presion_arterial')
        frecuencia_cardiaca = request.POST.get('frecuencia_cardiaca')
        frecuencia_respiratoria = request.POST.get('frecuencia_respiratoria')
        saturacion_oxigeno = request.POST.get('saturacion_oxigeno')
        descripcion_exploracion = request.POST.get('descripcion_exploracion').upper()
        imc = request.POST.get('imc')
        glucosa = request.POST.get('glucosa')
        notas = request.POST.get('notas').upper()

        examen_fisico = ExploracionFisica(
            paciente_id=paciente_id,
            medico=request.user.medico,
            fecha=date.today(),
            peso=peso,
            talla=talla,
            temperatura=temperatura,
            presion_arterial=presion_arterial,
            frecuencia_cardiaca=frecuencia_cardiaca,
            frecuencia_respiratoria=frecuencia_respiratoria,
            saturacion_oxigeno=saturacion_oxigeno,
            descripcion_exploracion=descripcion_exploracion,
            imc=imc,
            glucosa=glucosa,
            notas=notas
        )
        if not paciente_id:
            error_msg = "No se ha inicializado ningun paciente"
            return render(request, 'expedientes/create.html', {'error_msg_examen_fisico': error_msg})
        paciente = get_object_or_404(Paciente, id=paciente_id)

        error_msg = validar_campos_requeridos(request, campos_requeridos)
        if error_msg:
            return render(request, 'expedientes/create.html', {'paciente': paciente,'error_msg_examen_fisico': error_msg})

        error_msg = validar_datos(examen_fisico)
        if error_msg:
            return render(request, 'expedientes/create.html', {'paciente': paciente,'error_msg_examen_fisico': error_msg})

        # Guardar el objeto ExamenFisico en la base de datos
        examen_fisico.save()
        return render(request, 'expedientes/create.html', {'paciente': paciente,'success_msg_examen_fisico': 'Examen físico guardado con éxito'})
    
    return render(request, 'expedientes/create.html')

@login_required
def guarda_consulta_view(request):
    if request.method == 'POST':
        campos_requeridos = ['paciente_id','diagnostico','folio_receta']

        paciente_id = request.POST.get('paciente_id')
        diagnostico = request.POST.get('diagnostico').upper()
        folio_receta = request.POST.get('folio_receta')
        notas = request.POST.get('notas').upper()

        consulta = Consulta(
            paciente_id=paciente_id,
            medico=request.user.medico,
            fecha=datetime.now(),
            diagnostico=diagnostico,
            folio_receta=folio_receta,
            notas=notas
        )
        if not paciente_id:
            error_msg = "No se ha inicializado ningun paciente"
            return render(request, 'expedientes/create.html', {'error_msg_consulta': error_msg})
        paciente = get_object_or_404(Paciente, id=paciente_id)

        error_msg = validar_campos_requeridos(request, campos_requeridos)
        if error_msg:
            return render(request, 'expedientes/create.html', {'paciente': paciente,'error_msg_consulta': error_msg})

        error_msg = validar_datos(consulta)
        if error_msg:
            return render(request, 'expedientes/create.html', {'paciente': paciente,'error_msg_consulta': error_msg})

        # Guardar el objeto Consulta en la base de datos
        consulta.save()
        return render(request, 'expedientes/create.html', {'paciente': paciente,'success_msg_consulta': 'Consulta guardada con éxito'})
    
    return render(request, 'expedientes/create.html')
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .forms import LoginForm
from .models import Paciente, Antecedentes, Medico, PadecimientoActual, ExploracionFisica, Consulta
from datetime import datetime, date
from django.contrib import messages
import time


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
            return render(request, 'expedientes/create_ficha.html', {'error_msg_ficha': error_msg})

        error_msg = validar_datos(ficha)
        if error_msg:
            return render(request, 'expedientes/create_ficha.html', {'error_msg_ficha': error_msg})

        ficha.save()
        paciente = ficha
        time.sleep(2)
        return render(request, 'expedientes/create_antecedentes.html', {'paciente': paciente})
    
    return render(request, 'expedientes/create_ficha.html')

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
            return render(request, 'expedientes/create_antecedentes.html', {'paciente': paciente,'error_msg_antecedentes': error_msg})

        error_msg = validar_datos(antecedentes)
        if error_msg:
            return render(request, 'expedientes/create_antecedentes.html', {'paciente': paciente,'error_msg_antecedentes': error_msg})

        antecedentes.save()
        time.sleep(2)
        return render(request, 'expedientes/create_padecimientos.html', {'paciente': paciente})

    return render(request, 'expedientes/create_antecedentes.html')

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

def ver_expediente_view(request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)
    antecedentes = Antecedentes.objects.filter(paciente=paciente)
    padecimiento = PadecimientoActual.objects.filter(paciente=paciente).last()
    exploracion = ExploracionFisica.objects.filter(paciente=paciente).last()
    consultas = Consulta.objects.filter(paciente=paciente)
    
    context = {
        'paciente': paciente,
        'antecedentes': antecedentes,
        'padecimiento': padecimiento,
        'exploracion': exploracion,
        'consultas': consultas,
    }
    print(paciente.escolaridad)
    return render(request, 'expedientes/view.html', context)





# Enlaces de los formularios (create)
def createFicha_view(request):
    return render(request, 'expedientes/create_ficha.html')
def createAntecedentes_view(request):
    return render(request, 'expedientes/create_antecedentes.html')
def createPadecimientos_view(request):
    return render(request, 'expedientes/create_padecimientos.html')
def createExploracion_view(request):
    return render(request, 'expedientes/create_exploracion.html')
def createConsultas_view(request):
    return render(request, 'expedientes/create_consultas.html')

# Enlaces de los formularios (update)
@login_required
def update_ficha_identificacion_view(request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)
    
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

        # Actualizar los campos del paciente existente
        paciente.nombre = nombre
        paciente.apellido_pat = apellido_pat
        paciente.apellido_mat = apellido_mat
        paciente.fecha_nacimiento = fecha_nacimiento
        paciente.genero = genero
        paciente.estado_civil = estado_civil
        paciente.grupo_rh = grupo_rh
        paciente.alergias = alergias
        paciente.curp = curp
        paciente.nacionalidad = nacionalidad
        paciente.escolaridad = escolaridad
        paciente.religion = religion
        paciente.direccion = direccion
        paciente.ocupacion = ocupacion
        paciente.empleador = empleador
        paciente.telefono_personal = telefono_personal
        paciente.nombre_contacto_emergencia = nombre_contacto_emergencia
        paciente.telefono_contacto_emergencia = telefono_contacto_emergencia
        paciente.notas = notas

        #print(paciente)

        error_msg = validar_campos_requeridos(request, campos_requeridos)
        if error_msg:
            return render(request, 'expedientes/update_ficha.html', {'error_msg_ficha': error_msg})

        error_msg = validar_datos(paciente)
        if error_msg:
            return render(request, 'expedientes/update_ficha.html', {'error_msg_ficha': error_msg})

        paciente.save()
        time.sleep(2)
        return render(request, 'expedientes/update_ficha.html', {'paciente': paciente})
    #print(paciente)
    return render(request, 'expedientes/update_ficha.html', {'paciente': paciente})



def update_antecedentes_view(request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)

    if request.method == 'POST':
        campos_requeridos = ['ahf', 'apnp', 'app']

        ahf = request.POST.get('ahf').upper()
        apnp = request.POST.get('apnp').upper()
        app = request.POST.get('app').upper()
        ago = request.POST.get('ago').upper()

        # Actualizar los campos de antecedentes existentes
        antecedentes, created = Antecedentes.objects.get_or_create(paciente=paciente)
        antecedentes.ahf = ahf
        antecedentes.apnp = apnp
        antecedentes.app = app
        antecedentes.ago = ago
        antecedentes.fecha = date.today()

        error_msg = validar_campos_requeridos(request, campos_requeridos)
        if error_msg:
            return render(request, 'expedientes/update_antecedentes.html', {'error_msg_antecedentes': error_msg, 'paciente': paciente})

        error_msg = validar_datos(paciente)
        if error_msg:
            return render(request, 'expedientes/update_antecedentes.html', {'error_msg_antecedentes': error_msg, 'paciente': paciente})

        antecedentes.save()
        time.sleep(2)
        return render(request, 'expedientes/update_antecedentes.html', {'paciente': paciente})

    return render(request, 'expedientes/update_antecedentes.html', {'paciente': paciente})


def updatePadecimientos_view(request,id_paciente):
    return render(request, 'expedientes/update_padecimientos.html')
def updateExploracion_view(request,id_paciente):
    return render(request, 'expedientes/update_exploracion.html')
def updateConsultas_view(request,id_paciente):
    return render(request, 'expedientes/update_consultas.html')
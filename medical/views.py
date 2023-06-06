from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .forms import LoginForm
from .models import Paciente, HistoriaClinica, Antecedentes
from datetime import datetime, date


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
        paciente.historias_clinicas = HistoriaClinica.objects.filter(paciente=paciente)
    return render(request, 'home.html', {'pacientes': pacientes})

@login_required
def createExp_view(request):
    return render(request, 'expedientes/create.html' )

@login_required
def guarda_ficha_identificacion_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre').upper()
        apellido_pat = request.POST.get('apellido_pat').upper()
        apellido_mat = request.POST.get('apellido_mat').upper()
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        genero = request.POST.get('genero').upper()
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
            notas=notas
        )
        try:
            ficha.full_clean()  # Validación de campos del modelo
        except ValidationError as e:
            print(e)
            msg_ficha_error= 'Favor de llenar todos los campos obligatorios (*)'
            return render(request, 'expedientes/create.html', {'msg_ficha_error': msg_ficha_error})

        ficha.save()

        historia_clinica = HistoriaClinica(
            paciente=ficha,
            medico=request.user.medico,
            fecha=date.today(),
        )

        # Guardar el objeto HistoriaClinica en la base de datos
        historia_clinica.save()

        # Obtener el ID de la historia clínica
        historia_clinica_id = historia_clinica.id

        # Mensaje de éxito
        msg_ficha_success = 'Datos guardados con éxito'

        # Redireccionar a la vista "guarda_ficha_identificacion" con el ID de la historia clínica y el mensaje de éxito
        return redirect('guarda_antecedentes', historia_clinica_id=historia_clinica_id, msg_ficha_success=msg_ficha_success)

    return render(request, 'expedientes/create.html')  # Renderiza nuevamente el formulario en caso de una solicitud GET

@login_required
def guarda_antecedentes_view(request):
    if request.method == 'POST':
        ahf = request.POST.get('ahf')
        apnp = request.POST.get('apnp')
        app = request.POST.get('app')
        ago = request.POST.get('ago')
        notas = request.POST.get('notas')
        historia_clinica_id = request.POST.get('historia_clinica_id')

        # Obtener la instancia de HistoriaClinica y Medico
        #historia_clinica = HistoriaClinica.objects.get(id=historia_clinica_id)
        medico = request.user.medico

        # Crear instancia de Antecedentes
        antecedentes = Antecedentes(
            historia_clinica=historia_clinica_id,
            medico=medico,
            fecha=date.now(),
            ahf=ahf,
            apnp=apnp,
            app=app,
            ago=ago,
            notas=notas
        )
        antecedentes.save()

        return redirect('guarda_antecedentes', {'msg_ficha_success': 'Datos guardados con éxito'})

    return render(request, 'expedientes/create.html')
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .forms import LoginForm
from .models import Paciente, Antecedentes, PadecimientoActual, ExploracionFisica, Consulta
from datetime import datetime, date
import time
from django.template import loader
from django.urls import reverse


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
            paciente.antecedentes = Antecedentes.objects.get(paciente=paciente) # type: ignore
        except Antecedentes.DoesNotExist:
            paciente.antecedentes = None # type: ignore
    
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


def renderiza_antecedentes_view(request):
    if request.method == 'GET':
        return render(request, 'expedientes/create_antecedentes.html')

def renderiza_padecimiento_view(request):
    if request.method == 'GET':
        return render(request, 'expedientes/create_padecimiento.html')

def renderiza_exploracion_view(request):
    if request.method == 'GET':
        return render(request, 'expedientes/create_exploracion.html')

def renderiza_consulta_view(request):
    if request.method == 'GET':
        return render(request, 'expedientes/create_consultas.html')

def renderiza_ayuda_view(request):
    if request.method == 'GET':
        return render(request, 'help.html')

@login_required
def guarda_ficha_identificacion_view(request):
    datos_formulario = request.POST.dict()
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

        paciente = Paciente(
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
            return render(request, 'expedientes/create_ficha.html', {'error_msg_ficha': error_msg, 'datos_formulario': datos_formulario})

        error_msg = validar_datos(paciente)
        if error_msg:
            return render(request, 'expedientes/create_ficha.html', {'error_msg_ficha': error_msg, 'datos_formulario': datos_formulario})

        paciente.save()
        time.sleep(2)
        return redirect(reverse('medical:guarda_antecedentes', args=[paciente.id]))

        
    return render(request, 'expedientes/create_ficha.html')

@login_required
def guarda_antecedentes_view(request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)
    datos_formulario = request.POST.dict()

    if request.method == 'POST':
        campos_requeridos = ['ahf', 'apnp', 'app']

        ahf = request.POST.get('ahf').upper()
        apnp = request.POST.get('apnp').upper()
        app = request.POST.get('app').upper()
        ago = request.POST.get('ago').upper()
        #paciente_id = request.POST.get('paciente_id')

        antecedentes = Antecedentes(
            paciente=paciente,
            medico=request.user.medico,
            fecha=date.today(),
            ahf=ahf,
            apnp=apnp,
            app=app,
            ago=ago
        )

        error_msg = validar_campos_requeridos(request, campos_requeridos)
        if error_msg:
            return render(request, 'expedientes/create_antecedentes.html', {'paciente': paciente, 'error_msg_antecedentes': error_msg, 'datos_formulario': datos_formulario})

        error_msg = validar_datos(antecedentes)
        if error_msg:
            return render(request, 'expedientes/create_antecedentes.html', {'paciente': paciente, 'error_msg_antecedentes': error_msg, 'datos_formulario': datos_formulario})

        antecedentes.save()
        time.sleep(2)
        return redirect(reverse('medical:guarda_padecimiento', args=[paciente.id]))

    print('get')
    return render(request, 'expedientes/create_antecedentes.html', {'paciente': paciente})


@login_required
def guarda_padecimiento_view(request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)
    datos_formulario = request.POST.dict()

    if request.method == 'POST':
        campos_requeridos = ['padecimiento_actual','piel_tegumentos','cabeza_cuello','torax','abdomen','genitourinario','musculo_extremidades','neurologico',]

        #paciente_id = request.POST.get('paciente_id')
        padecimiento_actual = request.POST.get('padecimiento_actual').upper()
        piel_tegumentos = request.POST.get('piel_tegumentos').upper()
        cabeza_cuello = request.POST.get('cabeza_cuello').upper()
        torax = request.POST.get('torax').upper()
        abdomen = request.POST.get('abdomen').upper()
        genitourinario = request.POST.get('genitourinario').upper()
        musculo_extremidades = request.POST.get('musculo_extremidades').upper()
        neurologico = request.POST.get('neurologico').upper()
        notas = request.POST.get('notas')
        if notas:
            notas = notas.upper()

        padecimiento = PadecimientoActual(
            paciente=paciente,
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

        error_msg = validar_campos_requeridos(request, campos_requeridos)
        if error_msg:
            return render(request, 'expedientes/create_padecimiento.html', {'paciente': paciente,'error_msg_padecimiento': error_msg, 'datos_formulario': datos_formulario})

        error_msg = validar_datos(padecimiento)
        if error_msg:
            return render(request, 'expedientes/create_padecimiento.html', {'paciente': paciente,'error_msg_padecimiento': error_msg, 'datos_formulario': datos_formulario})

        # Guardar el objeto PadecimientoActual en la base de datos
        padecimiento.save()
        time.sleep(2)
        return redirect(reverse('medical:guarda_exploracion', args=[paciente.id]))
    
    return render(request, 'expedientes/create_padecimiento.html', {'paciente': paciente, })

def guarda_exploracion_view(request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)
    datos_formulario = request.POST.dict()

    if request.method == 'POST':
        campos_requeridos = ['frecuencia_cardiaca','frecuencia_respiratoria','presion_arterial','temperatura','descripcion_exploracion']

        paciente_id = request.POST.get('paciente_id')
        frecuencia_cardiaca = request.POST.get('frecuencia_cardiaca')
        frecuencia_respiratoria = request.POST.get('frecuencia_respiratoria')
        temperatura = request.POST.get('temperatura')
        presion_arterial = request.POST.get('presion_arterial')
        descripcion_exploracion = request.POST.get('descripcion_exploracion').upper()

        peso = request.POST.get('peso')
        if not peso:
            peso = None

        talla = request.POST.get('talla')
        if not talla:
            talla = None

        saturacion_oxigeno = request.POST.get('saturacion_oxigeno')
        if not saturacion_oxigeno:
            saturacion_oxigeno = None

        imc = request.POST.get('imc')
        if not imc:
            imc = None

        glucosa = request.POST.get('glucosa')
        if not glucosa:
            glucosa = None

        notas = request.POST.get('notas')
        if notas:
            notas = notas.upper()


        exploracion = ExploracionFisica(
            paciente=paciente,
            medico=request.user.medico,
            fecha=datetime.now(),  
            peso=peso,
            talla=talla,
            frecuencia_cardiaca=frecuencia_cardiaca,
            frecuencia_respiratoria=frecuencia_respiratoria,
            temperatura=temperatura,
            presion_arterial=presion_arterial,
            descripcion_exploracion=descripcion_exploracion,
            saturacion_oxigeno=saturacion_oxigeno,
            imc=imc,
            glucosa=glucosa,
            notas=notas
        )

        error_msg = validar_campos_requeridos(request, campos_requeridos)
        if error_msg:
            return render(request, 'expedientes/create_exploracion.html', {'paciente': paciente,'error_msg_exploracion': error_msg, 'datos_formulario': datos_formulario})

        error_msg = validar_datos(exploracion)
        if error_msg:
            return render(request, 'expedientes/create_exploracion.html', {'paciente': paciente,'error_msg_exploracion': error_msg, 'datos_formulario': datos_formulario})

        # Guardar el objeto PadecimientoActual en la base de datos
        exploracion.save()
        time.sleep(2)
        return redirect(reverse('medical:guarda_consultas', args=[paciente.id]))

    return render(request, 'expedientes/create_exploracion.html', {'paciente': paciente,})


def guarda_consulta_view(request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)
    datos_formulario = request.POST.dict()

    if request.method == 'POST':
        campos_requeridos = ['folio_receta','diagnostico']

        paciente_id = request.POST.get('paciente_id')
        #motivo_consulta = request.POST.get('motivo_consulta').upper()
        fecha = request.POST.get('fecha')
        diagnostico = request.POST.get('diagnostico').upper()
        folio_receta = request.POST.get('folio_receta')
        notas = request.POST.get('notas')
        if notas:
            notas = notas.upper()

        consulta = Consulta(
            paciente=paciente,
            medico=request.user.medico,
            fecha=fecha,
            #motivo_consulta=motivo_consulta,
            diagnostico=diagnostico,
            folio_receta=folio_receta,
            notas=notas
        )

        error_msg = validar_campos_requeridos(request, campos_requeridos)
        if error_msg:
            return render(request, 'expedientes/create_consultas.html', {'paciente': paciente,'error_msg_consulta': error_msg, 'datos_formulario': datos_formulario})

        error_msg = validar_datos(consulta)
        if error_msg:
            return render(request, 'expedientes/create_consultas.html', {'paciente': paciente,'error_msg_consulta': error_msg, 'datos_formulario': datos_formulario})

        # Guardar el objeto PadecimientoActual en la base de datos
        consulta.save()
        time.sleep(2)
        return redirect(reverse('medical:ver_expediente', args=[paciente.id]))
        #return render(request, 'expedientes/view.html', {'paciente': paciente,})

    return render(request, 'expedientes/create_consultas.html', {'paciente': paciente,})


@login_required
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
    return render(request, 'expedientes/view.html', context)


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

        error_msg = validar_campos_requeridos(request, campos_requeridos)
        if error_msg:
            return render(request, 'expedientes/update_ficha.html', {'error_msg_ficha': error_msg})

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

        error_msg = validar_datos(paciente)
        if error_msg:
            return render(request, 'expedientes/update_ficha.html', {'error_msg_ficha': error_msg})

        paciente.save()
        time.sleep(2)
        return render(request, 'expedientes/update_ficha.html', {'paciente': paciente})

    return render(request, 'expedientes/update_ficha.html', {'paciente': paciente})



def update_antecedentes_view(request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)
    antecedentes = Antecedentes.objects.filter(paciente=paciente)

    if request.method == 'POST':
        campos_requeridos = ['ahf', 'apnp', 'app']

        ahf = request.POST.get('ahf').upper()
        apnp = request.POST.get('apnp').upper()
        app = request.POST.get('app').upper()
        ago = request.POST.get('ago').upper()

        # Actualizar los campos de antecedentes existentes
        antecedentes = Antecedentes.objects.filter(paciente=paciente).first()
        
        if antecedentes is None:
            antecedentes = Antecedentes(paciente=paciente)

        antecedentes.paciente = paciente
        antecedentes.medico = request.user.medico 
        antecedentes.ahf = ahf
        antecedentes.apnp = apnp
        antecedentes.app = app
        antecedentes.ago = ago
        antecedentes.fecha = date.today()

        error_msg = validar_campos_requeridos(request, campos_requeridos)
        if error_msg:
            return render(request, 'expedientes/update_antecedentes.html', {'error_msg_antecedentes': error_msg, 'paciente': paciente, 'antecedentes': antecedentes})

        error_msg = validar_datos(antecedentes)
        if error_msg:
            return render(request, 'expedientes/update_antecedentes.html', {'error_msg_antecedentes': error_msg, 'paciente': paciente, 'antecedentes': antecedentes})

        antecedentes.save()
        time.sleep(2)
        return render(request, 'expedientes/update_antecedentes.html', {'paciente': paciente, 'antecedentes': antecedentes})

    template = loader.get_template('expedientes/update_antecedentes.html')
    context = {'paciente': paciente, 'antecedentes': antecedentes}
    return HttpResponse(template.render(context, request))
    #return render(request, 'expedientes/update_antecedentes.html', {'paciente': paciente})



def update_padecimiento_view(request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)

    if request.method == 'POST':
        campos_requeridos = ['padecimiento_actual', 'piel_tegumentos', 'cabeza_cuello', 'torax', 'abdomen', 'genitourinario', 'musculo_extremidades', 'neurologico']

        padecimiento_actual = request.POST.get('padecimiento_actual').upper()
        piel_tegumentos = request.POST.get('piel_tegumentos').upper()
        cabeza_cuello = request.POST.get('cabeza_cuello').upper()
        torax = request.POST.get('torax').upper()
        abdomen = request.POST.get('abdomen').upper()
        genitourinario = request.POST.get('genitourinario').upper()
        musculo_extremidades = request.POST.get('musculo_extremidades').upper()
        neurologico = request.POST.get('neurologico').upper()
        notas = request.POST.get('notas')

        # Obtener el último registro de PadecimientoActual asociado al paciente
        if PadecimientoActual.objects.filter(paciente=paciente).exists():
            padecimiento = PadecimientoActual.objects.filter(paciente=paciente).latest('fecha')
        else:
            padecimiento = PadecimientoActual()
        padecimiento.paciente = paciente
        padecimiento.medico = request.user.medico  # Asigna el médico actualmente logueado
        padecimiento.fecha = datetime.now()
        padecimiento.padecimiento_actual = padecimiento_actual
        padecimiento.piel_tegumentos = piel_tegumentos
        padecimiento.cabeza_cuello = cabeza_cuello
        padecimiento.torax = torax
        padecimiento.abdomen = abdomen
        padecimiento.genitourinario = genitourinario
        padecimiento.musculo_extremidades = musculo_extremidades
        padecimiento.neurologico = neurologico
        padecimiento.notas = notas

        error_msg = validar_campos_requeridos(request, campos_requeridos)
        if error_msg:
            return render(request, 'expedientes/update_padecimiento.html', {'error_msg_padecimiento': error_msg, 'paciente': paciente, 'padecimiento': padecimiento})

        error_msg = validar_datos(padecimiento)
        if error_msg:
            return render(request, 'expedientes/update_padecimiento.html', {'error_msg_padecimiento': error_msg, 'paciente': paciente, 'padecimiento': padecimiento})

        padecimiento.save()
        time.sleep(2)
        return render(request, 'expedientes/update_padecimiento.html', {'paciente': paciente, 'padecimiento': padecimiento})

    # Obtener el último registro de PadecimientoActual asociado al paciente
    padecimiento = PadecimientoActual.objects.filter(paciente=paciente).order_by('-fecha').first()

    template = loader.get_template('expedientes/update_padecimiento.html')
    context = {'paciente': paciente, 'padecimiento': padecimiento}
    return HttpResponse(template.render(context, request))


def update_exploracion_view(request,id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)

    if request.method == 'POST':
        campos_requeridos = ['frecuencia_cardiaca','frecuencia_respiratoria','presion_arterial','temperatura','descripcion_exploracion']

        paciente_id = request.POST.get('paciente_id')
        frecuencia_cardiaca = request.POST.get('frecuencia_cardiaca')
        frecuencia_respiratoria = request.POST.get('frecuencia_respiratoria')
        temperatura = request.POST.get('temperatura')
        presion_arterial = request.POST.get('presion_arterial')
        descripcion_exploracion = request.POST.get('descripcion_exploracion').upper()

        peso = request.POST.get('peso')
        if not peso:
            peso = None

        talla = request.POST.get('talla')
        if not talla:
            talla = None

        saturacion_oxigeno = request.POST.get('saturacion_oxigeno')
        if not saturacion_oxigeno:
            saturacion_oxigeno = None

        imc = request.POST.get('imc')
        if not imc:
            imc = None

        glucosa = request.POST.get('glucosa')
        if not glucosa:
            glucosa = None

        notas = request.POST.get('notas')
        if notas:
            notas = notas.upper()

        # Obtener el último registro de Exploracion asociado al paciente
        if ExploracionFisica.objects.filter(paciente=paciente).exists():
            exploracion = ExploracionFisica.objects.filter(paciente=paciente).latest('fecha')
        else:
            exploracion = ExploracionFisica()
        exploracion.paciente = paciente
        exploracion.medico = request.user.medico  # Asigna el médico actualmente logueado
        exploracion.fecha = datetime.now()
        exploracion.peso = peso
        exploracion.talla = talla
        exploracion.frecuencia_cardiaca = frecuencia_cardiaca
        exploracion.frecuencia_respiratoria = frecuencia_respiratoria
        exploracion.temperatura = temperatura
        exploracion.presion_arterial = presion_arterial
        exploracion.descripcion_exploracion = descripcion_exploracion
        exploracion.saturacion_oxigeno = saturacion_oxigeno
        exploracion.imc = imc
        exploracion.glucosa = glucosa
        exploracion.notas = notas

        error_msg = validar_campos_requeridos(request, campos_requeridos)
        if error_msg:
            return render(request, 'expedientes/update_exploracion.html', {'error_msg_exploracion': error_msg, 'paciente': paciente, 'exploracion': exploracion})

        error_msg = validar_datos(exploracion)
        if error_msg:
            return render(request, 'expedientes/update_exploracion.html', {'error_msg_exploracion': error_msg, 'paciente': paciente, 'exploracion': exploracion})

        exploracion.save()
        time.sleep(2)
        return render(request, 'expedientes/update_exploracion.html', {'paciente': paciente, 'exploracion': exploracion})

    # Obtener el último registro de Exploracion asociado al paciente
    exploracion = ExploracionFisica.objects.filter(paciente=paciente).order_by('-fecha').first()

    template = loader.get_template('expedientes/update_exploracion.html')
    context = {'paciente': paciente, 'exploracion': exploracion}
    return HttpResponse(template.render(context, request))

def update_consultas_view(request,id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)
    

    if request.method == 'POST':
        campos_requeridos = ['folio_receta','diagnostico']

        #motivo_consulta = request.POST.get('motivo_consulta').upper()
        fecha = request.POST.get('fecha')
        diagnostico = request.POST.get('diagnostico').upper()
        folio_receta = request.POST.get('folio_receta')
        notas = request.POST.get('notas')
        if notas:
            notas = notas.upper()

        # Obtener el último registro de Consulta asociado al paciente
        if Consulta.objects.filter(paciente=paciente).exists():
            consulta = Consulta.objects.filter(paciente=paciente).latest('fecha')
        else:
            consulta = Consulta()
        consulta.paciente = paciente
        consulta.medico = request.user.medico
        consulta.fecha = fecha
        consulta.diagnostico = diagnostico
        consulta.folio_receta = folio_receta
        consulta.notas = notas

        error_msg = validar_campos_requeridos(request, campos_requeridos)
        if error_msg:
            return render(request, 'expedientes/update_consultas.html', {'error_msg_consulta': error_msg, 'paciente': paciente, 'consulta': consulta})

        error_msg = validar_datos(consulta)
        if error_msg:
            return render(request, 'expedientes/update_consultas.html', {'error_msg_consulta': error_msg, 'paciente': paciente, 'consulta': consulta})

        consulta.save()
        time.sleep(2)
        return render(request, 'expedientes/update_consultas.html', {'paciente': paciente, 'consulta': consulta})

    consulta = Consulta.objects.filter(paciente=paciente).order_by('-fecha').first()

    template = loader.get_template('expedientes/update_consultas.html')
    context = {'paciente': paciente, 'consulta': consulta}
    return HttpResponse(template.render(context, request))

#eliminar un paciente
def elimina_paciente_view(request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)
    paciente.delete()
    return redirect('medical:home')

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .forms import LoginForm
from .models import Paciente, HistoriaClinica


# Create your views here.
def test(request):
    return render(request, "test.html")

def login_view(request):
    error_message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                error_message = 'Invalid username or password'
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

# Crear nuevo expediente
def createExp_view(request):
    return render(request, 'expedientes/create.html' )

def guarda_ficha_identificacion(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido_pat = request.POST.get('apellido_pat')
        apellido_mat = request.POST.get('apellido_mat')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        genero = request.POST.get('genero')
        estado_civil = request.POST.get('estado_civil')
        grupo_rh = request.POST.get('grupo_rh')
        #alergias = request.POST.get('alergias')
        #curp = request.POST.get('curp')
        nacionalidad = request.POST.get('nacionalidad')
        escolaridad = request.POST.get('escolaridad')
        religion = request.POST.get('religion')
        direccion = request.POST.get('direccion')
        ocupacion = request.POST.get('ocupacion')
        #empleador = request.POST.get('empleador')
        telefono_personal = request.POST.get('telefono_personal')
        #nombre_contacto_emergencia = request.POST.get('nombre_contacto_emergencia')
        #telefono_contacto_emergencia = request.POST.get('telefono_contacto_emergencia')
        notas = request.POST.get('notas')

        ficha = Paciente(
            nombre=nombre,
            apellido_pat=apellido_pat,
            apellido_mat=apellido_mat,
            fecha_nacimiento=fecha_nacimiento,
            genero=genero,
            estado_civil=estado_civil,
            grupo_rh=grupo_rh,
            #alergias=alergias,
            #curp=curp,
            nacionalidad=nacionalidad,
            escolaridad=escolaridad,
            religion=religion,
            direccion=direccion,
            ocupacion=ocupacion,
            #empleador=empleador,
            telefono_personal=telefono_personal,
            #nombre_contacto_emergencia=nombre_contacto_emergencia,
            #telefono_contacto_emergencia=telefono_contacto_emergencia,
            notas=notas
        )
        try:
            ficha.full_clean()  # Validación de campos del modelo
        except ValidationError as e:
            return render(request, 'expedientes/create.html', {'msg': str(e)})
            
        ficha.save()
        return render(request, 'expedientes/create.html', {'msg': 'guardado con exito'})  # Puedes redirigir a una página de éxito o hacer cualquier otra acción que necesites
       
    print('aca')
    return render(request, 'expedientes/create.html')  # Renderiza nuevamente el formulario en caso de una solicitud GET
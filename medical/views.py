from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def test(request):
    return render(request, "test.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = ''
    return render(request, 'login.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'home.html')

# Crear nuevo expediente
def createExp_view(request):
    return render(request, 'expedientes/create.html' )
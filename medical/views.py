from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'test.html')

def login(request):
    pass

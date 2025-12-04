from django.shortcuts import render
from .models import Chave

# Create your views here.

def index (request):
    # Busca todas as chaves cadastradas no banco
    chaves = Chave.objects.all()
    
    # Envia as chaves para o HTML dentro do "contexto"
    return render(request, 'index.html', {'chaves': chaves})

def perfil (request):
    return render(request, 'perfil.html')

# def login(request):
#     return render(request, 'login.html')

def sobre(request):
    return render(request, 'sobrenos.html')


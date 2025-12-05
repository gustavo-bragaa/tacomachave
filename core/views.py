from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from .models import Chave, Usuario, Movimentacao
from .forms import LoginForm, UsuarioForm, EmprestarForm

# Create your views here.

def index (request):
    # Busca todas as chaves cadastradas no banco
    chaves = Chave.objects.all()
    
    # Envia as chaves para o HTML dentro do "contexto"
    return render(request, 'index.html', {'chaves': chaves})

def perfil (request):
    return render(request, 'perfil.html')

def login(request):
    return render(request, 'tela_login.html')

def sobre(request):
    return render(request, 'sobrenos.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # também popular sessão customizada para compatibilidade com o código existente
                try:
                    perfil_usuario = None
                    # se existir um Usuário customizado relacionado pelo login, populamos sessão
                    usuario_obj = Usuario.objects.filter(login=username).first()
                    if usuario_obj:
                        request.session['usuario_id'] = usuario_obj.id
                        request.session['usuario_nome'] = usuario_obj.nome
                        request.session['usuario_perfil'] = usuario_obj.perfil
                    else:
                        # fallback: usar dados do User do Django
                        request.session['usuario_id'] = user.id
                        request.session['usuario_nome'] = user.get_full_name() or user.username
                        request.session['usuario_perfil'] = 'admin' if user.is_staff else 'porteiro'
                except Exception:
                    pass

                messages.success(request, f"Bem-vindo, {user.get_full_name() or user.username}!")
                return redirect('index')
            else:
                messages.error(request, "Login ou senha inválidos.")
        else:
            messages.error(request, "Erro de validação do formulário.")
    else:
        form = LoginForm()

    return render(request, 'tela_login.html', {'form': form})


def logout_view(request):
    # limpar sessão customizada e deslogar do sistema Django
    request.session.flush()
    auth_logout(request)
    messages.info(request, "Você saiu da sua conta.")
    return redirect('login')



def lista_usuarios(request):
    usuarios = Usuario.objects.all().order_by('nome')
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

def criar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.senha = make_password(form.cleaned_data['senha'])
            usuario.save()
            messages.success(request, "Usuário criado com sucesso.")
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    
    return render(request, 'form_usuario.html', {'form': form, 'tipo': 'Criar'})

def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.senha = make_password(form.cleaned_data['senha'])
            usuario.save()
            messages.success(request, "Usuário atualizado com sucesso.")
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(initial={
            'nome': usuario.nome,
            'matricula': usuario.matricula,
            'login': usuario.login,
            'perfil': usuario.perfil
        })

    return render(request, 'form_usuario.html', {'form': form, 'tipo': 'Editar'})

def deletar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        try:
            usuario.delete()
            messages.success(request, "Usuário excluído com sucesso.")
        except:
            messages.error(request, "Não foi possível excluir. Este usuário pode ter movimentações associadas.")
        return redirect('lista_usuarios')
    
    return render(request, 'confirmar_delete_usuario.html', {'usuario': usuario})


def emprestar_chave(request, id_chave):
    if 'usuario_id' not in request.session:
        messages.error(request, "Acesso restrito a porteiros.")
        return redirect('login')
    
    porteiro_logado = Usuario.objects.get(id=request.session['usuario_id'])
    chave = get_object_or_404(Chave, id=id_chave)

    if chave.status == 'indisponivel':
        messages.error(request, f"A chave {chave.nome_sala} já está in uso.")
        return redirect('index')

    if request.method == 'POST':
        form = EmprestarForm(request.POST)
        if form.is_valid():
   
            mov = form.save(commit=False)
            mov.chave = chave
            mov.porteiro_liberou = porteiro_logado
            mov.data_retirada = timezone.now() 
            mov.save()
            

            chave.status = 'indisponivel'
            chave.save()
            
            messages.success(request, f"Chave {chave.nome_sala} emprestada para {mov.nome_solicitante}.")
            return redirect('index')
    else:
        form = EmprestarForm()

    return render(request, 'emprestar_chave.html', {
        'form': form, 
        'chave': chave
    })


def devolver_chave(request, id_chave):
    if 'usuario_id' not in request.session:
        messages.error(request, "Acesso restrito a porteiros.")
        return redirect('login')
        
    chave = get_object_or_404(Chave, id=id_chave)

    try:
        mov = Movimentacao.objects.filter(chave=chave, data_devolucao=None).latest('data_retirada')
    except Movimentacao.DoesNotExist:
        messages.error(request, f"Erro: A chave {chave.nome_sala} já consta como 'Disponível'.")
        return redirect('index')

    if request.method == 'POST':
        mov.data_devolucao = timezone.now()
        mov.save()
        
        chave.status = 'disponivel'
        chave.save()
        
        messages.success(request, f"Chave {chave.nome_sala} devolvida.")
        return redirect('index')

    return render(request, 'confirmar_devolucao.html', {
        'chave': chave,
        'movimentacao': mov
    })


def historico_movimentacoes(request):
    movimentacoes = Movimentacao.objects.all().order_by('-data_retirada')
    
    return render(request, 'historico.html', {'movimentacoes': movimentacoes})
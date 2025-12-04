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

def login_view(request):
    if 'usuario_id' in request.session:
        return redirect('index')

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            senha = form.cleaned_data['senha']
            
            try:
                usuario = Usuario.objects.get(login=login)
                
                if check_password(senha, usuario.senha):
                    request.session['usuario_id'] = usuario.id
                    request.session['usuario_nome'] = usuario.nome
                    request.session['usuario_perfil'] = usuario.perfil
                    
                    messages.success(request, f"Bem-vindo, {usuario.nome}!")
                    return redirect('index') 
                else:
                    messages.error(request, "Login ou senha inválidos.")
            except Usuario.DoesNotExist:
                messages.error(request, "Login ou senha inválidos.")

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    request.session.flush()
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
        messages.error(request, f"A chave {chave.nome_sala} já está em uso.")
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
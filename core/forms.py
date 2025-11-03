from django import forms
from .models import Chave, Permissao, Usuario, Movimentacao

class ChaveForm(forms.ModelForm):
    class Meta:
        model = Chave
        fields = ['nome_sala', 'numero_porta', 'status']
        widgets = {
            'nome_sala': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_porta': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class UsuarioCreateForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
                            label="Senha")

    class Meta:
        model = Usuario
        fields = ['nome', 'matricula', 'login', 'senha', 'perfil']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'login': forms.TextInput(attrs={'class': 'form-control'}),
            'perfil': forms.Select(attrs={'class': 'form-select'}),
        }

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'matricula', 'login', 'perfil']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'login': forms.TextInput(attrs={'class': 'form-control'}),
            'perfil': forms.Select(attrs={'class': 'form-select'}),
        }

class MovimentacaoCreateForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['chave', 'porteiro_liberou', 'nome_solicitante', 'matricula_solicitante']
        widgets = {
            'chave': forms.Select(attrs={'class': 'form-select'}),
            'porteiro_liberou': forms.Select(attrs={'class': 'form-select'}),
            'nome_solicitante': forms.TextInput(attrs={'class': 'form-control'}),
            'matricula_solicitante': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PermissaoForm(forms.ModelForm):
    class Meta:
        model = Permissao
        fields = ['usuario', 'chave']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'chave': forms.Select(attrs={'class': 'form-select'}),
        }
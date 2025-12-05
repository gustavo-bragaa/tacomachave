from django import forms
from .models import Chave, Permissao, Usuario, Movimentacao

class ChaveForm(forms.ModelForm):
    class Meta:
        model = Chave
        fields = ['nome_sala', 'numero_porta', 'status']

class UsuarioCreateForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput(render_value=False), 
        required=True,
        help_text="Crie uma senha forte."
    )

    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(render_value=False), 
        required=True, 
        label="Confirmar Senha"
    )
    class Meta:
        model = Usuario
        fields = ['nome', 'matricula', 'login', 'perfil', 'senha', 'confirmar_senha']

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")

        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error('confirmar_senha', "As senhas não coincidem.")
            
        return cleaned_data

# Alias para manter compatibilidade com o código existente
UsuarioForm = UsuarioCreateForm

# Formulário de login ajustado para usar os nomes padrão do Django (username, password)
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class EmprestarForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        # Campos que o porteiro deve preencher ao emprestar
        fields = ['nome_solicitante', 'matricula_solicitante']
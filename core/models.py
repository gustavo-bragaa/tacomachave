from django.db import models

class Chave(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('indisponivel', 'Indisponível'),
    ]
    nome_sala = models.CharField(max_length=100, help_text="Nome da sala ou do local (Ex: Laboratório de Redes)")
    numero_porta = models.CharField(max_length=45, blank=True, help_text="Número da porta (Ex: 101 ou B203)")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='disponivel', help_text="Status atual da chave")

    def __str__(self):
        return f"{self.nome_sala} ({self.get_status_display()})"

class Usuario(models.Model):
    PERFIL_CHOICES = [
        ('porteiro', 'Porteiro'),
        ('admin', 'Administrador'),
    ]

    nome = models.CharField(max_length=255)
    matricula = models.CharField(max_length=45, unique=True, help_text="Matrícula única do usuário no IFRN")
    login = models.CharField(max_length=45, unique=True)
    senha = models.CharField(max_length=255, help_text="A senha deve ser armazenada usando hash")
    perfil = models.CharField(max_length=15, choices=PERFIL_CHOICES)

    def __str__(self):
        return self.nome

class Movimentacao(models.Model):
    chave = models.ForeignKey(Chave, on_delete=models.CASCADE, help_text="Chave que foi movimentada")
    porteiro_liberou = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='movimentacoes_liberadas', help_text="Porteiro que registrou a saída")
    
    # informações da pessoa que retirou a chave (não precisa ser um usuário do sistema)
    nome_solicitante = models.CharField(max_length=255, help_text="Nome de quem retirou a chave")
    matricula_solicitante = models.CharField(max_length=45, help_text="Matrícula de quem retirou a chave")
    
    data_retirada = models.DateTimeField(auto_now_add=True, help_text="Data e hora em que a chave foi retirada")
    data_devolucao = models.DateTimeField(null=True, blank=True, help_text="Data e hora em que a chave foi devolvida")
    observacao = models.TextField(null=True, blank=True, help_text="Observações sobre a movimentação")

    def __str__(self):
        return f"Chave {self.chave.nome_sala} retirada por {self.nome_solicitante}"

# tabela para definir as regras de quem pode pegar qual chave
class Permissao(models.Model):

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, help_text="Usuário que recebe a permissão")
    chave = models.ForeignKey(Chave, on_delete=models.CASCADE, help_text="Chave para a qual a permissão é concedida")

    class Meta:
        unique_together = ('usuario', 'chave')

    def __str__(self):
        return f"Permissão para {self.usuario.nome} na chave {self.chave.nome_sala}"
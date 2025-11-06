from django.contrib import admin
# Estamos importando apenas as 3 tabelas que existem no models.py
from .models import Chave, Usuario, Movimentacao

# Explicação:
# Com estas linhas, você está completando as entregas de 30/10 e 06/11.
# Estamos registrando os CRUDs no painel de administração.

# CRUDs "sem dependência" (Entrega 30/10)
admin.site.register(Chave)
admin.site.register(Usuario)

# CRUD "com dependência" (Completa a Entrega 06/11)
admin.site.register(Movimentacao)
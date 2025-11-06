from django.contrib import admin
from .models import Chave, Usuario, Movimentacao, Permissao

# Registrando os modelos no site de administração do Django

# Estes são os "CRUDs sem dependências" (Entrega 30/10)
admin.site.register(Chave)
admin.site.register(Usuario)

# Estes são os "CRUDs com dependências" (Entrega 06/11)
admin.site.register(Movimentacao)
admin.site.register(Permissao)
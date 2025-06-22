# Reset de Ambiente - Evil Force JWT

Este conjunto de scripts foi criado para corrigir definitivamente os problemas de instalação e dependências do projeto Evil Force JWT.

## Problemas Corrigidos

1. **Distribuições inválidas do pip** (ex: `~vicorn`)
2. **Conflitos de dependências** (anyio 4.x vs openai que requer <4)
3. **Problemas de QApplication** sendo criada após widgets
4. **Cache corrompido do pip**
5. **Versões incompatíveis de dependências**

## Scripts Disponíveis

### Windows
```batch
reset_env.bat
```

### Linux/Mac
```bash
reset_env.sh
```

### Python (Multiplataforma)
```bash
python reset_env.py
```

## Como Usar

### 1. Execute o Script de Reset

**Windows:**
```cmd
reset_env.bat
```

**Linux/Mac:**
```bash
./reset_env.sh
```

**Ou diretamente:**
```bash
python reset_env.py
```

### 2. Aguarde a Conclusão

O script irá:
- ✅ Verificar informações do Python
- ✅ Limpar distribuições inválidas
- ✅ Corrigir conflitos de dependências
- ✅ Atualizar o pip
- ✅ Instalar dependências principais
- ✅ Instalar dependências da GUI
- ✅ Verificar instalações
- ✅ Criar script de teste

### 3. Teste o Ambiente

Após a conclusão, execute o teste:
```bash
python test_environment.py
```

Se uma janela de teste aparecer com "✅ Ambiente funcionando corretamente!", o reset foi bem-sucedido.

### 4. Execute o Painel Admin

Agora você pode executar o painel admin:
```bash
python AdminPanel_EJF/admin_panel.py
```

## O que o Script Faz

### Limpeza
- Remove distribuições inválidas do pip
- Limpa cache do pip
- Corrige conflitos de versões

### Instalação
- Atualiza pip para versão mais recente
- Instala dependências essenciais com versões específicas
- Instala PyQt5 com versões compatíveis

### Verificação
- Testa importação de todos os pacotes
- Cria script de teste automático
- Fornece feedback detalhado

## Dependências Instaladas

### Core
- fastapi==0.111.0
- uvicorn==0.29.0
- python-jose[cryptography]==3.3.0
- passlib[bcrypt]==1.7.4
- python-multipart==0.0.9
- pydantic==2.7.1
- requests==2.31.0
- pyjwt==2.8.0
- jinja2==3.1.4

### GUI
- PyQt5==5.15.9
- PyQt5-Qt5==5.15.2
- PyQt5-sip==12.12.2

## Solução de Problemas

### Se o script falhar:
1. Execute novamente: `python reset_env.py`
2. Verifique se está em um ambiente virtual
3. Se persistir, recrie o ambiente virtual

### Se o teste falhar:
1. Verifique se PyQt5 foi instalado corretamente
2. Execute: `pip show PyQt5`
3. Se necessário, reinstale: `pip install PyQt5==5.15.9`

### Se o painel admin não funcionar:
1. Verifique se a API está rodando
2. Execute: `python auth_api/main.py`
3. Verifique logs de erro

## Logs e Debug

O script fornece logs detalhados de cada etapa. Se houver problemas, verifique:

1. **Saída do comando**: Mostra o que foi executado
2. **Stderr**: Mostra erros específicos
3. **Código de retorno**: 0 = sucesso, 1 = erro

## Ambiente Virtual

O script detecta automaticamente se você está em um ambiente virtual. É recomendado usar um ambiente virtual para evitar conflitos.

Para criar um novo ambiente virtual:
```bash
python -m venv evil_jwt_env
```

Para ativar:
```bash
# Windows
evil_jwt_env\Scripts\activate

# Linux/Mac
source evil_jwt_env/bin/activate
```

## Suporte

Se você encontrar problemas persistentes:

1. Execute o script com `--verbose` para mais detalhes
2. Verifique se Python 3.8+ está instalado
3. Certifique-se de ter permissões de administrador (Windows)
4. Considere usar um ambiente virtual limpo

---

**Nota**: Este script é seguro e não remove dados do projeto, apenas corrige o ambiente Python. 
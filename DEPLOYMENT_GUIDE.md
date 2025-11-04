# 🚀 Guia Completo de Deploy - Architectural AI Agent

Este guia fornece instruções passo a passo para fazer deploy da aplicação Azure Function com integração CI/CD via GitHub Actions.

---

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Configuração Inicial do Azure](#configuração-inicial-do-azure)
3. [Preparar o Repositório Git](#preparar-o-repositório-git)
4. [Configurar GitHub Secrets](#configurar-github-secrets)
5. [Deploy Automático com GitHub Actions](#deploy-automático-com-github-actions)
6. [Monitorar o Deploy](#monitorar-o-deploy)
7. [Validar o Deploy](#validar-o-deploy)
8. [Troubleshooting](#troubleshooting)

---

## 🔧 Pré-requisitos

Antes de começar, você precisa ter:

### **Ferramentas Instaladas**
- ✅ [Git](https://git-scm.com/download) (v2.30+)
- ✅ [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) (v2.50+)
- ✅ [Python](https://www.python.org/downloads/) (v3.9+)
- ✅ [Azure Functions Core Tools](https://github.com/Azure/azure-functions-core-tools) (v4.0+)

### **Contas e Recursos**
- ✅ Conta GitHub com acesso ao repositório
- ✅ Conta Azure com permissão para criar recursos
- ✅ Função Azure já criada (ex: `guruarchtech`)
- ✅ Azure OpenAI Service deployado (modelo GPT-4.1)
- ✅ Credenciais do Azure OpenAI (API Key, Endpoint)

### **Verificar Instalações**

```bash
# Verificar versões
git --version
az --version
python --version
func --version
```

---

## 🌐 Configuração Inicial do Azure

### **Passo 1: Fazer Login no Azure**

```bash
az login
```

Isso abrirá uma janela do navegador. Faça login com sua conta Azure.

### **Passo 2: Listar Recursos**

```bash
# Ver subscription atual
az account show

# Listar Function Apps
az functionapp list --output table

# Listar recursos OpenAI
az cognitiveservices account list --output table
```

### **Passo 3: Configurar Variáveis de Ambiente no Azure Portal**

A função precisa de 4 variáveis configuradas no Azure Portal:

1. Vá para: https://portal.azure.com
2. Procure por sua Function App: **`guruarchtech`**
3. Clique em **"Configuration"** (ou **"Configuração"**)
4. Clique em **"New application setting"** (ou **"Nova configuração de aplicação"**)

Adicione as 4 variáveis:

| Nome | Valor | Descrição |
|------|-------|-----------|
| `AZURE_OPENAI_API_KEY` | `<sua-chave-api>` | Chave da API do Azure OpenAI |
| `AZURE_OPENAI_ENDPOINT` | `https://<seu-recurso>.cognitiveservices.azure.com/` | Endpoint do recurso |
| `AZURE_OPENAI_API_VERSION` | `2024-12-01-preview` | Versão da API |
| `AZURE_OPENAI_DEPLOYMENT` | `gpt-4.1` | Nome do deployment GPT |

**Como obter essas credenciais:**

1. Vá para https://portal.azure.com
2. Procure por **"Azure OpenAI Service"**
3. Clique em seu recurso
4. Vá para **"Keys and Endpoint"** (ou **"Chaves e Ponto de Extremidade"**)
5. Copie **Key 1** e **Endpoint**

### **Passo 4: Salvar e Testar**

Após adicionar as variáveis:
1. Clique em **"Save"** (ou **"Salvar"**)
2. Aguarde a função reiniciar (alguns segundos)
3. Teste a função manualmente (ver seção [Validar o Deploy](#validar-o-deploy))

---

## 📦 Preparar o Repositório Git

### **Passo 1: Clonar o Repositório (se não tiver)**

```bash
git clone https://github.com/brunomalhano/agent-ia-live.git
cd agent-ia-live
```

### **Passo 2: Verificar a Estrutura**

```bash
# Verificar se os workflows estão presentes
ls -la .github/workflows/

# Você deve ver 3 arquivos:
# - test-and-build.yml
# - deploy.yml
# - validate.yml
```

### **Passo 3: Verificar Branch Principal**

```bash
# Verificar branch atual
git branch

# Garantir que está em main
git checkout main

# Atualizar com últimas mudanças
git pull origin main
```

---

## 🔐 Configurar GitHub Secrets

Os secrets são credenciais armazenadas de forma segura no GitHub. O GitHub Actions usa esses secrets para fazer deploy sem expor as credenciais.

### **Passo 1: Acessar Secrets no GitHub**

1. Vá para seu repositório: https://github.com/brunomalhano/agent-ia-live
2. Clique em **Settings** (⚙️)
3. No menu lateral, clique em **Secrets and variables** → **Actions**
4. Clique em **"New repository secret"**

### **Passo 2: Adicionar Secret `AZURE_CREDENTIALS` (Obrigatório)**

Este é o secret mais importante. Ele contém as credenciais do Azure para fazer deploy.

**Criar o Secret:**

1. Execute este comando no terminal:

```bash
# Substituir pelos seus valores reais
SUBSCRIPTION_ID="seu-subscription-id"
RESOURCE_GROUP="seu-resource-group"

az ad sp create-for-rbac \
  --name "GitHub-Actions-Deploy" \
  --role contributor \
  --scopes /subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP \
  --json-auth
```

2. O comando vai retornar um JSON parecido com:

```json
{
  "clientId": "xxx-xxx-xxx",
  "clientSecret": "xxx-xxx-xxx",
  "subscriptionId": "xxx-xxx-xxx",
  "tenantId": "xxx-xxx-xxx",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

3. **Copie todo o JSON** (incluindo chaves e parênteses)
4. No GitHub, preencha:
   - **Name**: `AZURE_CREDENTIALS`
   - **Value**: Cole o JSON completo
5. Clique em **"Add secret"**

### **Passo 3: Adicionar Secret `FUNCAPP_NAME`**

1. Clique em **"New repository secret"**
2. Preencha:
   - **Name**: `FUNCAPP_NAME`
   - **Value**: `guruarchtech`
3. Clique em **"Add secret"**

### **Passo 4: Adicionar Secret `FUNCAPP_URL`**

1. Clique em **"New repository secret"**
2. Preencha:
   - **Name**: `FUNCAPP_URL`
   - **Value**: `https://guruarchtech.azurewebsites.net`
3. Clique em **"Add secret"**

### **Passo 5: Adicionar Secret `FUNCAPP_CODE` (Opcional)**

Este é usado para testes pós-deploy.

1. Vá para https://portal.azure.com
2. Procure por sua Function App
3. Vá para **Functions** → **agent** → **Function Keys**
4. Copie o valor de **default**
5. No GitHub:
   - **Name**: `FUNCAPP_CODE`
   - **Value**: Cole o código copiado
6. Clique em **"Add secret"**

### **Verificar Secrets Adicionados**

Após adicionar, você deve ver na página de Secrets:

```
✓ AZURE_CREDENTIALS
✓ FUNCAPP_NAME
✓ FUNCAPP_URL
✓ FUNCAPP_CODE (opcional)
```

---

## 🚀 Deploy Automático com GitHub Actions

Agora que tudo está configurado, o deploy é automático!

### **Como Funciona o Fluxo**

```
Você faz push para main
    ↓
GitHub Actions é acionado automaticamente
    ↓
[1] Test & Build
    - Executa linting (flake8)
    - Executa testes unitários
    - Verifica formatação (black)
    ↓
[2] Deploy (aguarda aprovação)
    - Faz build do artefato
    - Valida a função
    - Aguarda você aprovar manualmente ⏸️
    ↓
[3] Deploy to Azure
    - Faz upload do código
    - Publica na Azure Function
    - Aguarda ficar online
    ↓
[4] Validate
    - Testa a função em produção
    - Verifica se está respondendo
    - Gera relatório
    ↓
✅ Deploy Completo!
```

### **Fazer um Deploy Teste**

1. Faça uma pequena mudança no código (opcional):

```bash
git checkout -b test/deployment-verification
echo "# Teste de deployment" >> README.md
git add README.md
git commit -m "test: deployment verification"
git push origin test/deployment-verification
```

2. Abra um Pull Request:
   - Vá para: https://github.com/brunomalhano/agent-ia-live/pulls
   - Clique em **"Compare & pull request"**
   - Clique em **"Create pull request"**

3. **GitHub Actions vai rodar testes automaticamente** ✅

4. Se os testes passarem, clique em **"Merge pull request"**

5. O deploy será acionado automaticamente para `main`

---

## 📊 Monitorar o Deploy

### **Ver Status dos Workflows**

1. Vá para: https://github.com/brunomalhano/agent-ia-live/actions
2. Você verá os workflows em execução:

```
✓ test-and-build         [Em execução ou Completo]
⏳ deploy                 [Aguardando ou Em execução]
⏸️ deploy (Aprovação)     [Aguardando sua aprovação]
⏳ validate               [Aguardando ou Em execução]
```

### **Aprovar o Deploy (Manual)**

Quando o workflow chegar em **"Review deployments"**:

1. Vá para https://github.com/brunomalhano/agent-ia-live/actions
2. Clique na execução de workflow ativa
3. Procure por **"Review deployments"** (ou **"Aguardando revisão"**)
4. Clique em **"Review deployments"**
5. Selecione **"Approve and deploy"**
6. Clique em **"Approve and deploy"** novamente para confirmar

O deploy começará imediatamente! ✅

### **Monitorar Logs em Tempo Real**

```bash
# Ver logs da Function App no Azure
az functionapp log tail --name guruarchtech --resource-group seu-resource-group

# Ou via Azure Portal:
# 1. Vá para https://portal.azure.com
# 2. Procure por "guruarchtech"
# 3. Vá para "Log Stream"
```

---

## ✅ Validar o Deploy

### **Teste 1: Verificar se a Função Está Online**

```bash
curl -I https://guruarchtech.azurewebsites.net/api/agent
```

Você deve receber:
```
HTTP/1.1 401 Unauthorized
```

(401 significa que a função está online, mas precisa do código de autenticação)

### **Teste 2: Chamar a Função com Parâmetro**

```bash
# Substituir <SEU_CODIGO> pelo código da função
curl -X POST "https://guruarchtech.azurewebsites.net/api/agent?code=<SEU_CODIGO>" \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "Design a scalable microservices architecture for an e-commerce platform with 10M users",
    "critic": false
  }'
```

Resposta esperada:
```json
{
  "status": "success",
  "proposal": "Sua resposta de arquitetura aqui...",
  "execution_time": 2.45
}
```

### **Teste 3: Com Crítica**

```bash
curl -X POST "https://guruarchtech.azurewebsites.net/api/agent?code=<SEU_CODIGO>" \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "Design a scalable microservices architecture for an e-commerce platform with 10M users",
    "critic": true
  }'
```

Resposta esperada:
```json
{
  "status": "success",
  "proposal": "Sua proposta de arquitetura...",
  "critic": "Análise crítica da proposta...",
  "execution_time": 4.23
}
```

### **Teste 4: Ver Logs no Azure Portal**

1. Vá para https://portal.azure.com
2. Procure por **"guruarchtech"** (sua Function App)
3. Vá para **"Monitor"** → **"Logs"**
4. Você verá todos os requests e logs da função

---

## 🔍 Troubleshooting

### **Problema: Deploy Falhou - "Unauthorized"**

**Causa:** Secret `AZURE_CREDENTIALS` inválido ou expirado

**Solução:**

```bash
# Criar novo Service Principal
az ad sp create-for-rbac \
  --name "GitHub-Actions-Deploy-v2" \
  --role contributor \
  --scopes /subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP \
  --json-auth

# Atualizar o secret no GitHub com os novos valores
```

### **Problema: Função Retorna Erro 500**

**Causa:** Variáveis de ambiente não configuradas no Azure Portal

**Solução:**

1. Verificar se as 4 variáveis estão configuradas:
   - `AZURE_OPENAI_API_KEY`
   - `AZURE_OPENAI_ENDPOINT`
   - `AZURE_OPENAI_API_VERSION`
   - `AZURE_OPENAI_DEPLOYMENT`

2. Reiniciar a Function App:

```bash
az functionapp restart --name guruarchtech --resource-group seu-resource-group
```

### **Problema: GitHub Actions Nunca Começa**

**Causa:** Secrets não configurados corretamente

**Solução:**

1. Verificar se todos os 3 secrets obrigatórios existem:
   - `AZURE_CREDENTIALS`
   - `FUNCAPP_NAME`
   - `FUNCAPP_URL`

2. Re-configurar os secrets se necessário

### **Problema: Testes Falharam no GitHub Actions**

**Causa:** Dependências Python não instaladas ou código com erro

**Solução:**

1. Ver logs do teste:
   - Vá para https://github.com/brunomalhano/agent-ia-live/actions
   - Clique na execução falha
   - Vá para **"test-and-build"** → **"Run tests"**

2. Instalar dependências localmente e testar:

```bash
python -m pip install -r requirements.txt
python test_local.py
```

### **Problema: Função Lenta ou Timeout**

**Causa:** Azure OpenAI está lento ou limite de tokens atingido

**Solução:**

1. Verificar se há erro nas variáveis OpenAI:

```bash
# Ver logs
az functionapp log tail --name guruarchtech --resource-group seu-resource-group
```

2. Aumentar o timeout na Function App:
   - Vá para **Configuration** → **Function runtime settings**
   - Aumente **"functionTimeout"** para `"00:10:00"` (10 minutos)

---

## 📝 Resumo dos Passos

✅ **Configuração Inicial (Uma vez)**
- [ ] Instalar ferramentas (Git, Azure CLI, Python, Azure Functions Core Tools)
- [ ] Fazer login no Azure com `az login`
- [ ] Configurar 4 variáveis no Azure Portal

✅ **Configuração GitHub (Uma vez)**
- [ ] Clonar repositório
- [ ] Adicionar 3 secrets no GitHub (AZURE_CREDENTIALS, FUNCAPP_NAME, FUNCAPP_URL)

✅ **Deploy (Automático)**
- [ ] Fazer push para `main` (ou merge do PR)
- [ ] GitHub Actions começa automaticamente
- [ ] Aprovar o deploy manualmente no GitHub
- [ ] Aguardar validação
- [ ] ✅ Deploy completo!

---

## 🆘 Suporte Rápido

| Problema | Comando de Debug |
|----------|------------------|
| Ver variáveis Azure | `az functionapp config appsettings list --name guruarchtech --resource-group seu-resource-group` |
| Ver logs da função | `az functionapp log tail --name guruarchtech --resource-group seu-resource-group` |
| Reiniciar função | `az functionapp restart --name guruarchtech --resource-group seu-resource-group` |
| Ver status do workflow | Vá para https://github.com/brunomalhano/agent-ia-live/actions |
| Testar localmente | `python test_local.py` |

---

## 📚 Recursos Adicionais

- 📖 [Azure Functions Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/)
- 🔐 [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- 🤖 [Azure OpenAI API Reference](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference)
- ⚡ [Azure Functions Python Developer Guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)

---

**Criado em:** Novembro 4, 2025  
**Versão:** 1.0  
**Status:** Production Ready ✅

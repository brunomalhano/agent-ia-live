# 🚀 CI/CD com GitHub Actions - Guia de Configuração

## 📋 Workflows Implementados

### 1. **Test & Build** (`test-and-build.yml`)
Executa em: `push` para `main` ou `develop`, e em `pull_request`

- ✅ Testa em Python 3.10 e 3.11
- ✅ Lint com flake8
- ✅ Verificação de formato com black
- ✅ Executa testes locais (`test_local.py`)
- ✅ Arquiva resultados

### 2. **Deploy Azure Function** (`deploy.yml`)
Executa em: `push` para `main`

- ✅ Build e validação de sintaxe
- ✅ **Requer aprovação manual** (environment: production)
- ✅ Deploy com `func azure functionapp publish`
- ✅ Testes pós-deploy
- ✅ Notificações no Slack

### 3. **Post-Deploy Validation** (`validate.yml`)
Executa em: Após deploy bem-sucedido, ou a cada 6 horas, ou manual

- ✅ Verifica saúde da função (CORS, OPTIONS)
- ✅ Teste com crítica
- ✅ Teste sem crítica
- ✅ Validação de erro (request inválido)
- ✅ Verificação de performance

---

## 🔐 Configurar Secrets no GitHub

### **Passo 1: Acessar Secrets**

1. Vá para seu repositório GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Clique em **New repository secret**

### **Passo 2: Adicionar os Secrets**

Você precisa criar 6 secrets:

#### **1. AZURE_CREDENTIALS** (Necessário para login no Azure)

```bash
# Execute este comando no seu terminal:
az ad sp create-for-rbac \
  --name "GitHub-Actions-guruarchtech" \
  --role contributor \
  --scopes /subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP} \
  --json-auth
```

**Resultado:** Copie todo o JSON e adicione como secret `AZURE_CREDENTIALS`

Ou use o Azure Portal:
- Azure Portal → Azure Active Directory → App registrations → New registration
- Salve o JSON das credentials

#### **2. FUNCAPP_NAME**

```
guruarchtech
```

#### **3. FUNCAPP_URL**

```
https://guruarchtech.azurewebsites.net
```

#### **4. FUNCAPP_CODE**

```
5IyyW9isLIYHW0mwfvqbVxHm0VsRmSViVABU8HIHqSZDAzFu2IEBtQ==
```

#### **5. AZURE_OPENAI_API_KEY**

```
(Sua chave Azure OpenAI)
```

**⚠️ IMPORTANTE:** Esta chave foi exposta! Gere uma nova:

```bash
az cognitiveservices account keys regenerate \
  --name genaihubmalhano \
  --resource-group <RESOURCE_GROUP> \
  --key-name key1
```

#### **6. SLACK_WEBHOOK** (Opcional)

Para notificações no Slack:

1. Vá para: https://api.slack.com/apps
2. Create New App → From scratch
3. Name: "guruarchtech-deploy"
4. Workspace: Selecione seu workspace
5. Features → Incoming Webhooks → Add New Webhook to Workspace
6. Copie a URL (começa com `https://hooks.slack.com/services/...`)

---

## 📝 Resumo dos Secrets

| Secret | Valor | Tipo |
|--------|-------|------|
| `AZURE_CREDENTIALS` | JSON do Service Principal | Necessário |
| `FUNCAPP_NAME` | `guruarchtech` | Necessário |
| `FUNCAPP_URL` | `https://guruarchtech.azurewebsites.net` | Necessário |
| `FUNCAPP_CODE` | Código da função | Necessário |
| `AZURE_OPENAI_API_KEY` | Chave Azure OpenAI | Para testes |
| `AZURE_OPENAI_ENDPOINT` | Endpoint Azure OpenAI | Para testes |
| `SLACK_WEBHOOK` | URL Slack | Opcional |

---

## 🔄 Fluxo de CI/CD

```
1. Push para main (ou PR para main)
   ↓
2. Test & Build dispara
   ├─ Testa em Python 3.10 e 3.11
   ├─ Lint (flake8)
   ├─ Format check (black)
   └─ Testes locais (test_local.py)
   ↓
3. Se tudo OK → Deploy dispara
   ├─ Validação de sintaxe
   ├─ [AGUARDA APROVAÇÃO] 🔒
   ├─ Deploy no Azure
   ├─ Testes pós-deploy
   └─ Notifica Slack ✅
   ↓
4. Validation dispara
   ├─ Health check
   ├─ Teste com crítica
   ├─ Teste sem crítica
   ├─ Validação de erro
   ├─ Performance check
   └─ Notifica Slack
```

---

## ✅ Como Usar

### **1. Fazer Commit e Push**

```bash
git add .github/workflows/
git commit -m "feat: add CI/CD workflows"
git push origin main
```

### **2. Monitorar GitHub Actions**

Vá para: **Actions** no seu repositório GitHub

### **3. Aprovar Deploy**

Quando deploy estiver aguardando aprovação:
1. Clique em **Review deployments** na ação
2. Selecione o environment **production**
3. Clique em **Approve and deploy**

### **4. Receber Notificações no Slack**

Se `SLACK_WEBHOOK` está configurado, você receberá:
- ✅ Notificação quando deploy for bem-sucedido
- ❌ Notificação se deploy falhar
- ✅ Notificação de validações

---

## 🐛 Troubleshooting

### **Erro: "Context access might be invalid"**
Isso é um aviso do linter. Os secrets serão criados automaticamente.

### **Deploy falha com "AZURE_CREDENTIALS not found"**
Verifique se o secret `AZURE_CREDENTIALS` está criado no GitHub.

### **Testes falham localmente mas não no GitHub**
Certifique-se de que os secrets `AZURE_OPENAI_*` estão configurados no GitHub.

### **Deploy aprovado mas não executa**
Verifique se a aprovação foi clicada corretamente em "Review deployments".

---

## 📊 Monitoramento

### Ver logs de uma ação:
1. **Actions** → Clique na ação
2. Clique em **build** ou **deploy**
3. Expanda os steps para ver os logs

### Histórico de deployments:
**Settings** → **Deployments**

---

## 🔒 Segurança

### ✅ Boas Práticas Implementadas:
- ✅ Secrets nunca aparecem nos logs
- ✅ Deploy requer aprovação manual
- ✅ Testes executam antes de deploy
- ✅ Validação pós-deploy
- ✅ Notificações de falha

### ⚠️ Próximas Ações:
1. Revogue a chave Azure OpenAI exposta
2. Gere uma nova chave
3. Atualize o secret no GitHub
4. Resetar histórico Git para remover chave

---

## 📞 Comandos Úteis

```bash
# Criar Service Principal para GitHub Actions
az ad sp create-for-rbac --name "GitHub-Actions-guruarchtech" \
  --role contributor \
  --scopes /subscriptions/{id}/resourceGroups/{rg} \
  --json-auth

# Listar chaves de uma Function App
az functionapp config appsettings list \
  --name guruarchtech \
  --resource-group <RG>

# Revogar chave Azure OpenAI
az cognitiveservices account keys regenerate \
  --name genaihubmalhano \
  --resource-group <RG> \
  --key-name key1
```

---

## 🎯 Próximos Passos

1. ✅ Configure os 6 secrets no GitHub
2. ✅ Faça um push para testar
3. ✅ Aprove o deploy quando aparecer
4. ✅ Monitore o Slack para notificações
5. ✅ Verifique o log de deployments

---

**Status:** ✅ Workflows implementados e prontos para usar!

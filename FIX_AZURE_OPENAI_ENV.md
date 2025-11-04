# 🔧 SOLUÇÃO: Cliente Azure OpenAI Não Inicializado

## ❌ Erro Recebido

```
Exception: ❌ Cliente Azure OpenAI não inicializado
```

## 🔍 Causa

As **variáveis de ambiente não estão configuradas no Azure Portal**. 

No Azure, o arquivo `local.settings.json` NÃO é usado. Você precisa configurar as variáveis diretamente no Azure Portal ou via CLI.

---

## ✅ SOLUÇÃO (escolha uma):

### **Opção 1: Azure Portal (Mais Fácil - GUI)**

1. Abra: https://portal.azure.com
2. Procure: **guruarchtech** (sua Function App)
3. Clique em: **Settings** → **Environment variables** (ou **Configuration**)
4. Clique em: **New application setting**
5. Adicione estas 4 variáveis:

```
AZURE_OPENAI_API_KEY
<SEU_VALOR_NO_GITHUB_SECRETS>

AZURE_OPENAI_ENDPOINT
https://genaihubmalhano.cognitiveservices.azure.com/

AZURE_OPENAI_API_VERSION
2024-12-01-preview

AZURE_OPENAI_DEPLOYMENT
gpt-4.1
```

6. Clique em: **Save**
7. Aguarde alguns segundos para salvar

---

### **Opção 2: Azure CLI (Terminal)**

```bash
# Login no Azure (se necessário)
az login

# Executar script de configuração
bash setup_env_azure.sh
```

Ou manualmente:

```bash
az functionapp config appsettings set \
  --name guruarchtech \
  --resource-group <SEU_RESOURCE_GROUP> \
  --settings \
    AZURE_OPENAI_API_KEY="<SEU_VALOR_AQUI>" \
    AZURE_OPENAI_ENDPOINT="https://genaihubmalhano.cognitiveservices.azure.com/" \
    AZURE_OPENAI_API_VERSION="2024-12-01-preview" \
    AZURE_OPENAI_DEPLOYMENT="gpt-4.1"
```

---

## 🔄 Após Configurar: Reiniciar a Função

### Via Portal
1. Vá para: **Functions** → **agent**
2. Clique em: **Restart**
3. Aguarde alguns segundos

### Via CLI
```bash
az functionapp restart --name guruarchtech --resource-group <RESOURCE_GROUP>
```

---

## 🧪 Teste Após Configurar

```bash
curl -X POST "https://guruarchtech.azurewebsites.net/api/agent?code=<SEU_CODIGO_AQUI>" \
  -H "Content-Type: application/json" \
  -d '{"problem": "Teste", "critic": false}'
```

Resultado esperado:
```json
{
  "ok": true,
  "data": {
    "proposal": "...",
    "critic_review": null
  }
}
```

---

## 🔍 Verificar se as Variáveis Estão Configuradas

```bash
bash check_env_azure.sh
```

Deve exibir as 4 variáveis configuradas.

---

## ⚠️ IMPORTANTE: Segurança

**Sua chave Azure OpenAI foi exposta nos logs!**

### 🚨 Ações necessárias:

1. **Revogar a chave atual:**
   ```bash
   az cognitiveservices account keys regenerate \
     --name genaihubmalhano \
     --resource-group <SEU_RESOURCE_GROUP> \
     --key-name key1
   ```

2. **Obter a nova chave:**
   ```bash
   az cognitiveservices account keys list \
     --name genaihubmalhano \
     --resource-group <SEU_RESOURCE_GROUP>
   ```

3. **Atualizar no Azure Portal** com a nova chave

4. **Resetar o histórico Git** para remover a chave dos logs

---

## 🎯 Checklist

- [ ] Variáveis de ambiente configuradas no Azure Portal
- [ ] Função reiniciada
- [ ] Teste com cURL funcionou (HTTP 200)
- [ ] Logs mostram: `✓ Cliente Azure OpenAI inicializado com sucesso`
- [ ] Chave antiga foi revogada
- [ ] Nova chave foi configurada

---

## 📊 Fluxo de Funcionamento (Correto)

```
1. Requisição chega ao /api/agent
   ↓
2. __init__.py carrega
   ↓
3. agent_logic.py carrega
   ↓
4. Variáveis de ambiente são lidas do Azure Portal
   ✓ AZURE_OPENAI_API_KEY ← Azure Portal
   ✓ AZURE_OPENAI_ENDPOINT ← Azure Portal
   ✓ AZURE_OPENAI_API_VERSION ← Azure Portal
   ✓ AZURE_OPENAI_DEPLOYMENT ← Azure Portal
   ↓
5. Cliente Azure OpenAI é inicializado
   ✓ CLIENT = AzureOpenAI(...)
   ↓
6. Pipeline executa com sucesso
   ↓
7. Response HTTP 200 com proposta
```

---

## ✨ Depois de configurar...

Você verá nos logs do Azure Portal:

```
✓ Azure OpenAI configurado: endpoint=https://..., deployment=gpt-4.1
✓ Cliente Azure OpenAI inicializado com sucesso
→ Executando pipeline: problem=... chars, critic=...
✓ Proposta gerada: ... chars
✓ Crítica gerada: ... chars
```

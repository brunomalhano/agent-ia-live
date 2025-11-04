# 🚀 Guia de Deploy - Agent IA Live

## Status Atual

✅ **Código:** Funcionando perfeitamente localmente  
✅ **Lógica:** Azure OpenAI integrado e testado  
❌ **Azure:** Erro 500 (dependências não instaladas)  

## 🔧 Solução: Deploy com Build Remoto

### Método 1: Via VS Code Extension (Recomendado)

1. **Instale a extensão Azure Functions** (se não tiver)
2. **Clique em Deploy na aba Azure**
3. **VS Code irá:**
   - Empacotar o código
   - Instalar dependências automaticamente
   - Fazer upload para Azure

### Método 2: Via Azure Portal (Web)

1. **Azure Portal** → Sua Function App `guruarchtech`
2. **Deployment Center** → **Source Control**
3. **Conecte seu repositório Git**
4. **Cada push fará deploy automático com build remoto**

### Método 3: Via Azure CLI (Terminal)

```bash
# Instalar Azure CLI (se não tiver)
brew install azure-cli

# Instalar Azure Functions Core Tools
brew tap azure/formulae
brew install azure-functions

# Login no Azure
az login

# Deploy com build remoto (recompila dependências no Azure)
func azure functionapp publish guruarchtech --build remote
```

## 🧪 Teste Após Deploy

### Requisição cURL

```bash
curl -X POST "https://guruarchtech.azurewebsites.net/api/agent?code=5IyyW9isLIYHW0mwfvqbVxHm0VsRmSViVABU8HIHqSZDAzFu2IEBtQ==" \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "Preciso de um chatbot de suporte ao cliente usando IA",
    "critic": true
  }'
```

### Resposta Esperada

```json
{
  "ok": true,
  "data": {
    "proposal": "...",
    "critic_review": "..."
  }
}
```

## 🔍 Verificar Logs no Azure

```bash
# Ver logs em tempo real
az functionapp log tail --name guruarchtech --resource-group <SEU_RESOURCE_GROUP>

# Ou via Azure Portal:
# Functions → agent → Monitor → Logs
```

## 📋 Checklist

- [ ] Código localmente testado ✅
- [ ] `requirements.txt` configurado ✅
- [ ] `.gitignore` protege `local.settings.json` ✅
- [ ] Deploy feito com `--build remote` 🔄
- [ ] Teste POST com cURL retorna 200 ⏳
- [ ] Verificar logs se erro 500 🔄
- [ ] Confirmar resposta com proposta e crítica ✅

## 🐛 Se Ainda Houver Erro 500

1. **Verifique os logs no Azure Portal**
2. **Procure por:** `No module named 'tenacity'` ou `No module named 'openai'`
3. **Se encontrar:** Significa que o `--build remote` não foi usado
4. **Solução:** Delete a Function App e redeploye com `--build remote`

## 📚 Recursos

- [Azure Functions Deployment Guide](https://learn.microsoft.com/en-us/azure/azure-functions/functions-deployment-technologies)
- [Azure Functions Python Developer Guide](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- [Azure OpenAI Integration](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource)

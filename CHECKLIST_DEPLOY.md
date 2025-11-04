# ✅ CHECKLIST - AGENT IA LIVE PRONTO PARA DEPLOY

## 📋 Pré-Deploy

- [x] Código local testado (2/2 testes passando)
- [x] Tratamento de erros implementado
- [x] Logging adicionado em todos os pontos críticos
- [x] Validação de variáveis de ambiente
- [x] CORS configurado
- [x] Documentação atualizada

## 🚀 Deploy

Escolha UMA das opções:

### Opção A: Script Automatizado (Recomendado)
```bash
chmod +x DEPLOY_AGORA.sh
./DEPLOY_AGORA.sh
```

### Opção B: Azure CLI Manual
```bash
az login
func azure functionapp publish guruarchtech --build remote
```

### Opção C: VS Code Extension
1. Instale "Azure Functions" extension
2. Clique em Azure Explorer
3. Selecione sua Function App
4. Clique em "Deploy to Function App"

## ✅ Pós-Deploy

### Validação 1: CORS
```bash
curl -i -X OPTIONS 'https://guruarchtech.azurewebsites.net/api/agent' \
  -H 'Origin: https://portal.azure.com'
```
Resultado esperado:
```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://portal.azure.com
```

### Validação 2: Função
```bash
curl -X POST 'https://guruarchtech.azurewebsites.net/api/agent?code=<SEU_CODIGO_AQUI>' \
  -H 'Content-Type: application/json' \
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

### Validação 3: Azure Portal
1. Vá para Azure Portal
2. Sua Function App → Functions → agent
3. Clique em "Code + Test"
4. Clique em "Test/Run"
5. Adicione body e execute

### Validação 4: Logs
```bash
az functionapp log tail --name guruarchtech --resource-group <SEU_RESOURCE_GROUP>
```
Procure por:
```
✓ Azure OpenAI configurado
✓ Cliente Azure OpenAI inicializado com sucesso
→ Executando pipeline
✓ Proposta gerada
✓ Crítica gerada (se habilitada)
```

## 🐛 Resolução de Problemas

### Erro: "No module named 'tenacity'"
**Causa:** Deploy sem --build remote
**Solução:** Reaplicar deploy com:
```bash
func azure functionapp publish guruarchtech --build remote
```

### Erro: CORS bloqueado
**Causa:** host.json não foi atualizado
**Solução:** Verificar se host.json tem bloco "cors" e redeploy

### Erro: "Invalid API key"
**Causa:** AZURE_OPENAI_API_KEY inválida
**Solução:** Renovar chave no Azure Portal e atualizar no Application Settings

### Erro: Importação de módulo falha
**Causa:** agent_logic.py não encontrado
**Solução:** Verificar se arquivo existe e está no diretório correto

## 📞 Suporte

Se houver problemas:

1. **Verificar logs** via Application Insights
2. **Testar localmente** via `python3 test_local.py`
3. **Validar variáveis** no Azure Portal → Function App → Settings
4. **Consultar documentação** em FIXES_APPLIED.md

## 🎯 Próximos Passos Após Validação

- [ ] Testar em produção
- [ ] Configurar alertas no Application Insights
- [ ] Documentar endpoint para consumidores
- [ ] Criar testes de integração
- [ ] Configurar CI/CD automático

---

**Status:** ✅ PRONTO PARA DEPLOY

**Data:** 2025-11-04

**Versão:** 1.0 - Correções Críticas Implementadas

#!/bin/bash
# Deploy Rápido - Agent IA Live

set -e

echo "🚀 DEPLOY RÁPIDO - Agent IA Live"
echo "=================================="
echo ""

# Verificar se func está disponível
if ! command -v func &> /dev/null; then
    echo "❌ Azure Functions Core Tools não encontrado"
    echo "   Instale com: brew tap azure/formulae && brew install azure-functions"
    exit 1
fi

echo "📝 Confirmando alterações..."
echo "   ✓ agent/__init__.py (tratamento de erros)"
echo "   ✓ agent/agent_logic.py (validação + logging)"
echo "   ✓ host.json (CORS configurado)"
echo ""

read -p "Continuar com o deploy? (S/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    exit 1
fi

echo ""
echo "⏱️  Iniciando deploy... (isso pode levar 2-3 minutos)"
echo ""

# Deploy com build remoto (recompila dependências no Azure)
func azure functionapp publish guruarchtech --build remote

echo ""
echo "✅ Deploy concluído!"
echo ""
echo "📋 Próximas validações:"
echo ""
echo "1. Testar CORS:"
echo "   curl -i -X OPTIONS 'https://guruarchtech.azurewebsites.net/api/agent' \\"
echo "     -H 'Origin: https://portal.azure.com'"
echo ""
echo "2. Testar função:"
echo "   curl -X POST 'https://guruarchtech.azurewebsites.net/api/agent?code=5IyyW9isLIYHW0mwfvqbVxHm0VsRmSViVABU8HIHqSZDAzFu2IEBtQ==' \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"problem\": \"Teste\", \"critic\": false}'"
echo ""
echo "3. Ver logs:"
echo "   az functionapp log tail --name guruarchtech --resource-group <RG>"
echo ""

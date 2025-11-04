#!/bin/bash
# Script para configurar variáveis de ambiente no Azure

set -e

echo "🔧 CONFIGURAR VARIÁVEIS DE AMBIENTE - Azure Function"
echo "═══════════════════════════════════════════════════════════════"
echo ""

FUNCTION_APP_NAME="guruarchtech"

# Tentar obter resource group
RESOURCE_GROUP=$(az group list --query "[0].name" -o tsv 2>/dev/null || echo "")

if [ -z "$RESOURCE_GROUP" ]; then
    echo "❌ Nenhum resource group encontrado"
    echo "   Faça login: az login"
    exit 1
fi

echo "📋 Informações:"
echo "  Function App: $FUNCTION_APP_NAME"
echo "  Resource Group: $RESOURCE_GROUP"
echo ""

# Valores das variáveis
API_KEY="5EMF7QNEFDUQd74x4RCJAGNsoh0ihVNXbUjtK8wH2nhk2gB1F441JQQJ99BKACMsfrFXJ3w3AAAAACOGYwUM"
ENDPOINT="https://genaihubmalhano.cognitiveservices.azure.com/"
API_VERSION="2024-12-01-preview"
DEPLOYMENT="gpt-4.1"

echo "⚠️  AVISO: Você está usando uma chave que foi exposta!"
echo "    Recomendo revogar e gerar uma nova chave no Azure Portal"
echo ""

read -p "Continuar com essa chave? (S/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    exit 1
fi

echo ""
echo "🔄 Configurando variáveis de ambiente..."
echo ""

# Configurar variáveis
az functionapp config appsettings set \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    AZURE_OPENAI_API_KEY="$API_KEY" \
    AZURE_OPENAI_ENDPOINT="$ENDPOINT" \
    AZURE_OPENAI_API_VERSION="$API_VERSION" \
    AZURE_OPENAI_DEPLOYMENT="$DEPLOYMENT"

echo ""
echo "✅ Variáveis configuradas com sucesso!"
echo ""
echo "🔄 Reiniciando a função..."
az functionapp restart \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP

echo ""
echo "✅ Função reiniciada!"
echo ""
echo "🧪 Teste a função com:"
echo ""
echo "curl -X POST 'https://guruarchtech.azurewebsites.net/api/agent?code=...' \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"problem\": \"Teste\", \"critic\": false}'"
echo ""

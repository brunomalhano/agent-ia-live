#!/bin/bash
# Script de Deploy e Teste para Azure Functions

set -e

APP_NAME="guruarchtech"
RESOURCE_GROUP=""

echo "🚀 Agent IA Live - Deploy Script"
echo "=================================="
echo ""

# Verificar se Azure CLI está instalado
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI não encontrado. Instalando..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install azure-cli
    else
        echo "Instale Azure CLI: https://learn.microsoft.com/cli/azure/install-azure-cli"
        exit 1
    fi
fi

# Verificar se func CLI está instalado
if ! command -v func &> /dev/null; then
    echo "❌ Azure Functions Core Tools não encontrado. Instalando..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew tap azure/formulae
        brew install azure-functions
    else
        echo "Instale Azure Functions Core Tools: https://learn.microsoft.com/azure/azure-functions/functions-run-local"
        exit 1
    fi
fi

# Login no Azure
echo "🔐 Fazendo login no Azure..."
az login

# Listar resource groups
echo ""
echo "📦 Selectione seu Resource Group:"
RESOURCE_GROUPS=$(az group list --query "[].name" -o tsv)
select RG in $RESOURCE_GROUPS; do
    RESOURCE_GROUP=$RG
    break
done

echo ""
echo "📋 Informações de Deploy:"
echo "  App: $APP_NAME"
echo "  Resource Group: $RESOURCE_GROUP"
echo ""

# Deploy
read -p "Deseja continuar? (S/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    exit 1
fi

echo ""
echo "📤 Fazendo deploy com build remoto..."
echo "   (Isso pode levar alguns minutos)"
echo ""

func azure functionapp publish $APP_NAME --build remote

echo ""
echo "✅ Deploy concluído!"
echo ""

# Obter a chave da função
echo "🔑 Obtendo chave da função..."
FUNCTION_KEY=$(az functionapp function keys list \
    --name $APP_NAME \
    --function-name agent \
    --resource-group $RESOURCE_GROUP \
    --query "default" -o tsv 2>/dev/null || echo "")

if [ -z "$FUNCTION_KEY" ]; then
    FUNCTION_KEY="SEU_CODIGO_DE_FUNCAO"
    echo "⚠️  Não consegui obter a chave automaticamente."
    echo "   Vá para Azure Portal > Function App > agent > Function Keys"
fi

echo ""
echo "🧪 Testando a função..."
echo ""

RESPONSE=$(curl -s -X POST "https://$APP_NAME.azurewebsites.net/api/agent?code=$FUNCTION_KEY" \
  -H "Content-Type: application/json" \
  -d '{"problem": "Chatbot de suporte usando IA", "critic": true}')

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "https://$APP_NAME.azurewebsites.net/api/agent?code=$FUNCTION_KEY" \
  -H "Content-Type: application/json" \
  -d '{"problem": "Teste", "critic": false}')

echo "HTTP Status: $HTTP_CODE"
echo ""

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ SUCESSO!"
    echo ""
    echo "Resposta (primeiros 500 caracteres):"
    echo "$RESPONSE" | jq '.' 2>/dev/null | head -30
else
    echo "❌ Erro HTTP $HTTP_CODE"
    echo ""
    echo "Verifique os logs:"
    echo "  az functionapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP"
fi

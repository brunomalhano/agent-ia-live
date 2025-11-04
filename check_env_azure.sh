#!/bin/bash
# Script para verificar variáveis de ambiente no Azure

FUNCTION_APP_NAME="guruarchtech"
RESOURCE_GROUP="$(az group list --query "[0].name" -o tsv)"

echo "🔍 Verificando variáveis de ambiente..."
echo "Function App: $FUNCTION_APP_NAME"
echo "Resource Group: $RESOURCE_GROUP"
echo ""

# Listar variáveis de ambiente
az functionapp config appsettings list \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "[?name=='AZURE_OPENAI_API_KEY' || name=='AZURE_OPENAI_ENDPOINT' || name=='AZURE_OPENAI_API_VERSION' || name=='AZURE_OPENAI_DEPLOYMENT']" \
  -o table

echo ""
echo "Se nenhuma linha aparecer acima, as variáveis NÃO estão configuradas!"
echo ""
echo "Configure com:"
echo "  az functionapp config appsettings set \\"
echo "    --name $FUNCTION_APP_NAME \\"
echo "    --resource-group $RESOURCE_GROUP \\"
echo "    --settings AZURE_OPENAI_API_KEY='<sua_chave>'"

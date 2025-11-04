# Agente Generativo Serverless (Azure Functions + Azure OpenAI)

Endpoint HTTP `/api/agent` que aciona um **agente generativo** (planner) com um **critic pass** opcional.
Deploy serverless em **Azure Functions**, logs e traces no **Application Insights**.

## 🔧 Requisitos
- Python 3.10+
- Azure Functions Core Tools
- Azure CLI
- Uma instância do Azure OpenAI com um deployment (ex.: `gpt-4o`)

## 📦 Instalação (local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp local.settings.example.json local.settings.json  # edite com suas chaves
func start
```

Teste:
```bash
curl -X POST "http://localhost:7071/api/agent"   -H "Content-Type: application/json"   -d '{"problem":"Quero um agente que resuma PDFs e gere um parecer executivo.", "critic": true}'
```

## ☁️ Deploy no Azure (exemplo)
```bash
# preencha variáveis e execute
az login
# ...crie RG, SA, Function App...
# depois publique:
func azure functionapp publish <SEU_FUNCTION_APP>
```

Configure app settings (exemplo):
```bash
az functionapp config appsettings set -g <RG> -n <APP> --settings \
  "AZURE_OPENAI_API_KEY=<SUA_CHAVE>" \
  "AZURE_OPENAI_ENDPOINT=https://<seu-endpoint>.openai.azure.com/" \
  "AZURE_OPENAI_API_VERSION=2024-06-01" \
  "AZURE_OPENAI_DEPLOYMENT=gpt-4o"
```

## 🔭 Observabilidade
- Logs via `logging` → **Application Insights**
- Sugestões de métricas: latência, taxa de erro, tokens (customMetrics)

## 🔐 Segurança
- `authLevel=function` por padrão (recomendado usar **API Management**/Front Door)
- Segredos em **Key Vault** (App Settings → Key Vault references)

## 🧭 Estrutura
```
agent-ia-live/
├─ agent/
│  ├─ __init__.py          # HTTP trigger
│  ├─ function.json
│  └─ agent_logic.py       # Agente planner + crítico
├─ requirements.txt
├─ host.json
├─ local.settings.example.json
└─ .github/workflows/deploy.yml
```

import os
import logging
from tenacity import retry, wait_exponential, stop_after_attempt
from openai import AzureOpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Azure OpenAI client configuration
API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1")

# Validar que as variáveis estão configuradas
if not API_KEY:
    logger.error("❌ AZURE_OPENAI_API_KEY não configurada!")
if not ENDPOINT:
    logger.error("❌ AZURE_OPENAI_ENDPOINT não configurada!")

logger.info(f"✓ Azure OpenAI configurado: endpoint={ENDPOINT}, deployment={DEPLOYMENT}")

# Initialize Azure OpenAI client
try:
    CLIENT = AzureOpenAI(
        api_key=API_KEY,
        api_version=API_VERSION,
        azure_endpoint=ENDPOINT,
    )
    logger.info("✓ Cliente Azure OpenAI inicializado com sucesso")
except Exception as e:
    logger.error(f"❌ Erro ao inicializar cliente Azure OpenAI: {e}")
    CLIENT = None

SYSTEM_PROMPT = (
    "Você é um ARQUITETO DE SOLUÇÕES cloud-native especializado em IA generativa e agentes. "
    "Receberá um problema e deve devolver uma proposta clara, objetiva e acionável. "
    "Formato de saída: \n"
    "1) Visão geral (3-5 bullets) \n"
    "2) Arquitetura (componentes e fluxo) \n"
    "3) Padrões cloud-native (resiliência/observabilidade) \n"
    "4) Custos & riscos (resumo) \n"
    "5) Próximos passos (checklist curto) \n"
)

CRITIC_PROMPT = (
    "Atue como um REVISOR ESTRUTURADO. Avalie a resposta do arquiteto e devolva: "
    "(a) pontos fortes (b) lacunas técnicas (c) riscos não cobertos (d) ajustes rápidos."
)

@retry(wait=wait_exponential(multiplier=1, min=1, max=8), stop=stop_after_attempt(3))
def _chat(messages):
    if not CLIENT:
        raise Exception("❌ Cliente Azure OpenAI não inicializado")
    
    logger.info("→ Invocando Azure OpenAI…")
    resp = CLIENT.chat.completions.create(
        model=DEPLOYMENT,
        messages=messages,
        temperature=0.2,
        max_completion_tokens=900,
    )
    return resp.choices[0].message.content.strip()

def generate_architecture_advice(problem: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Problema: {problem}"}
    ]
    return _chat(messages)

def critic_review(architecture_answer: str) -> str:
    messages = [
        {"role": "system", "content": CRITIC_PROMPT},
        {"role": "user", "content": architecture_answer}
    ]
    return _chat(messages)

def run_agent_pipeline(problem: str, enable_critic: bool = True) -> dict:
    logger.info(f"→ Executando pipeline: problem={len(problem)} chars, critic={enable_critic}")
    proposal = generate_architecture_advice(problem)
    logger.info(f"✓ Proposta gerada: {len(proposal)} chars")
    
    review = None
    if enable_critic:
        review = critic_review(proposal)
        logger.info(f"✓ Crítica gerada: {len(review)} chars")
    
    return {"proposal": proposal, "critic_review": review}

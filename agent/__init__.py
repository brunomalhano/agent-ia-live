import json
import logging
import azure.functions as func
import sys
import os

# Garantir que o diretório atual está no path
sys.path.insert(0, os.path.dirname(__file__))

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("HTTP trigger /agent recebido.")
    
    try:
        # Importar aqui (lazy import) para detectar erros mais cedo
        import agent_logic
    except ImportError as e:
        logging.error(f"Erro ao importar agent_logic: {e}", exc_info=True)
        return func.HttpResponse(
            json.dumps({"error": f"Erro ao carregar módulo: {str(e)}"}, ensure_ascii=False),
            status_code=500,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Erro geral na importação: {e}", exc_info=True)
        return func.HttpResponse(
            json.dumps({"error": f"Erro ao carregar: {str(e)}"}, ensure_ascii=False),
            status_code=500,
            mimetype="application/json"
        )

    try:
        body = req.get_json()
    except Exception as e:
        logging.error(f"Erro ao parsear JSON: {e}")
        return func.HttpResponse(
            json.dumps({"error": "Body inválido. Envie JSON { 'problem': '...', 'critic': true/false }"}, ensure_ascii=False),
            status_code=400,
            mimetype="application/json"
        )

    problem = body.get("problem")
    critic = bool(body.get("critic", True))

    if not problem or not isinstance(problem, str) or len(problem) < 8:
        return func.HttpResponse(
            json.dumps({"error": "Campo 'problem' é obrigatório (string com descrição do caso)."}, ensure_ascii=False),
            status_code=400,
            mimetype="application/json"
        )

    try:
        result = agent_logic.run_agent_pipeline(problem=problem, enable_critic=critic)
        
        logging.info("Problem length=%s critic=%s", len(problem), critic)
        logging.info("Proposal size=%s", len(result.get("proposal") or ""))

        return func.HttpResponse(
            json.dumps({"ok": True, "data": result}, ensure_ascii=False),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Erro ao executar pipeline: {e}", exc_info=True)
        return func.HttpResponse(
            json.dumps({"error": f"Erro ao processar: {str(e)}"}, ensure_ascii=False),
            status_code=500,
            mimetype="application/json"
        )

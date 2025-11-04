#!/usr/bin/env python3
"""
Script para testar a aplicação localmente sem Azure Functions CLI
"""
import os
import sys
import json
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Adicionar o diretório do agent ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent'))

# Carregar variáveis de ambiente do local.settings.json
def load_settings():
    """Carrega settings do arquivo local.settings.json"""
    settings_path = os.path.join(os.path.dirname(__file__), 'local.settings.json')
    
    if not os.path.exists(settings_path):
        logger.error(f"❌ Arquivo {settings_path} não encontrado!")
        sys.exit(1)
    
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    
    # Configurar variáveis de ambiente
    for key, value in settings.get('Values', {}).items():
        os.environ[key] = value
        if 'KEY' in key or 'PASSWORD' in key or 'TOKEN' in key:
            logger.info(f"✓ {key} = ***")
        else:
            logger.info(f"✓ {key} = {value}")
    
    return settings

# Importar após configurar as variáveis de ambiente
def import_agent_module():
    """Importa o módulo agent após carregar settings"""
    try:
        import agent_logic
        return agent_logic
    except Exception as e:
        logger.error(f"❌ Erro ao importar agent_logic: {e}")
        sys.exit(1)

def test_agent():
    """Testa o agente com um exemplo"""
    logger.info("\n" + "="*60)
    logger.info("🚀 INICIANDO TESTE LOCAL DO AGENTE")
    logger.info("="*60 + "\n")
    
    # Carregar settings
    logger.info("📁 Carregando configurações...")
    load_settings()
    
    # Importar agent_logic
    logger.info("\n📦 Importando módulos...")
    agent_logic = import_agent_module()
    
    # Teste 1: Problema simples
    logger.info("\n" + "-"*60)
    logger.info("📝 TESTE 1: Problema Simples (com crítica)")
    logger.info("-"*60)
    
    problem1 = "Preciso de um chatbot de suporte ao cliente usando IA"
    
    logger.info(f"\nProblema: {problem1}\n")
    
    try:
        result = agent_logic.run_agent_pipeline(problem=problem1, enable_critic=True)
        
        logger.info("\n✅ RESPOSTA DO AGENTE:")
        logger.info("-" * 40)
        print("\n[PROPOSTA]")
        print(result.get("proposal", "Sem proposta"))
        
        if result.get("critic_review"):
            print("\n[CRÍTICA]")
            print(result.get("critic_review", "Sem crítica"))
        
        logger.info("-" * 40)
        
    except Exception as e:
        logger.error(f"❌ Erro no teste 1: {e}", exc_info=True)
        return False
    
    # Teste 2: Problema complexo
    logger.info("\n" + "-"*60)
    logger.info("📝 TESTE 2: Problema Complexo (sem crítica)")
    logger.info("-"*60)
    
    problem2 = "Arquitetura serverless para processamento em tempo real de logs com 100k eventos/min"
    
    logger.info(f"\nProblema: {problem2}\n")
    
    try:
        result = agent_logic.run_agent_pipeline(problem=problem2, enable_critic=False)
        
        logger.info("\n✅ RESPOSTA DO AGENTE:")
        logger.info("-" * 40)
        print("\n[PROPOSTA]")
        print(result.get("proposal", "Sem proposta"))
        logger.info("-" * 40)
        
    except Exception as e:
        logger.error(f"❌ Erro no teste 2: {e}", exc_info=True)
        return False
    
    logger.info("\n" + "="*60)
    logger.info("✨ TESTES CONCLUÍDOS COM SUCESSO!")
    logger.info("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    success = test_agent()
    sys.exit(0 if success else 1)

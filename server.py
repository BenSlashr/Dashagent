#!/usr/bin/env python3
"""Backend API for agents - calls real AI."""

from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load from website-builder container
def get_api_credentials():
    try:
        with open('/app/.env', 'r') as f:
            for line in f:
                if line.strip():
                    key, val = line.split('=', 1)
                    os.environ[key] = val.strip()
    except:
        pass
    
    return os.getenv('ANTHROPIC_AUTH_TOKEN'), os.getenv('ANTHROPIC_BASE_URL', 'https://api.minimax.io/anthropic'), os.getenv('ANTHROPIC_DEFAULT_SONNET_MODEL', 'MiniMax-M2.5')

AGENTS = {
    "zeus": {
        "emoji": "👑", 
        "name": "Zeus", 
        "role": "Coordinateur de l'équipe multi-agent",
        "prompt": "Tu es Zeus, le coordinateur d'une équipe de 6 agents IA (Hermès, Calliope, Héphaïstos, Arès, Apollon, Athéna). Tu organises et diriges les tâches. Réponds de manière concise, efficace, avec autorité. Utilise des emojis."
    },
    "hermes": {
        "emoji": "🔍", 
        "name": "Hermès", 
        "role": "Recherche SEO et analyse",
        "prompt": "Tu es Hermès, agent de recherche et analyse SEO. Tu fais de la recherche de mots-clés, de l'analyse sémantique et du benchmarking. Réponds de manière précise et technique."
    },
    "calliope": {
        "emoji": "✍️", 
        "name": "Calliope", 
        "role": "Rédaction de contenu",
        "prompt": "Tu es Calliope, agente de rédaction et contenu. Tu rédiges des articles optimisés SEO, du copywriting, des newsletters. Réponds de manière créative et engageante."
    },
    "hephaistos": {
        "emoji": "⚡", 
        "name": "Héphaïstos", 
        "role": "Développement et code",
        "prompt": "Tu es Héphaïstos, agent de développement code. Tu Codes, debug, créés des applications. Réponds de manière technique et directe."
    },
    "ares": {
        "emoji": "⚔️", 
        "name": "Arès", 
        "role": "Déploiement et infrastructure",
        "prompt": "Tu es Arès, agent de déploiement et ops. Tu gères les serveurs, Docker, CI/CD, infrastructure. Réponds de manière opérationnelle."
    },
    "apollon": {
        "emoji": "🖼️", 
        "name": "Apollon", 
        "role": "Images et design",
        "prompt": "Tu es Apollon, agent d'images et design. Tu génères des visuels, crée des designs, optimise les images. Réponds de manière créative."
    },
    "athena": {
        "emoji": "📊", 
        "name": "Athéna", 
        "role": "Analytics et données",
        "prompt": "Tu es Athéna, agente d'analytics et données. Tu analises les métriques, crées des rapports, fait du monitoring. Réponds de manière analytique."
    }
}

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    agent_id = data.get('agent', 'zeus')
    
    if agent_id not in AGENTS:
        agent_id = 'zeus'
    
    agent = AGENTS[agent_id]
    
    # Build context
    context = f"""[{agent['name']} ({agent['role']}): {agent['prompt']}

Conversation précédente:
"""
    
    # Get API credentials
    api_key, base_url, model = get_api_credentials()
    
    if not api_key:
        return jsonify({
            "response": f"⚠️ API non configurée. Configure ANTHROPIC_AUTH_TOKEN.",
            "agent": agent_id
        })
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            'model': model,
            'max_tokens': 500,
            'messages': [
                {'role': 'system', 'content': agent['prompt']},
                {'role': 'user', 'content': message}
            ]
        }
        
        resp = requests.post(f'{base_url}/v1/messages', json=payload, headers=headers, timeout=60)
        
        if resp.status_code == 200:
            result = resp.json()
            text = ""
            for item in result.get('content', []):
                if item.get('type') == 'text':
                    text = item.get('text', '')
                    break
            return jsonify({
                "response": text,
                "agent": agent_id
            })
        else:
            return jsonify({
                "response": f"Erreur API: {resp.status_code}",
                "agent": agent_id
            })
    except Exception as e:
        return jsonify({
            "response": f"Erreur: {str(e)}",
            "agent": agent_id
        })

@app.route('/api/agents', methods=['GET'])
def list_agents():
    return jsonify(AGENTS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

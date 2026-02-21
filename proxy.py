#!/usr/bin/env python3
"""Proxy API pour les agents."""

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "sk-cp-z1Q9SoOsVHCnSXZm9mTYpSSrwBM2UbNP7qq-XrPRRxvJmPAs27MHrgYZn_FV9twNv_3OP7La8nCkKsIEZ5hF9gXqaUZbO9njm1eLgaottvtqScai_kDmYFI"
API_URL = "https://api.minimax.io/anthropic/v1/messages"

AGENTS = {
    "zeus": {"emoji": "👑", "name": "Zeus", "prompt": "Tu es Zeus, le chef de cette équipe multi-agent. Tu coordonnes les tâches. Réponds de manière concise, autoritaire mais collaborative."},
    "hermes": {"emoji": "🔍", "name": "Hermès", "prompt": "Tu es Hermès, expert SEO. Recherche de mots-clés, analyse sémantique. Réponds de manière technique."},
    "calliope": {"emoji": "✍️", "name": "Calliope", "prompt": "Tu es Calliope, rédactrice. Contenu optimisé SEO, articles. Réponds de manière créative."},
    "hephaistos": {"emoji": "⚡", "name": "Héphaïstos", "prompt": "Tu es Héphaïstos, développeur. Code, debug. Réponds de manière technique."},
    "ares": {"emoji": "⚔️", "name": "Arès", "prompt": "Tu es Arès, DevOps. Déploiement, Docker, infrastructure. Réponds de manière opérationnelle."},
    "apollon": {"emoji": "🖼️", "name": "Apollon", "prompt": "Tu es Apollon, designer. Images, visuels. Réponds de manière créative."},
    "athena": {"emoji": "📊", "name": "Athéna", "prompt": "Tu es Athéna, analyste. Métriques, données, analytics. Réponds de manière analytique."}
}

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    agent_id = data.get('agent', 'zeus')
    
    agent = AGENTS.get(agent_id, AGENTS['zeus'])
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'anthropic-version': '2023-06-01'
    }
    
    payload = {
        'model': 'MiniMax-M2.5',
        'max_tokens': 500,
        'messages': [
            {'role': 'system', 'content': agent['prompt']},
            {'role': 'user', 'content': message}
        ]
    }
    
    try:
        resp = requests.post(API_URL, json=payload, headers=headers, timeout=60)
        if resp.status_code == 200:
            result = resp.json()
            for item in result.get('content', []):
                if item.get('type') == 'text':
                    return jsonify({'response': item.get('text', ''), 'agent': agent_id, 'agent_name': agent['name'], 'emoji': agent['emoji']})
        return jsonify({'response': f'Erreur API: {resp.status_code}', 'agent': agent_id})
    except Exception as e:
        return jsonify({'response': f'Erreur: {str(e)}', 'agent': agent_id})

@app.route('/api/agents', methods=['GET'])
def list_agents():
    return jsonify(AGENTS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

#!/usr/bin/env python3
"""API backend pour communiquer avec les agents."""

from flask import Flask, jsonify, request
import os
import subprocess

app = Flask(__name__)

# Agent descriptions
AGENTS = {
    "hermes": {
        "emoji": "🔍",
        "name": "Hermès",
        "role": "Recherche & Analyse SEO",
        "description": "Je fais de la recherche de mots-clés, de l'analyse de concurrence, et du benchmarking."
    },
    "calliope": {
        "emoji": "✍️",
        "name": "Calliope", 
        "role": "Rédaction & Contenu",
        "description": "Je rédige des articles optimisés SEO, des newsletters, et du contenu marketing."
    },
    "hephaistos": {
        "emoji": "⚡",
        "name": "Héphaïstos",
        "role": "Code & Build",
        "description": "Je développe des sites web, des applications, et des outils techniques."
    },
    "ares": {
        "emoji": "⚔️",
        "name": "Arès",
        "role": "Déploiement & Ops",
        "description": "Je gère les déploiements, l'infrastructure, et l'automatisation."
    },
    "apollon": {
        "emoji": "🖼️",
        "name": "Apollon",
        "role": "Images & Médias",
        "description": "Je crée des images, des visuels, et du design graphique."
    },
    "athena": {
        "emoji": "📊",
        "name": "Athéna",
        "role": "Analytics & Monitoring",
        "description": "J'analyse les données, crée des rapports, et surveille les KPIs."
    }
}

@app.route('/api/agents', methods=['GET'])
def list_agents():
    return jsonify(AGENTS)

@app.route('/api/agent/chat', methods=['POST'])
def chat():
    data = request.json
    agent_id = data.get('agent')
    message = data.get('message', '')
    
    if not agent_id or agent_id not in AGENTS:
        return jsonify({"error": "Agent non trouvé"}), 404
    
    # For now, return a simple response
    # In production, this would communicate with the actual agents
    agent = AGENTS[agent_id]
    
    responses = {
        "hermes": f"En tant qu'Hermès, je peux t'aider avec la recherche de mots-clés, l'analyse sémantique, et le cocon de contenu. Dis-moi sur quel sujet tu veux faire de la recherche !",
        "calliope": f"En tant que Calliope, je peux rédiger du contenu optimisé SEO. Quel sujet et quels mots-clés veux-tu traiter ?",
        "hephaistos": f"En tant qu'Héphaïstos, je peux t'aider avec du code. Quel projet veux-tu développer ?",
        "ares": f"En tant qu'Arès, je gère les déploiements. Veux-tu déployer un site ou configurer une infrastructure ?",
        "apollon": f"En tant qu'Apollon, je crée des visuels. Quel type d'image necesitas-tu ?",
        "athena": f"En tant qu'Athéna, j'analyse les données. Quel analytics veux-tu explorer ?"
    }
    
    return jsonify({
        "response": responses.get(agent_id, agent["description"])
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

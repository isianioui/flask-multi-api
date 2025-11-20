"""
Orchestration API - Système de Coordination
Agrège et coordonne les données de tous les organes simulés
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime
from typing import Dict, Any, List
import time

app = Flask(__name__)
CORS(app)

# Configuration des APIs d'organes
ORGAN_APIS = {
    "cardiac": {
        "url": "http://localhost:5001",
        "name": "Système Cardiovasculaire",
        "health_endpoint": "/health"
    },
    "respiratory": {
        "url": "http://localhost:5002",
        "name": "Système Respiratoire",
        "health_endpoint": "/health"
    },
    "neural": {
        "url": "http://localhost:5003",
        "name": "Système Nerveux Central",
        "health_endpoint": "/health"
    }
}

class OrchestrationManager:
    """Gestionnaire de l'orchestration des APIs d'organes"""
    
    def __init__(self):
        self.timeout = 5  # secondes
        
    def check_api_health(self, organ: str) -> Dict[str, Any]:
        """Vérifie la santé d'une API d'organe"""
        if organ not in ORGAN_APIS:
            return {"status": "unknown", "error": "Unknown organ"}
        
        try:
            api_config = ORGAN_APIS[organ]
            url = f"{api_config['url']}{api_config['health_endpoint']}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "response_time": response.elapsed.total_seconds(),
                    "data": response.json()
                }
            else:
                return {
                    "status": "unhealthy",
                    "error": f"Status code: {response.status_code}"
                }
        except requests.exceptions.Timeout:
            return {"status": "timeout", "error": "Request timeout"}
        except requests.exceptions.ConnectionError:
            return {"status": "offline", "error": "Cannot connect to API"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_all_health_status(self) -> Dict[str, Any]:
        """Vérifie la santé de toutes les APIs"""
        health_status = {}
        for organ in ORGAN_APIS.keys():
            health_status[organ] = self.check_api_health(organ)
        
        # Calculer le statut général
        all_healthy = all(
            status.get("status") == "healthy" 
            for status in health_status.values()
        )
        
        return {
            "overall_status": "healthy" if all_healthy else "degraded",
            "timestamp": datetime.now().isoformat(),
            "organs": health_status
        }
    
    def get_organ_status(self, organ: str) -> Dict[str, Any]:
        """Récupère le statut d'un organe spécifique"""
        if organ not in ORGAN_APIS:
            return {"error": "Unknown organ"}
        
        try:
            api_config = ORGAN_APIS[organ]
            url = f"{api_config['url']}/api/{organ}/status"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status code: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_organ_data(self, organ: str, count: int = 1) -> Dict[str, Any]:
        """Récupère les données d'un organe spécifique"""
        if organ not in ORGAN_APIS:
            return {"error": "Unknown organ"}
        
        try:
            api_config = ORGAN_APIS[organ]
            url = f"{api_config['url']}/api/{organ}/data"
            params = {"count": count}
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status code: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_all_organ_data(self, count: int = 1) -> Dict[str, Any]:
        """Récupère les données de tous les organes"""
        all_data = {
            "timestamp": datetime.now().isoformat(),
            "data_count": count,
            "organs": {}
        }
        
        for organ in ORGAN_APIS.keys():
            all_data["organs"][organ] = self.get_organ_data(organ, count)
        
        return all_data
    
    def simulate_condition(self, organ: str, condition: str) -> Dict[str, Any]:
        """Simule une condition sur un organe spécifique"""
        if organ not in ORGAN_APIS:
            return {"error": "Unknown organ"}
        
        try:
            api_config = ORGAN_APIS[organ]
            url = f"{api_config['url']}/api/{organ}/simulate/{condition}"
            response = requests.post(url, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status code: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def simulate_multiple_conditions(self, conditions: Dict[str, str]) -> Dict[str, Any]:
        """Simule plusieurs conditions sur différents organes"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "simulations": {}
        }
        
        for organ, condition in conditions.items():
            results["simulations"][organ] = self.simulate_condition(organ, condition)
        
        return results
    
    def update_organ_parameters(self, organ: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Met à jour les paramètres d'un organe"""
        if organ not in ORGAN_APIS:
            return {"error": "Unknown organ"}
        
        try:
            api_config = ORGAN_APIS[organ]
            url = f"{api_config['url']}/api/{organ}/parameters"
            response = requests.post(url, json=params, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status code: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def update_all_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Met à jour les paramètres de tous les organes"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "updates": {}
        }
        
        for organ in ORGAN_APIS.keys():
            results["updates"][organ] = self.update_organ_parameters(organ, params)
        
        return results
    
    def get_system_overview(self) -> Dict[str, Any]:
        """Obtient une vue d'ensemble du système"""
        overview = {
            "timestamp": datetime.now().isoformat(),
            "system_health": self.get_all_health_status(),
            "organ_statuses": {}
        }
        
        for organ in ORGAN_APIS.keys():
            overview["organ_statuses"][organ] = self.get_organ_status(organ)
        
        return overview

# Instance globale du gestionnaire
manager = OrchestrationManager()

# Routes API
@app.route('/')
def index():
    """Page d'accueil de l'API d'orchestration"""
    return jsonify({
        "api": "Orchestration API",
        "version": "1.0.0",
        "description": "API centralisée de coordination des systèmes d'organes",
        "available_organs": list(ORGAN_APIS.keys()),
        "endpoints": {
            "health": "/api/orchestration/health",
            "overview": "/api/orchestration/overview",
            "all_data": "/api/orchestration/data/all",
            "organ_data": "/api/orchestration/data/<organ>",
            "simulate": "/api/orchestration/simulate",
            "parameters": "/api/orchestration/parameters"
        }
    })

@app.route('/api/orchestration/health', methods=['GET'])
def check_health():
    """GET /api/orchestration/health - Vérifie la santé de tous les systèmes"""
    try:
        health_status = manager.get_all_health_status()
        return jsonify(health_status), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orchestration/overview', methods=['GET'])
def get_overview():
    """GET /api/orchestration/overview - Vue d'ensemble complète du système"""
    try:
        overview = manager.get_system_overview()
        return jsonify(overview), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orchestration/data/all', methods=['GET'])
def get_all_data():
    """GET /api/orchestration/data/all - Données de tous les organes"""
    try:
        count = request.args.get('count', default=1, type=int)
        count = min(count, 100)
        
        all_data = manager.get_all_organ_data(count)
        return jsonify(all_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orchestration/data/<organ>', methods=['GET'])
def get_organ_data(organ):
    """GET /api/orchestration/data/<organ> - Données d'un organe spécifique"""
    try:
        count = request.args.get('count', default=1, type=int)
        count = min(count, 100)
        
        data = manager.get_organ_data(organ, count)
        
        if "error" in data:
            return jsonify(data), 404
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orchestration/status/<organ>', methods=['GET'])
def get_organ_status(organ):
    """GET /api/orchestration/status/<organ> - Statut d'un organe spécifique"""
    try:
        status = manager.get_organ_status(organ)
        
        if "error" in status:
            return jsonify(status), 404
        return jsonify(status), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orchestration/simulate', methods=['POST'])
def simulate_conditions():
    """POST /api/orchestration/simulate - Simule des conditions sur un ou plusieurs organes"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Format: {"organ": "condition"} ou {"cardiac": "tachycardia", "respiratory": "asthma"}
        if isinstance(data, dict):
            results = manager.simulate_multiple_conditions(data)
            return jsonify(results), 200
        else:
            return jsonify({"error": "Invalid data format"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orchestration/simulate/<organ>/<condition>', methods=['POST'])
def simulate_single_condition(organ, condition):
    """POST /api/orchestration/simulate/<organ>/<condition> - Simule une condition sur un organe"""
    try:
        result = manager.simulate_condition(organ, condition)
        
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orchestration/parameters', methods=['POST'])
def update_parameters():
    """POST /api/orchestration/parameters - Met à jour les paramètres de tous les organes"""
    try:
        params = request.get_json()
        
        if not params:
            return jsonify({"error": "No parameters provided"}), 400
        
        results = manager.update_all_parameters(params)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orchestration/parameters/<organ>', methods=['POST'])
def update_organ_parameters(organ):
    """POST /api/orchestration/parameters/<organ> - Met à jour les paramètres d'un organe"""
    try:
        params = request.get_json()
        
        if not params:
            return jsonify({"error": "No parameters provided"}), 400
        
        result = manager.update_organ_parameters(organ, params)
        
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orchestration/organs', methods=['GET'])
def list_organs():
    """GET /api/orchestration/organs - Liste tous les organes disponibles"""
    return jsonify({
        "organs": ORGAN_APIS,
        "count": len(ORGAN_APIS)
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check de l'orchestrateur lui-même"""
    return jsonify({
        "status": "healthy",
        "service": "orchestration",
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏥 ORCHESTRATION API - Système de Coordination")
    print("="*60)
    print("\nDémarrage de l'API d'orchestration...")
    print("\n⚠️  IMPORTANT: Assurez-vous que les APIs suivantes sont démarrées:")
    for organ, config in ORGAN_APIS.items():
        print(f"  - {config['name']} ({organ}): {config['url']}")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
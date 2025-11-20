"""
Respiratory API - Système Respiratoire
Simulation du fonctionnement pulmonaire avec génération de données synthétiques
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import time
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, Any, List

app = Flask(__name__)
CORS(app)

@dataclass
class RespiratoryData:
    """Modèle de données respiratoires"""
    timestamp: str
    respiratory_rate: int  # respirations/minute
    tidal_volume: int  # mL
    vital_capacity: int  # mL
    pao2: float  # mmHg - Pression artérielle en oxygène
    paco2: float  # mmHg - Pression artérielle en CO2
    ph: float  # pH sanguin
    oxygen_saturation: float  # %
    status: str

class RespiratorySimulator:
    """Simulateur du système respiratoire"""
    
    def __init__(self):
        self.age = 35
        self.sex = "M"
        self.activity_level = "normal"
        self.condition = "normal"
        
        # Valeurs physiologiques de référence
        self.base_rr = 16  # respirations/min
        self.base_tv = 500  # mL
        self.base_vc = 4800  # mL
        self.base_pao2 = 95  # mmHg
        self.base_paco2 = 40  # mmHg
        self.base_ph = 7.40
        self.base_spo2 = 98
        
    def set_parameters(self, age: int = None, sex: str = None, 
                      activity_level: str = None):
        """Configure les paramètres du patient simulé"""
        if age: self.age = age
        if sex: self.sex = sex
        if activity_level: self.activity_level = activity_level
        
    def _apply_age_factor(self, value: float, param_type: str) -> float:
        """Applique un facteur d'âge aux valeurs"""
        if param_type == "capacity":
            # La capacité diminue avec l'âge
            age_factor = 1 - (self.age - 35) * 0.008
        else:
            age_factor = 1 - (self.age - 35) * 0.002
        return value * age_factor
    
    def _apply_sex_factor(self, value: float, param_type: str) -> float:
        """Applique un facteur de sexe"""
        if self.sex == "F" and param_type == "capacity":
            return value * 0.85  # Les femmes ont généralement une capacité plus faible
        return value
    
    def _apply_activity_factor(self, value: float, param_type: str) -> float:
        """Applique un facteur d'activité"""
        activity_factors = {
            "resting": 0.7,
            "normal": 1.0,
            "light_exercise": 1.5,
            "intense_exercise": 2.2
        }
        factor = activity_factors.get(self.activity_level, 1.0)
        
        if param_type == "rate":
            return value * factor
        elif param_type == "volume":
            return value * (1 + (factor - 1) * 0.5)
        return value
    
    def _add_natural_variation(self, value: float, variation_percent: float = 0.05) -> float:
        """Ajoute une variation naturelle aux données"""
        variation = value * variation_percent
        return value + random.uniform(-variation, variation)
    
    def generate_normal_data(self) -> RespiratoryData:
        """Génère des données respiratoires normales"""
        # Fréquence respiratoire
        rr = self.base_rr
        rr = self._apply_activity_factor(rr, "rate")
        rr = self._add_natural_variation(rr, 0.1)
        rr = int(max(12, min(25, rr)))
        
        # Volume courant
        tv = self.base_tv
        tv = self._apply_activity_factor(tv, "volume")
        tv = self._add_natural_variation(tv, 0.08)
        tv = int(max(350, min(750, tv)))
        
        # Capacité vitale
        vc = self.base_vc
        vc = self._apply_age_factor(vc, "capacity")
        vc = self._apply_sex_factor(vc, "capacity")
        vc = self._add_natural_variation(vc, 0.05)
        vc = int(max(3000, min(6000, vc)))
        
        # Gaz du sang
        pao2 = self._add_natural_variation(self.base_pao2, 0.03)
        pao2 = round(max(80, min(100, pao2)), 1)
        
        paco2 = self._add_natural_variation(self.base_paco2, 0.05)
        paco2 = round(max(35, min(45, paco2)), 1)
        
        ph = self._add_natural_variation(self.base_ph, 0.01)
        ph = round(max(7.35, min(7.45, ph)), 2)
        
        spo2 = self._add_natural_variation(self.base_spo2, 0.02)
        spo2 = round(max(95, min(100, spo2)), 1)
        
        return RespiratoryData(
            timestamp=datetime.now().isoformat(),
            respiratory_rate=rr,
            tidal_volume=tv,
            vital_capacity=vc,
            pao2=pao2,
            paco2=paco2,
            ph=ph,
            oxygen_saturation=spo2,
            status="healthy"
        )
    
    def simulate_asthma(self) -> RespiratoryData:
        """Simule une crise d'asthme"""
        self.condition = "asthma"
        data = self.generate_normal_data()
        
        # Augmentation de la fréquence, diminution des volumes
        data.respiratory_rate = random.randint(25, 35)
        data.tidal_volume = random.randint(300, 400)
        data.vital_capacity = int(data.vital_capacity * 0.7)
        data.oxygen_saturation = round(random.uniform(88, 94), 1)
        data.pao2 = round(random.uniform(70, 85), 1)
        data.status = "abnormal"
        
        return data
    
    def simulate_copd(self) -> RespiratoryData:
        """Simule une BPCO (Bronchopneumopathie Chronique Obstructive)"""
        self.condition = "copd"
        data = self.generate_normal_data()
        
        # Diminution de la capacité, rétention de CO2
        data.respiratory_rate = random.randint(22, 30)
        data.vital_capacity = int(data.vital_capacity * 0.6)
        data.tidal_volume = random.randint(350, 450)
        data.oxygen_saturation = round(random.uniform(85, 92), 1)
        data.pao2 = round(random.uniform(60, 75), 1)
        data.paco2 = round(random.uniform(45, 55), 1)
        data.ph = round(random.uniform(7.32, 7.38), 2)
        data.status = "abnormal"
        
        return data
    
    def simulate_hyperventilation(self) -> RespiratoryData:
        """Simule une hyperventilation"""
        self.condition = "hyperventilation"
        data = self.generate_normal_data()
        
        # Augmentation excessive de la fréquence respiratoire
        data.respiratory_rate = random.randint(30, 45)
        data.tidal_volume = random.randint(600, 800)
        data.paco2 = round(random.uniform(25, 33), 1)
        data.ph = round(random.uniform(7.45, 7.55), 2)  # Alcalose
        data.status = "abnormal"
        
        return data
    
    def simulate_apnea(self) -> RespiratoryData:
        """Simule une apnée"""
        self.condition = "apnea"
        data = self.generate_normal_data()
        
        # Arrêt ou forte diminution de la respiration
        data.respiratory_rate = random.randint(0, 8)
        data.tidal_volume = random.randint(100, 300)
        data.oxygen_saturation = round(random.uniform(75, 88), 1)
        data.pao2 = round(random.uniform(50, 70), 1)
        data.paco2 = round(random.uniform(48, 60), 1)
        data.ph = round(random.uniform(7.28, 7.35), 2)  # Acidose
        data.status = "critical"
        
        return data
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut actuel du système respiratoire"""
        data = self.generate_normal_data()
        
        return {
            "organ": "lungs",
            "status": "operational",
            "condition": self.condition,
            "current_data": asdict(data),
            "patient_info": {
                "age": self.age,
                "sex": self.sex,
                "activity_level": self.activity_level
            }
        }

# Instance globale du simulateur
simulator = RespiratorySimulator()

# Routes API
@app.route('/')
def index():
    """Page d'accueil de l'API"""
    return jsonify({
        "api": "Respiratory API",
        "version": "1.0.0",
        "description": "API de simulation du système respiratoire",
        "endpoints": {
            "status": "/api/respiratory/status",
            "data": "/api/respiratory/data",
            "simulate": "/api/respiratory/simulate/<condition>",
            "parameters": "/api/respiratory/parameters"
        }
    })

@app.route('/api/respiratory/status', methods=['GET'])
def get_status():
    """GET /api/respiratory/status - Statut du système respiratoire"""
    try:
        status = simulator.get_status()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/respiratory/data', methods=['GET'])
def get_data():
    """GET /api/respiratory/data - Données synthétiques courantes"""
    try:
        count = request.args.get('count', default=1, type=int)
        count = min(count, 100)
        
        data_points = []
        for _ in range(count):
            if simulator.condition == "normal":
                data = simulator.generate_normal_data()
            elif simulator.condition == "asthma":
                data = simulator.simulate_asthma()
            elif simulator.condition == "copd":
                data = simulator.simulate_copd()
            elif simulator.condition == "hyperventilation":
                data = simulator.simulate_hyperventilation()
            elif simulator.condition == "apnea":
                data = simulator.simulate_apnea()
            else:
                data = simulator.generate_normal_data()
                
            data_points.append(asdict(data))
            time.sleep(0.01)
        
        return jsonify({
            "organ": "lungs",
            "count": len(data_points),
            "data": data_points if count > 1 else data_points[0]
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/respiratory/simulate/<condition>', methods=['POST'])
def simulate_condition(condition):
    """POST /api/respiratory/simulate/<condition> - Simulation de pathologie"""
    try:
        valid_conditions = ["asthma", "copd", "hyperventilation", "apnea", "normal"]
        
        if condition not in valid_conditions:
            return jsonify({
                "error": "Invalid condition",
                "valid_conditions": valid_conditions
            }), 400
        
        simulator.condition = condition
        
        if condition == "normal":
            data = simulator.generate_normal_data()
        elif condition == "asthma":
            data = simulator.simulate_asthma()
        elif condition == "copd":
            data = simulator.simulate_copd()
        elif condition == "hyperventilation":
            data = simulator.simulate_hyperventilation()
        elif condition == "apnea":
            data = simulator.simulate_apnea()
        
        return jsonify({
            "message": f"Condition '{condition}' activated",
            "current_data": asdict(data)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/respiratory/parameters', methods=['GET', 'POST'])
def manage_parameters():
    """GET/POST /api/respiratory/parameters - Gestion des paramètres"""
    if request.method == 'GET':
        return jsonify({
            "current_parameters": {
                "age": simulator.age,
                "sex": simulator.sex,
                "activity_level": simulator.activity_level,
                "condition": simulator.condition
            },
            "available_parameters": {
                "age": "integer (0-120)",
                "sex": ["M", "F"],
                "activity_level": ["resting", "normal", "light_exercise", "intense_exercise"],
                "condition": ["normal", "asthma", "copd", "hyperventilation", "apnea"]
            }
        }), 200
    
    elif request.method == 'POST':
        try:
            params = request.get_json()
            
            if 'age' in params:
                simulator.age = max(0, min(120, int(params['age'])))
            if 'sex' in params:
                if params['sex'] in ['M', 'F']:
                    simulator.sex = params['sex']
            if 'activity_level' in params:
                valid_levels = ["resting", "normal", "light_exercise", "intense_exercise"]
                if params['activity_level'] in valid_levels:
                    simulator.activity_level = params['activity_level']
            
            return jsonify({
                "message": "Parameters updated",
                "current_parameters": {
                    "age": simulator.age,
                    "sex": simulator.sex,
                    "activity_level": simulator.activity_level,
                    "condition": simulator.condition
                }
            }), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 400

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "organ": "respiratory",
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
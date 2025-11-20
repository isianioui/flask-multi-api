

from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import time
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, Any, List
import math

app = Flask(__name__)
CORS(app)

@dataclass
class CardiacData:
    """Modèle de données cardiaques"""
    timestamp: str
    heart_rate: int  # bpm
    systolic_pressure: int  # mmHg
    diastolic_pressure: int  # mmHg
    oxygen_saturation: float  # %
    cardiac_output: float  # L/min
    rhythm: str
    status: str

class CardiacSimulator:
    """Simulateur du système cardiovasculaire"""
    
    def __init__(self):
        self.age = 35
        self.sex = "M"
        self.activity_level = "normal"
        self.condition = "normal"
        
        # Valeurs physiologiques de référence
        self.base_hr = 70
        self.base_systolic = 120
        self.base_diastolic = 80
        self.base_spo2 = 98
        
    def set_parameters(self, age: int = None, sex: str = None, 
                      activity_level: str = None):
        """Configure les paramètres du patient simulé"""
        if age: self.age = age
        if sex: self.sex = sex
        if activity_level: self.activity_level = activity_level
        
    def _apply_age_factor(self, value: float, is_pressure: bool = False) -> float:
        """Applique un facteur d'âge aux valeurs"""
        if is_pressure:
            # La pression augmente avec l'âge
            age_factor = 1 + (self.age - 35) * 0.005
        else:
            # La fréquence cardiaque diminue légèrement avec l'âge
            age_factor = 1 - (self.age - 35) * 0.002
        return value * age_factor
    
    def _apply_activity_factor(self, value: float, param_type: str) -> float:
        """Applique un facteur d'activité"""
        activity_factors = {
            "resting": 0.8,
            "normal": 1.0,
            "light_exercise": 1.3,
            "intense_exercise": 1.8
        }
        factor = activity_factors.get(self.activity_level, 1.0)
        
        if param_type == "heart_rate":
            return value * factor
        elif param_type == "pressure":
            return value * (1 + (factor - 1) * 0.3)
        return value
    
    def _add_natural_variation(self, value: float, variation_percent: float = 0.05) -> float:
        """Ajoute une variation naturelle aux données"""
        variation = value * variation_percent
        return value + random.uniform(-variation, variation)
    
    def generate_normal_data(self) -> CardiacData:
        """Génère des données cardiaques normales"""
        # Calcul de la fréquence cardiaque
        hr = self.base_hr
        hr = self._apply_age_factor(hr)
        hr = self._apply_activity_factor(hr, "heart_rate")
        hr = self._add_natural_variation(hr, 0.08)
        hr = int(max(50, min(100, hr)))
        
        # Calcul de la pression artérielle
        systolic = self._apply_age_factor(self.base_systolic, True)
        systolic = self._apply_activity_factor(systolic, "pressure")
        systolic = self._add_natural_variation(systolic, 0.05)
        systolic = int(max(90, min(140, systolic)))
        
        diastolic = self._apply_age_factor(self.base_diastolic, True)
        diastolic = self._apply_activity_factor(diastolic, "pressure")
        diastolic = self._add_natural_variation(diastolic, 0.05)
        diastolic = int(max(60, min(90, diastolic)))
        
        # Saturation en oxygène
        spo2 = self._add_natural_variation(self.base_spo2, 0.02)
        spo2 = round(max(95, min(100, spo2)), 1)
        
        # Débit cardiaque (L/min) = Volume d'éjection × Fréquence cardiaque / 1000
        stroke_volume = 70  # mL
        cardiac_output = (stroke_volume * hr) / 1000
        cardiac_output = round(cardiac_output, 2)
        
        return CardiacData(
            timestamp=datetime.now().isoformat(),
            heart_rate=hr,
            systolic_pressure=systolic,
            diastolic_pressure=diastolic,
            oxygen_saturation=spo2,
            cardiac_output=cardiac_output,
            rhythm="normal",
            status="healthy"
        )
    
    def simulate_tachycardia(self) -> CardiacData:
        """Simule une tachycardie"""
        self.condition = "tachycardia"
        data = self.generate_normal_data()
        
        # Augmentation significative de la fréquence cardiaque
        data.heart_rate = random.randint(110, 150)
        data.cardiac_output = round((70 * data.heart_rate) / 1000, 2)
        data.rhythm = "tachycardia"
        data.status = "abnormal"
        
        return data
    
    def simulate_bradycardia(self) -> CardiacData:
        """Simule une bradycardie"""
        self.condition = "bradycardia"
        data = self.generate_normal_data()
        
        # Diminution de la fréquence cardiaque
        data.heart_rate = random.randint(40, 55)
        data.cardiac_output = round((70 * data.heart_rate) / 1000, 2)
        data.rhythm = "bradycardia"
        data.status = "abnormal"
        
        return data
    
    def simulate_arrhythmia(self) -> CardiacData:
        """Simule une arythmie"""
        self.condition = "arrhythmia"
        data = self.generate_normal_data()
        
        # Fréquence cardiaque irrégulière
        data.heart_rate = random.randint(60, 120)
        data.rhythm = "irregular"
        data.status = "abnormal"
        
        return data
    
    def simulate_hypertension(self) -> CardiacData:
        """Simule une hypertension"""
        self.condition = "hypertension"
        data = self.generate_normal_data()
        
        # Augmentation de la pression artérielle
        data.systolic_pressure = random.randint(145, 180)
        data.diastolic_pressure = random.randint(95, 110)
        data.status = "abnormal"
        
        return data
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut actuel du système cardiaque"""
        data = self.generate_normal_data()
        
        return {
            "organ": "heart",
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
simulator = CardiacSimulator()

# Routes API
@app.route('/')
def index():
    """Page d'accueil de l'API"""
    return jsonify({
        "api": "Cardiac API",
        "version": "1.0.0",
        "description": "API de simulation du système cardiovasculaire",
        "endpoints": {
            "status": "/api/cardiac/status",
            "data": "/api/cardiac/data",
            "simulate": "/api/cardiac/simulate/<condition>",
            "parameters": "/api/cardiac/parameters"
        }
    })

@app.route('/api/cardiac/status', methods=['GET'])
def get_status():
    """GET /api/cardiac/status - Statut du système cardiaque"""
    try:
        status = simulator.get_status()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cardiac/data', methods=['GET'])
def get_data():
    """GET /api/cardiac/data - Données synthétiques courantes"""
    try:
        # Récupération des paramètres de requête optionnels
        count = request.args.get('count', default=1, type=int)
        count = min(count, 100)  # Limite maximale
        
        data_points = []
        for _ in range(count):
            if simulator.condition == "normal":
                data = simulator.generate_normal_data()
            elif simulator.condition == "tachycardia":
                data = simulator.simulate_tachycardia()
            elif simulator.condition == "bradycardia":
                data = simulator.simulate_bradycardia()
            elif simulator.condition == "arrhythmia":
                data = simulator.simulate_arrhythmia()
            elif simulator.condition == "hypertension":
                data = simulator.simulate_hypertension()
            else:
                data = simulator.generate_normal_data()
                
            data_points.append(asdict(data))
            time.sleep(0.01)  # Petite pause entre les mesures
        
        return jsonify({
            "organ": "heart",
            "count": len(data_points),
            "data": data_points if count > 1 else data_points[0]
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cardiac/simulate/<condition>', methods=['POST'])
def simulate_condition(condition):
    """POST /api/cardiac/simulate/<condition> - Simulation de pathologie"""
    try:
        valid_conditions = ["tachycardia", "bradycardia", "arrhythmia", 
                          "hypertension", "normal"]
        
        if condition not in valid_conditions:
            return jsonify({
                "error": "Invalid condition",
                "valid_conditions": valid_conditions
            }), 400
        
        simulator.condition = condition
        
        # Génère des données selon la condition
        if condition == "normal":
            data = simulator.generate_normal_data()
        elif condition == "tachycardia":
            data = simulator.simulate_tachycardia()
        elif condition == "bradycardia":
            data = simulator.simulate_bradycardia()
        elif condition == "arrhythmia":
            data = simulator.simulate_arrhythmia()
        elif condition == "hypertension":
            data = simulator.simulate_hypertension()
        
        return jsonify({
            "message": f"Condition '{condition}' activated",
            "current_data": asdict(data)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cardiac/parameters', methods=['GET', 'POST'])
def manage_parameters():
    """GET/POST /api/cardiac/parameters - Gestion des paramètres de simulation"""
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
                "condition": ["normal", "tachycardia", "bradycardia", "arrhythmia", "hypertension"]
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
    """Health check endpoint pour l'orchestrateur"""
    return jsonify({
        "status": "healthy",
        "organ": "cardiac",
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
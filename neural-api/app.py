"""
Neural API - Système Nerveux Central
Simulation de l'activité cérébrale avec génération de données synthétiques
"""

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
class NeuralData:
    """Modèle de données neurologiques"""
    timestamp: str
    eeg_alpha: float  # 8-13 Hz - Relaxation éveillée
    eeg_beta: float  # 13-30 Hz - Activité mentale
    eeg_theta: float  # 4-8 Hz - Somnolence
    eeg_delta: float  # 0.5-4 Hz - Sommeil profond
    brain_activity_level: float  # 0-100%
    dopamine: float  # µg/dL
    serotonin: float  # ng/mL
    norepinephrine: float  # pg/mL
    reaction_time: int  # ms
    cortical_activity: str
    status: str

class NeuralSimulator:
    """Simulateur du système nerveux central"""
    
    def __init__(self):
        self.age = 35
        self.sex = "M"
        self.mental_state = "alert"
        self.condition = "normal"
        
        # Valeurs de référence
        self.base_dopamine = 0.04  # µg/dL
        self.base_serotonin = 150  # ng/mL
        self.base_norepinephrine = 200  # pg/mL
        self.base_reaction_time = 250  # ms
        
    def _calculate_eeg_waves(self) -> tuple:
        """Calcule les ondes EEG selon l'état mental"""
        if self.mental_state == "alert":
            alpha = random.uniform(20, 40)
            beta = random.uniform(50, 70)
            theta = random.uniform(10, 20)
            delta = random.uniform(5, 10)
        elif self.mental_state == "relaxed":
            alpha = random.uniform(50, 70)
            beta = random.uniform(20, 35)
            theta = random.uniform(15, 25)
            delta = random.uniform(5, 15)
        elif self.mental_state == "drowsy":
            alpha = random.uniform(15, 30)
            beta = random.uniform(10, 20)
            theta = random.uniform(45, 65)
            delta = random.uniform(15, 25)
        elif self.mental_state == "sleeping":
            alpha = random.uniform(5, 15)
            beta = random.uniform(5, 10)
            theta = random.uniform(25, 35)
            delta = random.uniform(55, 75)
        else:  # stressed
            alpha = random.uniform(15, 25)
            beta = random.uniform(60, 85)
            theta = random.uniform(10, 15)
            delta = random.uniform(5, 10)
        
        # Normaliser à 100%
        total = alpha + beta + theta + delta
        return (
            round(alpha / total * 100, 1),
            round(beta / total * 100, 1),
            round(theta / total * 100, 1),
            round(delta / total * 100, 1)
        )
    
    def _calculate_brain_activity(self) -> float:
        """Calcule le niveau d'activité cérébrale"""
        activity_levels = {
            "alert": random.uniform(75, 95),
            "relaxed": random.uniform(55, 75),
            "drowsy": random.uniform(35, 55),
            "sleeping": random.uniform(15, 35),
            "stressed": random.uniform(80, 100)
        }
        return round(activity_levels.get(self.mental_state, 70), 1)
    
    def _add_natural_variation(self, value: float, variation_percent: float = 0.1) -> float:
        """Ajoute une variation naturelle"""
        variation = value * variation_percent
        return value + random.uniform(-variation, variation)
    
    def generate_normal_data(self) -> NeuralData:
        """Génère des données neurologiques normales"""
        # Ondes EEG
        alpha, beta, theta, delta = self._calculate_eeg_waves()
        
        # Niveau d'activité cérébrale
        brain_activity = self._calculate_brain_activity()
        
        # Neurotransmetteurs
        dopamine = self._add_natural_variation(self.base_dopamine, 0.15)
        dopamine = round(max(0.02, min(0.08, dopamine)), 3)
        
        serotonin = self._add_natural_variation(self.base_serotonin, 0.12)
        serotonin = round(max(100, min(250, serotonin)), 1)
        
        norepinephrine = self._add_natural_variation(self.base_norepinephrine, 0.15)
        norepinephrine = round(max(150, min(300, norepinephrine)), 1)
        
        # Temps de réaction
        rt = self._add_natural_variation(self.base_reaction_time, 0.15)
        rt = int(max(150, min(400, rt)))
        
        # Activité corticale
        cortical_activities = {
            "alert": "high",
            "relaxed": "moderate",
            "drowsy": "low",
            "sleeping": "minimal",
            "stressed": "very_high"
        }
        cortical = cortical_activities.get(self.mental_state, "moderate")
        
        return NeuralData(
            timestamp=datetime.now().isoformat(),
            eeg_alpha=alpha,
            eeg_beta=beta,
            eeg_theta=theta,
            eeg_delta=delta,
            brain_activity_level=brain_activity,
            dopamine=dopamine,
            serotonin=serotonin,
            norepinephrine=norepinephrine,
            reaction_time=rt,
            cortical_activity=cortical,
            status="healthy"
        )
    
    def simulate_epilepsy(self) -> NeuralData:
        """Simule une crise d'épilepsie"""
        self.condition = "epilepsy"
        data = self.generate_normal_data()
        
        # Activité électrique anormale
        data.eeg_beta = random.uniform(70, 90)
        data.eeg_alpha = random.uniform(5, 15)
        data.eeg_theta = random.uniform(5, 10)
        data.eeg_delta = random.uniform(5, 10)
        data.brain_activity_level = random.uniform(95, 100)
        data.cortical_activity = "seizure"
        data.reaction_time = random.randint(500, 1000)
        data.status = "critical"
        
        return data
    
    def simulate_migraine(self) -> NeuralData:
        """Simule une migraine"""
        self.condition = "migraine"
        data = self.generate_normal_data()
        
        # Activation corticale anormale
        data.brain_activity_level = random.uniform(85, 98)
        data.serotonin = random.uniform(80, 110)  # Baisse de sérotonine
        data.norepinephrine = random.uniform(250, 350)
        data.cortical_activity = "hyperactive"
        data.reaction_time = random.randint(350, 500)
        data.status = "abnormal"
        
        return data
    
    def simulate_sleep_disorder(self) -> NeuralData:
        """Simule un trouble du sommeil"""
        self.condition = "sleep_disorder"
        data = self.generate_normal_data()
        
        # Ondes de sommeil perturbées
        data.eeg_alpha = random.uniform(30, 45)
        data.eeg_beta = random.uniform(25, 40)
        data.eeg_theta = random.uniform(15, 25)
        data.eeg_delta = random.uniform(10, 20)
        data.brain_activity_level = random.uniform(50, 70)
        data.cortical_activity = "irregular"
        data.serotonin = random.uniform(100, 130)
        data.status = "abnormal"
        
        return data
    
    def simulate_stress(self) -> NeuralData:
        """Simule un état de stress"""
        self.condition = "stress"
        self.mental_state = "stressed"
        data = self.generate_normal_data()
        
        # Augmentation de l'activité et des hormones de stress
        data.brain_activity_level = random.uniform(85, 100)
        data.norepinephrine = random.uniform(300, 450)
        data.dopamine = random.uniform(0.05, 0.09)
        data.cortical_activity = "very_high"
        data.reaction_time = random.randint(180, 250)
        data.status = "abnormal"
        
        return data
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut actuel du système nerveux"""
        data = self.generate_normal_data()
        
        return {
            "organ": "brain",
            "status": "operational",
            "condition": self.condition,
            "mental_state": self.mental_state,
            "current_data": asdict(data),
            "patient_info": {
                "age": self.age,
                "sex": self.sex,
                "mental_state": self.mental_state
            }
        }

# Instance globale du simulateur
simulator = NeuralSimulator()

# Routes API
@app.route('/')
def index():
    """Page d'accueil de l'API"""
    return jsonify({
        "api": "Neural API",
        "version": "1.0.0",
        "description": "API de simulation du système nerveux central",
        "endpoints": {
            "status": "/api/neural/status",
            "data": "/api/neural/data",
            "simulate": "/api/neural/simulate/<condition>",
            "parameters": "/api/neural/parameters"
        }
    })

@app.route('/api/neural/status', methods=['GET'])
def get_status():
    """GET /api/neural/status - Statut du système nerveux"""
    try:
        status = simulator.get_status()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/neural/data', methods=['GET'])
def get_data():
    """GET /api/neural/data - Données synthétiques courantes"""
    try:
        count = request.args.get('count', default=1, type=int)
        count = min(count, 100)
        
        data_points = []
        for _ in range(count):
            if simulator.condition == "normal":
                data = simulator.generate_normal_data()
            elif simulator.condition == "epilepsy":
                data = simulator.simulate_epilepsy()
            elif simulator.condition == "migraine":
                data = simulator.simulate_migraine()
            elif simulator.condition == "sleep_disorder":
                data = simulator.simulate_sleep_disorder()
            elif simulator.condition == "stress":
                data = simulator.simulate_stress()
            else:
                data = simulator.generate_normal_data()
                
            data_points.append(asdict(data))
            time.sleep(0.01)
        
        return jsonify({
            "organ": "brain",
            "count": len(data_points),
            "data": data_points if count > 1 else data_points[0]
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/neural/simulate/<condition>', methods=['POST'])
def simulate_condition(condition):
    """POST /api/neural/simulate/<condition> - Simulation de pathologie"""
    try:
        valid_conditions = ["epilepsy", "migraine", "sleep_disorder", "stress", "normal"]
        
        if condition not in valid_conditions:
            return jsonify({
                "error": "Invalid condition",
                "valid_conditions": valid_conditions
            }), 400
        
        simulator.condition = condition
        
        if condition == "normal":
            simulator.mental_state = "alert"
            data = simulator.generate_normal_data()
        elif condition == "epilepsy":
            data = simulator.simulate_epilepsy()
        elif condition == "migraine":
            data = simulator.simulate_migraine()
        elif condition == "sleep_disorder":
            data = simulator.simulate_sleep_disorder()
        elif condition == "stress":
            data = simulator.simulate_stress()
        
        return jsonify({
            "message": f"Condition '{condition}' activated",
            "current_data": asdict(data)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/neural/parameters', methods=['GET', 'POST'])
def manage_parameters():
    """GET/POST /api/neural/parameters - Gestion des paramètres"""
    if request.method == 'GET':
        return jsonify({
            "current_parameters": {
                "age": simulator.age,
                "sex": simulator.sex,
                "mental_state": simulator.mental_state,
                "condition": simulator.condition
            },
            "available_parameters": {
                "age": "integer (0-120)",
                "sex": ["M", "F"],
                "mental_state": ["alert", "relaxed", "drowsy", "sleeping", "stressed"],
                "condition": ["normal", "epilepsy", "migraine", "sleep_disorder", "stress"]
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
            if 'mental_state' in params:
                valid_states = ["alert", "relaxed", "drowsy", "sleeping", "stressed"]
                if params['mental_state'] in valid_states:
                    simulator.mental_state = params['mental_state']
            
            return jsonify({
                "message": "Parameters updated",
                "current_parameters": {
                    "age": simulator.age,
                    "sex": simulator.sex,
                    "mental_state": simulator.mental_state,
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
        "organ": "neural",
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
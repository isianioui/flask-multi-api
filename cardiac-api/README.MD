# Cardiac API - Système Cardiovasculaire

## Description
API Flask de simulation du système cardiovasculaire avec génération de données médicales synthétiques réalistes.

## Fonctionnalités
- Génération de données cardiaques synthétiques (fréquence cardiaque, pression artérielle, saturation en oxygène)
- Simulation de conditions pathologiques (tachycardie, bradycardie, arythmie, hypertension)
- Paramétrage du patient (âge, sexe, niveau d'activité)
- Variation naturelle des données physiologiques

## Installation

### Prérequis
- Python 3.8 ou supérieur
- pip

### Étapes d'installation

1. Créer un environnement virtuel :
```bash
python -m venv venv
```

2. Activer l'environnement virtuel :
- Windows : `venv\Scripts\activate`
- Linux/Mac : `source venv/bin/activate`

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Démarrage

Lancer l'API :
```bash
python app.py
```

L'API sera accessible sur : `http://localhost:5001`

## Endpoints

### 1. Page d'accueil
```
GET /
```
Retourne les informations sur l'API et la liste des endpoints disponibles.

### 2. Statut du système cardiaque
```
GET /api/cardiac/status
```
Retourne le statut actuel du système cardiaque et les informations du patient.

**Réponse exemple :**
```json
{
  "organ": "heart",
  "status": "operational",
  "condition": "normal",
  "current_data": {
    "timestamp": "2025-11-19T10:30:00",
    "heart_rate": 72,
    "systolic_pressure": 120,
    "diastolic_pressure": 80,
    "oxygen_saturation": 98.2,
    "cardiac_output": 5.04,
    "rhythm": "normal",
    "status": "healthy"
  },
  "patient_info": {
    "age": 35,
    "sex": "M",
    "activity_level": "normal"
  }
}
```

### 3. Données synthétiques courantes
```
GET /api/cardiac/data?count=1
```
Génère des données cardiaques synthétiques.

**Paramètres de requête :**
- `count` (optionnel) : Nombre de points de données à générer (1-100, défaut: 1)

**Réponse exemple :**
```json
{
  "organ": "heart",
  "count": 1,
  "data": {
    "timestamp": "2025-11-19T10:30:00",
    "heart_rate": 75,
    "systolic_pressure": 122,
    "diastolic_pressure": 78,
    "oxygen_saturation": 97.8,
    "cardiac_output": 5.25,
    "rhythm": "normal",
    "status": "healthy"
  }
}
```

### 4. Simulation de pathologie
```
POST /api/cardiac/simulate/<condition>
```
Active une condition pathologique spécifique.

**Conditions disponibles :**
- `normal` : Fonctionnement normal
- `tachycardia` : Fréquence cardiaque élevée (>100 bpm)
- `bradycardia` : Fréquence cardiaque basse (<60 bpm)
- `arrhythmia` : Rythme cardiaque irrégulier
- `hypertension` : Pression artérielle élevée

**Exemple :**
```bash
curl -X POST http://localhost:5001/api/cardiac/simulate/tachycardia
```

**Réponse exemple :**
```json
{
  "message": "Condition 'tachycardia' activated",
  "current_data": {
    "timestamp": "2025-11-19T10:30:00",
    "heart_rate": 125,
    "systolic_pressure": 130,
    "diastolic_pressure": 85,
    "oxygen_saturation": 96.5,
    "cardiac_output": 8.75,
    "rhythm": "tachycardia",
    "status": "abnormal"
  }
}
```

### 5. Gestion des paramètres
```
GET /api/cardiac/parameters
POST /api/cardiac/parameters
```

**GET** - Récupère les paramètres actuels et disponibles.

**POST** - Modifie les paramètres de simulation.

**Corps de la requête (POST) :**
```json
{
  "age": 45,
  "sex": "F",
  "activity_level": "light_exercise"
}
```

**Paramètres disponibles :**
- `age` : 0-120 ans
- `sex` : "M" ou "F"
- `activity_level` : "resting", "normal", "light_exercise", "intense_exercise"

### 6. Health Check
```
GET /health
```
Endpoint de vérification de santé pour l'orchestrateur.

## Données Générées

### Valeurs Physiologiques Normales
- **Fréquence cardiaque** : 60-100 bpm
- **Pression systolique** : 90-140 mmHg
- **Pression diastolique** : 60-90 mmHg
- **Saturation en oxygène** : 95-100%
- **Débit cardiaque** : 4-8 L/min

### Facteurs d'Influence
Les données générées prennent en compte :
- L'âge du patient (impact sur la pression artérielle et la fréquence cardiaque)
- Le sexe
- Le niveau d'activité physique
- Les conditions pathologiques activées
- Une variation naturelle physiologique

## Exemples d'Utilisation

### Python
```python
import requests

# Récupérer le statut
response = requests.get('http://localhost:5001/api/cardiac/status')
print(response.json())

# Simuler une tachycardie
response = requests.post('http://localhost:5001/api/cardiac/simulate/tachycardia')
print(response.json())

# Modifier les paramètres
params = {"age": 60, "activity_level": "resting"}
response = requests.post('http://localhost:5001/api/cardiac/parameters', json=params)
print(response.json())

# Récupérer des données
response = requests.get('http://localhost:5001/api/cardiac/data?count=5')
print(response.json())
```

### cURL
```bash
# Statut
curl http://localhost:5001/api/cardiac/status

# Données
curl http://localhost:5001/api/cardiac/data?count=3

# Simulation
curl -X POST http://localhost:5001/api/cardiac/simulate/hypertension

# Paramètres
curl -X POST http://localhost:5001/api/cardiac/parameters \
  -H "Content-Type: application/json" \
  -d '{"age": 50, "sex": "F"}'
```

## Structure du Code

```
cardiac-api/
├── app.py              # Application Flask principale
├── requirements.txt    # Dépendances Python
└── README.md          # Cette documentation
```

## Aspects Techniques

### Classes Principales
- **CardiacData** : Dataclass représentant les données cardiaques
- **CardiacSimulator** : Classe de simulation du système cardiovasculaire

### Méthodes de Simulation
- `generate_normal_data()` : Génère des données normales
- `simulate_tachycardia()` : Simule une tachycardie
- `simulate_bradycardia()` : Simule une bradycardie
- `simulate_arrhythmia()` : Simule une arythmie
- `simulate_hypertension()` : Simule une hypertension

### Gestion des Erreurs
- Validation des paramètres d'entrée
- Codes de réponse HTTP appropriés
- Messages d'erreur descriptifs

## Tests

### Test Manuel avec curl
```bash
# Test de base
curl http://localhost:5001/

# Test du statut
curl http://localhost:5001/api/cardiac/status

# Test de génération de données
curl http://localhost:5001/api/cardiac/data

# Test de simulation
curl -X POST http://localhost:5001/api/cardiac/simulate/tachycardia
```

### Test avec Postman
Importer la collection et tester tous les endpoints avec différents paramètres.

## Considérations Éthiques

⚠️ **IMPORTANT** : Cette API génère des données **SYNTHÉTIQUES** à des fins **PÉDAGOGIQUES** uniquement.

- Les données ne sont PAS basées sur de vrais patients
- Ne JAMAIS utiliser pour des diagnostics médicaux réels
- Usage strictement éducatif et de formation
- Aucune donnée personnelle de santé réelle n'est utilisée

## Port par Défaut
Port : **5001**

## Auteur
Projet pédagogique - Développement d'APIs Flask

## Licence
Usage éducatif uniquement
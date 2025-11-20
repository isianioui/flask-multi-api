# Orchestration API - Système de Coordination

## Description
API centralisée qui orchestre et coordonne toutes les APIs d'organes. Elle permet l'agrégation des données, la surveillance globale et la coordination des simulations.

## Installation
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Configuration

### Prérequis
Avant de démarrer l'orchestrateur, **TOUTES** les APIs d'organes doivent être lancées :
- Cardiac API (port 5001)
- Respiratory API (port 5002)
- Neural API (port 5003)

### Démarrage
```bash
python app.py
```
Port : **5000**

## Endpoints

### 1. Vue d'ensemble du système
```
GET /api/orchestration/overview
```
Retourne une vue complète incluant l'état de santé et le statut de tous les organes.

**Réponse exemple :**
```json
{
  "timestamp": "2025-11-19T10:30:00",
  "system_health": {
    "overall_status": "healthy",
    "organs": {
      "cardiac": {"status": "healthy"},
      "respiratory": {"status": "healthy"},
      "neural": {"status": "healthy"}
    }
  },
  "organ_statuses": {
    "cardiac": {...},
    "respiratory": {...},
    "neural": {...}
  }
}
```

### 2. Vérification de santé
```
GET /api/orchestration/health
```
Vérifie l'état de santé de toutes les APIs d'organes.

### 3. Données agrégées
```
GET /api/orchestration/data/all?count=1
```
Récupère les données de tous les organes en une seule requête.

**Paramètres :**
- `count` : Nombre de points de données (1-100)

### 4. Données d'un organe spécifique
```
GET /api/orchestration/data/<organ>?count=1
```
Récupère les données d'un organe via l'orchestrateur.

**Organes disponibles :** `cardiac`, `respiratory`, `neural`

### 5. Statut d'un organe
```
GET /api/orchestration/status/<organ>
```
Récupère le statut détaillé d'un organe spécifique.

### 6. Simulation de conditions
```
POST /api/orchestration/simulate
```
Simule des conditions sur un ou plusieurs organes simultanément.

**Corps de la requête :**
```json
{
  "cardiac": "tachycardia",
  "respiratory": "asthma",
  "neural": "stress"
}
```

**Alternative - Simulation sur un seul organe :**
```
POST /api/orchestration/simulate/<organ>/<condition>
```

### 7. Mise à jour des paramètres
```
POST /api/orchestration/parameters
```
Met à jour les paramètres de tous les organes en une fois.

**Corps de la requête :**
```json
{
  "age": 45,
  "sex": "F",
  "activity_level": "light_exercise"
}
```

**Alternative - Paramètres d'un seul organe :**
```
POST /api/orchestration/parameters/<organ>
```

### 8. Liste des organes
```
GET /api/orchestration/organs
```
Retourne la liste de tous les organes disponibles avec leurs configurations.

## Exemples d'Utilisation

### Python

```python
import requests
import json

BASE_URL = "http://localhost:5000"

# 1. Vérifier la santé du système
health = requests.get(f"{BASE_URL}/api/orchestration/health")
print(json.dumps(health.json(), indent=2))

# 2. Vue d'ensemble complète
overview = requests.get(f"{BASE_URL}/api/orchestration/overview")
print(json.dumps(overview.json(), indent=2))

# 3. Récupérer toutes les données
all_data = requests.get(f"{BASE_URL}/api/orchestration/data/all?count=1")
print(json.dumps(all_data.json(), indent=2))

# 4. Simuler plusieurs conditions simultanément
simulations = {
    "cardiac": "tachycardia",
    "respiratory": "asthma",
    "neural": "stress"
}
response = requests.post(
    f"{BASE_URL}/api/orchestration/simulate",
    json=simulations
)
print(json.dumps(response.json(), indent=2))

# 5. Mettre à jour les paramètres globaux
params = {
    "age": 50,
    "sex": "M",
    "activity_level": "intense_exercise"
}
response = requests.post(
    f"{BASE_URL}/api/orchestration/parameters",
    json=params
)
print(json.dumps(response.json(), indent=2))

# 6. Récupérer les données mises à jour
updated_data = requests.get(f"{BASE_URL}/api/orchestration/data/all")
print(json.dumps(updated_data.json(), indent=2))
```

### cURL

```bash
# Vue d'ensemble
curl http://localhost:5000/api/orchestration/overview

# Santé du système
curl http://localhost:5000/api/orchestration/health

# Toutes les données
curl http://localhost:5000/api/orchestration/data/all?count=5

# Données d'un organe
curl http://localhost:5000/api/orchestration/data/cardiac

# Simulation multiple
curl -X POST http://localhost:5000/api/orchestration/simulate \
  -H "Content-Type: application/json" \
  -d '{"cardiac":"hypertension","respiratory":"copd"}'

# Simulation simple
curl -X POST http://localhost:5000/api/orchestration/simulate/cardiac/tachycardia

# Paramètres globaux
curl -X POST http://localhost:5000/api/orchestration/parameters \
  -H "Content-Type: application/json" \
  -d '{"age":60,"sex":"F","activity_level":"resting"}'

# Paramètres d'un organe
curl -X POST http://localhost:5000/api/orchestration/parameters/neural \
  -H "Content-Type: application/json" \
  -d '{"mental_state":"relaxed"}'

# Liste des organes
curl http://localhost:5000/api/orchestration/organs
```

## Scénarios d'Utilisation

### Scénario 1 : Monitoring Complet
```python
import requests
import time

BASE_URL = "http://localhost:5000"

# Boucle de monitoring
while True:
    overview = requests.get(f"{BASE_URL}/api/orchestration/overview").json()
    
    print(f"\n=== État du Système à {overview['timestamp']} ===")
    print(f"Statut global: {overview['system_health']['overall_status']}")
    
    for organ, status in overview['system_health']['organs'].items():
        print(f"  {organ}: {status['status']}")
    
    time.sleep(10)  # Vérifier toutes les 10 secondes
```

### Scénario 2 : Simulation d'Urgence Médicale
```python
import requests

BASE_URL = "http://localhost:5000"

# Simuler une crise cardiaque avec complications respiratoires
emergency_conditions = {
    "cardiac": "tachycardia",
    "respiratory": "hyperventilation",
    "neural": "stress"
}

print("⚠️  Simulation d'urgence médicale...")
response = requests.post(
    f"{BASE_URL}/api/orchestration/simulate",
    json=emergency_conditions
)

print("Conditions activées:")
for organ, result in response.json()['simulations'].items():
    print(f"  {organ}: {result['message']}")

# Récupérer les données pendant la crise
data = requests.get(f"{BASE_URL}/api/orchestration/data/all?count=10").json()
print(f"\nDonnées collectées: {data['data_count']} points par organe")
```

### Scénario 3 : Test de Résistance Physique
```python
import requests
import time

BASE_URL = "http://localhost:5000"

# Simulation d'exercice intense
print("🏃 Démarrage simulation d'exercice intense...")

# Configurer l'activité intense
params = {"activity_level": "intense_exercise"}
requests.post(f"{BASE_URL}/api/orchestration/parameters", json=params)

# Collecter les données pendant 30 secondes
for i in range(6):
    data = requests.get(f"{BASE_URL}/api/orchestration/data/all").json()
    
    cardiac = data['organs']['cardiac']['data']
    respiratory = data['organs']['respiratory']['data']
    
    print(f"\nTemps {i*5}s:")
    print(f"  Fréquence cardiaque: {cardiac['heart_rate']} bpm")
    print(f"  Fréquence respiratoire: {respiratory['respiratory_rate']} /min")
    print(f"  Saturation O2: {cardiac['oxygen_saturation']}%")
    
    time.sleep(5)

# Retour au repos
requests.post(
    f"{BASE_URL}/api/orchestration/parameters",
    json={"activity_level": "resting"}
)
print("\n✓ Retour au repos")
```

## Architecture

```
┌─────────────────────────────────┐
│   Orchestration API (5000)      │
│   Coordination centrale          │
└──────────┬──────────────────────┘
           │
     ┌─────┴─────┬──────────┐
     │           │          │
┌────▼────┐ ┌───▼────┐ ┌──▼─────┐
│Cardiac  │ │Respira-│ │Neural  │
│API      │ │tory API│ │API     │
│(5001)   │ │(5002)  │ │(5003)  │
└─────────┘ └────────┘ └────────┘
```

## Gestion des Erreurs

L'orchestrateur gère plusieurs types d'erreurs :

- **API Offline** : L'API d'un organe n'est pas accessible
- **Timeout** : L'API ne répond pas dans le délai imparti
- **Invalid Request** : Paramètres invalides
- **Partial Failure** : Certaines APIs répondent, d'autres non

Exemple de réponse en cas d'erreur partielle :
```json
{
  "organs": {
    "cardiac": {
      "data": {...}
    },
    "respiratory": {
      "error": "Cannot connect to API"
    },
    "neural": {
      "data": {...}
    }
  }
}
```

## Considérations de Performance

- **Timeout** : 5 secondes par requête API
- **Parallélisme** : Les requêtes peuvent être optimisées avec threading
- **Cache** : Possibilité d'ajouter un cache pour les données fréquentes
- **Rate Limiting** : À implémenter pour la production

## Tests

### Test de Connectivité
```bash
# Tester que toutes les APIs sont accessibles
curl http://localhost:5000/api/orchestration/health
```

### Test d'Intégration
```bash
# Test complet du workflow
curl http://localhost:5000/api/orchestration/overview
curl -X POST http://localhost:5000/api/orchestration/simulate \
  -H "Content-Type: application/json" \
  -d '{"cardiac":"normal","respiratory":"normal","neural":"normal"}'
curl http://localhost:5000/api/orchestration/data/all?count=3
```

## Considérations Éthiques

⚠️ **IMPORTANT** : Cette API coordonne des données **SYNTHÉTIQUES** à des fins **PÉDAGOGIQUES**.

- Les données agrégées sont synthétiques
- Ne JAMAIS utiliser pour des diagnostics réels
- Usage strictement éducatif
- Aucune donnée personnelle de santé réelle

## Port par Défaut
Port : **5000**

## Auteur
Projet pédagogique - Développement d'APIs Flask
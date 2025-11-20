# Neural API - Système Nerveux Central

## Description
API Flask de simulation du système nerveux central avec génération de données EEG et neurotransmetteurs synthétiques.

## Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Démarrage
```bash
python app.py
```
Port : **5003**

## Endpoints

### GET /api/neural/status
Retourne le statut du système nerveux

### GET /api/neural/data?count=1
Génère des données neurologiques synthétiques

### POST /api/neural/simulate/<condition>
Simule une pathologie neurologique

**Conditions disponibles :**
- `normal` : Fonctionnement normal
- `epilepsy` : Crise d'épilepsie
- `migraine` : Migraine
- `sleep_disorder` : Trouble du sommeil
- `stress` : État de stress

### GET/POST /api/neural/parameters
Gère les paramètres de simulation (mental_state: alert, relaxed, drowsy, sleeping, stressed)

## Données Générées

### Ondes EEG (%)
- **Alpha (8-13 Hz)** : Relaxation éveillée
- **Beta (13-30 Hz)** : Activité mentale
- **Theta (4-8 Hz)** : Somnolence
- **Delta (0.5-4 Hz)** : Sommeil profond

### Neurotransmetteurs
- **Dopamine** : 0.02-0.08 µg/dL
- **Sérotonine** : 100-250 ng/mL
- **Noradrénaline** : 150-300 pg/mL

### Autres Mesures
- **Temps de réaction** : 150-400 ms
- **Activité cérébrale** : 0-100%
- **Activité corticale** : minimal, low, moderate, high, very_high

## Exemples
```bash
# Statut
curl http://localhost:5003/api/neural/status

# Simuler stress
curl -X POST http://localhost:5003/api/neural/simulate/stress

# Changer état mental
curl -X POST http://localhost:5003/api/neural/parameters \
  -H "Content-Type: application/json" \
  -d '{"mental_state": "relaxed"}'
```
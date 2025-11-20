# Respiratory API - Système Respiratoire

## Description
API Flask de simulation du système respiratoire avec génération de données médicales synthétiques.

## Installation

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Démarrage
```bash
python app.py
```
Port : **5002**

## Endpoints

### GET /api/respiratory/status
Retourne le statut du système respiratoire

### GET /api/respiratory/data?count=1
Génère des données respiratoires synthétiques

### POST /api/respiratory/simulate/<condition>
Simule une pathologie respiratoire

**Conditions disponibles :**
- `normal` : Respiration normale
- `asthma` : Crise d'asthme
- `copd` : BPCO
- `hyperventilation` : Hyperventilation
- `apnea` : Apnée

### GET/POST /api/respiratory/parameters
Gère les paramètres de simulation

## Données Générées

- **Fréquence respiratoire** : 12-20 respirations/min
- **Volume courant** : 350-750 mL
- **Capacité vitale** : 3000-6000 mL
- **PaO2** : 80-100 mmHg
- **PaCO2** : 35-45 mmHg
- **pH sanguin** : 7.35-7.45
- **Saturation O2** : 95-100%

## Exemples

```bash
# Statut
curl http://localhost:5002/api/respiratory/status

# Simuler asthme
curl -X POST http://localhost:5002/api/respiratory/simulate/asthma

# Obtenir données
curl http://localhost:5002/api/respiratory/data?count=5
```
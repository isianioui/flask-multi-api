# Projet APIs Flask - Simulation d'Organes Humains

## 📋 Description du Projet

Ce projet implémente un système distribué d'APIs Flask simulant le fonctionnement des organes humains et générant des données médicales synthétiques réalistes. Il comprend :

- **3 APIs d'organes** : Cardiaque, Respiratoire, Neurologique
- **1 API d'orchestration** : Coordination et agrégation des données
- **Génération de données synthétiques** : Basées sur des valeurs physiologiques réalistes
- **Simulation de pathologies** : Conditions médicales variées
- **Architecture microservices** : APIs indépendantes et communicantes

## 🏗️ Architecture du Projet

```
projet-organes/
├── cardiac-api/              # API Système Cardiovasculaire (Port 5001)
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
├── respiratory-api/          # API Système Respiratoire (Port 5002)
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
├── neural-api/              # API Système Nerveux (Port 5003)
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
├── orchestration-api/       # API de Coordination (Port 5000)
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
├── documentation/
│   ├── API_DOCUMENTATION.md
│   ├── GUIDE_UTILISATION.md
│   └── RAPPORT_TECHNIQUE.md
│
├── scripts/
│   ├── setup.sh            # Script d'installation (Linux/Mac)
│   ├── setup.bat           # Script d'installation (Windows)
│   ├── start_all.sh        # Démarrage de toutes les APIs (Linux/Mac)
│   └── start_all.bat       # Démarrage de toutes les APIs (Windows)
│
├── tests/
│   ├── test_cardiac.py
│   ├── test_respiratory.py
│   ├── test_neural.py
│   └── test_orchestration.py
│
└── README.md               # Ce fichier
```

## 🚀 Installation Rapide

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Terminal/Invite de commandes

### Installation Automatique

#### Linux/Mac
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

#### Windows
```batch
scripts\setup.bat
```

### Installation Manuelle

1. **Cloner ou télécharger le projet**
```bash
cd projet-organes
```

2. **Installer chaque API**

Pour chaque API (cardiac-api, respiratory-api, neural-api, orchestration-api) :

```bash
cd cardiac-api
python -m venv venv
source venv/bin/activate  # Linux/Mac   
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt
deactivate
cd ..
```

Répéter pour respiratory-api, neural-api et orchestration-api.

## 🎮 Démarrage des APIs

### Méthode 1 : Démarrage Automatique

#### Linux/Mac
```bash
chmod +x scripts/start_all.sh
./scripts/start_all.sh
```

#### Windows
```batch
scripts\start_all.bat
```

### Méthode 2 : Démarrage Manuel

**Important** : Ouvrir 4 terminaux séparés, un pour chaque API.

**Terminal 1 - Cardiac API**
```bash
cd cardiac-api
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
python app.py
```

**Terminal 2 - Respiratory API**
```bash
cd respiratory-api
source venv/bin/activate
python app.py
```

**Terminal 3 - Neural API**
```bash
cd neural-api
source venv/bin/activate
python app.py
```

**Terminal 4 - Orchestration API**
```bash
cd orchestration-api
source venv/bin/activate
python app.py
```

### Vérification du Démarrage

Une fois toutes les APIs démarrées, testez :

```bash
# Tester chaque API
curl http://localhost:5001/api/cardiac/status
curl http://localhost:5002/api/respiratory/status
curl http://localhost:5003/api/neural/status

# Tester l'orchestration
curl http://localhost:5000/api/orchestration/health
```

## 📊 Aperçu des APIs

### 1. Cardiac API (Port 5001)
Simule le système cardiovasculaire.

**Données générées :**
- Fréquence cardiaque (60-100 bpm)
- Pression artérielle (systolique/diastolique)
- Saturation en oxygène (95-100%)
- Débit cardiaque (4-8 L/min)

**Pathologies :**
- Tachycardie, Bradycardie, Arythmie, Hypertension

### 2. Respiratory API (Port 5002)
Simule le système respiratoire.

**Données générées :**
- Fréquence respiratoire (12-20 /min)
- Volumes pulmonaires
- Gaz du sang (PaO2, PaCO2, pH)

**Pathologies :**
- Asthme, BPCO, Hyperventilation, Apnée

### 3. Neural API (Port 5003)
Simule le système nerveux central.

**Données générées :**
- Ondes EEG (alpha, beta, theta, delta)
- Neurotransmetteurs (dopamine, sérotonine, noradrénaline)
- Activité cérébrale
- Temps de réaction

**Pathologies :**
- Épilepsie, Migraine, Troubles du sommeil, Stress

### 4. Orchestration API (Port 5000)
Coordonne toutes les APIs d'organes.

**Fonctionnalités :**
- Agrégation de données
- Surveillance globale
- Simulation coordonnée
- Gestion centralisée des paramètres

## 💡 Exemples d'Utilisation

### Exemple 1 : Récupération de Données

```python
import requests
import json

# Données cardiaques
response = requests.get('http://localhost:5001/api/cardiac/data')
print(json.dumps(response.json(), indent=2))

# Toutes les données via l'orchestrateur
response = requests.get('http://localhost:5000/api/orchestration/data/all')
print(json.dumps(response.json(), indent=2))
```

### Exemple 2 : Simulation de Pathologie

```python
import requests

# Simuler une tachycardie
response = requests.post('http://localhost:5001/api/cardiac/simulate/tachycardia')
print(response.json())

# Récupérer les données affectées
response = requests.get('http://localhost:5001/api/cardiac/data?count=5')
print(response.json())
```

### Exemple 3 : Simulation Coordonnée

```python
import requests

# Simuler un état d'exercice intense sur tous les organes
params = {
    "age": 30,
    "sex": "M",
    "activity_level": "intense_exercise"
}

# Mettre à jour tous les organes
response = requests.post(
    'http://localhost:5000/api/orchestration/parameters',
    json=params
)

# Récupérer les données pendant l'exercice
response = requests.get('http://localhost:5000/api/orchestration/data/all?count=10')
data = response.json()

# Afficher les fréquences cardiaques et respiratoires
for point in data['organs']['cardiac']['data']:
    print(f"FC: {point['heart_rate']} bpm")
```

### Exemple 4 : Monitoring en Temps Réel

```python
import requests
import time

while True:
    # Vue d'ensemble
    overview = requests.get('http://localhost:5000/api/orchestration/overview')
    data = overview.json()
    
    print(f"\n=== {data['timestamp']} ===")
    print(f"Statut système: {data['system_health']['overall_status']}")
    
    # Afficher l'état de chaque organe
    for organ, status in data['system_health']['organs'].items():
        print(f"  {organ}: {status['status']}")
    
    time.sleep(5)  # Vérifier toutes les 5 secondes
```

## 🧪 Tests

### Tests Unitaires

Des tests unitaires sont fournis pour chaque API :

```bash
# Tester l'API cardiaque
cd tests
python test_cardiac.py

# Tester l'API respiratoire
python test_respiratory.py

# Tester l'API neurologique
python test_neural.py

# Tester l'orchestration
python test_orchestration.py
```

### Tests Manuels avec cURL

```bash
# Test Cardiac API
curl http://localhost:5001/api/cardiac/status
curl http://localhost:5001/api/cardiac/data?count=3
curl -X POST http://localhost:5001/api/cardiac/simulate/tachycardia

# Test Respiratory API
curl http://localhost:5002/api/respiratory/status
curl -X POST http://localhost:5002/api/respiratory/simulate/asthma

# Test Neural API
curl http://localhost:5003/api/neural/status
curl -X POST http://localhost:5003/api/neural/simulate/stress

# Test Orchestration
curl http://localhost:5000/api/orchestration/overview
curl http://localhost:5000/api/orchestration/health
```

### Tests avec Postman

Importez les collections Postman fournies dans le dossier `tests/postman/`.

## 📚 Documentation Complète

- **[API_DOCUMENTATION.md](documentation/API_DOCUMENTATION.md)** : Documentation technique des endpoints
- **[GUIDE_UTILISATION.md](documentation/GUIDE_UTILISATION.md)** : Guide d'utilisation détaillé
- **[RAPPORT_TECHNIQUE.md](documentation/RAPPORT_TECHNIQUE.md)** : Rapport technique du projet

## 🔧 Configuration

### Ports par Défaut
- Cardiac API : 5001
- Respiratory API : 5002
- Neural API : 5003
- Orchestration API : 5000

### Modification des Ports

Pour changer les ports, modifiez la dernière ligne de chaque `app.py` :

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=VOTRE_PORT)
```

Et mettez à jour la configuration dans `orchestration-api/app.py`.

## 🎯 Fonctionnalités Principales

### Génération de Données Synthétiques
- ✅ Valeurs physiologiques réalistes
- ✅ Variation naturelle
- ✅ Influence de l'âge, du sexe, de l'activité
- ✅ Cohérence entre les mesures

### Simulation de Pathologies
- ✅ Conditions cardiaques (tachycardie, bradycardie, arythmie, hypertension)
- ✅ Conditions respiratoires (asthme, BPCO, hyperventilation, apnée)
- ✅ Conditions neurologiques (épilepsie, migraine, troubles du sommeil, stress)

### Orchestration
- ✅ Agrégation des données de tous les organes
- ✅ Surveillance de la santé des APIs
- ✅ Coordination des simulations
- ✅ Gestion centralisée des paramètres

### API REST
- ✅ Endpoints standardisés
- ✅ Réponses JSON
- ✅ Gestion des erreurs
- ✅ CORS activé

## ⚠️ Considérations Éthiques

**IMPORTANT** : Ce projet est strictement pédagogique.

- ❌ **NE PAS** utiliser pour des diagnostics médicaux réels
- ❌ **NE PAS** considérer les données comme réelles
- ✅ **USAGE ÉDUCATIF UNIQUEMENT**
- ✅ Les données sont 100% synthétiques
- ✅ Aucune donnée personnelle de santé réelle

## 🐛 Dépannage

### Problème : Port déjà utilisé
```
OSError: [Errno 48] Address already in use
```
**Solution** : Un autre processus utilise le port. Terminez-le ou changez le port.

### Problème : Module non trouvé
```
ModuleNotFoundError: No module named 'flask'
```
**Solution** : Activez l'environnement virtuel et installez les dépendances.

### Problème : Cannot connect to API
**Solution** : Vérifiez que toutes les APIs sont démarrées avant l'orchestration.

### Problème : CORS Error
**Solution** : flask-cors est installé et activé. Vérifiez que l'installation est complète.

## 📝 Contributeurs

Projet réalisé dans le cadre du TP "Développement d'APIs Flask".

## 📄 Licence

Usage éducatif uniquement - Projet pédagogique

## 🔗 Ressources

- [Documentation Flask](https://flask.palletsprojects.com/)
- [REST API Best Practices](https://restfulapi.net/)
- [Physiologie humaine](https://www.physiologie.org/)

## 📞 Support

Pour toute question ou problème :
1. Consultez la documentation dans `/documentation`
2. Vérifiez les logs de chaque API
3. Testez les endpoints individuellement

---

**Version** : 1.0.0  
**Date** : Novembre 2025  
**Objectif** : Pédagogique - Formation aux APIs REST et architecture microservices
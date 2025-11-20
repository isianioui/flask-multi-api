# Guide des Commandes - Projet APIs Organes

## 📋 Référence Rapide de Toutes les Commandes

---

## 1. Installation

### Linux/Mac
```bash
# Rendre le script exécutable
chmod +x scripts/setup.sh

# Lancer l'installation
./scripts/setup.sh
```

### Windows
```batch
# Lancer l'installation
scripts\setup.bat
```

### Installation Manuelle d'une API
```bash
cd cardiac-api
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

## 2. Démarrage des APIs

### Démarrage Automatique

**Linux/Mac :**
```bash
chmod +x scripts/start_all.sh
./scripts/start_all.sh
```

**Windows :**
```batch
scripts\start_all.bat
```

### Démarrage Manuel

**Terminal 1 - Cardiac API :**
```bash
cd cardiac-api
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
python app.py
```

**Terminal 2 - Respiratory API :**
```bash
cd respiratory-api
source venv/bin/activate
python app.py
```

**Terminal 3 - Neural API :**
```bash
cd neural-api
source venv/bin/activate
python app.py
```

**Terminal 4 - Orchestration API :**
```bash
cd orchestration-api
source venv/bin/activate
python app.py
```

---

## 3. Tests de Connectivité

### Vérifier que les APIs sont démarrées

```bash
# Test Cardiac API
curl http://localhost:5001/

# Test Respiratory API
curl http://localhost:5002/

# Test Neural API
curl http://localhost:5003/

# Test Orchestration API
curl http://localhost:5000/

# Test de santé global
curl http://localhost:5000/api/orchestration/health
```

---

## 4. Commandes par API

### Cardiac API (Port 5001)

```bash
# Statut
curl http://localhost:5001/api/cardiac/status

# Données (1 point)
curl http://localhost:5001/api/cardiac/data

# Données (5 points)
curl http://localhost:5001/api/cardiac/data?count=5

# Simuler tachycardie
curl -X POST http://localhost:5001/api/cardiac/simulate/tachycardia

# Simuler bradycardie
curl -X POST http://localhost:5001/api/cardiac/simulate/bradycardia

# Simuler hypertension
curl -X POST http://localhost:5001/api/cardiac/simulate/hypertension

# Retour à la normale
curl -X POST http://localhost:5001/api/cardiac/simulate/normal

# Voir paramètres disponibles
curl http://localhost:5001/api/cardiac/parameters

# Modifier paramètres (âge, sexe, activité)
curl -X POST http://localhost:5001/api/cardiac/parameters \
  -H "Content-Type: application/json" \
  -d '{"age": 50, "sex": "F", "activity_level": "light_exercise"}'
```

### Respiratory API (Port 5002)

```bash
# Statut
curl http://localhost:5002/api/respiratory/status

# Données
curl http://localhost:5002/api/respiratory/data?count=3

# Simuler asthme
curl -X POST http://localhost:5002/api/respiratory/simulate/asthma

# Simuler BPCO
curl -X POST http://localhost:5002/api/respiratory/simulate/copd

# Simuler hyperventilation
curl -X POST http://localhost:5002/api/respiratory/simulate/hyperventilation

# Simuler apnée
curl -X POST http://localhost:5002/api/respiratory/simulate/apnea

# Retour à la normale
curl -X POST http://localhost:5002/api/respiratory/simulate/normal

# Modifier paramètres
curl -X POST http://localhost:5002/api/respiratory/parameters \
  -H "Content-Type: application/json" \
  -d '{"age": 60, "sex": "M", "activity_level": "resting"}'
```

### Neural API (Port 5003)

```bash
# Statut
curl http://localhost:5003/api/neural/status

# Données
curl http://localhost:5003/api/neural/data

# Simuler épilepsie
curl -X POST http://localhost:5003/api/neural/simulate/epilepsy

# Simuler migraine
curl -X POST http://localhost:5003/api/neural/simulate/migraine

# Simuler stress
curl -X POST http://localhost:5003/api/neural/simulate/stress

# Simuler trouble du sommeil
curl -X POST http://localhost:5003/api/neural/simulate/sleep_disorder

# Retour à la normale
curl -X POST http://localhost:5003/api/neural/simulate/normal

# Changer état mental
curl -X POST http://localhost:5003/api/neural/parameters \
  -H "Content-Type: application/json" \
  -d '{"mental_state": "relaxed"}'

# États mentaux disponibles: alert, relaxed, drowsy, sleeping, stressed
```

### Orchestration API (Port 5000)

```bash
# Vue d'ensemble complète
curl http://localhost:5000/api/orchestration/overview

# Vérifier santé de tous les services
curl http://localhost:5000/api/orchestration/health

# Toutes les données (1 point par organe)
curl http://localhost:5000/api/orchestration/data/all

# Toutes les données (5 points par organe)
curl http://localhost:5000/api/orchestration/data/all?count=5

# Données d'un organe spécifique
curl http://localhost:5000/api/orchestration/data/cardiac
curl http://localhost:5000/api/orchestration/data/respiratory
curl http://localhost:5000/api/orchestration/data/neural

# Statut d'un organe
curl http://localhost:5000/api/orchestration/status/cardiac

# Liste des organes disponibles
curl http://localhost:5000/api/orchestration/organs

# Simuler conditions multiples
curl -X POST http://localhost:5000/api/orchestration/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "cardiac": "tachycardia",
    "respiratory": "asthma",
    "neural": "stress"
  }'

# Simuler condition sur un organe
curl -X POST http://localhost:5000/api/orchestration/simulate/cardiac/hypertension

# Mettre à jour paramètres de tous les organes
curl -X POST http://localhost:5000/api/orchestration/parameters \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "sex": "F",
    "activity_level": "intense_exercise"
  }'

# Mettre à jour paramètres d'un organe
curl -X POST http://localhost:5000/api/orchestration/parameters/neural \
  -H "Content-Type: application/json" \
  -d '{"mental_state": "sleeping"}'
```

---

## 5. Scénarios Complets

### Scénario 1 : Test Basique

```bash
# 1. Vérifier que tout fonctionne
curl http://localhost:5000/api/orchestration/health

# 2. Obtenir une vue d'ensemble
curl http://localhost:5000/api/orchestration/overview

# 3. Récupérer des données
curl http://localhost:5000/api/orchestration/data/all
```

### Scénario 2 : Simulation d'Exercice Intense

```bash
# 1. Configurer exercice intense
curl -X POST http://localhost:5000/api/orchestration/parameters \
  -H "Content-Type: application/json" \
  -d '{"activity_level": "intense_exercise"}'

# 2. Récupérer les données pendant l'exercice
curl http://localhost:5000/api/orchestration/data/all?count=10

# 3. Retour au repos
curl -X POST http://localhost:5000/api/orchestration/parameters \
  -H "Content-Type: application/json" \
  -d '{"activity_level": "resting"}'

# 4. Données au repos
curl http://localhost:5000/api/orchestration/data/all?count=5
```

### Scénario 3 : Simulation d'Urgence Médicale

```bash
# 1. Simuler une crise
curl -X POST http://localhost:5000/api/orchestration/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "cardiac": "tachycardia",
    "respiratory": "hyperventilation",
    "neural": "stress"
  }'

# 2. Observer les données critiques
curl http://localhost:5000/api/orchestration/data/all?count=3

# 3. Normaliser tous les systèmes
curl -X POST http://localhost:5000/api/orchestration/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "cardiac": "normal",
    "respiratory": "normal",
    "neural": "normal"
  }'
```

### Scénario 4 : Patient Âgé au Repos

```bash
# 1. Configurer patient âgé
curl -X POST http://localhost:5000/api/orchestration/parameters \
  -H "Content-Type: application/json" \
  -d '{"age": 75, "sex": "M", "activity_level": "resting"}'

# 2. Obtenir les données
curl http://localhost:5000/api/orchestration/data/all

# 3. Simuler hypertension (fréquente chez personnes âgées)
curl -X POST http://localhost:5000/api/orchestration/simulate/cardiac/hypertension

# 4. Observer l'impact
curl http://localhost:5000/api/orchestration/data/cardiac?count=5
```

---

## 6. Scripts Python

### Script : Monitoring Continu

Créer un fichier `monitor.py` :

```python
import requests
import time
import json

BASE_URL = "http://localhost:5000"

while True:
    try:
        response = requests.get(f"{BASE_URL}/api/orchestration/overview")
        data = response.json()
        
        print(f"\n{'='*60}")
        print(f"Timestamp: {data['timestamp']}")
        print(f"Statut Système: {data['system_health']['overall_status']}")
        print(f"{'='*60}")
        
        for organ, health in data['system_health']['organs'].items():
            status = health.get('status', 'unknown')
            print(f"  {organ.upper()}: {status}")
        
        time.sleep(5)
        
    except KeyboardInterrupt:
        print("\nArrêt du monitoring")
        break
    except Exception as e:
        print(f"Erreur: {e}")
        time.sleep(5)
```

Exécuter :
```bash
python monitor.py
```

### Script : Collecte de Données

Créer un fichier `collect_data.py` :

```python
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

# Collecter 10 échantillons sur 50 secondes
samples = []
for i in range(10):
    print(f"Collecte échantillon {i+1}/10...")
    
    response = requests.get(f"{BASE_URL}/api/orchestration/data/all")
    data = response.json()
    
    samples.append({
        'timestamp': datetime.now().isoformat(),
        'data': data
    })
    
    time.sleep(5)

# Sauvegarder dans un fichier
with open('medical_data.json', 'w') as f:
    json.dump(samples, f, indent=2)

print(f"\n{len(samples)} échantillons sauvegardés dans medical_data.json")
```

Exécuter :
```bash
python collect_data.py
```

### Script : Test de Stress

Créer un fichier `stress_test.py` :

```python
import requests
import concurrent.futures
import time

BASE_URL = "http://localhost:5000"

def make_request():
    try:
        response = requests.get(f"{BASE_URL}/api/orchestration/data/all")
        return response.status_code == 200
    except:
        return False

print("Démarrage du test de stress...")
print("100 requêtes simultanées sur 10 workers")

start = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(make_request) for _ in range(100)]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

elapsed = time.time() - start

success = sum(results)
print(f"\nRésultats:")
print(f"  Requêtes réussies: {success}/100")
print(f"  Temps total: {elapsed:.2f}s")
print(f"  Temps moyen: {elapsed/100:.3f}s par requête")
```

Exécuter :
```bash
python stress_test.py
```

---

## 7. Dépannage

### Problème : Port déjà utilisé

```bash
# Trouver le processus utilisant le port (Linux/Mac)
lsof -i :5001

# Tuer le processus
kill -9 <PID>

# Windows
netstat -ano | findstr :5001
taskkill /PID <PID> /F
```

### Problème : Module non trouvé

```bash
# Vérifier l'environnement virtuel
which python  # Linux/Mac
where python  # Windows

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Problème : API ne répond pas

```bash
# Vérifier que l'API est démarrée
curl http://localhost:5001/health

# Vérifier les logs dans le terminal de l'API
```

---

## 8. Arrêt des APIs

### Linux/Mac
```bash
# Dans chaque terminal où une API tourne
Ctrl + C
```

### Windows
```bash
# Dans chaque fenêtre de commande
Ctrl + C
# ou fermer la fenêtre
```

---

## 9. Commandes Git

```bash
# Initialiser le dépôt
git init

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit - Projet APIs Organes"

# Ajouter remote (si nécessaire)
git remote add origin <URL_DU_REPO>

# Push
git push -u origin main
```

---

## 10. Nettoyage

```bash
# Supprimer tous les environnements virtuels
rm -rf */venv  # Linux/Mac
rmdir /s */venv  # Windows

# Supprimer les caches Python
find . -type d -name __pycache__ -exec rm -rf {} +  # Linux/Mac
```

---

**Fin du Guide des Commandes**

Pour plus d'informations, consultez :
- README.md (vue d'ensemble)
- documentation/RAPPORT_TECHNIQUE.md (détails techniques)
- Chaque README.md dans les dossiers d'API
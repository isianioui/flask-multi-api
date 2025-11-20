# @echo off
# REM Script de démarrage pour toutes les APIs
# REM Compatible Windows

# echo ======================================
# echo Demarrage des APIs Organes
# echo ======================================
# echo.
# echo [!] Ce script va ouvrir 4 fenetres de commande.
# echo     Fermez-les pour arreter les APIs.
# echo.

# REM Démarrer Cardiac API
# echo Demarrage de Cardiac API (Port 5001)...
# start "Cardiac API - Port 5001" cmd /k "cd cardiac-api && venv\Scripts\activate && python app.py"
# timeout /t 3 /nobreak >nul

# REM Démarrer Respiratory API
# echo Demarrage de Respiratory API (Port 5002)...
# start "Respiratory API - Port 5002" cmd /k "cd respiratory-api && venv\Scripts\activate && python app.py"
# timeout /t 3 /nobreak >nul

# REM Démarrer Neural API
# echo Demarrage de Neural API (Port 5003)...
# start "Neural API - Port 5003" cmd /k "cd neural-api && venv\Scripts\activate && python app.py"

# echo.
# echo Attente du demarrage des APIs d'organes (10 secondes)...
# timeout /t 10 /nobreak >nul

# REM Démarrer Orchestration API
# echo Demarrage de Orchestration API (Port 5000)...
# start "Orchestration API - Port 5000" cmd /k "cd orchestration-api && venv\Scripts\activate && python app.py"

# echo.
# echo ======================================
# echo [OK] Toutes les APIs sont en cours de demarrage
# echo ======================================
# echo.
# echo URLs d'acces :
# echo   - Cardiac API:        http://localhost:5001
# echo   - Respiratory API:    http://localhost:5002
# echo   - Neural API:         http://localhost:5003
# echo   - Orchestration API:  http://localhost:5000
# echo.
# echo Test de sante :
# echo   curl http://localhost:5000/api/orchestration/health
# echo.
# echo Pour arreter, fermez les fenetres ouvertes.
# echo.
# pause
# 🤖 Automatisierungs-Guide - ML Pipeline

## 📋 Übersicht

Das System hat jetzt eine **vollautomatische Pipeline**, die:

1. ✅ **Neue Matches fetcht** (Riot API)
2. ✅ **Modelle trainiert** (Game State + Champion Matchup)
3. ✅ **Frontend aktualisiert** (model_performance.json, item_builds.json, etc.)
4. ✅ **Notifications sendet** (bei Fehlern)
5. ✅ **Logs erstellt** (für Debugging)

---

## 🚀 Schnellstart

### **Option 1: Manuelle Ausführung**

```bash
# Test-Modus (zeigt nur, was passieren würde)
python3 automated_pipeline.py --dry-run

# Echte Ausführung
python3 automated_pipeline.py --force

# Logs anschauen
tail -f pipeline.log
```

### **Option 2: Cron Job (Mac/Linux)**

```bash
# Setup-Skript ausführen
bash setup_automation.sh

# Oder manuell:
crontab -e

# Diese Zeile hinzufügen (täglich um 3 Uhr nachts):
0 3 * * * cd "/Users/merlinmechler/Library/Mobile Documents/com~apple~CloudDocs/Data Analysis/Win_Predicition_System_WR" && python3 automated_pipeline.py >> pipeline.log 2>&1
```

### **Option 3: GitHub Actions (Cloud)**

1. Repository auf GitHub pushen
2. Secrets in GitHub hinzufügen:
   - `RIOT_API_KEY`
   - `POSTGRES_URL`
   - `INTERNAL_API_KEY`
3. Workflow läuft automatisch täglich um 3 Uhr UTC

---

## 📊 Pipeline-Flow

```
┌─────────────────────────────────────────────────────┐
│  1. DATA FETCHING                                   │
│  fetch_matches_with_timeline_incremental.py         │
│  → Holt neue Matches von Riot API                  │
│  → Speichert in PostgreSQL                         │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  2. MODEL TRAINING - Game State                     │
│  train_game_state_predictor.py                      │
│  → Trainiert Modell mit Timeline-Daten             │
│  → 79.28% Accuracy                                  │
│  → Speichert: models/game_state_predictor.pkl      │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  3. MODEL TRAINING - Champion Matchup               │
│  train_champion_matchup.py                          │
│  → Trainiert Draft-Prediction                      │
│  → 52% Accuracy (normal für Draft-Only)            │
│  → Speichert: models/champion_predictor.pkl        │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  4. DATA PROCESSING - Item Builds                   │
│  generate_item_builds.py                            │
│  → Analysiert Item-Builds aus Matches              │
│  → Speichert: data/champion_data/item_builds.json  │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  5. FRONTEND STATS GENERATION                       │
│  generate_frontend_stats.py                         │
│  → Erstellt model_performance.json                 │
│  → Zeigt 79.28% im Frontend                        │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  6. FRONTEND SYNC                                   │
│  → Kopiert Files nach:                             │
│    lol-coach-frontend/public/data/                  │
│  → model_performance.json                          │
│  → champion_stats.json                             │
│  → item_builds.json                                │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  7. BACKEND RESTART (optional)                      │
│  → Lädt neue Modelle                               │
│  → Manuell: python3 api_v2.py                      │
└─────────────────────────────────────────────────────┘
```

---

## 🔧 Konfiguration

### **Wann wird neu trainiert?**

Die Pipeline prüft automatisch:

1. ✅ **Force-Flag** (`--force`): Immer trainieren
2. ✅ **Kein Performance-File**: Erstes Training
3. ✅ **Letzte Aktualisierung > 7 Tage**: Wöchentliches Retraining
4. ✅ **Neue Matches > 1000** (TODO: Implementierung mit DB-Query)

### **Environment Variables**

Stelle sicher, dass `.env` existiert:

```env
RIOT_API_KEY=RGAPI-xxx
POSTGRES_URL=postgres://...
INTERNAL_API_KEY=victory-secret-key-2025
```

---

## 📁 Wichtige Dateien

### **Pipeline-Skripte**

| Datei | Zweck |
|-------|-------|
| `automated_pipeline.py` | **Haupt-Orchestrator** (nutze diesen!) |
| `pipeline.py` | Legacy-Skript (manuell) |
| `mlops_pipeline.py` | MLOps-Funktionen (wird integriert) |

### **Training-Skripte**

| Datei | Modell | Output |
|-------|--------|--------|
| `train_game_state_predictor.py` | Game State (79.28%) | `models/game_state_predictor.pkl` |
| `train_champion_matchup.py` | Champion Matchup (52%) | `models/champion_predictor.pkl` |

### **Daten-Skripte**

| Datei | Zweck |
|-------|-------|
| `fetch_matches_with_timeline_incremental.py` | Fetcht neue Matches |
| `generate_item_builds.py` | Erstellt Item-Builds |
| `generate_frontend_stats.py` | Erstellt Frontend-JSON |

### **Output-Dateien**

| Datei | Wird kopiert nach Frontend? |
|-------|----------------------------|
| `models/game_state_predictor.pkl` | ❌ (nur Backend) |
| `models/champion_predictor.pkl` | ❌ (nur Backend) |
| `models/game_state_performance.json` | ✅ → `model_performance.json` |
| `data/champion_data/item_builds.json` | ✅ |
| `data/champion_data/champion_stats.json` | ✅ |

---

## 🔍 Monitoring

### **Logs ansehen**

```bash
# Echtzeit-Logs
tail -f pipeline.log

# Letzte 100 Zeilen
tail -100 pipeline.log

# Nach Fehlern suchen
grep -i "error\|failed" pipeline.log
```

### **Pipeline-Status prüfen**

```bash
# Letzte Ausführung
cat pipeline.log | grep "PIPELINE EXECUTION SUMMARY" -A 20 | tail -20

# Cron-Job Status
crontab -l | grep automated_pipeline

# Systemd-Timer (Linux)
systemctl status lol-pipeline.timer
```

### **Model-Performance prüfen**

```bash
# Backend
cat models/game_state_performance.json | jq

# Frontend
cat lol-coach-frontend/public/data/model_performance.json | jq
```

---

## 🐛 Troubleshooting

### **Problem: Pipeline startet nicht**

```bash
# Prüfe Python-Version
python3 --version  # Sollte >= 3.8 sein

# Prüfe Dependencies
pip install -r requirements.txt

# Teste Pipeline manuell
python3 automated_pipeline.py --dry-run
```

### **Problem: Cron läuft nicht**

```bash
# Prüfe Cron-Logs (Mac)
log show --predicate 'process == "cron"' --last 1h

# Prüfe Cron-Logs (Linux)
grep CRON /var/log/syslog

# Teste Cron manuell
/usr/sbin/cron
```

### **Problem: Frontend zeigt alte Daten**

```bash
# Prüfe Timestamp
cat lol-coach-frontend/public/data/model_performance.json | jq .timestamp

# Forciere Sync
python3 automated_pipeline.py --force

# Frontend neu builden (falls Next.js cacht)
cd lol-coach-frontend
npm run build
```

### **Problem: Backend lädt alte Modelle**

```bash
# Backend neu starten
pkill -f api_v2.py
python3 api_v2.py

# Oder mit Systemd
sudo systemctl restart lol-backend
```

---

## 🎯 Best Practices

### **1. Testen vor Automatisierung**

```bash
# Erst dry-run
python3 automated_pipeline.py --dry-run

# Dann force
python3 automated_pipeline.py --force

# Erst dann Cron aktivieren
bash setup_automation.sh
```

### **2. Regelmäßige Backups**

```bash
# Modelle sichern
cp -r models models_backup_$(date +%Y%m%d)

# Daten sichern
cp -r data data_backup_$(date +%Y%m%d)
```

### **3. Performance überwachen**

```bash
# Wöchentlich prüfen
cat pipeline.log | grep "SUMMARY" -A 10
```

### **4. Disk-Space beachten**

```bash
# Alte Logs rotieren (> 30 Tage)
find . -name "pipeline.log.*" -mtime +30 -delete

# CSV-Backups komprimieren
gzip data/*.csv
```

---

## 📈 Erweiterte Features

### **Notifications (TODO)**

```python
# In automated_pipeline.py
def send_notification(success: bool, summary: str):
    # Email via SMTP
    # Slack Webhook
    # Discord Webhook
    pass
```

### **Database-Integration (TODO)**

```python
# Prüfe neue Matches in PostgreSQL
def check_new_matches() -> int:
    conn = psycopg2.connect(os.getenv('POSTGRES_URL'))
    # Query für neue Matches seit letztem Training
    return new_count
```

### **Auto-Backend-Restart (TODO)**

```bash
# Mit Systemd
sudo systemctl reload lol-backend

# Mit PM2
pm2 reload lol-backend

# Mit Supervisor
supervisorctl restart lol-backend
```

---

## 📞 Support

**Bei Problemen:**

1. Prüfe `pipeline.log`
2. Führe `--dry-run` aus
3. Prüfe Environment-Variables
4. Teste Skripte einzeln

**Logs:**
- Pipeline: `pipeline.log`
- Backend: `uvicorn.log`
- Cron: `/var/log/syslog` (Linux) oder `log show` (Mac)

---

## 🎉 Erfolg-Kriterien

Pipeline ist erfolgreich, wenn:

✅ Alle Steps completed
✅ Frontend zeigt neue Zahlen (79.28%)
✅ Backend lädt neue Modelle
✅ Logs zeigen keine Errors
✅ Frontend-Files haben aktuellen Timestamp

**Prüfen:**

```bash
# Frontend-Timestamp
cat lol-coach-frontend/public/data/model_performance.json | jq .timestamp

# Backend-Modell-Timestamp
ls -lh models/*.pkl

# Pipeline-Logs
tail -50 pipeline.log | grep "completed successfully"
```

---

## 🔄 Manuelle Pipeline-Ausführung

Wenn du die Pipeline manuell ausführen willst:

```bash
# Kompletter Flow
python3 automated_pipeline.py --force

# Nur einzelne Steps (Legacy)
python3 fetch_matches_with_timeline_incremental.py
python3 train_game_state_predictor.py
python3 train_champion_matchup.py
python3 generate_item_builds.py
python3 generate_frontend_stats.py
```

---

**Viel Erfolg mit der Automatisierung! 🚀**

# Quick Start Guide: Massives Training mit öffentlichen Daten

Dieses Guide zeigt dir, wie du dein Win-Prediction-Modell mit Millionen von öffentlichen Match-Daten trainierst.

## Übersicht der Datenquellen

### 1. Kaggle Datasets (Empfohlen)
- **Vorteile**: Millionen vorbereitete Matches, keine API-Limits, sofort verfügbar
- **Nachteile**: Nicht die aktuellsten Daten
- **Größe**: 50.000 - 4+ Millionen Matches

### 2. Riot Games API
- **Vorteile**: Aktuelle Live-Daten, eigene Auswahl der Matches
- **Nachteile**: API Rate Limits (20 req/sec), langsamer
- **Größe**: Begrenzt durch Zeit und Rate Limits

### 3. Kombination (Beste Option!)
- **Training**: Kaggle Daten für Basis-Modell
- **Fine-Tuning**: Riot API für aktuelle Trends
- **Resultat**: Bestes aus beiden Welten

---

## Setup-Anleitung

### Schritt 1: Kaggle API einrichten

```bash
# 1. Installiere Kaggle Package
pip install kaggle

# 2. Gehe zu https://www.kaggle.com/settings
# 3. Scrolle zu "API" -> "Create New API Token"
# 4. Lade kaggle.json herunter
# 5. Platziere es in:
#    - Linux/Mac: ~/.kaggle/kaggle.json
#    - Windows: C:\Users\<username>\.kaggle\kaggle.json

# 6. Setze Berechtigungen (nur Mac/Linux):
chmod 600 ~/.kaggle/kaggle.json
```

### Schritt 2: Lade Kaggle Datasets

```bash
# Führe den Kaggle Data Loader aus
python kaggle_data_loader.py
```

Das lädt automatisch das "Diamond Ranked Games" Dataset (~50.000 Matches) herunter und normalisiert es.

**Erwartete Ausgabe:**
```
✓ Kaggle API konfiguriert
📥 Lade Dataset: diamond_ranked
✓ Download erfolgreich!
✓ Verarbeitete Daten gespeichert: ./data/kaggle_processed_features.csv
   Zeilen: 49,425
```

### Schritt 3: Trainiere Modell

```bash
# Option A: NUR mit Kaggle Daten (schnell, kein API Key nötig)
python Win_predicition_generator.py --kaggle-only

# Option B: Kaggle + Riot API (beste Qualität)
export RIOT_API_KEY='dein-api-key'
python Win_predicition_generator.py --use-kaggle

# Option C: Nur Riot API (ohne Kaggle)
python Win_predicition_generator.py
```

---

## Verfügbare Datasets

### Klein & Schnell (für Tests)
```python
dataset_key = 'diamond_ranked'
# Größe: ~50.000 Matches
# Download: ~50 MB
# Training: ~2-5 Minuten
```

### Mittelgroß (gute Balance)
```python
dataset_key = 'challenger_games'
# Größe: ~200.000 Matches
# Download: ~200 MB
# Training: ~10-15 Minuten
```

### Riesig (beste Modell-Qualität)
```python
dataset_key = 'ranked_games'
# Größe: 4+ Millionen Matches
# Download: ~2-4 GB
# Training: 1-2 Stunden
# ⚠️  Benötigt min. 8 GB RAM!
```

---

## Beispiel-Workflows

### Workflow 1: Schnellstart (5 Minuten)
```bash
# 1. Kaggle API Setup (einmalig)
# 2. Lade kleines Dataset
python kaggle_data_loader.py

# 3. Trainiere Modell
python Win_predicition_generator.py --kaggle-only

# Fertig! Modell in ./models/
```

### Workflow 2: Maximale Qualität
```bash
# 1. Lade ALLE Kaggle Datasets
python -c "
from kaggle_data_loader import KaggleDataLoader
loader = KaggleDataLoader()

# Lade mehrere Datasets
for key in ['diamond_ranked', 'challenger_games', 'ranked_games']:
    print(f'Lade {key}...')
    loader.download_dataset(key)
    df = loader.load_dataset_to_dataframe(key)
    normalized = loader.normalize_to_standard_format(df, key)
    normalized.to_csv(f'./data/{key}_features.csv', index=False)
"

# 2. Kombiniere alle Daten manuell
python -c "
import pandas as pd
from pathlib import Path

dfs = []
for csv in Path('./data').glob('*_features.csv'):
    print(f'Lade {csv}...')
    dfs.append(pd.read_csv(csv))

combined = pd.concat(dfs, ignore_index=True)
combined.to_csv('./data/kaggle_processed_features.csv', index=False)
print(f'✓ {len(combined):,} Matches kombiniert!')
"

# 3. Trainiere mit allen Daten + Riot API Updates
export RIOT_API_KEY='dein-key'
python Win_predicition_generator.py --use-kaggle
```

### Workflow 3: Inkrementelles Training
```bash
# 1. Basis-Modell mit Kaggle
python Win_predicition_generator.py --kaggle-only

# 2. Fine-Tune mit aktuellen Riot API Daten (später)
export RIOT_API_KEY='dein-key'
python Win_predicition_generator.py --use-kaggle
```

---

## Performance-Tipps

### Für große Datasets (> 1 Million Matches)

```python
# In kaggle_data_loader.py anpassen:

# 1. Aktiviere Batch-Processing
processor = BatchDataProcessor(batch_size=10000)

# 2. Reduziere Memory-Nutzung
import dask.dataframe as dd
# Dask lädt Daten lazy (nur bei Bedarf)

# 3. Feature-Selection
# Entferne unwichtige Features um Speicher zu sparen
```

### RAM-Anforderungen
- < 100k Matches: 4 GB RAM
- 100k - 1M Matches: 8 GB RAM
- 1M+ Matches: 16 GB RAM oder Batch-Processing

---

## Modell-Qualität Erwartungen

### Mit 50.000 Matches (diamond_ranked)
```
Accuracy: ~72-75%
ROC-AUC: ~0.78-0.82
Training Zeit: 2-5 min
```

### Mit 500.000 Matches (mehrere Datasets)
```
Accuracy: ~75-78%
ROC-AUC: ~0.82-0.86
Training Zeit: 15-30 min
```

### Mit 4+ Millionen Matches (ranked_games)
```
Accuracy: ~78-82%
ROC-AUC: ~0.85-0.90
Training Zeit: 1-2 Stunden
```

---

## Troubleshooting

### Problem: "Kaggle API nicht konfiguriert"
**Lösung:**
```bash
# Prüfe ob kaggle.json existiert
ls ~/.kaggle/kaggle.json

# Falls nicht:
# 1. Gehe zu https://www.kaggle.com/settings
# 2. Erstelle neuen API Token
# 3. Kopiere kaggle.json nach ~/.kaggle/
```

### Problem: "Memory Error" beim Training
**Lösung:**
```python
# Option 1: Reduziere batch_size
processor = BatchDataProcessor(batch_size=5000)

# Option 2: Sample die Daten
df_sampled = df.sample(n=100000, random_state=42)

# Option 3: Aktiviere Dask für Out-of-Memory Processing
```

### Problem: "API Rate Limit exceeded"
**Lösung:**
```python
# Riot API sammelt langsam, das ist normal
# Verwende Kaggle für schnelleres Training:
python Win_predicition_generator.py --kaggle-only
```

### Problem: Dataset-Download schlägt fehl
**Lösung:**
```bash
# Manueller Download:
# 1. Gehe zu https://www.kaggle.com/datasets/bobbyscience/league-of-legends-diamond-ranked-games-10-min
# 2. Klicke "Download"
# 3. Entpacke in ./kaggle_data/diamond_ranked/
```

---

## Nächste Schritte

1. **Modell verbessern**:
   - Mehr Features hinzufügen (Champions, Items, Runes)
   - Hyperparameter-Tuning
   - Ensemble-Methoden (Kombiniere Random Forest + XGBoost)

2. **Real-Time Predictions**:
   - Integriere mit Riot Live Client API
   - Baue Web-Dashboard mit Streamlit

3. **Item-Recommendation**:
   - Erweitere um Item-Build-Vorschläge
   - Analysiere Win-Rates nach Items

4. **Deployment**:
   - Deploye auf Google Cloud Platform
   - Erstelle REST API mit Flask/FastAPI

---

## Ressourcen

### Kaggle Datasets
- [Diamond Ranked Games](https://www.kaggle.com/datasets/bobbyscience/league-of-legends-diamond-ranked-games-10-min)
- [Challenger Games 2020](https://www.kaggle.com/datasets/gyejr95/league-of-legends-challenger-ranked-games2020)
- [4M+ Ranked Games](https://www.kaggle.com/datasets/datasnaek/league-of-legends)

### Riot API
- [Developer Portal](https://developer.riotgames.com/)
- [API Documentation](https://developer.riotgames.com/apis)
- [Rate Limits](https://developer.riotgames.com/docs/portal#web-apis_rate-limiting)

### Machine Learning
- [scikit-learn Docs](https://scikit-learn.org/stable/)
- [Random Forest Guide](https://scikit-learn.org/stable/modules/ensemble.html#forest)
- [Model Evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)

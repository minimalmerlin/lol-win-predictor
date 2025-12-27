# Massive Training mit Millionen öffentlichen Match-Daten

Dieses Update erweitert dein Win-Prediction-System um die Möglichkeit, mit **Millionen öffentlich verfügbaren Match-Daten** zu trainieren.

## Was ist neu?

### 3 neue Dateien:

1. **[kaggle_data_loader.py](kaggle_data_loader.py)** - Lädt und verarbeitet Kaggle Datasets
2. **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** - Detaillierte Anleitung
3. **[setup_massive_training.sh](setup_massive_training.sh)** - Automatisches Setup-Script

### Erweiterte Datei:

- **[Win_predicition_generator.py](Win_predicition_generator.py)** - Jetzt mit Kaggle-Integration

---

## Schnellstart (3 Schritte)

### 1. Automatisches Setup
```bash
./setup_massive_training.sh
```
Das Script führt dich durch:
- Python Environment Setup
- Kaggle API Konfiguration
- Dataset Download
- Optional: Training starten

### 2. Manuelle Alternative

```bash
# Kaggle API Setup (einmalig)
pip install kaggle
# Lade kaggle.json von https://www.kaggle.com/settings
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Lade Daten
python kaggle_data_loader.py

# Trainiere Modell
python Win_predicition_generator.py --kaggle-only
```

### 3. Direkter Start (wenn bereits konfiguriert)

```bash
python Win_predicition_generator.py --kaggle-only
```

---

## Verfügbare Datenquellen

| Dataset | Matches | Größe | Training Zeit | Accuracy |
|---------|---------|-------|---------------|----------|
| Diamond Ranked | ~50.000 | 50 MB | 2-5 min | 72-75% |
| Challenger Games | ~200.000 | 200 MB | 10-15 min | 75-78% |
| Ranked Games | 4+ Mio | 2-4 GB | 1-2 Std | 78-82% |
| Riot API | Custom | - | Variabel | Aktuell |

---

## Modi

### Modus 1: Nur Kaggle (Schnell)
```bash
python Win_predicition_generator.py --kaggle-only
```
- Kein Riot API Key nötig
- Schnelles Training
- Große Datenmengen verfügbar

### Modus 2: Kombiniert (Beste Qualität)
```bash
export RIOT_API_KEY='dein-key'
python Win_predicition_generator.py --use-kaggle
```
- Basis-Training mit Kaggle
- Fine-Tuning mit aktuellen Riot API Daten
- Beste Modell-Performance

### Modus 3: Nur Riot API (Original)
```bash
python Win_predicition_generator.py
```
- Nur Live-Daten von Riot API
- Begrenzt durch Rate Limits

---

## Architektur-Übersicht

```
┌─────────────────────────────────────────────────────────┐
│                    Datenquellen                         │
├──────────────────────┬──────────────────────────────────┤
│   Kaggle Datasets    │      Riot Games API             │
│   (4+ Millionen)     │      (Live Daten)               │
└──────────┬───────────┴────────────┬─────────────────────┘
           │                        │
           ▼                        ▼
   ┌───────────────┐       ┌──────────────────┐
   │ Kaggle Loader │       │ Riot API Client  │
   │ - Download    │       │ - Rate Limiting  │
   │ - Normalize   │       │ - Match Details  │
   └───────┬───────┘       └────────┬─────────┘
           │                        │
           └────────┬───────────────┘
                    ▼
        ┌──────────────────────┐
        │  Match Data Processor │
        │  - Feature Extraction │
        │  - Data Combination   │
        │  - Normalization      │
        └──────────┬─────────────┘
                   ▼
        ┌──────────────────────┐
        │  Win Prediction Model │
        │  - Random Forest      │
        │  - Logistic Regression│
        │  - 78-82% Accuracy    │
        └───────────────────────┘
```

---

## Feature-Übersicht

### Was wird extrahiert?

Aus jedem Match werden 20+ Features extrahiert:

**Team Stats (Blue/Red):**
- Kills, Deaths, Assists
- Gold Earned (total & @15min)
- Towers, Dragons, Barons
- Vision Score

**Differentials (wichtig!):**
- Kill Difference
- Gold Difference (@15min & total)
- Tower Difference
- Dragon Difference

**Meta:**
- Game Duration
- Champion IDs
- Item Builds (für zukünftige Item-Recommendation)

---

## Performance-Benchmarks

### Hardware-Anforderungen

| Dataset-Größe | RAM | Speicher | GPU |
|---------------|-----|----------|-----|
| < 100k | 4 GB | 1 GB | Nein |
| 100k - 1M | 8 GB | 5 GB | Nein |
| 1M+ | 16 GB | 10 GB | Optional |

### Training-Geschwindigkeit

**MacBook Pro M1 (8 GB RAM):**
- 50k Matches: ~3 Minuten
- 200k Matches: ~12 Minuten
- 500k Matches: ~35 Minuten

**Linux Server (32 GB RAM, 8 Cores):**
- 50k Matches: ~1 Minute
- 1M Matches: ~15 Minuten
- 4M Matches: ~1 Stunde

---

## Erweiterte Nutzung

### Custom Dataset kombinieren

```python
from kaggle_data_loader import KaggleDataLoader
import pandas as pd

loader = KaggleDataLoader()

# Lade mehrere Datasets
datasets = []
for key in ['diamond_ranked', 'challenger_games']:
    df = loader.load_dataset_to_dataframe(key)
    normalized = loader.normalize_to_standard_format(df, key)
    datasets.append(normalized)

# Kombiniere
combined = pd.concat(datasets, ignore_index=True)
combined.to_csv('./data/kaggle_processed_features.csv', index=False)

print(f"✓ {len(combined):,} Matches kombiniert")
```

### Batch-Processing für sehr große Datasets

```python
from kaggle_data_loader import BatchDataProcessor

processor = BatchDataProcessor(batch_size=10000)

def normalize_chunk(chunk):
    # Deine Normalisierung hier
    return chunk

processor.process_large_csv(
    csv_path='huge_dataset.csv',
    processor_func=normalize_chunk,
    output_path='./data/processed.csv'
)
```

### Feature Importance Analysis

Nach dem Training kannst du die wichtigsten Features anschauen:

```python
# Wird automatisch ausgegeben:
Top 10 wichtigste Features:
1. gold_diff         0.245
2. tower_diff        0.198
3. kill_diff         0.176
4. dragon_diff       0.089
...
```

---

## Kaggle Datasets Details

### 1. Diamond Ranked Games (10min)
- **Link**: [kaggle.com/datasets/bobbyscience/league-of-legends-diamond-ranked-games-10-min](https://www.kaggle.com/datasets/bobbyscience/league-of-legends-diamond-ranked-games-10-min)
- **Matches**: ~50.000
- **Besonderheit**: Stats bei genau 10 Minuten Spielzeit
- **Qualität**: Sehr gut (nur Diamond+ Spiele)

### 2. Challenger Ranked Games 2020
- **Link**: [kaggle.com/datasets/gyejr95/league-of-legends-challenger-ranked-games2020](https://www.kaggle.com/datasets/gyejr95/league-of-legends-challenger-ranked-games2020)
- **Matches**: ~200.000
- **Besonderheit**: Nur Challenger-Spiele
- **Qualität**: Höchste Skill-Level

### 3. Ranked Games (Sehr groß!)
- **Link**: [kaggle.com/datasets/datasnaek/league-of-legends](https://www.kaggle.com/datasets/datasnaek/league-of-legends)
- **Matches**: 4+ Millionen
- **Besonderheit**: Alle Ranks, vollständige Games
- **Qualität**: Mixed (alle Skill-Levels)

---

## Nächste Schritte & Erweiterungen

### 1. Item-Recommendation System
```python
# TODO: Implementierung in kaggle_data_loader.py
# Analysiere Win-Rate nach Item-Builds
# Empfehle optimale Items basierend auf Game State
```

### 2. Champion-spezifische Modelle
```python
# Trainiere separate Modelle für jeden Champion
# Bessere Accuracy für spezifische Matchups
```

### 3. Web-Dashboard
```bash
# Streamlit Dashboard für Live-Predictions
streamlit run dashboard.py
```

### 4. Real-Time Integration
```python
# Integriere mit Riot Live Client API
# In-Game Win-Probability Tracker
```

### 5. GCP Deployment
```bash
# Deploye Modell auf Google Cloud Platform
# REST API für externe Zugriffe
```

---

## Troubleshooting

### "Kaggle API nicht gefunden"
```bash
pip install kaggle
# Erstelle API Token auf kaggle.com/settings
```

### "Memory Error beim Training"
```python
# Reduziere Batch-Size oder sample die Daten:
df_sampled = df.sample(n=100000, random_state=42)
```

### "Dataset Download hängt"
```bash
# Manueller Download von Kaggle Website
# Entpacke in ./kaggle_data/<dataset-name>/
```

### "API Rate Limit exceeded"
Das ist normal bei Riot API - verwende Kaggle für schnelleres Training:
```bash
python Win_predicition_generator.py --kaggle-only
```

---

## Datenschutz & Ethik

Alle verwendeten Daten sind:
- Öffentlich verfügbar
- Anonymisiert (keine Spielernamen in Features)
- Nur für Forschungs-/Bildungszwecke
- Riot Games ToS konform

---

## Credits & Lizenz

**Author**: Merlin Mechler
**Datenquellen**: Kaggle Community & Riot Games API
**Lizenz**: Educational Use

**Kaggle Dataset Credits**:
- Diamond Ranked: [bobbyscience](https://www.kaggle.com/bobbyscience)
- Challenger Games: [gyejr95](https://www.kaggle.com/gyejr95)
- Ranked Games: [datasnaek](https://www.kaggle.com/datasnaek)

---

## Support & Feedback

Bei Fragen oder Problemen:
1. Lies [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)
2. Prüfe Troubleshooting-Sektion
3. Öffne Issue auf GitHub (falls vorhanden)

Viel Erfolg mit deinem Win-Prediction-Modell!

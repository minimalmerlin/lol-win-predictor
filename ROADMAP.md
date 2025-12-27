##🗺️ LoL Intelligent Coach - Development Roadmap

## ✅ Phase 0: Foundation (FERTIG)
- [x] Basic Win Prediction Model (97.9% Accuracy)
- [x] REST API (Flask)
- [x] Railway Deployment
- [x] Streamlit Frontend
- [x] Data Collection Pipeline

---

## ✅ Phase 1: Auto-Learning System (COMPLETED)

### 1.1 Automatische Datensammlung
```bash
# Einmaliges Update
python auto_trainer.py --mode once --collect

# Kontinuierlich (alle 24h)
python auto_trainer.py --mode schedule --interval 24 --collect
```

**Features:**
- ✅ Automatische Match-Sammlung aus diversen Quellen
- ✅ Intelligente Model-Verbesserung (nur wenn besser)
- ✅ Backup-System für alte Models
- ✅ Performance-Tracking über Zeit
- ✅ Auto-Trainer getestet (97.9% Accuracy)
- [ ] Auto-Deploy zu Railway (git push automation)
- [ ] Email-Benachrichtigung bei Verbesserungen

### 1.2 Data Quality
- ✅ Diverse Player Sampling (Smart Collector)
- [ ] Duplicate Detection
- [ ] Outlier Removal
- [ ] Balance Check (Win/Loss Ratio)
- [ ] Elo-Distribution Monitoring

---

## ✅ Phase 2: Champion-basierte Analyse (COMPLETED - Basic)

### 2.1 Champion Data Collection
```python
# Neue Datenstruktur
{
    "match_id": "...",
    "game_duration": 20,
    "blue_team": {
        "champions": ["Jinx", "Thresh", "Zed", "Vi", "Orianna"],
        "roles": ["ADC", "Support", "Mid", "Jungle", "Top"],
        "items": [...]
    },
    "red_team": {...},
    "winner": "blue"
}
```

**Tasks:**
- ✅ Erweitere Data Collector für Champion-Daten (`collect_champion_data.py`)
- ✅ Item-Build Extraction
- ✅ Role Detection
- ✅ Champion Win-Rate Database (172 Champions)
- [ ] Champion Synergy Matrix

### 2.2 Champion Win-Rate Model
```python
class ChampionMatchupPredictor:
    """Vorhersage basierend auf Champion-Matchups"""

    def predict(self, blue_champs, red_champs):
        # Berücksichtigt:
        # - Individual Champion Win-Rates ✅
        # - Team Average Win-Rate ✅
        # - Champion Encodings ✅
        pass
```

- ✅ Champion Win-Rate Database (champion_stats.json)
- ✅ Basic Champion Matchup Model (61.6% Accuracy)
- ✅ Champion Predictor trained and saved
- [ ] Matchup-Matrix (jeder vs jeden)
- [ ] Synergy-Score Berechnung
- [ ] Counter-Pick Detection

### 2.3 Item Recommendation Engine
```python
class ItemRecommendationEngine:
    """Intelligente Item-Empfehlungen"""

    def recommend_items(self, champion, role, enemy_team, game_state):
        # Faktoren:
        # - Champion Core Items
        # - Situational Items (gegen enemy team)
        # - Win-Rate nach Item-Build
        # - Game State (ahead/behind)
        pass
```

- ✅ Item-Build Database (item_builds.json)
- ✅ Item Win-Rates per Champion
- [ ] Item Recommendation API
- [ ] Situational Item Logic (vs AP/AD/Tank)
- [ ] Timing Recommendations (Early/Mid/Late)
- [ ] Cost-Efficiency Analysis

---

## 📸 Phase 3: Screenshot-Erkennung (Computer Vision)

### 3.1 Champion Select Recognition
```python
import cv2
from PIL import Image
import pytesseract  # OCR
import torch  # Deep Learning

class ChampionSelectDetector:
    """Erkenne Champions aus Screenshot"""

    def detect_champions(self, screenshot_path):
        # 1. Champion Portraits erkennen
        # 2. OCR für Champion-Namen
        # 3. Team-Zuordnung (Blue/Red)
        # 4. Role Detection
        pass
```

**Dependencies:**
```bash
pip install opencv-python pillow pytesseract torch torchvision
```

**Tasks:**
- [ ] Champion Portrait Dataset (140 Champions)
- [ ] Image Classification Model
- [ ] OCR Integration
- [ ] Bounding Box Detection
- [ ] Screenshot Templates (verschiedene Auflösungen)

### 3.2 In-Game HUD Recognition
```python
class GameStateDetector:
    """Erkenne Game-State aus In-Game Screenshot"""

    def detect_game_state(self, screenshot_path):
        # Erkenne:
        # - Gold (beide Teams)
        # - Kills/Deaths
        # - Towers
        # - Dragons/Barons
        # - Spielzeit
        pass
```

- [ ] HUD Template Matching
- [ ] OCR für Zahlen (Gold, Kills, etc.)
- [ ] Icon Detection (Dragon/Baron)
- [ ] Mini-Map Analysis

### 3.3 Frontend Upload
```python
# In app.py
uploaded_file = st.file_uploader("📸 Upload Champion Select Screenshot", type=['png', 'jpg'])

if uploaded_file:
    detector = ChampionSelectDetector()
    blue_champs, red_champs = detector.detect_champions(uploaded_file)

    # Auto-fill Form
    st.session_state.blue_champions = blue_champs
    st.session_state.red_champions = red_champs
```

---

## 🧠 Phase 4: Spielstrategie-Empfehlungen

### 4.1 Role-Specific Advice
```python
class StrategyAdvisor:
    """Gib spezifische Spieltipps"""

    def get_advice(self, champion, role, matchup, game_state):
        return {
            "laning_phase": "Play safe, farm under tower",
            "focus_target": "Focus enemy ADC in fights",
            "itemization": "Rush Zhonya's vs Zed",
            "macro_play": "Split-push bot lane after 20min"
        }
```

**Advice-Kategorien:**
- [ ] Laning Phase Tips
- [ ] Teamfight Positioning
- [ ] Target Priority
- [ ] Map Awareness Reminders
- [ ] Objective Timing

### 4.2 Win-Condition Analysis
```python
def analyze_win_condition(blue_team, red_team, game_state):
    """Wie gewinnt mein Team?"""

    # Beispiele:
    # - "Your team scales better - stall to late game"
    # - "Enemy has better late - end before 30min"
    # - "Focus Baron control - you have better teamfight"
    pass
```

### 4.3 Danger Warnings
```python
def check_threats(my_champion, enemy_team):
    """Warne vor gefährlichen Matchups"""

    threats = []
    # "⚠️ Enemy Zed can one-shot you - buy Zhonya's"
    # "⚠️ Enemy has 3 hard CC - buy QSS"
    # "⚠️ Enemy team comp scales harder - win early"

    return threats
```

---

## 🎨 Phase 5: Advanced Frontend

### 5.1 Pre-Game Analysis Tab
```
Tab 1: Champion Select
├── Upload Screenshot ODER Manual Input
├── Champion Portraits anzeigen
├── Win-Probability
├── Matchup-Analysis
└── Recommendations
    ├── Wer sollte bannen
    ├── Counter-Picks
    └── Team-Composition Score
```

### 5.2 In-Game Coach Tab
```
Tab 2: Live Game
├── Upload Screenshot (während Spiel)
├── Aktueller Game-State
├── Win-Probability Update
├── Item Recommendations
└── Strategic Advice
    ├── Was kaufen (Next Item)
    ├── Wo auf Map sein
    ├── Welche Objectives priorisieren
```

### 5.3 Post-Game Analysis Tab
```
Tab 3: Match Review
├── Match-Historie hochladen
├── Fehler-Analyse
├── Verbesserungs-Vorschläge
└── Learning Points
```

---

## 📦 Dependencies Update

```txt
# requirements.txt ergänzen:

# Auto-Training
schedule>=1.1.0

# Computer Vision
opencv-python>=4.8.0
pillow>=10.0.0
pytesseract>=0.3.10

# Deep Learning (optional für CV)
torch>=2.0.0
torchvision>=0.15.0

# OCR Enhancement
easyocr>=1.7.0  # Alternative zu pytesseract

# Champion Data
requests-cache>=1.1.0  # Cache für API calls
```

---

## 🚀 Deployment Strategy

### Development
```bash
# Lokal testen
streamlit run app.py

# Auto-Trainer lokal
python auto_trainer.py --mode once --collect
```

### Production
```bash
# Railway: API + Auto-Trainer (Cron Job)
# Streamlit Cloud: Frontend
# GitHub Actions: Scheduled Model Updates
```

---

## 📊 Success Metrics

### Model Performance
- [ ] Win Prediction: >98% Accuracy
- [ ] Champion Matchup: >85% Accuracy
- [ ] Item Recommendation: >80% Player Satisfaction

### User Experience
- [ ] Screenshot Detection: >95% Accuracy
- [ ] Response Time: <2s für Predictions
- [ ] User Retention: >50% return users

---

## 🎯 MVP (Minimum Viable Product) - Next 2 Weeks

**Week 1:**
1. ✅ Auto-Trainer funktionsfähig
2. [ ] Champion-Daten in Collector integrieren
3. [ ] Champion Win-Rate Model (basic)
4. [ ] Item Recommendation (rule-based)

**Week 2:**
1. [ ] Screenshot Upload im Frontend
2. [ ] Basic OCR für Champion-Namen
3. [ ] Frontend: Champion-Input anstatt nur Stats
4. [ ] Erste strategische Empfehlungen

---

## 💡 Future Ideas (Nice-to-Have)

- [ ] Discord Bot Integration
- [ ] Twitch Extension
- [ ] Mobile App
- [ ] Replay Analysis (LOL Replay Files)
- [ ] Custom Champion Builds speichern
- [ ] Community-Features (Build-Sharing)
- [ ] Multi-Language Support
- [ ] Voice Commands (während Spiel)

---

**Let's build the smartest LoL Coach! 🚀**

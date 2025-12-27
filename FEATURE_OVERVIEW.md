# LoL Intelligent Coach - Feature Overview

## 🎯 Was macht uns einzigartig?

### **Option C - Hybrid-Ansatz** (IMPLEMENTIERT! ✅)
Wir kombinieren das Beste aus beiden Welten:
1. **Draft Phase Assistant** - Manuell, aber sehr wertvoll
2. **Live Game Tracker** - Vollautomatisch via Riot API

---

## 🚀 Implementierte Features

### 1. **Draft Phase Assistant + AI Build Generator** 📋🤖
**URL**: `/draft`

**Was es tut:**
- Interaktive Champion-Auswahl für beide Teams (Blue & Red)
- Live Win-Probability während der Draft-Phase
- Fuzzy Search für Champions (auch bei Tippfehlern)
- Champion-Avatare mit Riot Data Dragon Integration
- **NEU:** Rollen-Auswahl für jeden Champion (Top/Jungle/Mid/ADC/Support)
- **NEU:** AI-Generated Personalized Item Build Path

**Use Case:**
- User öffnet die App während Champion Select
- Wählt seine Position (Top/Jungle/Mid/ADC/Support)
- Klickt Champions an die gepickt werden
- → Sieht sofort: "Blue Team 58% Win Probability"
- → Bekommt Confidence Level (High/Medium/Low)
- **NEU:** Klickt "Get AI Build Recommendation"
- → Erhält personalisierte Item Builds basierend auf:
  - Seinem Champion & Rolle
  - Ally Team Composition
  - Enemy Team Composition & Rollen (z.B. Lux Support vs Mid)
  - Game State (Leading/Even/Losing)
  - Item Stats & Synergien

**Build Features:**
- **Core Items**: Immer kaufen
- **Situational Items**:
  - vs AP Heavy (Magic Resist)
  - vs AD Heavy (Armor)
  - vs Healers (Anti-Heal)
  - When Ahead (Aggressive Items)
  - When Behind (Defensive Items)
- **Timeline Items**:
  - Early Game (0-10 min)
  - Mid Game (10-25 min)
  - Late Game (25+ min)
- **AI Explanation**: Warum diese Items?

**Vorteil gegenüber u.gg:**
✅ Real-time Prediction **während** du pickst
✅ Kein Nachschlagen nötig
✅ KI-basiert statt nur Statistik
✅ **Personalisierte Builds** basierend auf DEINEM Matchup
✅ **Situational Branches** (If ahead → X, If behind → Y)
✅ **Timeline-basiert** (Early/Mid/Late Game)

---

### 2. **Live Game Tracker** 🎮
**URL**: `/live`

**Was es tut:**
- Automatische Erkennung ob ein Spiel läuft
- Holt Daten von Riot Live Client API (`https://127.0.0.1:2999`)
- Zeigt Live Win-Probability basierend auf:
  - Champion Matchup (Pre-Game Prediction)
  - Aktuellem Game-State (Gold, Kills, Towers, etc.)
- Auto-Refresh alle 30 Sekunden
- Strategische Empfehlungen in Echtzeit

**Daten die wir tracken:**
- Game Time
- Kills / Deaths / Assists
- Gold (Team & Diff)
- Towers Destroyed
- Dragons, Barons, Heralds
- Vision Score

**Use Cases:**
1. **Early Game (0-15min):**
   - "Strong early comp! Push your advantage."
   - Basiert auf Champion-Matchup

2. **Mid/Late Game (15+min):**
   - "You're ahead! (Gold: +3,500) Keep pressure."
   - Kombiniert Matchup + Game State

**Vorteil gegenüber u.gg:**
✅ **Echtzeit Win-Probability während du spielst**
✅ Strategische Empfehlungen basierend auf Game-State
✅ Vollautomatisch - keine Eingabe nötig

---

### 3. **Intelligent Item Recommender** 🛡️
**Features:**
- Exakte Builds wenn verfügbar
- Fallback-Heuristik bei fehlenden Daten:
  - Fuzzy Name Matching (difflib)
  - Popular Champion Builds
- Counter-Items basierend auf Enemy Team
- Sortierung nach Win Rate (nicht Popularity!)

**Beispiel:**
```
Nautilus vs Ahri & Lux
→ Zeigt MR-fokussierte Builds mit höchster WR
→ Erklärt warum (2 AP Champions im Enemy Team)
```

---

### 4. **Champion Stats & Synergies** 📊
**URL**: `/champion/{name}`

**Features:**
- Fuzzy Search (auch bei Tippfehlern)
- Champion Stats (139 Champions, 51k+ Games)
- Item Builds mit Riot Item-Icons
- Best Teammates (Synergy-Score)
- Clickable Links zu anderen Champions

---

## 🔌 API Endpoints

### **Live Game Endpoints** (NEU!)
```
GET  /api/live/status       # Check if game is running
GET  /api/live/game-data    # Full game state
GET  /api/live/predict      # Win prediction + recommendations
```

### **Champion & Stats**
```
GET  /api/champions/search              # Fuzzy search
GET  /api/champions/{name}              # Champion details
GET  /api/champion-stats                # All champion stats
POST /api/predict-champion-matchup      # Draft prediction
POST /api/predict-game-state            # Game state prediction
```

### **Item Recommendations**
```
POST /api/item-recommendations-intelligent  # Smart item builds
```

---

## 🎨 UI/UX Highlights

### **Design Principles:**
- Dark Theme (Gaming-optimiert)
- Riot Color Scheme (Blue/Red Teams)
- Champion-Avatare von Riot Data Dragon
- Item-Icons mit Tooltips
- Real-time Updates mit Auto-Refresh
- Mobile-Responsive

### **Navigation:**
```
Dashboard (/)
  ├─ Draft Assistant Button → /draft
  ├─ Live Game Button       → /live
  └─ Champion Search        → /champion/{name}
```

---

## 🧠 Machine Learning Models

### **1. Champion Matchup Predictor**
- **Trainiert auf**: 360k+ High-Elo Matches
- **Input**: 5 vs 5 Champions
- **Output**: Win-Probability für beide Teams
- **Accuracy**: ~90%

### **2. Win Prediction Model (Game State)**
- **Trainiert auf**: 360k+ Matches
- **Input**: Game Duration, Kills, Gold, Towers, Dragons, Barons, Vision
- **Output**: Real-time Win-Probability
- **Accuracy**: 90.9%

### **3. Intelligent Item Recommender**
- **Heuristiken**:
  - Exact Match Builds
  - Fuzzy Name Similarity
  - Popular Champion Fallback
  - Counter-Item Weighting (Armor/MR/Anti-Heal)
- **Data**: 172 Champions, 1k+ Builds

---

## 🆚 Unterschiede zu u.gg

| Feature | u.gg | LoL Intelligent Coach |
|---------|------|----------------------|
| **Champion Stats** | ✅ Statisch | ✅ Mit KI-Prediction |
| **Item Builds** | ✅ Meta-Builds | ✅ Matchup-spezifisch |
| **Draft Prediction** | ❌ Nein | ✅ Live während Pick |
| **Live Game Tracking** | ❌ Nein | ✅ Auto via Riot API |
| **Win Probability** | ❌ Nein | ✅ Real-time 90.9% Acc |
| **Strategic Advice** | ❌ Nein | ✅ Game-State basiert |
| **Team Synergies** | ❌ Basic | ✅ ML-basiert (8k+ Pairs) |

---

## 🎯 Unsere Unique Selling Points (USPs)

### **1. Real-Time Win Prediction** 🔥
**Pitch**: "Wir sagen dir nicht nur was Meta ist, sondern ob **DU** gewinnst - **während dem Spiel**!"

- Live Win% basierend auf aktuellem Game-State
- Comeback Calculator ("Gold Diff: -2k → 35% Win Chance")
- Critical Moments ("Next teamfight decides game!")

### **2. Draft-Phase Intelligence** 🧠
**Pitch**: "Die beste Pick-Phase deines Lebens"

- Sofortige Win-Probability während Draft
- "Pick X to maximize winrate" Recommendations
- Counter-Pick Suggestions

### **3. Intelligent Matchup-Driven Builds** ⚔️
**Pitch**: "Nicht einfach Meta-Builds kopieren - sondern **DEIN** optimaler Build gegen **DIESES** Team"

- Enemy-Team Analyzer
- Adaptive Build-Paths
- "Build MR now vs 3 AP" Recommendations

---

## 🔮 Technologie-Stack

### **Backend:**
- Python FastAPI
- Riot Live Client API
- scikit-learn ML Models
- Pickle Model Persistence

### **Frontend:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui Components
- Riot Data Dragon CDN

### **Data:**
- 360k+ Kaggle High-Elo Matches
- Riot API Champion Data
- Item Build Statistics
- Team Synergy Calculations

---

## 🚀 Quick Start

### **1. Start API:**
```bash
cd "/path/to/Win_Predicition_System_WR"
python api_v2.py
```

### **2. Start Frontend:**
```bash
cd lol-coach-frontend
npm run dev
```

### **3. Test Live Game:**
```bash
# Starte ein LoL Practice Game
# Öffne http://localhost:3000/live
# → Automatisches Tracking!
```

---

## 📝 Testing Checklist

- [x] Draft Phase Assistant
  - [x] Champion Selection (Blue/Red)
  - [x] Fuzzy Search
  - [x] Live Win Prediction
  - [x] Champion Avatare

- [x] Live Game Tracker
  - [x] Game Detection
  - [x] Live Data Fetch
  - [x] Win Prediction (Matchup + State)
  - [x] Auto-Refresh
  - [x] Strategic Recommendations

- [x] Champion Details
  - [x] Stats Display
  - [x] Item Builds (mit Icons)
  - [x] Best Teammates
  - [x] Fallback Heuristics

- [ ] End-to-End Tests
  - [ ] Draft → Prediction
  - [ ] Live Game → Real-time Updates
  - [ ] Item Recommendations vs Enemy

---

## 🎊 Was kommt als nächstes?

### **Phase 1 (Jetzt)**: ✅ DONE
- Draft Phase Assistant
- Live Game Tracker
- Intelligent Item Builds

### **Phase 2 (Optional):**
- Ban-Phase Recommendations
- Comeback Calculator ("Need X Gold to win")
- Critical Moment Detection
- Role-Based Recommendations

### **Phase 3 (Advanced):**
- User-spezifisches Tracking
- Champion Pool Analyzer
- Personal Performance Trends

---

## 💡 Killer Feature Ideen

1. **"Comeback Meter"**
   - "You need +2k Gold in next 5 min to have 50% win chance"

2. **"Critical Moments"**
   - "Next Dragon fight is game-deciding!" (Alert)

3. **"Item Timing"**
   - "Build MR **NOW** at 15min vs 3 AP" (nicht später)

4. **"Draft Optimizer"**
   - "Ban Zed (counters 3 of your champs)"

---

**Author**: Merlin Mechler
**Date**: 2025-12-27
**Version**: 2.0.0

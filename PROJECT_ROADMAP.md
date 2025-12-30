# 🎯 PROJECT ROADMAP - LoL Intelligent Coach (Das Meisterwerk)

**Version:** 2.0
**Erstellt:** 2025-12-29
**Autor:** Merlin Mechler
**Typ:** Data Science Masterarbeit / Production-Ready Tool

---

## 📋 EXECUTIVE SUMMARY

**Vision:** Ein intelligentes Echtzeit-Coaching-System für League of Legends, das durch Kombination von Machine Learning, Ontologie und Heuristik präzise Vorhersagen und Empfehlungen liefert.

**Kern-Innovation:** Hybrid-System aus:
- 🤖 **Machine Learning** (Random Forest, Gradient Boosting) für Muster-Erkennung
- 🧠 **Ontologie** (PostgreSQL-basiert) für Wissensrepräsentation
- ⚡ **Heuristik** (Regelbasiert) für kausale Logik

**Zielgruppe:**
- League of Legends Spieler (Bronze bis Master)
- Data Science Portfolio / Abschlussarbeit
- Potenzielle Monetarisierung (Premium Features)

---

## 🏗️ SYSTEM-ARCHITEKTUR

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js 14)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Draft Phase  │  │ Item Builder │  │ Live Tracker │      │
│  │   UI         │  │     UI       │  │     UI       │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓ REST API
┌─────────────────────────────────────────────────────────────┐
│              BACKEND API (FastAPI / Python)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          Intelligent Recommendation Engine           │   │
│  │  ┌────────────┐ ┌──────────┐ ┌──────────────────┐  │   │
│  │  │ ML Models  │ │ Ontology │ │ Heuristic Rules  │  │   │
│  │  │ (RF, GB)   │ │ (Graph)  │ │ (Rule Engine)    │  │   │
│  │  └────────────┘ └──────────┘ └──────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Draft        │  │ Game State   │  │ Item         │      │
│  │ Predictor    │  │ Predictor    │  │ Recommender  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   DATA LAYER                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ PostgreSQL   │  │ Training     │  │ Riot API     │      │
│  │ (Ontologie)  │  │ Data (CSV)   │  │ (Live/Data)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📅 5-MONATS-ENTWICKLUNGSPLAN

### **MONAT 1: Data Engineering & Fundament** ✅ (Jan 2025)
**Parallel zur Weiterbildung:** SQL, Data Modeling, ETL

#### Woche 1-2: PostgreSQL Setup & Ontologie
- [x] PostgreSQL Installation & Konfiguration
- [ ] Champion Ontologie Schema (Tabellen: champions, roles, types, tags, matchups, synergies)
- [ ] Item Ontologie Schema (Tabellen: items, components, counters, synergies, tags)
- [ ] Ward Rules Schema (Tabellen: ward_rules, ward_spots, game_phases)
- [ ] Champion Aliases & Fuzzy Search Datenbank

**Deliverables:**
- ✅ PostgreSQL Datenbank mit vollständigem Ontologie-Schema
- ✅ SQL-Scripts für Initialisierung
- ✅ Dokumentation der Datenbank-Architektur

#### Woche 3-4: Data Dragon API Integration
- [ ] Riot Data Dragon API Crawler für Items (alle Items + Stats + Build Paths)
- [ ] Riot Data Dragon API Crawler für Champions (Namen, IDs, Rollen, Stats)
- [ ] Automatisches Import-Script (Data Dragon → PostgreSQL)
- [ ] Champion Aliases manuell pflegen (MF, TF, Naut, etc.)

**Deliverables:**
- ✅ Item-Datenbank vollständig (alle Items mit Stats, Kosten, Build Paths)
- ✅ Champion-Datenbank vollständig (172 Champions mit Metadaten)
- ✅ Tägliches Update-Script für neue Patches

**Skills Development:**
- SQL (Joins, Normalisierung, Indexing)
- ETL-Pipelines (Extract, Transform, Load)
- API Integration (REST, Rate Limiting)

---

### **MONAT 2: Feature Engineering & Champion System** (Feb 2025)
**Parallel zur Weiterbildung:** Feature Engineering, Exploratory Data Analysis

#### Woche 1-2: Champion Matchup Analyse
- [ ] Historische Match-Daten analysieren (Champion Win Rates)
- [ ] Champion Matchup Matrix berechnen (wer countert wen?)
- [ ] Champion Synergy Matrix berechnen (wer synergiert mit wem?)
- [ ] Feature Engineering: Team Composition Scores
  - CC-Score (Crowd Control)
  - Engage-Score (Initiation Potential)
  - Peel-Score (Protection)
  - Damage-Mix (AD/AP Ratio)
  - Win-Condition Score (Early/Mid/Late)

**Deliverables:**
- ✅ Champion Matchup Matrix (172x172)
- ✅ Champion Synergy Matrix (172x172)
- ✅ Team Composition Scoring System

#### Woche 3-4: Fuzzy Search System
- [ ] Levenshtein Distance Implementation für Tippfehler-Toleranz
- [ ] Soundex/Metaphone für phonetische Suche
- [ ] Semantic Search Engine (Ontologie-basiert)
- [ ] Multi-Layer Search Algorithmus (Exact → Alias → Fuzzy → Phonetic → Semantic)
- [ ] Search API Endpoint (/api/champions/search?q=nautlisus)

**Deliverables:**
- ✅ Intelligent Champion Search API
- ✅ Benchmark: <50ms Response Time, >95% Recall bei Tippfehlern
- ✅ Unit Tests für alle Search-Layers

**Skills Development:**
- Feature Engineering (Domain-spezifische Features)
- String Matching Algorithmen
- API Design (REST Best Practices)

---

### **MONAT 3: Machine Learning Models** (März 2025)
**Parallel zur Weiterbildung:** Machine Learning, Supervised Learning, Model Evaluation

#### Woche 1-2: Draft Phase Predictor (Champion Matchup Model)
- [x] Training Data: 12,834 Matches mit Champion Picks ✅
- [x] Features: 17 (Champion IDs + Win Rates) ✅
- [x] Model: Random Forest ✅
- [ ] **Erweiterte Features hinzufügen:**
  - [ ] Team Composition Scores (aus Monat 2)
  - [ ] Synergy Scores
  - [ ] Counter Scores
  - [ ] Meta-Features (Patch, Elo, Region)
- [ ] **Model Re-Training mit erweiterten Features**
- [ ] **Target:** >60% Accuracy (aktuell: 51.69%)

**Deliverables:**
- ✅ Champion Matchup Predictor Model (>60% Accuracy)
- ✅ Feature Importance Analysis
- ✅ Model Performance Report

#### Woche 3-4: Game State Predictor (Timeline Model)
- [ ] **Timeline Data Crawling:** 5,000 Matches mit 10/15/20min Snapshots
- [ ] Features: 140 (Gold, XP, CS, Kills, Objectives @ 10/15/20min)
- [ ] Model: Random Forest + Gradient Boosting (Ensemble)
- [ ] **Target:** >70% Accuracy (deutlich besser als Draft-Phase!)
- [ ] Multi-Snapshot Training (beste Snapshot-Zeit finden)

**Deliverables:**
- ✅ Game State Predictor Model (>70% Accuracy @ 15min)
- ✅ Comparative Analysis (10min vs 15min vs 20min)
- ✅ Feature Importance: Welche Stats sind am wichtigsten?

**Skills Development:**
- Supervised Machine Learning (Classification)
- Feature Engineering (Time-Series Features)
- Model Evaluation (Accuracy, ROC-AUC, Confusion Matrix)
- Hyperparameter Tuning

---

### **MONAT 4: Heuristik & Recommendation Engine** (April 2025)
**Parallel zur Weiterbildung:** Business Logic, Decision Systems

#### Woche 1-2: Champion Recommendation Heuristik
- [ ] **Rule Engine Implementation**
- [ ] Heuristik-Regeln definieren:
  - [ ] Team Balance (Need AP? Need Tank? Need Engage?)
  - [ ] Counter-Pick Logic (Gegner hat X → Empfehle Y)
  - [ ] Synergy Logic (Team hat X → Empfehle Y)
  - [ ] Meta-Awareness (High Win-Rate Champions)
  - [ ] Role-Specific Logic (Support anders als Mid)
- [ ] **Hybrid Recommender:** ML + Heuristik kombinieren
- [ ] Confidence Scores & Explanations ("Empfehle X, weil...")

**Deliverables:**
- ✅ Champion Recommendation API (/api/draft/recommend)
- ✅ Top-3 Champion-Empfehlungen mit Begründung
- ✅ Real-Time Update während Draft

#### Woche 3-4: Item Recommendation Heuristik
- [ ] **Item Counter-Logic:**
  - [ ] Anti-Heal gegen Healer (Soraka, Yuumi → Grievous Wounds)
  - [ ] Armor gegen AD-heavy Teams
  - [ ] MR gegen AP-heavy Teams
  - [ ] Penetration gegen Tanks
- [ ] **Item Build Path Optimization:**
  - [ ] Komponenten-Reihenfolge (was kaufe ich zuerst?)
  - [ ] Power-Spike Timing (wann ist Item fertig = fight?)
  - [ ] Gold-Effizienz Berechnung
- [ ] **Dynamic Build Adjuster:**
  - [ ] Basis-Build aus Datenbank (U.GG-Style)
  - [ ] Anpassung basierend auf Gegner-Items (live)
  - [ ] Anpassung basierend auf Game State (vorne/hinten)

**Deliverables:**
- ✅ Item Recommendation API (/api/items/recommend)
- ✅ Build Path mit Begründung (Schritt-für-Schritt)
- ✅ Dynamische Anpassung an Matchup

**Skills Development:**
- Rule-Based Systems
- Hybrid AI (ML + Logic)
- Explainable AI (warum diese Empfehlung?)

---

### **MONAT 5: Live Game Tracking & Production** (Mai 2025)
**Parallel zur Weiterbildung:** Deployment, Monitoring, Abschlussarbeit

#### Woche 1-2: Live Game Integration
- [ ] **Riot Live Client API Integration**
  - [ ] Connection Handler (localhost:2999)
  - [ ] Live Data Polling (alle 30-60s)
  - [ ] Game State Parsing (Gold, Kills, Items, Objectives)
- [ ] **Live Item Recommendations:**
  - [ ] "Du hast 1200 Gold → Kaufe X"
  - [ ] Item-Anpassung basierend auf Gegner-Items
  - [ ] Power-Spike Warnings ("Dein 3-Item Spike in 800 Gold!")
- [ ] **Live Win Probability:**
  - [ ] Game State Model Inference (real-time)
  - [ ] Probability Graph (verlauf über Zeit)

**Deliverables:**
- ✅ Live Game Tracker API (/api/live/status, /api/live/recommend)
- ✅ Real-Time Updates (WebSocket oder Polling)
- ✅ Frontend Integration

#### Woche 3-4: Ward System & Comeback-Strategien
- [ ] **Dynamic Ward Recommendations:**
  - [ ] Ward Spot Database (optimal locations per game phase)
  - [ ] Heuristik-Regeln:
    - [ ] Vor Objectives (Drake spawns in 60s → Ward pit)
    - [ ] Defensive Wards wenn hinten (eigener Jungle)
    - [ ] Offensive Wards wenn vorne (feindlicher Jungle)
  - [ ] Priority Scoring (welcher Ward jetzt am wichtigsten?)
- [ ] **Comeback-Strategie Engine:**
  - [ ] IF gold_diff < -3000 THEN empfehle:
    - [ ] Safe Farming Spots
    - [ ] Vision Control Zones
    - [ ] Power Spike Timing ("Farm bis Item X")
    - [ ] Objective Trading ("Opfere Drake, nimm Top Tower")

**Deliverables:**
- ✅ Ward Recommendation API (/api/live/wards)
- ✅ Comeback Strategy API (/api/live/strategy)
- ✅ Interactive Map mit Ward-Spots

#### Woche 4: Production Deployment & Abschlussarbeit
- [ ] **Deployment:**
  - [ ] Vercel (Frontend + Python Serverless Functions)
  - [ ] Supabase/RDS (PostgreSQL)
- [ ] **Monitoring:**
  - [ ] Sentry (Error Tracking)
  - [ ] Plausible (Analytics)
  - [ ] Model Performance Monitoring
- [ ] **Abschlussarbeit schreiben:**
  - [ ] Einleitung (Problem, Vision)
  - [ ] Methodik (Ontologie + ML + Heuristik)
  - [ ] Implementation (Architektur, Code)
  - [ ] Evaluation (Model Performance, User Feedback)
  - [ ] Diskussion (Learnings, Future Work)

**Deliverables:**
- ✅ Production-Ready Tool (live unter eigener Domain)
- ✅ Abschlussarbeit (40-60 Seiten)
- ✅ Portfolio-Piece für Data Science Bewerbungen

**Skills Development:**
- Deployment (Cloud, DevOps)
- Monitoring & Analytics
- Technical Writing

---

## 🗄️ POSTGRESQL DATENBANK-SCHEMA

### **Champions Ontologie**

```sql
-- ============================================================================
-- CHAMPIONS BASE TABLE
-- ============================================================================
CREATE TABLE champions (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    name_normalized VARCHAR(50) NOT NULL, -- lowercase, no spaces
    soundex_code VARCHAR(10),              -- Phonetic code für Fuzzy Search
    key VARCHAR(50),                       -- Riot API Key (z.B. "Annie")
    title VARCHAR(100),                    -- "the Dark Child"
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_champions_name_normalized ON champions(name_normalized);
CREATE INDEX idx_champions_soundex ON champions(soundex_code);

-- ============================================================================
-- CHAMPION ALIASES (für Fuzzy Search)
-- ============================================================================
CREATE TABLE champion_aliases (
    id SERIAL PRIMARY KEY,
    champion_id INTEGER REFERENCES champions(id) ON DELETE CASCADE,
    alias VARCHAR(50) NOT NULL,
    alias_type VARCHAR(20), -- 'abbreviation', 'nickname', 'common_typo'
    usage_frequency FLOAT DEFAULT 0.5 -- Wie oft wird dieser Alias genutzt?
);

-- Beispiele:
-- Annie: Ani, Dark Child
-- Miss Fortune: MF, Fortune
-- Nautilus: Naut, Nautlisus (typo)

CREATE INDEX idx_aliases_alias ON champion_aliases(alias);

-- ============================================================================
-- CHAMPION ROLES
-- ============================================================================
CREATE TABLE champion_roles (
    champion_id INTEGER REFERENCES champions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- Top, Jungle, Mid, ADC, Support
    priority INTEGER NOT NULL, -- 1 = Primary, 2 = Secondary, 3 = Off-Meta
    play_rate FLOAT,           -- Wie oft wird Champion in dieser Role gespielt
    win_rate FLOAT,            -- Win-Rate in dieser Role
    PRIMARY KEY (champion_id, role)
);

-- ============================================================================
-- CHAMPION TYPES/CLASSES (Ontologie)
-- ============================================================================
CREATE TABLE champion_types (
    champion_id INTEGER REFERENCES champions(id) ON DELETE CASCADE,
    type_category VARCHAR(30) NOT NULL, -- 'class', 'damage_type', 'range', 'difficulty'
    type_value VARCHAR(30) NOT NULL,    -- 'Mage', 'AP', 'Ranged', 'Easy'
    relevance FLOAT DEFAULT 1.0,        -- Wie relevant ist dieser Type? (0-1)
    PRIMARY KEY (champion_id, type_category, type_value)
);

-- Beispiel für Annie:
-- (Annie, 'class', 'Mage', 1.0)
-- (Annie, 'class', 'Burst', 0.8)
-- (Annie, 'damage_type', 'AP', 1.0)
-- (Annie, 'range', 'Ranged', 1.0)
-- (Annie, 'difficulty', 'Easy', 1.0)

-- ============================================================================
-- CHAMPION TAGS (für semantische Suche)
-- ============================================================================
CREATE TABLE champion_tags (
    champion_id INTEGER REFERENCES champions(id) ON DELETE CASCADE,
    tag VARCHAR(50) NOT NULL, -- 'tank', 'engage', 'peel', 'burst', 'mobile', 'immobile'
    relevance FLOAT NOT NULL, -- 0-1 Score
    PRIMARY KEY (champion_id, tag)
);

-- Beispiel für Nautilus:
-- (Nautilus, 'tank', 1.0)
-- (Nautilus, 'engage', 0.9)
-- (Nautilus, 'peel', 0.7)
-- (Nautilus, 'cc', 1.0)

CREATE INDEX idx_tags_tag ON champion_tags(tag);

-- ============================================================================
-- CHAMPION MATCHUPS (Counter-Matrix)
-- ============================================================================
CREATE TABLE champion_matchups (
    champion_id INTEGER REFERENCES champions(id) ON DELETE CASCADE,
    opponent_id INTEGER REFERENCES champions(id) ON DELETE CASCADE,
    matchup_score FLOAT NOT NULL, -- -1 (hard countered) to +1 (hard counter)
    lane_matchup_score FLOAT,     -- Spezifisch für Lane-Phase
    teamfight_score FLOAT,         -- Spezifisch für Teamfights
    games_analyzed INTEGER,        -- Wie viele Matches wurden analysiert
    reason TEXT,                   -- "Outranges", "Outdamages", etc.
    PRIMARY KEY (champion_id, opponent_id)
);

-- Beispiel:
-- (Zed, Malphite, -0.8, -0.9, -0.5, 1500, "Armor counters lethality")
-- (Annie, Zed, 0.3, -0.2, 0.6, 800, "Weak in lane, strong in teamfights with AOE stun")

-- ============================================================================
-- CHAMPION SYNERGIES
-- ============================================================================
CREATE TABLE champion_synergies (
    champion1_id INTEGER REFERENCES champions(id) ON DELETE CASCADE,
    champion2_id INTEGER REFERENCES champions(id) ON DELETE CASCADE,
    synergy_score FLOAT NOT NULL, -- 0-1
    synergy_type VARCHAR(50),      -- 'engage_combo', 'peel', 'poke_comp', 'wombo_combo'
    reason TEXT,
    games_analyzed INTEGER,
    PRIMARY KEY (champion1_id, champion2_id)
);

-- Beispiel:
-- (Yasuo, Malphite, 0.9, 'wombo_combo', "Malphite R → Yasuo R = guaranteed knockup")
-- (Jinx, Leona, 0.75, 'engage_follow', "Leona CC allows Jinx safe damage")

-- ============================================================================
-- CHAMPION STATS (Win Rates, Pick Rates)
-- ============================================================================
CREATE TABLE champion_stats (
    champion_id INTEGER REFERENCES champions(id) ON DELETE CASCADE,
    patch VARCHAR(10) NOT NULL,    -- "14.23"
    role VARCHAR(20),               -- Kann NULL sein (overall)
    tier VARCHAR(10),               -- 'S', 'A', 'B', 'C', 'D'
    win_rate FLOAT,
    pick_rate FLOAT,
    ban_rate FLOAT,
    games_analyzed INTEGER,
    last_updated TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (champion_id, patch, role)
);
```

---

### **Items Ontologie**

```sql
-- ============================================================================
-- ITEMS BASE TABLE
-- ============================================================================
CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    name_normalized VARCHAR(100),
    description TEXT,
    plaintext TEXT,                 -- Short description
    total_gold INTEGER NOT NULL,
    base_gold INTEGER,
    sell_gold INTEGER,
    purchasable BOOLEAN DEFAULT TRUE,
    stats JSONB,                    -- Flexibel: {ad: 55, ap: 0, armor: 30, ...}
    passive TEXT,                   -- Passive Ability Text
    active TEXT,                    -- Active Ability Text
    mythic BOOLEAN DEFAULT FALSE,
    legendary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_items_name ON items(name_normalized);

-- ============================================================================
-- ITEM BUILD PATHS (Komponenten)
-- ============================================================================
CREATE TABLE item_components (
    item_id INTEGER REFERENCES items(id) ON DELETE CASCADE,
    component_id INTEGER REFERENCES items(id) ON DELETE CASCADE,
    build_order INTEGER,            -- Reihenfolge (1, 2, 3, ...)
    PRIMARY KEY (item_id, component_id)
);

-- Beispiel: Infinity Edge
-- (3031, 1038, 1) -- BF Sword
-- (3031, 1018, 2) -- Cloak of Agility

-- ============================================================================
-- ITEM TAGS
-- ============================================================================
CREATE TABLE item_tags (
    item_id INTEGER REFERENCES items(id) ON DELETE CASCADE,
    tag VARCHAR(50) NOT NULL, -- 'armor', 'mr', 'ad', 'ap', 'anti_heal', 'penetration'
    value FLOAT,              -- Numerischer Wert (z.B. Armor: 30)
    PRIMARY KEY (item_id, tag)
);

CREATE INDEX idx_item_tags_tag ON item_tags(tag);

-- ============================================================================
-- ITEM COUNTERS (Was countert was?)
-- ============================================================================
CREATE TABLE item_counters (
    item_id INTEGER REFERENCES items(id) ON DELETE CASCADE,
    counters_type VARCHAR(50) NOT NULL, -- 'champion_type', 'damage_type', 'mechanic'
    counters_value VARCHAR(50) NOT NULL, -- 'Assassin', 'AP', 'Healing'
    effectiveness FLOAT NOT NULL,        -- 0-1
    reason TEXT
);

-- Beispiel: Thornmail
-- (3075, 'damage_type', 'AD', 0.9, "Reflects damage + reduces healing")
-- (3075, 'champion_type', 'Assassin', 0.7, "Armor + reflected damage")

-- ============================================================================
-- ITEM SYNERGIES
-- ============================================================================
CREATE TABLE item_synergies (
    item1_id INTEGER REFERENCES items(id) ON DELETE CASCADE,
    item2_id INTEGER REFERENCES items(id) ON DELETE CASCADE,
    synergy_score FLOAT NOT NULL, -- 0-1
    reason TEXT,
    PRIMARY KEY (item1_id, item2_id)
);

-- Beispiel:
-- (3031, 3094, 0.95, "Infinity Edge + Rapid Firecannon = max crit DPS")

-- ============================================================================
-- CHAMPION ITEM BUILDS (Empfohlene Builds aus Daten)
-- ============================================================================
CREATE TABLE champion_item_builds (
    id SERIAL PRIMARY KEY,
    champion_id INTEGER REFERENCES champions(id) ON DELETE CASCADE,
    role VARCHAR(20),
    build_order JSONB NOT NULL,  -- [3006, 3031, 3094, 3087, ...]
    games INTEGER,
    wins INTEGER,
    win_rate FLOAT,
    build_name VARCHAR(50),      -- "Crit Build", "Lethality Build"
    patch VARCHAR(10)
);
```

---

### **Ward & Strategy Ontologie**

```sql
-- ============================================================================
-- WARD SPOTS (Predefined optimal locations)
-- ============================================================================
CREATE TABLE ward_spots (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,     -- "Drake Pit Bush", "Baron Tri-Bush"
    x_coordinate FLOAT NOT NULL,
    y_coordinate FLOAT NOT NULL,
    map_zone VARCHAR(50),           -- "Blue Jungle", "Red Jungle", "River"
    description TEXT
);

-- ============================================================================
-- WARD RULES (Heuristik)
-- ============================================================================
CREATE TABLE ward_rules (
    id SERIAL PRIMARY KEY,
    rule_name VARCHAR(100) NOT NULL,
    game_phase VARCHAR(20),         -- 'Early', 'Mid', 'Late'
    gold_diff_min INTEGER,          -- Nur anwenden wenn Gold-Diff in Range
    gold_diff_max INTEGER,
    objective VARCHAR(50),          -- 'Drake', 'Baron', 'None'
    objective_spawn_time_min INTEGER, -- Sekunden bis Spawn
    objective_spawn_time_max INTEGER,
    ward_spot_id INTEGER REFERENCES ward_spots(id),
    ward_type VARCHAR(20),          -- 'Stealth', 'Control'
    priority VARCHAR(20),           -- 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    reasoning TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Beispiel-Regel:
-- rule_name: "Drake Control Pre-Spawn"
-- game_phase: "Mid"
-- objective: "Drake"
-- objective_spawn_time_min: 30
-- objective_spawn_time_max: 90
-- ward_spot: "Drake Pit Bush"
-- ward_type: "Control"
-- priority: "HIGH"
-- reasoning: "Secure vision before drake spawns to contest safely"

-- ============================================================================
-- STRATEGY RULES (Comeback Logic)
-- ============================================================================
CREATE TABLE strategy_rules (
    id SERIAL PRIMARY KEY,
    rule_name VARCHAR(100) NOT NULL,
    condition_type VARCHAR(50),     -- 'gold_diff', 'tower_diff', 'kill_diff'
    condition_operator VARCHAR(10), -- '<', '>', '<=', '>=', '=='
    condition_value INTEGER,
    game_phase VARCHAR(20),
    strategy_type VARCHAR(50),      -- 'Defensive', 'Aggressive', 'Objective_Trade'
    recommendation TEXT NOT NULL,
    reasoning TEXT NOT NULL
);

-- Beispiel:
-- rule_name: "Defensive Farming"
-- condition_type: "gold_diff"
-- condition_operator: "<"
-- condition_value: -3000
-- strategy_type: "Defensive"
-- recommendation: "Focus safe farming, avoid risky fights. Ward defensively."
-- reasoning: "Team is significantly behind. Need to reach power spikes before fighting."
```

---

## 🛠️ TECHNOLOGY STACK

### **Frontend**
- **Framework:** Next.js 14 (App Router, React Server Components)
- **UI Library:** shadcn/ui (Radix UI + Tailwind CSS)
- **State Management:** Zustand / React Context
- **API Client:** TanStack Query (React Query)
- **Real-Time:** WebSocket / Server-Sent Events
- **Deployment:** Vercel

### **Backend**
- **Framework:** FastAPI (Python 3.11+)
- **ML Libraries:**
  - scikit-learn (Random Forest, Gradient Boosting)
  - joblib (Model Persistence)
  - pandas (Data Processing)
  - numpy (Numerical Computing)
- **Search Libraries:**
  - jellyfish (Phonetic Matching: Soundex, Metaphone)
  - fuzzywuzzy / RapidFuzz (Levenshtein Distance)
- **API Integration:** requests, httpx
- **Deployment:** Vercel Serverless Functions

### **Database**
- **Primary:** PostgreSQL 15+ (Ontologie, Structured Data)
- **Hosting:** Vercel Postgres / Supabase / AWS RDS
- **ORM:** SQLAlchemy (Python)
- **Migrations:** Alembic

### **MLOps**
- **Training:** GitHub Actions (Daily at 04:00 UTC)
- **Model Versioning:** DVC (Data Version Control)
- **Monitoring:** Sentry (Errors), Plausible (Analytics)
- **CI/CD:** GitHub Actions → Vercel

### **Data Sources**
- **Riot Games API:**
  - Match-V5 API (Historical Matches)
  - Match Timeline API (Game State Snapshots)
  - Live Client API (In-Game Data)
  - Data Dragon API (Static Data: Champions, Items)

---

## 📊 SUCCESS METRICS

### **Model Performance**
- ✅ Draft Phase Predictor: **>60% Accuracy** (current: 51.69%)
- ✅ Game State Predictor: **>70% Accuracy** @ 15min
- ✅ Champion Recommendation: **Top-3 includes optimal pick in >80% of cases**
- ✅ Item Recommendation: **User satisfaction >4.0/5.0**

### **System Performance**
- ✅ API Response Time: **<200ms** (p95)
- ✅ Search Response Time: **<50ms**
- ✅ Live Game Update Frequency: **30-60 seconds**
- ✅ Uptime: **>99.5%**

### **User Metrics** (Post-Launch)
- 🎯 **100 Daily Active Users** (Month 1)
- 🎯 **1,000 Daily Active Users** (Month 6)
- 🎯 **>70% 7-Day Retention**
- 🎯 **Avg. Session Duration: >10 minutes**

---

## 🚀 MVP DEFINITION

### **MVP 1: Draft Assistant** (End of Month 3)
**Features:**
- ✅ Champion Selection UI (wähle Team + Gegner)
- ✅ Real-Time Win Probability (nach jedem Pick update)
- ✅ Top-3 Champion Recommendations mit Begründung
- ✅ Fuzzy Champion Search

**Acceptance Criteria:**
- User kann Draft simulieren
- Win Probability wird korrekt angezeigt
- Empfehlungen sind plausibel (manuell geprüft)

### **MVP 2: Item Builder** (End of Month 4)
**Features:**
- ✅ Item Database browsing
- ✅ Initial Build Recommendation (basierend auf Matchup)
- ✅ Build Path Visualization (Komponenten → Final Item)
- ✅ Counter-Item Suggestions

**Acceptance Criteria:**
- User sieht empfohlenen Build
- Build ändert sich basierend auf Gegner-Auswahl
- Begründungen sind klar

### **MVP 3: Live Tracker** (End of Month 5)
**Features:**
- ✅ Live Game Connection (Riot Live Client API)
- ✅ Current Game State Display (Gold, Kills, Objectives)
- ✅ Live Win Probability
- ✅ Dynamic Item Recommendations
- ✅ Ward Recommendations

**Acceptance Criteria:**
- Tool verbindet sich automatisch mit laufendem Game
- Empfehlungen aktualisieren sich alle 30-60s
- User kann Tool auf 2. Monitor nutzen

---

## 📚 LEARNING GOALS (Data Science Skills)

### **Month 1: Data Engineering**
- ✅ PostgreSQL (Schema Design, Normalisierung, Indexing)
- ✅ ETL Pipelines (API → Database)
- ✅ Data Modeling (Ontologie-Design)

### **Month 2: Feature Engineering**
- ✅ Domain-Specific Features (Team Composition Scores)
- ✅ String Matching (Levenshtein, Soundex)
- ✅ Correlation Analysis (Matchups, Synergies)

### **Month 3: Machine Learning**
- ✅ Supervised Learning (Classification)
- ✅ Ensemble Methods (Random Forest, Gradient Boosting)
- ✅ Model Evaluation (Accuracy, ROC-AUC, Feature Importance)
- ✅ Hyperparameter Tuning

### **Month 4: Hybrid AI**
- ✅ Rule-Based Systems (Heuristik)
- ✅ Ontologie + ML Integration
- ✅ Explainable AI (Recommendation Reasoning)

### **Month 5: Production & Deployment**
- ✅ Cloud Deployment (Vercel Single Project)
- ✅ Monitoring & Analytics
- ✅ CI/CD (GitHub Actions)
- ✅ Technical Writing (Abschlussarbeit)

---

## 🎓 ABSCHLUSSARBEIT OUTLINE

**Titel:** "Intelligentes Echtzeit-Coaching-System für League of Legends: Ein Hybrid-Ansatz aus Machine Learning, Ontologie und Heuristik"

### **Struktur (40-60 Seiten):**

1. **Einleitung** (5 Seiten)
   - Problem: Komplexität von LoL, Informationsflut
   - Vision: AI-gestütztes Coaching
   - Forschungsfragen

2. **Theoretischer Hintergrund** (10 Seiten)
   - Machine Learning (Random Forest, Gradient Boosting)
   - Ontologie-basierte Systeme
   - Heuristik & Regelbasierte Systeme
   - Hybrid AI Ansätze

3. **Methodik** (10 Seiten)
   - Datensammlung (Riot API)
   - Ontologie-Design (PostgreSQL Schema)
   - Feature Engineering
   - Model Training & Evaluation

4. **Implementation** (15 Seiten)
   - Systemarchitektur
   - Draft Phase Predictor
   - Game State Predictor
   - Recommendation Engine (Hybrid)
   - Frontend/Backend Integration

5. **Evaluation** (10 Seiten)
   - Model Performance (Accuracy, ROC-AUC)
   - System Performance (Response Time, Uptime)
   - User Feedback (Umfragen, Interviews)

6. **Diskussion** (5 Seiten)
   - Learnings
   - Limitationen
   - Future Work

7. **Fazit** (3 Seiten)

**Anhang:**
- Datenbank-Schema
- Code-Snippets (wichtige Algorithmen)
- User Survey Ergebnisse

---

## 🔄 DAILY/WEEKLY WORKFLOWS

### **Daily (während Entwicklung):**
- 04:00 UTC: Automatisches Data Crawling (GitHub Actions)
- 05:00 UTC: Model Retraining (wenn neue Daten)
- Morning: Code Review der nächtlichen Pipeline
- Development: Feature Implementation
- Evening: Commit & Push, Documentation Update

### **Weekly:**
- **Montag:** Sprint Planning (Wochenziele)
- **Mittwoch:** Mid-Week Check-in (Blocker identifizieren)
- **Freitag:** Sprint Review & Retro
- **Samstag:** Learning & Weiterbildung (Parallelität zur Schulung)

### **Monthly:**
- Model Performance Review
- Database Optimization
- User Feedback Collection (nach Launch)
- Roadmap Adjustments

---

## 📞 SUPPORT & KOMMUNIKATION

### **Dokumentation:**
- **Haupt-Roadmap:** Dieses Dokument (PROJECT_ROADMAP.md)
- **Session Logs:** COMPLETE_SESSION_DOCUMENTATION.md
- **Code Comments:** Inline + Docstrings
- **API Docs:** Auto-generated (FastAPI Swagger)

### **Versionierung:**
- **Git:** GitHub (Private Repo während Entwicklung)
- **Branches:** main, develop, feature/*, hotfix/*
- **Commits:** Conventional Commits (feat:, fix:, docs:)

### **Backlog Management:**
- **Tool:** GitHub Projects / Linear
- **Labels:** bug, feature, enhancement, documentation
- **Milestones:** MVP1, MVP2, MVP3, Production

---

## ✅ CHECKPOINTS & GATES

### **End of Month 1:**
- [ ] PostgreSQL fully set up with Ontologie
- [ ] Item Database complete (all items from Data Dragon)
- [ ] Champion Database complete (all champions)

### **End of Month 2:**
- [ ] Champion Matchup Matrix complete
- [ ] Champion Synergy Matrix complete
- [ ] Fuzzy Search System working

### **End of Month 3:**
- [ ] Draft Phase Predictor >60% Accuracy
- [ ] Game State Predictor >70% Accuracy
- [ ] MVP1 deployed (Draft Assistant)

### **End of Month 4:**
- [ ] Item Recommendation Engine working
- [ ] Heuristik Rules implemented
- [ ] MVP2 deployed (Item Builder)

### **End of Month 5:**
- [ ] Live Game Tracker working
- [ ] Ward System implemented
- [ ] MVP3 deployed (Full System)
- [ ] Abschlussarbeit submitted

---

## 🎯 FINAL DELIVERABLES

1. ✅ **Production Tool** (live unter eigener Domain)
2. ✅ **PostgreSQL Ontologie** (vollständig dokumentiert)
3. ✅ **ML Models** (>60% & >70% Accuracy)
4. ✅ **Hybrid Recommendation Engine** (ML + Ontologie + Heuristik)
5. ✅ **Abschlussarbeit** (40-60 Seiten)
6. ✅ **GitHub Repository** (clean, documented, portfolio-ready)
7. ✅ **Presentation** (15-20min für Abschlusspräsentation)

---

## 🚨 RISKS & MITIGATION

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Riot API Rate Limits** | High | Medium | Caching, Request Batching, Multiple API Keys |
| **Model Accuracy zu niedrig** | High | Medium | Feature Engineering, Mehr Daten, Ensemble Methods |
| **PostgreSQL Performance** | Medium | Low | Indexing, Query Optimization, Connection Pooling |
| **Scope Creep** | High | High | Strikte MVP-Definition, Backlog Priorisierung |
| **Zeit-Management** | High | Medium | Wöchentliche Sprints, Klare Deadlines |
| **Deployment-Probleme** | Medium | Low | Früh testen (MVP1), Monitoring Setup |

---

## 📖 REFERENCES & RESOURCES

### **Riot API Documentation:**
- Match-V5: https://developer.riotgames.com/apis#match-v5
- Data Dragon: https://developer.riotgames.com/docs/lol#data-dragon
- Live Client: https://developer.riotgames.com/docs/lol#game-client-api

### **Libraries & Tools:**
- scikit-learn: https://scikit-learn.org/
- FastAPI: https://fastapi.tiangolo.com/
- PostgreSQL: https://www.postgresql.org/docs/
- Next.js: https://nextjs.org/docs

### **Similar Tools (Inspiration):**
- U.GG (Item Builds, Win Rates)
- Porofessor (Draft Analysis)
- Blitz.gg (Live Tracker)
- OP.GG (Champion Stats)

---

**Version:** 2.0
**Last Updated:** 2025-12-29
**Status:** 🚀 READY TO BUILD!

---

**Next Steps:**
1. Start Month 1, Week 1: PostgreSQL Setup
2. Initialize GitHub Repository
3. Setup Development Environment
4. Begin Champion Ontologie Schema Implementation

**LET'S BUILD THE MEISTERWERK!** 🎯🔥

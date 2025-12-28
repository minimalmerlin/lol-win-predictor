# Design Guidelines: Halo-Inspired Strategic Interface

## 1. Der Markenkern & Visuelle Strategie

**Inspiration:** Halo 2 & Halo 3 Main Menu Interface - Das legendäre militärische Sci-Fi HUD.

**Keywords:** Episch, Militärisch, Strategisch, Holographisch, Tactical, Elite

**Visuelle Ästhetik:** Tiefes Dunkelblau mit holographischen blauen Elementen. Wie ein UNSC-Terminal oder Cortanas Interface. Klare, scharfe Kontraste. Keine grellen Farben auf hellem Hintergrund. Alles wirkt wie ein militärisches Strategie-System.

---

## 2. Das Logo

Gaming Controller mit Neural Network - bleibt bestehen, wird aber in Halo-Blau-Tönen dargestellt.

**Verwendung:** Immer mit blauem Glow auf dunklem Hintergrund.

---

## 3. Die Farbpalette

### 3.1. Hintergrundfarben (The Void)

**Deep Space Black** (Haupthintergrund)
- HEX: `#000814`
- RGB: 0, 8, 20
- Sehr dunkles Blau-Schwarz, fast schwarz aber mit leichtem Blauton

**UNSC Navy** (Sekundärer Hintergrund / Cards)
- HEX: `#001D3D`
- RGB: 0, 29, 61
- Tiefes Dunkelblau wie Halo UI Panels

**Tactical Blue** (Tertiary / Hover States)
- HEX: `#003566`
- RGB: 0, 53, 102
- Mittleres Dunkelblau für aktive Elemente

### 3.2. Primärfarben (Holographic Elements)

**Cortana Blue** (Primary - Main UI Color)
- HEX: `#4CC9F0`
- RGB: 76, 201, 240
- Das ikonische helle Blau von Cortana / Halo UI

**Shield Blue** (Akzent)
- HEX: `#0096C7`
- RGB: 0, 150, 199
- Etwas dunkleres Blau für Variationen

**Energy Cyan** (Highlights)
- HEX: `#00B4D8`
- RGB: 0, 180, 216
- Für wichtige Highlights und Buttons

### 3.3. Textfarben

**Tech White** (Haupttext für Überschriften)
- HEX: `#E8F1F5`
- RGB: 232, 241, 245
- Leicht bläuliches Weiß

**Tactical Grey** (Fließtext & Labels)
- HEX: `#90B8D8`
- RGB: 144, 184, 216
- Bläulich-grau für gute Lesbarkeit

### 3.4. Semantische Farben

**Success Green** (Positive States / Wins)
- HEX: `#06D6A0`
- RGB: 6, 214, 160
- Helles Grün wie Halo Shield Recharge

**Alert Orange** (Warnings)
- HEX: `#FFB703`
- RGB: 255, 183, 3
- Orange für Warnungen (wie Halo Motion Tracker)

**Danger Red** (Errors / Critical)
- HEX: `#EF476F`
- RGB: 239, 71, 111
- Rot für kritische Zustände

---

## 4. Typografie

### 4.1. Überschriften: "Rajdhani"
Eine militärisch-technische Schrift, die an Halo's UI erinnert.

- **Verwendung:** Alle Überschriften (H1-H3), wichtige Stats, Buttons
- **Gewichte:** Bold (700), Semi-Bold (600)
- **Stil:** Uppercase für militärischen Look

### 4.2. Fließtext: "Inter"
Bleibt für optimale Lesbarkeit.

- **Verwendung:** Beschreibungen, Labels, Fließtext
- **Gewichte:** Regular (400), Medium (500)
- **Textfarbe:** Tactical Grey (`#90B8D8`)

---

## 5. Visuelle Effekte

### 5.1. Holographische Effekte

**Box Glow (Halo-Style):**
```css
box-shadow:
  0 0 20px rgba(76, 201, 240, 0.3),
  inset 0 0 30px rgba(76, 201, 240, 0.05);
```

**Text Glow:**
```css
text-shadow:
  0 0 10px rgba(76, 201, 240, 0.8),
  0 0 20px rgba(76, 201, 240, 0.4);
```

### 5.2. UI Elemente

**Panels / Cards:**
- Hintergrund: UNSC Navy (`#001D3D`)
- Border: 2px solid Cortana Blue (`#4CC9F0` mit 40% opacity)
- Subtiles Inner Glow
- Scharfe, eckige Kanten (border-radius minimal)

**Scan Lines (Halo Terminal Effect):**
```css
background-image: repeating-linear-gradient(
  0deg,
  rgba(76, 201, 240, 0.03),
  rgba(76, 201, 240, 0.03) 1px,
  transparent 1px,
  transparent 2px
);
```

**Divider Lines:**
- 1-2px solid
- Cortana Blue mit Glow
- Horizontale Streifen wie in Halo Menüs

### 5.3. Buttons

**Primary Button:**
- Background: Transparent
- Border: 2px solid Cortana Blue
- Text: Cortana Blue mit Glow
- Hover: Light blue background fill
- Font: Rajdhani Bold, Uppercase

**Active State:**
- Background: Cortana Blue mit 20% opacity
- Stronger Glow

---

## 6. Design Prinzipien

### 6.1. Klare Kontraste
- Dunkler Hintergrund (#000814)
- Helle blaue UI Elemente (#4CC9F0)
- NIEMALS helle Farben auf hellem Hintergrund
- Immer scharfe, klare Trennung

### 6.2. Militärisch-Strategisch
- Uppercase Headlines
- Technische, präzise Typografie
- Grid-basierte Layouts
- Sechseckige Elemente (Halo-typisch)

### 6.3. Holographische Ästhetik
- Alles wirkt wie projiziert
- Subtile Glows überall
- Scan Lines für Terminal-Feel
- Transparente Overlays

### 6.4. Epische Atmosphäre
- Großzügiger Weißraum (Dunkelraum)
- Monumentale Überschriften
- Tiefe durch Layering
- Ruhiges, kraftvolles Design

---

## 7. Zusammenfassung für Entwickler

```css
/* Halo Color Palette */
--bg-primary: #000814;      /* Deep Space Black */
--bg-secondary: #001D3D;    /* UNSC Navy */
--bg-tertiary: #003566;     /* Tactical Blue */

--text-primary: #E8F1F5;    /* Tech White */
--text-secondary: #90B8D8;  /* Tactical Grey */

--accent-primary: #4CC9F0;  /* Cortana Blue */
--accent-shield: #0096C7;   /* Shield Blue */
--accent-energy: #00B4D8;   /* Energy Cyan */

--success: #06D6A0;         /* Success Green */
--warning: #FFB703;         /* Alert Orange */
--error: #EF476F;           /* Danger Red */

/* Typography */
--font-heading: 'Rajdhani', sans-serif;
--font-body: 'Inter', sans-serif;

/* Glow Effects */
--glow-blue: 0 0 20px rgba(76, 201, 240, 0.4);
--glow-text: 0 0 10px rgba(76, 201, 240, 0.8);
```

**Prinzipien:**
- Tiefes Dunkelblau-Schwarz Background (#000814)
- Holographisches Blau (#4CC9F0) für UI
- Rajdhani Bold Uppercase für Headlines
- Sharp, kantige UI Elemente
- Subtile Glows überall
- Wie UNSC Tactical Interface
- Episch, militärisch, strategisch

---

**Referenz:** Halo 2 & Halo 3 Main Menu Interface, UNSC Terminals, Cortana Hologramme

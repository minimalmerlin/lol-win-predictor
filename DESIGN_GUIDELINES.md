# Design Guidelines: NeuroPlay Analytics (LoL Coach)

## 1. Der Markenkern & Visuelle Strategie

Das Produkt ist ein hochtechnologisches Werkzeug, das die Brücke zwischen intuitiven Gaming-Skills und harter Datenanalyse schlägt.

**Keywords:** Intelligent, Analytisch, Futuristisch, Präzise, "Game-Changing"

**Visuelle Ästhetik:** "Dark Mode First". Das Design lebt von leuchtenden Elementen auf dunklen Hintergründen. Es erinnert an Head-Up-Displays (HUDs) in Sci-Fi-Spielen oder Terminals in Cyberpunk-Filmen. Es darf niemals "brav" oder wie eine Standard-Bürosoftware aussehen.

---

## 2. Das Logo

Das Logo symbolisiert die Verschmelzung von Gaming-Hardware (Controller) und künstlicher Intelligenz (Neuronales Netz/Gehirn) zur Leistungssteigerung (Pfeil).

### 2.1. Hauptlogo (Primary)
Die bevorzugte Darstellung ist immer die "leuchtende" Neon-Variante auf dunklem Grund.

- **Verwendung:** Website-Header, App-Startbildschirm, Social Media Profile, digitale Werbung
- **Schutzraum (Clear Space):** Mindestabstand entsprechend der Höhe des "Pfeils" im Logo

### 2.2. Logo-Varianten

- **Flat-Variante:** Ohne "Glow"-Effekt für kleinere Darstellungen
- **Monochrom:** Schwarz/Weiß für einfache Anwendungen
- **Light Mode:** Vermeiden wenn möglich; bei Bedarf dunklere Töne verwenden

---

## 3. Die Farbpalette

### 3.1. Primärfarben (The Neon Glow)

**Cyber Cyan** (Links im Controller)
- HEX: `#00FFFF`
- RGB: 0, 255, 255
- **Verwendung:** Highlights, positive Tendenzen, primäre Call-to-Action Buttons

**Electric Magenta** (Rechts im Controller)
- HEX: `#E100FF`
- RGB: 225, 0, 255
- **Verwendung:** Sekundäre Highlights, spezielle KI-Features, Hover-Effekte

### 3.2. Hintergrundfarben (The Void)

**Deep Space Navy** (Haupthintergrund)
- HEX: `#0A0E17`
- RGB: 10, 14, 23

**Interface Grey** (Sekundärer Hintergrund)
- HEX: `#161B28`
- RGB: 22, 27, 40

### 3.3. Textfarben

**Tech White** (Haupttext für Überschriften)
- HEX: `#FFFFFF`
- RGB: 255, 255, 255

**HUD Grey** (Fließtext & Labels)
- HEX: `#B0B8C8`
- RGB: 176, 184, 200

### 3.4. Semantische Farben

**Success Green** (Verbesserung/Sieg)
- HEX: `#00E676`
- RGB: 0, 230, 118

**Warning Red** (Verschlechterung/Fehler)
- HEX: `#FF1744`
- RGB: 255, 23, 68

---

## 4. Typografie

### 4.1. Überschriften & Zahlen: "Chakra Petch"
- **Verwendung:** Hauptüberschriften (H1, H2), große Statistiken/Zahlen, Button-Texte
- **Gewichte:** Bold (700) für Überschriften, Medium (500) für Buttons
- **Beispiel:** `WIN RATE: 64%`

### 4.2. Fließtext & UI-Labels: "Inter"
- **Verwendung:** Analysetexte, Achsenbeschriftungen, Menüpunkte, Kleingedrucktes
- **Gewichte:** Regular (400) für Text, Semi-Bold (600) für wichtige Labels
- **Textfarbe:** HUD Grey (`#B0B8C8`) auf dunklem Hintergrund

---

## 5. Ikonografie & Design-Elemente

### 5.1. Icons
- Nur **Line Icons** (Linien-basiert)
- Strichstärke: 1px oder 2px
- **Aktiv:** Leuchten in Cyber Cyan
- **Inaktiv:** HUD Grey
- Icons wirken als wären sie aus Licht geformt

### 5.2. Datenvisualisierung

**Linien-Diagramme:**
- Dünne, leuchtende Linien (Cyan oder Magenta)
- Transparenter Farbverlauf unter der Linie

**Knotenpunkte:**
- Kleine leuchtende Punkte oder Hexagone

**Gitterlinien:**
- Extrem dünn und kaum sichtbar (dunkles Grau/Blau)

### 5.3. UI-Elemente

**Cards:**
- Hintergrund: Interface Grey (`#161B28`)
- Subtiler, dünner leuchtender Rand (`1px solid Cyber Cyan`)
- Leuchtende Ecken für HUD-Look

**Rahmen:**
- Keine fetten Schatten
- Subtile outer-glow CSS Effekte

---

## 6. Zusammenfassung für Entwickler

```css
/* Farben */
--bg-primary: #0A0E17;
--bg-secondary: #161B28;
--text-primary: #FFFFFF;
--text-secondary: #B0B8C8;
--accent-cyan: #00FFFF;
--accent-magenta: #E100FF;
--success: #00E676;
--error: #FF1744;

/* Typografie */
--font-heading: 'Chakra Petch', sans-serif;
--font-body: 'Inter', sans-serif;

/* Effekte */
--glow-cyan: 0 0 10px rgba(0, 255, 255, 0.5);
--glow-magenta: 0 0 10px rgba(225, 0, 255, 0.5);
```

**Prinzipien:**
- Hintergrund ist immer `#0A0E17`
- Text ist `#B0B8C8` (Inter Regular), Überschriften `#FFFFFF` (Chakra Petch Bold)
- Akzente sind `#00FFFF` und `#E100FF`
- Alles muss "leuchten" (subtile outer-glow CSS Effekte)
- **Keine Flächen füllen, wenn Linien ausreichen**
- HUD/Cyberpunk-Ästhetik durchgehend

---

**Logo:** Gaming Controller mit Neural Network - bereits implementiert als `/public/logo.png`

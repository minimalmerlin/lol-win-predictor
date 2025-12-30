import os

def fix_env():
    print("🔧 Starte .env Reparatur...")
    try:
        with open('.env', 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("❌ .env Datei nicht gefunden!")
        return

    # 1. Beste Datenbank-URL finden
    target_url = None
    
    # Suche zuerst nach Non-Pooling (besser für Scripts), dann normal
    for key in ["POSTGRES_URL_NON_POOLING", "POSTGRES_URL"]:
        for line in lines:
            if line.startswith(f"{key}="):
                # Wert extrahieren und Quotes entfernen
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    target_url = val
                    break
        if target_url: break

    if not target_url:
        print("❌ Keine POSTGRES_URL gefunden. Vercel Pull wiederholen?")
        return

    # Protocol fixen (postgres:// -> postgresql://)
    if target_url.startswith("postgres://"):
        target_url = target_url.replace("postgres://", "sql://", 1)

    print(f"✓ Datenbank-URL gefunden: {target_url[:20]}...")

    # 2. Datei neu schreiben (mit Quotes für Zsh Sicherheit)
    new_lines = []
    for line in lines:
        if not line.strip() or line.startswith("#"):
            new_lines.append(line)
            continue
            
        key_part = line.split("=", 1)[0]
        
        # SUPABASE_URL chreiben
        if key_part == "SUPABASE_URL":
            new_lines.append(f'SUPABASE_URL="{target_url}"\n')
            print("✓ SUPABASE_URL aktualisiert")
        # Alle anderen Zeilen sicher quoten
        elif "=" in line:
            key, val = line.split("=", 1)
            clean_val = val.strip().strip('"').strip("'")
            new_lines.append(f'{key}="{clean_val}"\n')
        else:
            new_lines.append(line)

    with open('.env', 'w') as f:
        f.writelines(new_lines)
    
    print("✅ .env erfolgreich repariert (Quotes hinzugefügt & URL gefixt).")

if __name__ == "__main__":
    fix_env()


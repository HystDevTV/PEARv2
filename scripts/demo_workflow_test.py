#!/usr/bin/env python3
"""
PEAR Demo Workflow Test Script
==============================

Dieses Skript demonstriert die Funktionalität des PEAR Demo-Workflows.
Es kann verwendet werden, um die Automatisierung lokal zu testen oder
die Workflow-Logik zu validieren.

Autor: PEAR-Automation-Bot
Datum: 2025-07-25
"""

import os
import sys
from datetime import datetime

def add_demo_entry_to_docs():
    """Fügt einen Demo-Eintrag zur PEAR-Dokumentation hinzu."""
    
    docs_path = "docs/dokumentation-pear.md"
    
    # Prüfen ob die Dokumentationsdatei existiert
    if not os.path.exists(docs_path):
        print(f"❌ Fehler: {docs_path} nicht gefunden!")
        return False
    
    # Aktueller Zeitstempel
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date_only = datetime.now().strftime('%Y-%m-%d')
    
    # Demo-Eintrag erstellen
    demo_entry = f"""## [NEU am {timestamp}] Demo-Eintrag für PEAR-Workflow
Automatisch generiert durch den PEAR Demo-Workflow zur Demonstration der automatisierten Projektdokumentation.
Workflow ausgeführt am {date_only} um {datetime.now().strftime('%H:%M:%S')} UTC - Zeigt erfolgreiche Integration von GitHub Actions für PEAR-Automatisierung.

"""
    
    try:
        # Eintrag zur Dokumentation hinzufügen
        with open(docs_path, 'a', encoding='utf-8') as f:
            f.write(demo_entry)
        
        print(f"✅ Demo-Eintrag erfolgreich zu {docs_path} hinzugefügt!")
        print(f"📅 Zeitstempel: {timestamp}")
        print(f"📝 Eintrag: Demo-Workflow Automatisierung")
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Schreiben der Datei: {e}")
        return False

def main():
    """Hauptfunktion für den Demo-Workflow-Test."""
    
    print("🚀 PEAR Demo-Workflow Test gestartet...")
    print("=" * 50)
    
    # Arbeitsverzeichnis anzeigen
    print(f"📁 Arbeitsverzeichnis: {os.getcwd()}")
    
    # Demo-Eintrag hinzufügen
    if add_demo_entry_to_docs():
        print("\n🎉 Demo-Workflow erfolgreich ausgeführt!")
        print("💡 Tipp: Prüfen Sie docs/dokumentation-pear.md für den neuen Eintrag.")
        return 0
    else:
        print("\n❌ Demo-Workflow fehlgeschlagen!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
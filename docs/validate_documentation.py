#!/usr/bin/env python3
"""
Validation script für die PEAR Projektdokumentation.
Überprüft die Konsistenz zwischen team.py und dokumentation-pear.md
"""

import os
import sys
from pathlib import Path

# Add the repository root to the path
repo_root = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_root))

from team import build_team

def validate_documentation():
    """Validiert die Dokumentationsstruktur."""
    
    # Check if documentation file exists
    doc_path = repo_root / "docs" / "dokumentation-pear.md"
    if not doc_path.exists():
        print("❌ FEHLER: dokumentation-pear.md nicht gefunden!")
        return False
    
    # Load team data
    team = build_team()
    project_manager = next((agent for agent in team if agent.name == "Projektmanager"), None)
    
    if not project_manager:
        print("❌ FEHLER: Projektmanager nicht im Team gefunden!")
        return False
    
    # Check if Project Manager has coordination tasks
    coordination_tasks = [
        "Meilensteine planen & Prioritäten setzen",
        "Sprint-basierte Projektphasen definieren",
        "Prioritätensystem",
        "Aufgabenlisten für alle Agenten"
    ]
    
    missing_tasks = []
    for task_keyword in coordination_tasks:
        if not any(task_keyword in task for task in project_manager.tasks):
            missing_tasks.append(task_keyword)
    
    if missing_tasks:
        print(f"⚠️  WARNUNG: Folgende Koordinationsaufgaben fehlen: {missing_tasks}")
    
    # Read documentation content
    with open(doc_path, 'r', encoding='utf-8') as f:
        doc_content = f.read()
    
    # Check for key sections
    required_sections = [
        "Meilenstein-Framework",
        "Prioritätensystem", 
        "Agent-spezifische Aufgabenlisten",
        "Sprint 1", "Sprint 2", "Sprint 3", "Sprint 4", "Sprint 5",
        "P1", "P2", "P3",
        "KPIs"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in doc_content:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"⚠️  WARNUNG: Folgende Dokumentationsabschnitte fehlen: {missing_sections}")
        return False
    
    print("✅ Dokumentation vollständig validiert!")
    print(f"✅ Projektmanager hat {len(project_manager.tasks)} definierte Aufgaben")
    print(f"✅ Dokumentation umfasst {len(doc_content)} Zeichen")
    print(f"✅ Alle {len(required_sections)} erforderlichen Abschnitte vorhanden")
    
    return True

if __name__ == "__main__":
    success = validate_documentation()
    sys.exit(0 if success else 1)
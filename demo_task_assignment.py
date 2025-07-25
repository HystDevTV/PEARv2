#!/usr/bin/env python3
"""
PEAR Task Assignment Demo

This script demonstrates the enhanced team.py system with the specific
German agent roles and tasks from issue #16.

Usage:
    python demo_task_assignment.py
"""

import os
import sys
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from team import Agent, TaskManager
except ImportError as e:
    print(f"❌ Cannot import team module: {e}")
    print("Make sure you have the required dependencies installed:")
    print("pip install PyGithub requests")
    sys.exit(1)

# Sample tasks based on issue #16 requirements
SAMPLE_TASKS = [
    {
        "title": "Cloud Build Trigger der PEARv2-VM testen",
        "description": "Build, Push, Deploy, Log-Bucket prüfen. Authorisierungsprobleme von PEAR-DEV-TeamV1 prüfen.",
        "category": "A",
        "issue_number": None,
        "labels": ["QA-Testing", "kategorie-a", "priority-1", "infrastructure"]
    },
    {
        "title": "Datenbank der PEARv2-VM prüfen: Struktur, Integrität, Performance",
        "description": "Datenbank ggf. erweitern. Backup- und Restore-Strategie dokumentieren und testen.",
        "category": "B", 
        "issue_number": None,
        "labels": ["Data-AI", "kategorie-b", "priority-2", "database"]
    },
    {
        "title": "Firebase-Authentifizierung ins Backend einbauen",
        "description": "Registrierung, Login, Token-Handling. Python-Code für User-Management. API-Endpunkte implementieren.",
        "category": "C",
        "issue_number": None,
        "labels": ["Backend", "kategorie-c", "priority-1", "feature"]
    },
    {
        "title": "Alle neuen Schritte in dokumentation-pear.md dokumentieren",
        "description": "Neue Einträge mit [NEU am Datum] kennzeichnen. Zusammenfassungen für Neueinsteiger ergänzen.",
        "category": "D",
        "issue_number": None,
        "labels": ["Documentation", "kategorie-d", "priority-2", "onboarding"]
    },
    {
        "title": "[EXTRA] Automatische Secrets-Verwaltung via Secret Manager",
        "description": "Optional: Secrets-Management implementieren wenn Zeit verfügbar.",
        "category": "A",
        "issue_number": None,
        "labels": ["EXTRA", "Security", "Infrastructure", "optional"]
    }
]


def print_header():
    """Print demonstration header"""
    print("=" * 80)
    print("🚀 PEAR Task Assignment Demonstration")
    print("=" * 80)
    print("Basierend auf Issue #16: Nächsten Aufgaben")
    print(f"Datum: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    print()


def create_agents():
    """Create the four main agents as defined in issue #16"""
    print("👥 Erstelle Agenten-Team:")
    print("-" * 40)
    
    agents = [
        Agent.from_container("gcr.io/pear-dev-teamv1/dev-team-pear-agenten:latest", "infrastructure"),
        Agent.from_container("gcr.io/pear-dev-teamv1/dev-team-pear-agenten:latest", "feature"),
        Agent.from_container("gcr.io/pear-dev-teamv1/dev-team-pear-agenten:latest", "workflow"),
        Agent.from_container("gcr.io/pear-dev-teamv1/dev-team-pear-agenten:latest", "onboarding")
    ]
    
    for agent in agents:
        print(f"✅ {agent.name}")
        print(f"   Rolle: {agent.role}")
        print(f"   Skills: {', '.join(agent.skills)}")
        print()
    
    return agents


def demonstrate_task_assignment(agents):
    """Demonstrate task assignment to agents"""
    print("📋 Task-Zuweisung:")
    print("-" * 40)
    
    # Create task manager
    task_manager = TaskManager("HystDevTV/PEARv2")
    
    # Register agents
    for agent in agents:
        task_manager.register_agent(agent)
    
    # Override fetch_tasks_from_github to use our sample tasks
    task_manager._get_sample_tasks = lambda: SAMPLE_TASKS
    task_manager.fetch_tasks_from_github = task_manager._get_sample_tasks
    
    # Assign tasks
    task_manager.assign_tasks_by_category()
    
    # Show task assignments
    for agent in agents:
        print(f"🤖 {agent.name}:")
        if agent.assigned_tasks:
            for i, task in enumerate(agent.assigned_tasks, 1):
                print(f"   {i}. {task['title']}")
                print(f"      Kategorie: {task['category']}")
                print(f"      Labels: {', '.join(task.get('labels', []))}")
        else:
            print("   (Keine Aufgaben zugewiesen)")
        print()


def demonstrate_task_execution(agents):
    """Demonstrate task execution"""
    print("⚡ Task-Ausführung (Simulation):")
    print("-" * 40)
    
    for agent in agents:
        if agent.assigned_tasks:
            print(f"🔄 {agent.name} führt Aufgaben aus...")
            results = agent.execute_tasks()
            
            for result in results:
                status_emoji = "✅" if result['status'] == "completed" else "🔄"
                print(f"   {status_emoji} {result['message']}")
            print()


def print_summary():
    """Print demonstration summary"""
    print("=" * 80)
    print("📊 ZUSAMMENFASSUNG")
    print("=" * 80)
    print("✅ Agenten-Team erfolgreich erstellt")
    print("✅ Aufgaben basierend auf Issue #16 zugewiesen")
    print("✅ Task-Ausführung simuliert")
    print()
    print("🎯 NÄCHSTE SCHRITTE:")
    print("1. GitHub Issues mit create_github_issues.py erstellen")
    print("2. Issues den entsprechenden Agenten zuweisen")
    print("3. Dokumentation mit [NEU am Datum] Markierungen aktualisieren")
    print("4. Regelmäßiges Monitoring und Statusupdates")
    print()
    print("💡 Für echte GitHub Integration: GITHUB_TOKEN environment variable setzen")


def main():
    """Main demonstration function"""
    print_header()
    
    # Create agents
    agents = create_agents()
    
    # Demonstrate task assignment
    demonstrate_task_assignment(agents)
    
    # Demonstrate task execution
    demonstrate_task_execution(agents)
    
    # Print summary
    print_summary()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demonstration abgebrochen")
    except Exception as e:
        print(f"\n❌ Fehler: {str(e)}")
        sys.exit(1)
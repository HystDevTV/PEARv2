#!/usr/bin/env python3
"""
GitHub Issue Creation Script for PEAR Task Distribution

This script creates GitHub issues for each task category defined in the
German task list from issue #16. Each issue will be assigned to the
appropriate agent role with proper labels and categories.

Usage:
    python create_github_issues.py

Required Environment Variables:
    GITHUB_TOKEN - Personal access token with repo permissions
"""

import os
import sys
from datetime import datetime
from typing import List, Dict, Any
import json

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from github import Github
    from github.GithubException import GithubException
except ImportError:
    print("PyGithub is required. Install with: pip install PyGithub")
    sys.exit(1)

# Configuration
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = "HystDevTV/PEARv2"
ASSIGNEE = "HystDevTV"  # Default assignee as per requirements

# Task definitions based on German requirements from issue #16
TASK_DEFINITIONS = {
    "QA_TESTING": {
        "title": "Cloud Build Trigger der PEARv2-VM testen",
        "body": """## Aufgabe: QA/Testing-Spezialist

### Beschreibung
Als QA/Testing-Spezialist soll die Cloud Build Pipeline der PEARv2-VM vollständig getestet werden.

### Teilaufgaben
- [ ] Cloud Build Trigger testen (Build, Push, Deploy, Log-Bucket prüfen)
- [ ] Prüfen, ob die Authorisierungsprobleme (wie in PEAR-DEV-TeamV1 gelöst) auch in PEARv2 auftreten
- [ ] Ggf. die Lösung aus PEAR-DEV-TeamV1 auf PEARv2 übertragen
- [ ] Automatisierte Tests für neue Features schreiben 
- [ ] Tests in die CI/CD-Pipeline integrieren

### Akzeptanzkriterien
- [ ] Cloud Build läuft fehlerfrei durch
- [ ] Alle Berechtigungsprobleme sind gelöst
- [ ] Automatisierte Tests sind implementiert und laufen in der Pipeline
- [ ] Dokumentation der Testergebnisse in `/docs/dokumentation-pear.md`

### Priorität
**KRITISCH** - Essential für Deployment und Security

### Referenzen
- Issue #16 - Nächsten Aufgaben
- `/docs/dokumentation-pear.md`
- Existing Cloud Build configuration in `cloudbuild.yaml`

**Hinweis**: Bei Fragen oder Unklarheiten bitte im Canvas oder im nächsten Standup klären.
""",
        "labels": ["QA-Testing", "kategorie-a", "priority-1", "infrastructure"],
        "assignee": ASSIGNEE
    },
    
    "DATABASE_ENGINEER": {
        "title": "Datenbank der PEARv2-VM prüfen und erweitern",
        "body": """## Aufgabe: Data/AI Engineer

### Beschreibung
Als Data/AI Engineer soll die Datenbank der PEARv2-VM analysiert und optimiert werden.

### Teilaufgaben
- [ ] Datenbank-Struktur prüfen und analysieren
- [ ] Datenbank-Integrität überprüfen
- [ ] Performance-Analyse durchführen
- [ ] Datenbank ggf. erweitern (neue Tabellen/Spalten für neue Features)
- [ ] Backup- und Restore-Strategie dokumentieren
- [ ] Backup- und Restore-Strategie testen

### Akzeptanzkriterien
- [ ] Vollständige Analyse der aktuellen Datenbankstruktur
- [ ] Performance-Bericht mit Optimierungsempfehlungen
- [ ] Erweiterte Datenbankschemas für neue Features
- [ ] Getestete und dokumentierte Backup-Strategie
- [ ] Dokumentation aller Änderungen in `/docs/dokumentation-pear.md`

### Technische Details
- Aktuelles System: MySQL auf projekt-pear-vm
- Datenbank: pear_app_db
- Schema-Import: schema.sql (bereits für MySQL angepasst)

### Referenzen
- Issue #16 - Nächsten Aufgaben
- `/docs/dokumentation-pear.md` - Abschnitt 3 (Infrastruktur-Setup)
- Existing database schema files

**Hinweis**: Bei Fragen oder Unklarheiten bitte im Canvas oder im nächsten Standup klären.
""",
        "labels": ["Data-AI", "kategorie-b", "priority-2", "database"],
        "assignee": ASSIGNEE
    },
    
    "BACKEND_DEVELOPER": {
        "title": "Firebase-Authentifizierung ins Backend einbauen",
        "body": """## Aufgabe: Backend-Entwickler

### Beschreibung
Als Backend-Entwickler soll Firebase-Authentifizierung in das bestehende FastAPI Backend integriert werden.

### Teilaufgaben
- [ ] Firebase-Authentifizierung Setup (Registrierung, Login, Token-Handling)
- [ ] Python-Code für Authentifizierung und User-Management schreiben
- [ ] API-Endpunkte für Authentifizierung implementieren
- [ ] API-Endpunkte für User-Profile implementieren
- [ ] Integration mit bestehender FastAPI-Struktur
- [ ] Tests für Authentifizierungs-Endpoints schreiben

### Akzeptanzkriterien
- [ ] Firebase-Authentifizierung ist vollständig integriert
- [ ] Benutzer können sich registrieren und anmelden
- [ ] Token-basierte Authentifizierung funktioniert
- [ ] User-Profile können erstellt und verwaltet werden
- [ ] API-Dokumentation ist aktualisiert
- [ ] Alle Tests sind grün
- [ ] Dokumentation in `/docs/dokumentation-pear.md` aktualisiert

### Technische Details
- Bestehendes Backend: FastAPI in `main.py`
- Aktuelle API: Port 8000, bereits erreichbar
- Integration mit: `/api/process-email-for-client` endpoint

### Security Anforderungen
- DSGVO-Konformität beachten
- Passwort-Hashing (bereits bcrypt implementiert)
- Sichere Token-Verwaltung
- HTTPS-only für Produktion

### Referenzen
- Issue #16 - Nächsten Aufgaben
- `/docs/dokumentation-pear.md` - Abschnitt 4 (Backend-Entwicklung)
- Existing `main.py` FastAPI implementation

**Hinweis**: Bei Fragen oder Unklarheiten bitte im Canvas oder im nächsten Standup klären.
""",
        "labels": ["Backend", "kategorie-c", "priority-1", "feature"],
        "assignee": ASSIGNEE
    },
    
    "DOCUMENTATION_AGENT": {
        "title": "Dokumentation für neue Features und Änderungen aktualisieren",
        "body": """## Aufgabe: Dokumentations-Agent

### Beschreibung
Als Dokumentations-Agent sollen alle neuen Schritte und Änderungen in der Projektdokumentation erfasst werden.

### Teilaufgaben
- [ ] Alle neuen Schritte und Änderungen in `/docs/dokumentation-pear.md` dokumentieren
- [ ] Neue Einträge mit aktuellem Datum und Kommentar "[NEU am {DATUM}]" kennzeichnen
- [ ] Kurze Zusammenfassungen der Änderungen/Erkenntnisse für Neueinsteiger ergänzen
- [ ] Existing documentation review und update
- [ ] Cross-references zwischen verschiedenen Dokumenten aktualisieren

### Dokumentationsstandards
- Datum-Format: DD.MM.YYYY (z.B. "[NEU am 25.07.2025]")
- Strukturierte Abschnitte für neue Features
- Klare Zusammenfassungen für Neueinsteiger
- Verweis auf relevante Issues und PRs

### Akzeptanzkriterien
- [ ] Alle neuen Features sind dokumentiert
- [ ] Datum-Markierungen sind korrekt gesetzt
- [ ] Zusammenfassungen sind verständlich für Neueinsteiger
- [ ] Konsistente Formatierung und Struktur
- [ ] Cross-referencing zwischen Dokumenten ist aktuell

### Zu dokumentierende Bereiche
- QA/Testing-Implementierung
- Datenbank-Erweiterungen
- Firebase-Authentifizierung
- Neue API-Endpunkte
- Deployment-Prozesse
- Sicherheits-Updates

### Referenzen
- Issue #16 - Nächsten Aufgaben
- `/docs/dokumentation-pear.md` - Hauptdokumentation
- Alle anderen Issues und PRs für Kontext

**Hinweis**: Bei Fragen oder Unklarheiten bitte im Canvas oder im nächsten Standup klären.
""",
        "labels": ["Documentation", "kategorie-d", "priority-2", "onboarding"],
        "assignee": ASSIGNEE
    },
    
    "SECRETS_MANAGEMENT": {
        "title": "[EXTRA] Automatische Secrets-Verwaltung via Secret Manager",
        "body": """## EXTRA Aufgabe: Automatische Secrets-Verwaltung

### Beschreibung
**Optional** - Diese Aufgabe kann verteilt werden, wenn Luft ist oder das Grundsystem läuft.

Implementierung einer automatisierten Secrets-Verwaltung über Google Cloud Secret Manager.

### Teilaufgaben
- [ ] Google Cloud Secret Manager Setup
- [ ] Migration von Umgebungsvariablen zu Secret Manager
- [ ] Automatisierte Secret-Rotation implementieren
- [ ] Integration in bestehende Cloud Build Pipeline
- [ ] Monitoring und Alerting für Secret-Zugriffe
- [ ] Dokumentation der Secret-Management-Strategie

### Akzeptanzkriterien
- [ ] Alle Secrets sind in Secret Manager gespeichert
- [ ] Automatisierte Rotation ist konfiguriert
- [ ] Cloud Build nutzt Secret Manager
- [ ] Monitoring und Alerting sind aktiv
- [ ] Dokumentation ist vollständig

### Sicherheitsaspekte
- Principle of least privilege
- Audit-Logging für Secret-Zugriffe
- Verschlüsselung at rest und in transit
- Regelmäßige Security-Reviews

### Referenzen
- Issue #16 - Nächsten Aufgaben (EXTRA)
- Google Cloud Secret Manager Documentation
- Existing `cloudbuild.yaml` configuration

**Status**: Optional - nur wenn Zeit und Ressourcen verfügbar sind.
""",
        "labels": ["EXTRA", "Security", "Infrastructure", "optional"],
        "assignee": ASSIGNEE
    },
    
    "DOCKER_MATRIX": {
        "title": "[EXTRA] Mehrere Docker Images parallel bauen (Matrix-Strategie)",
        "body": """## EXTRA Aufgabe: Docker Matrix Build

### Beschreibung
**Optional** - Diese Aufgabe kann verteilt werden, wenn Luft ist oder das Grundsystem läuft.

Implementierung einer Matrix-Strategie zum parallelen Bauen mehrerer Docker Images.

### Teilaufgaben
- [ ] Matrix-Build-Konfiguration in `cloudbuild.yaml` erweitern
- [ ] Multi-stage Docker-Builds optimieren
- [ ] Parallele Build-Strategien implementieren
- [ ] Build-Zeit-Optimierung durchführen
- [ ] Caching-Strategien verbessern
- [ ] Performance-Monitoring für Builds

### Akzeptanzkriterien
- [ ] Multiple Docker Images werden parallel gebaut
- [ ] Build-Zeit ist signifikant reduziert
- [ ] Caching funktioniert optimal
- [ ] Build-Pipeline ist stabil
- [ ] Performance-Metriken sind verfügbar

### Technische Anforderungen
- Google Cloud Build Matrix-Builds
- Docker multi-stage optimization
- Artifact Registry integration
- Build cache optimization

### Referenzen
- Issue #16 - Nächsten Aufgaben (EXTRA)
- Existing `cloudbuild.yaml`
- Docker multi-stage best practices

**Status**: Optional - nur wenn Zeit und Ressourcen verfügbar sind.
""",
        "labels": ["EXTRA", "Infrastructure", "Docker", "optional"],
        "assignee": ASSIGNEE
    },
    
    "WEB_UI_DASHBOARD": {
        "title": "[EXTRA] Web-UI für Deployments (internes Dashboard)",
        "body": """## EXTRA Aufgabe: Web-UI Dashboard

### Beschreibung
**Optional** - Diese Aufgabe kann verteilt werden, wenn Luft ist oder das Grundsystem läuft.

Entwicklung eines internen Web-Dashboards für Deployment-Management.

### Teilaufgaben
- [ ] Dashboard-Frontend entwickeln (React/Vue.js)
- [ ] Deployment-Status-API implementieren
- [ ] Build-Logs-Visualisierung
- [ ] Manual Deployment-Trigger
- [ ] System-Health-Monitoring
- [ ] User-Management für Dashboard

### Akzeptanzkriterien
- [ ] Web-Dashboard ist funktional
- [ ] Deployment-Status wird angezeigt
- [ ] Manual Deployments sind möglich
- [ ] Build-Logs sind einsehbar
- [ ] System-Monitoring funktioniert
- [ ] Benutzer-Authentifizierung ist implementiert

### UI/UX Anforderungen
- Responsive Design
- Intuitive Benutzerführung
- Real-time Updates
- Mobile-friendly

### Technische Stack
- Frontend: React/Vue.js
- Backend: FastAPI extension
- WebSocket für real-time updates
- Integration mit Google Cloud APIs

### Referenzen
- Issue #16 - Nächsten Aufgaben (EXTRA)
- Existing FastAPI backend
- `/docs/dokumentation-pear.md`

**Status**: Optional - nur wenn Zeit und Ressourcen verfügbar sind.
""",
        "labels": ["EXTRA", "Frontend", "Dashboard", "optional"],
        "assignee": ASSIGNEE
    }
}


def create_github_issues():
    """Create GitHub issues for all defined tasks"""
    
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN environment variable is required")
        print("Please set GITHUB_TOKEN with a personal access token that has repo permissions")
        return False
    
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(GITHUB_REPO)
        print(f"✅ Connected to repository: {GITHUB_REPO}")
    except Exception as e:
        print(f"❌ Failed to connect to GitHub: {str(e)}")
        return False
    
    created_issues = []
    failed_issues = []
    
    print(f"\n🚀 Creating {len(TASK_DEFINITIONS)} GitHub issues...")
    
    for task_key, task_data in TASK_DEFINITIONS.items():
        try:
            print(f"\n📝 Creating issue: {task_data['title']}")
            
            # Create the issue
            issue = repo.create_issue(
                title=task_data['title'],
                body=task_data['body'],
                assignee=task_data['assignee'],
                labels=task_data['labels']
            )
            
            created_issues.append({
                'key': task_key,
                'issue_number': issue.number,
                'title': task_data['title'],
                'url': issue.html_url
            })
            
            print(f"✅ Created issue #{issue.number}: {task_data['title']}")
            print(f"   URL: {issue.html_url}")
            
        except GithubException as e:
            error_msg = f"Failed to create issue '{task_data['title']}': {str(e)}"
            print(f"❌ {error_msg}")
            failed_issues.append({
                'key': task_key,
                'title': task_data['title'],
                'error': str(e)
            })
        except Exception as e:
            error_msg = f"Unexpected error creating issue '{task_data['title']}': {str(e)}"
            print(f"❌ {error_msg}")
            failed_issues.append({
                'key': task_key,
                'title': task_data['title'],
                'error': str(e)
            })
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print(f"✅ Successfully created: {len(created_issues)} issues")
    print(f"❌ Failed to create: {len(failed_issues)} issues")
    
    if created_issues:
        print(f"\n✅ CREATED ISSUES:")
        for issue in created_issues:
            print(f"  • #{issue['issue_number']}: {issue['title']}")
            print(f"    {issue['url']}")
    
    if failed_issues:
        print(f"\n❌ FAILED ISSUES:")
        for issue in failed_issues:
            print(f"  • {issue['title']}: {issue['error']}")
    
    # Save results to file for reference
    results = {
        'created_at': datetime.now().isoformat(),
        'created_issues': created_issues,
        'failed_issues': failed_issues,
        'total_attempted': len(TASK_DEFINITIONS),
        'success_rate': len(created_issues) / len(TASK_DEFINITIONS) * 100
    }
    
    with open('github_issues_creation_log.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Results saved to: github_issues_creation_log.json")
    
    return len(failed_issues) == 0


def print_instructions():
    """Print usage instructions"""
    print("""
🔧 GitHub Issues Creation Script für PEAR Task Distribution

Dieser Script erstellt GitHub Issues für alle Aufgaben aus Issue #16.

SETUP:
1. GitHub Personal Access Token erstellen:
   - Gehe zu: https://github.com/settings/tokens
   - Erstelle einen neuen Token mit 'repo' permissions
   - Kopiere den Token

2. Environment Variable setzen:
   export GITHUB_TOKEN="your_token_here"

3. Script ausführen:
   python create_github_issues.py

AUFGABEN DIE ERSTELLT WERDEN:
• QA/Testing-Spezialist - Cloud Build Trigger testen
• Data/AI Engineer - Datenbank prüfen und erweitern  
• Backend-Entwickler - Firebase-Authentifizierung einbauen
• Dokumentations-Agent - Dokumentation aktualisieren
• [EXTRA] Secrets-Verwaltung via Secret Manager
• [EXTRA] Docker Matrix-Builds
• [EXTRA] Web-UI Dashboard für Deployments

Nach der Ausführung können die Issues den entsprechenden Agenten zugewiesen werden.
""")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        print_instructions()
    else:
        success = create_github_issues()
        if not success:
            print("\n💡 Run with --help for setup instructions")
            sys.exit(1)
        else:
            print("\n🎉 All GitHub issues created successfully!")
            print("Die Issues können nun den entsprechenden Agenten zugewiesen werden.")
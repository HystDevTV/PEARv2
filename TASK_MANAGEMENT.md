# PEAR Task Management System

Dieses System implementiert die Aufgabenverteilung aus Issue #16 "Nächsten Aufgaben" mit strukturierter Zuordnung zu spezialisierten Agenten.

## 🚀 Schnellstart

### 1. Aufgaben-Demo ausführen
```bash
python demo_task_assignment.py
```
Zeigt die Zuordnung der deutschen Aufgaben zu den entsprechenden Agenten.

### 2. GitHub Issues erstellen (Optional)
```bash
# GitHub Token setzen
export GITHUB_TOKEN="your_personal_access_token"

# Issues erstellen
python create_github_issues.py
```

## 👥 Agenten-Rollen

Basierend auf Issue #16 wurden vier spezialisierte Agenten definiert:

### A. QA/Testing-Spezialist (`infrastructure`)
**Skills:** Cloud Build, CI/CD Testing, Authorization, Pipeline Integration, GCP, Docker

**Aufgaben:**
- Cloud Build Trigger der PEARv2-VM testen (Build, Push, Deploy, Log-Bucket prüfen)
- Authorisierungsprobleme (wie in PEAR-DEV-TeamV1 gelöst) prüfen und ggf. übertragen
- Automatisierte Tests für neue Features schreiben und in CI/CD-Pipeline integrieren

### B. Data/AI Engineer (`feature`)
**Skills:** MySQL, Database Design, Performance Analysis, Backup Strategies, Data Integrity, SQL

**Aufgaben:**
- Datenbank der PEARv2-VM prüfen: Struktur, Integrität, Performance
- Datenbank ggf. erweitern (neue Tabellen/Spalten für neue Features)
- Backup- und Restore-Strategie für die Datenbank dokumentieren und testen

### C. Backend-Entwickler (`workflow`)
**Skills:** FastAPI, Firebase Auth, Python, API Development, User Management, Security

**Aufgaben:**
- Firebase-Authentifizierung ins Backend einbauen (Registrierung, Login, Token-Handling)
- Python-Code für Authentifizierung und User-Management schreiben
- API-Endpunkte für Authentifizierung und User-Profile implementieren

### D. Dokumentations-Agent (`onboarding`)
**Skills:** Technical Writing, Documentation, Markdown, Knowledge Management, German, Process Documentation

**Aufgaben:**
- Alle neuen Schritte und Änderungen in der dokumentation-pear.md dokumentieren
- Neue Einträge mit aktuellem Datum und Kommentar "[NEU am <Datum>]" kennzeichnen
- Kurze Zusammenfassungen der Änderungen/Erkenntnisse für Neueinsteiger ergänzen

## 📋 EXTRA Aufgaben (Optional)

Können verteilt werden, wenn Zeit verfügbar ist oder das Grundsystem läuft:
- Automatische Secrets-Verwaltung via Secret Manager
- Mehrere Docker Images parallel bauen (Matrix-Strategie)
- Web-UI für Deployments (internes Dashboard)

## 🔧 Verwendung

### Programmatische Nutzung
```python
from team import Agent, TaskManager

# Agenten erstellen
agents = [
    Agent.from_container("container_url", "infrastructure"),  # QA/Testing
    Agent.from_container("container_url", "feature"),        # Data/AI
    Agent.from_container("container_url", "workflow"),       # Backend
    Agent.from_container("container_url", "onboarding")      # Documentation
]

# Task Manager initialisieren
task_manager = TaskManager("HystDevTV/PEARv2")
for agent in agents:
    task_manager.register_agent(agent)

# Aufgaben zuweisen und ausführen
task_manager.assign_tasks_by_category(agents)
task_manager.execute_all()
```

### GitHub Integration
Für echte GitHub-Integration wird ein Personal Access Token benötigt:
1. Token erstellen: https://github.com/settings/tokens
2. Token mit `repo` permissions versehen
3. Als Environment Variable setzen: `export GITHUB_TOKEN="token"`

## 📁 Dateien

- `team.py` - Hauptsystem für Agenten-Management
- `create_github_issues.py` - Script zum Erstellen von GitHub Issues
- `demo_task_assignment.py` - Demonstration der Aufgabenverteilung
- `docs/dokumentation-pear.md` - Hauptdokumentation (aktualisiert mit "[NEU am DATE]")

## 🎯 Prioritäten

**Kritisch (Priority-1):**
- Cloud Build Trigger testen
- Firebase-Authentifizierung implementieren

**Wichtig (Priority-2):**
- Datenbank-Analyse und -erweiterung
- Dokumentations-Updates

**Optional (EXTRA):**
- Secret Manager Integration
- Docker Matrix Builds
- Web Dashboard

## 📝 Dokumentation

Alle Änderungen werden in `/docs/dokumentation-pear.md` mit dem Format "[NEU am DD.MM.YYYY]" dokumentiert.

## 🚀 Nächste Schritte

1. **Issues erstellen:** `python create_github_issues.py` ausführen
2. **Agenten zuweisen:** Issues den entsprechenden Agenten im GitHub Repository zuweisen
3. **Fortschritt überwachen:** Regelmäßige Updates über GitHub Issues und Standups
4. **Dokumentation:** Laufende Aktualisierung der Dokumentation mit "[NEU am Datum]" Markierungen

## 🔍 Troubleshooting

**Import-Fehler:** 
```bash
pip install PyGithub requests google-cloud-storage
```

**GitHub-Zugriff:** 
Token mit `repo` permissions erforderlich.

**Agent-Status:** 
Demo-Script zeigt aktuellen Status aller Agenten.

---

**Basiert auf:** Issue #16 - Nächsten Aufgaben  
**Erstellt am:** 25.07.2025  
**Autor:** PEAR Development Team
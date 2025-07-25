"""
create_issues.py – Erstellt Aufgaben als GitHub-Issues und weist sie optional Agenten zu.

Voraussetzungen:
- python-dotenv und PyGithub müssen installiert sein (siehe requirements.txt)
- GITHUB_TOKEN muss als Umgebungsvariable oder in einer .env-Datei gesetzt sein

Nutzung:
- Aufgaben als Liste im Skript eintragen (title, body, labels)
- Skript ausführen: python create_issues.py
"""

import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

github_token = os.environ.get("GITHUB_TOKEN")
repo_name = "HystDevTV/PEARv2"  # ggf. anpassen

# Aufgabenliste: Jede Aufgabe als Dict mit Titel, Beschreibung und optionalen Labels
TASKS = [
    {
        "title": "Cloud Build Trigger der PEARv2-VM testen und Authorisierungsproblem lösen",
        "body": "QA/Testing-Spezialist: Teste den Cloud Build Trigger der PEARv2-VM. Übertrage die Lösung des Authorisierungsproblems aus PEAR-DEV-TeamV1 und dokumentiere das Ergebnis im Issue.",
        "labels": ["Qualitätssicherung"]
    },
    {
        "title": "Datenbank der PEARv2-VM prüfen und ausbauen",
        "body": "Data/AI Engineer: Überprüfe die Datenbankstruktur und erweitere sie bei Bedarf. Dokumentiere alle Änderungen und Erkenntnisse im Issue.",
        "labels": ["E-Mail- & KI-Verarbeitung"]
    },
    {
        "title": "Firebase-Authentifizierung ins Backend integrieren",
        "body": "Backend-Entwickler: Implementiere die Firebase-Authentifizierung in Python für Registrierung und Login. Dokumentiere den Prozess im Issue.",
        "labels": ["API & Datenbank"]
    },
    {
        "title": "Dokumentation aktualisieren: Neue Features und Änderungen",
        "body": "Dokumentations-Agent: Dokumentiere alle neuen Schritte und Änderungen in der dokumentation-pear.md. Kennzeichne neue Einträge mit aktuellem Datum und Kommentar.",
        "labels": ["Dokumentation"]
    }
]

def main():
    if not github_token:
        print("Fehler: GITHUB_TOKEN nicht gesetzt.")
        return
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    for task in TASKS:
        issue = repo.create_issue(
            title=task["title"],
            body=task["body"],
            labels=task.get("labels", [])
        )
        print(f"Issue erstellt: #{issue.number} – {issue.title}")

if __name__ == "__main__":
    main()

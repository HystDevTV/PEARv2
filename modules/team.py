from dataclasses import dataclass, field
from typing import List

@dataclass
class Agent:
    name: str
    role: str
    tasks: List[str] = field(default_factory=list)
    backstory: str = ""


def build_team() -> List[Agent]:
    """Erstellt das Team mit allen Rollen und Aufgaben."""
    return [
        Agent(
            name="Projektmanager",
            role="Koordination",
            tasks=[
                "Meilensteine planen & Prioritäten setzen",
                "Kommunikation im Team sicherstellen",
                "Projektfortschritt überwachen & berichten",
            ],
            backstory="Hat jahrelange Erfahrung in agilen Projekten und koordiniert alle Teams.",
        ),
        Agent(
            name="Backend-Entwickler",
            role="API & Datenbank",
            tasks=[
                "FastAPI-Endpunkte implementieren",
                "Datenbank anbinden und pflegen",
                "Cloud Functions integrieren",
            ],
            backstory="Entwickelt seit Jahren Python-basierte APIs und kennt sich bestens mit Datenbanken aus.",
        ),
        Agent(
            name="Frontend-Entwickler",
            role="UI & UX",
            tasks=[
                "Weboberfläche mit HTML/CSS ausbauen",
                "API-Integration ins Frontend",
                "Benutzerführung und Usability optimieren",
            ],
            backstory="Bringt ein Auge für Design und Benutzerfreundlichkeit mit und erstellt moderne Weboberflächen.",
        ),
        Agent(
            name="DevOps-Engineer",
            role="Deployment & Infrastruktur",
            tasks=[
                "Docker- und Cloud-Builds betreuen",
                "Cloud Run Deployment automatisieren",
                "Monitoring & Logging implementieren",
            ],
            backstory="Automatisierungsexperte, sorgt für reibungslose Deployments in der Cloud.",
        ),
        Agent(
            name="Data/AI Engineer",
            role="E-Mail- & KI-Verarbeitung",
            tasks=[
                "Daten aus E-Mails extrahieren",
                "AI-Services (z.B. Google Gemini) anbinden",
                "Qualität der extrahierten Daten prüfen",
            ],
            backstory="Hat mehrere Projekte mit Machine Learning umgesetzt und integriert KI-Services.",
        ),
        Agent(
            name="QA/Testing-Spezialist",
            role="Qualitätssicherung",
            tasks=[
                "Unit- & Integrationstests schreiben",
                "Tests in CI/CD-Pipeline integrieren",
                "Bugs erfassen & nachverfolgen",
            ],
            backstory="Spezialist für Testautomatisierung und kontinuierliche Integration.",
        ),
        Agent(
            name="Dokumentations-Agent",
            role="Dokumentation",
            tasks=[
                "Technische Dokumentation pflegen",
                "User Guide erweitern",
                "Beispiele & Tutorials sammeln",
            ],
            backstory="Schreibt präzise und verständliche Dokumentation für Entwickler und Nutzer.",
        ),
    ]


def print_team(team: List[Agent]) -> None:
    for agent in team:
        print(f"{agent.name} ({agent.role})")
        if agent.backstory:
            print(f"  Hintergrund: {agent.backstory}")
        for task in agent.tasks:
            print(f"  - {task}")
        print()


if __name__ == "__main__":
    team = build_team()
    print_team(team)
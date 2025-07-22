from dataclasses import dataclass, field
from typing import List

@dataclass
class Agent:
    name: str
    role: str
    tasks: List[str] = field(default_factory=list)

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
        ),
        Agent(
            name="Backend-Entwickler",
            role="API & Datenbank",
            tasks=[
                "FastAPI-Endpunkte implementieren",
                "Datenbank anbinden und pflegen",
                "Cloud Functions integrieren",
            ],
        ),
        Agent(
            name="Frontend-Entwickler",
            role="UI & UX",
            tasks=[
                "Weboberfläche mit HTML/CSS ausbauen",
                "API-Integration ins Frontend",
                "Benutzerführung und Usability optimieren",
            ],
        ),
        Agent(
            name="DevOps-Engineer",
            role="Deployment & Infrastruktur",
            tasks=[
                "Docker- und Cloud-Builds betreuen",
                "Cloud Run Deployment automatisieren",
                "Monitoring & Logging implementieren",
            ],
        ),
        Agent(
            name="Data/AI Engineer",
            role="E-Mail- & KI-Verarbeitung",
            tasks=[
                "Daten aus E-Mails extrahieren",
                "AI-Services (z.B. Google Gemini) anbinden",
                "Qualität der extrahierten Daten prüfen",
            ],
        ),
        Agent(
            name="QA/Testing-Spezialist",
            role="Qualitätssicherung",
            tasks=[
                "Unit- & Integrationstests schreiben",
                "Tests in CI/CD-Pipeline integrieren",
                "Bugs erfassen & nachverfolgen",
            ],
        ),
        Agent(
            name="Dokumentations-Agent",
            role="Dokumentation",
            tasks=[
                "Technische Dokumentation pflegen",
                "User Guide erweitern",
                "Beispiele & Tutorials sammeln",
            ],
        ),
    ]

def print_team(team: List[Agent]) -> None:
    for agent in team:
        print(f"{agent.name} ({agent.role})")
        for task in agent.tasks:
            print(f"  - {task}")
        print()

if __name__ == "__main__":
    team = build_team()
    print_team(team)
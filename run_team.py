from team import build_team
from crewai import Agent, Crew, Task
import requests
import os

# GitHub-Zugangsdaten (am besten als Umgebungsvariable speichern)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # oder direkt als String
REPO = "HystDevTV/PEARv2"      # z.B. "hystd/PEARv2"

def lade_github_issues():
    url = f"https://api.github.com/repos/{REPO}/issues"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Team laden und Agenten erzeugen
projekt_team = build_team()
crewai_agents = [
    Agent(
        name=ag.name,
        role=ag.role,
        goal=" und ".join(ag.tasks),
    )
    for ag in projekt_team
]

# GitHub Issues laden und als Tasks zuweisen
issues = lade_github_issues()
tasks = []
for i, issue in enumerate(issues):
    if "pull_request" in issue:
        continue  # PRs überspringen
    tasks.append(
        Task(
            description=issue["title"] + "\n" + (issue.get("body") or ""),
            expected_output="Löse das Issue.",
            agent=crewai_agents[i % len(crewai_agents)],  # Aufgaben rotierend zuweisen
        )
    )

# Crew erzeugen und laufen lassen
crew = Crew(
    agents=crewai_agents,
    tasks=tasks
)

if __name__ == "__main__":
    crew.kickoff()
from team import build_team
from crewai import Agent, Crew, Task  # CrewAI-Import

# Team aus deiner team.py laden
projekt_team = build_team()

# Beispiel: Die CrewAI-Agents aus deinen Daten erzeugen
crewai_agents = []
for ag in projekt_team:
    crewai_agents.append(
        Agent(
            name=ag.name,
            role=ag.role,
            goal=" und ".join(ag.tasks),
            # crewai expects: name, role, goal, (optional: backstory, tools, etc.)
        )
    )

# CrewAI-Tasks definieren (hier ein Dummy-Task als Beispiel)
tasks = [
    Task(
        description="Setze das erste Meilenstein-Meeting auf.",
        expected_output="Ein Termin und Agenda für das Kick-Off-Meeting.",
        agent=crewai_agents[0],  # z.B. der Projektmanager
    )
]

# Crew erzeugen und laufen lassen
crew = Crew(
    agents=crewai_agents,
    tasks=tasks
)

if __name__ == "__main__":
    crew.kickoff()  # oder crew.run(), je nach CrewAI-Version
"""Hilfsskript, um die Agenten aus ``team.py`` auszuführen."""

from pathlib import Path
import sys
import threading
import time

# ``team.py`` liegt eine Ebene höher im Repository.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from team import build_team

def agent_worker(agent):
    print(f"{agent.name} startet Aufgabenbearbeitung...")
    for task in agent.tasks:
        # Hier echte Automatisierung einbauen (z.B. OpenAI, Dateioperationen, etc.)
        print(f"{agent.name} erledigt: {task}")
        time.sleep(1)  # Simuliert Bearbeitungszeit
    print(f"{agent.name} hat alle Aufgaben erledigt.\n")

def run_agents() -> None:
    """Initialisiert das Team und lässt alle Agenten parallel arbeiten."""
    team = build_team()
    threads = []
    for agent in team:
        t = threading.Thread(target=agent_worker, args=(agent,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print("Alle Agenten sind fertig!")

if __name__ == "__main__":
    run_agents()
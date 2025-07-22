"""Hilfsskript, um die Agenten aus ``team.py`` auszuführen."""

from pathlib import Path
import sys

# ``team.py`` liegt eine Ebene höher im Repository.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from team import build_team, print_team


def run_agents() -> None:
    """Initialisiert das Team und gibt die Aufgaben aus."""
    team = build_team()
    print_team(team)


if __name__ == "__main__":
    run_agents()

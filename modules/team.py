
import logging
import mysql.connector
from mysql.connector import Error
import time
from dataclasses import dataclass, field
from typing import List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("PEAR-Team")

class DatabaseConnector:
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "pear_user"
        self.password = "SecurePear2024!"
        self.database = "pear_db"
        self.connection = None

    def connect(self) -> bool:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=True
            )
            logger.info("Datenbankverbindung erfolgreich hergestellt")
            return True
        except Error as e:
            logger.error(f"Datenbankverbindung fehlgeschlagen: {str(e)}")
            return False

    def create_tables(self):
        if not self.connection:
            logger.error("Keine Datenbankverbindung vorhanden")
            return False
        cursor = self.connection.cursor()
        try:
            agent_table = """
            CREATE TABLE IF NOT EXISTS agents (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE,
                role VARCHAR(50) NOT NULL,
                backstory TEXT,
                status VARCHAR(20) DEFAULT 'idle',
                tasks_completed INT DEFAULT 0,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            task_table = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(500) NOT NULL,
                description TEXT,
                category VARCHAR(50),
                priority INT DEFAULT 0,
                status VARCHAR(20) DEFAULT 'pending',
                agent_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_at TIMESTAMP NULL,
                completed_at TIMESTAMP NULL,
                result_data TEXT,
                FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE SET NULL
            )
            """
            cursor.execute(agent_table)
            cursor.execute(task_table)
            logger.info("Tabellen erfolgreich erstellt/überprüft")
            return True
        except Error as e:
            logger.error(f"Fehler beim Erstellen der Tabellen: {str(e)}")
            return False
        finally:
            cursor.close()

    def store_agent(self, name: str, role: str, backstory: str = "") -> Optional[int]:
        if not self.connection:
            return None
        cursor = self.connection.cursor()
        try:
            check_query = "SELECT id FROM agents WHERE name = %s"
            cursor.execute(check_query, (name,))
            result = cursor.fetchone()
            if result:
                agent_id = result[0]
                update_query = """UPDATE agents SET role = %s, backstory = %s, status = 'active', last_active = NOW() WHERE id = %s"""
                cursor.execute(update_query, (role, backstory, agent_id))
            else:
                insert_query = """INSERT INTO agents (name, role, backstory, status) VALUES (%s, %s, %s, 'active')"""
                cursor.execute(insert_query, (name, role, backstory))
                agent_id = cursor.lastrowid
            return agent_id
        except Error as e:
            logger.error(f"Fehler beim Speichern des Agenten {name}: {str(e)}")
            return None
        finally:
            cursor.close()

    def store_task(self, title: str, description: str = "", category: str = "", priority: int = 0, agent_id: Optional[int] = None) -> Optional[int]:
        if not self.connection:
            return None
        cursor = self.connection.cursor()
        try:
            query = """INSERT INTO tasks (title, description, category, priority, agent_id) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (title, description, category, priority, agent_id))
            task_id = cursor.lastrowid
            return task_id
        except Error as e:
            logger.error(f"Fehler beim Speichern der Aufgabe '{title}': {str(e)}")
            return None
        finally:
            cursor.close()

    def complete_task(self, task_id: int, agent_id: int, result_data: str = None) -> bool:
        if not self.connection:
            return False
        cursor = self.connection.cursor()
        try:
            query = """UPDATE tasks SET status = 'completed', completed_at = NOW(), result_data = %s WHERE id = %s AND agent_id = %s"""
            cursor.execute(query, (result_data, task_id, agent_id))
            agent_query = "UPDATE agents SET tasks_completed = tasks_completed + 1, last_active = NOW() WHERE id = %s"
            cursor.execute(agent_query, (agent_id,))
            return True
        except Error as e:
            logger.error(f"Fehler beim Abschließen der Aufgabe {task_id}: {str(e)}")
            return False
        finally:
            cursor.close()

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Datenbankverbindung geschlossen")

@dataclass
class Agent:
    name: str
    role: str
    tasks: List[str] = field(default_factory=list)
    backstory: str = ""
    db_connector: Optional[DatabaseConnector] = field(default=None, repr=False)
    db_agent_id: Optional[int] = field(default=None, init=False, repr=False)
    completed_tasks: List[str] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self):
        if self.db_connector:
            self.db_agent_id = self.db_connector.store_agent(self.name, self.role, self.backstory)
            logger.info(f"Agent {self.name} mit DB-ID {self.db_agent_id} registriert")

    def execute_task(self, task: str, category: str = "", priority: int = 0) -> bool:
        logger.info(f"{self.name} startet Aufgabe: {task}")
        task_id = None
        if self.db_connector and self.db_agent_id:
            task_id = self.db_connector.store_task(task, "", category, priority, self.db_agent_id)
        result = self._process_task_by_role(task)
        if self.db_connector and task_id and self.db_agent_id:
            self.db_connector.complete_task(task_id, self.db_agent_id, result)
        self.completed_tasks.append(task)
        logger.info(f"{self.name} hat Aufgabe abgeschlossen: {task}")
        return True

    def _process_task_by_role(self, task: str) -> str:
        processing_times = {
            "Koordination": 1,
            "API & Datenbank": 3,
            "UI & UX": 2,
            "Deployment & Infrastruktur": 2,
            "E-Mail- & KI-Verarbeitung": 3,
            "Qualitätssicherung": 2,
            "Dokumentation": 1
        }
        sleep_time = processing_times.get(self.role, 1)
        time.sleep(sleep_time)
        return f"Aufgabe '{task}' erfolgreich bearbeitet"

    def execute_all_tasks(self) -> None:
        logger.info(f"{self.name} führt {len(self.tasks)} Aufgaben aus")
        for i, task in enumerate(self.tasks, 1):
            self.execute_task(task, category=self.role, priority=len(self.tasks) - i + 1)

def build_team(db_connector: Optional[DatabaseConnector] = None) -> List[Agent]:
    return [
        Agent(
            name="Projektmanager",
            role="Koordination",
            tasks=[
                "Meilensteine planen & Prioritäten setzen",
                "Kommunikation im Team sicherstellen",
                "Projektfortschritt überwachen & berichten",
                "Tickets für alle Aufgaben im GitHub-Repo anlegen",
            ],
            backstory="Hat jahrelange Erfahrung in agilen Projekten und koordiniert alle Teams.",
            db_connector=db_connector
        ),
        Agent(
            name="Backend-Entwickler",
            role="API & Datenbank",
            tasks=[
                "FastAPI-Endpunkte implementieren",
                "Datenbank anbinden und pflegen",
                "Cloud Functions integrieren",
                "Stabilen Betrieb des Endpunkts /api/process-email-for-client sicherstellen",
                "Eventlogs analysieren und Fehler beheben",
                "DevOps beim Docker-Build unterstützen",
            ],
            backstory="Entwickelt seit Jahren Python-basierte APIs und kennt sich bestens mit Datenbanken aus.",
            db_connector=db_connector
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
            db_connector=db_connector
        ),
        Agent(
            name="DevOps-Engineer",
            role="Deployment & Infrastruktur",
            tasks=[
                "Schritt-für-Schritt-Anleitung für Docker-Image erstellen",
                "loud Build Rechte (IAM) detailliert prüfen (siehe /docs/dokumentation-pear.md)",
                "Dienstkonto-Berechtigungen und Authentifizierung testen",
                "Bei Bedarf dediziertes Dienstkonto mit Minimalrechten anlegen",
                "Cloud Run Deployment implementieren und dokumentieren",
                "Qualitätssicherung des Deployment-Prozesses",
            ],
            backstory="Automatisierungsexperte, sorgt für reibungslose Deployments in der Cloud.",
            db_connector=db_connector
        ),
        Agent(
            name="Data/AI Engineer",
            role="E-Mail- & KI-Verarbeitung",
            tasks=[
                "Daten aus E-Mails extrahieren",
                "AI-Services (z.B. Google Gemini) anbinden",
                "Qualität der extrahierten Daten prüfen",
                "SMTP-Client für den automatischen E-Mail-Versand implementieren",
            ],
            backstory="Hat mehrere Projekte mit Machine Learning umgesetzt und integriert KI-Services.",
            db_connector=db_connector
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
            db_connector=db_connector
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
            db_connector=db_connector
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

def main():
    db_connector = DatabaseConnector()
    if not db_connector.connect():
        logger.error("Datenbankverbindung fehlgeschlagen - System wird ohne DB-Integration gestartet")
        db_connector = None
    else:
        db_connector.create_tables()
        logger.info("Datenbank erfolgreich initialisiert")
    team = build_team(db_connector)
    for agent in team:
        agent.execute_all_tasks()
    if db_connector:
        db_connector.close()

if __name__ == "__main__":
    main()
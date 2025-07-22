Projektdokumentation PEAR (Version 0.1.1)
Stand: 18. Juli 2025, 08:00 Uhr CEST
Projektname: PEAR – Professionelle Einsatz-, Abrechnungs- und Ressourcenverwaltung Autor: HystDevTV Gesamt-App Version (aktueller Stand): 0.1.1 Frontend Version: 0.1.1 (Versioniert über package.json) Backend Version: 0.0.0

1. Einleitung
    • Zielsetzung: Entwicklung einer umfassenden Webanwendung zur Digitalisierung und Automatisierung der administrativen Aufgaben von Alltagsbegleitern in der Seniorenpflege. Das Kernziel ist es, Alltagsbegleitern und Verwaltungspersonal die tägliche Routine zu erleichtern, Zeit für die direkte Klientenbetreuung zu schaffen und die Datenverwaltung zu zentralisieren und abzusichern.
    • Motivation: Reduktion von administrativem Stress, Vermeidung von Fehlern, Zeitersparnis, Verbesserung der Kommunikation, Erhöhung der Datenqualität und -sicherheit, Möglichkeit zur Skalierung und Professionalisierung der Pflegedienstleistung.

2. Zielgruppe & Stakeholder
    • Primärnutzer: Alltagsbegleiter in der Seniorenpflege.
    • Sekundärnutzer: Verwaltungspersonal (Büroleitung, Buchhaltung).
    • Indirekte Stakeholder: Klienten und deren Angehörige (profitieren von besserer Organisation).
    • Lieferanten/Partner: Vermittlungsstellen (E-Mail-Schnittstelle).

3. Infrastruktur-Setup (Google Cloud Platform)
Ziel: Bereitstellung einer kosteneffizienten, stabilen und erreichbaren Hosting-Umgebung für PEAR.
3.1 Google Cloud Projekt
    • Name: PEARv2 (Umbenennung von "Projekt-Pear" für klare Projektidentifikation).
    • Zweck: Container für alle Cloud-Ressourcen des Projekts.
3.2 Virtuelle Maschine (VM)
    • Dienst: Google Compute Engine.
    • Instanz-ID: projekt-pear-vm (Neu erstellt nach Problemen der Vorgänger-VMs).
    • Maschinentyp: e2-medium (2 vCPUs, 4 GB RAM) - Kostenpflichtig (~0,022 /Stundein‘us−central1‘),Kostenwerdenvom300 Startguthaben gedeckt. Entscheidung für höhere Leistung in der Entwicklungsphase (max. 20 $ / 30 Tage Budgetanteil).
    • Region: us-central1 (Iowa) - Beibehalten für Kostenkontrolle.
    • Zone: us-central1-a.
    • Betriebssystem: Ubuntu 22.04 LTS (Minimal) Jammy - Schlank und ressourcenschonend.
    • Boot-Laufwerk: Gleichmäßig ausgelasteter nichtflüchtiger Speicher (Balanced Persistent Disk), 30 GB. (Maximaler Free Tier für Disk).
    • Verschlüsselung: Google-verwaltete Verschlüsselungsschlüssel (Standard, sicher und kostenlos).
    • Netzwerkschnittstelle:
        ◦ Subnetzwerk: default-us-central1 (Erstellt mit IP-Bereich 172.16.0.0/12 nach Kollisionen im 10.x.x.x-Bereich).
        ◦ Interne IP: 172.16.0.2.
    • Firewall-Regeln (Google Cloud):
        ◦ allow-http: TCP Port 80 (für Nginx).
        ◦ allow-https: TCP Port 443 (für Nginx).
        ◦ allow-backend-api: TCP Port 8000 (für FastAPI Backend).
        ◦ allow-n8n-port-5678: TCP Port 5678 (für N8N Weboberfläche).
3.3 Datenbank
    • System: MySQL (Wechsel von PostgreSQL nach hartnäckigen Installationsproblemen).
    • Hosting-Strategie: Manuelle Installation auf der projekt-pear-vm.
    • Installation:
        ◦ sudo apt install mysql-server -y.
        ◦ sudo mysql_secure_installation (Absicherung, Root-Passwort gesetzt/leer gelassen, anonyme User entfernt).
    • Datenbank-Name: pear_app_db (Korrigiert von "fleissige_birne_app_db").
    • Datenbank-Benutzer: app_user (mit starkem Passwort).
    • Zugriff: Nur intern (localhost) von Diensten auf derselben VM.
    • Schema-Import: schema.sql für MySQL angepasst und erfolgreich importiert.
        ◦ SERIAL PRIMARY KEY zu INT AUTO_INCREMENT PRIMARY KEY.
        ◦ TIMESTAMP WITH TIME ZONE zu DATETIME.
        ◦ tbl_begleiter um adresse_strasse, adresse_hausnummer, adresse_plz, adresse_ort, firmenname, steuernummer erweitert.

4. Frontend-Bereitstellung (Landing Page, Login, Registrierung)
Ziel: Statische Webseiten für Benutzer über das Internet bereitstellen.
    • Webserver: Nginx (Installation: sudo apt install nginx -y).
    • Web-Root: /var/www/html/ (Manuell erstellt und Berechtigungen gesetzt).
    • Dateien: index.html, login.html, register.html, style.css (lokal entwickelt, in GitHub versioniert).
    • Design: Modernes, klares Design mit Google Fonts (Montserrat für Titel, Poppins für Text). Responsives Design für mobile Geräte (Media Queries) und Sticky Footer implementiert. Formularfelder auf Registrierungsseite in zwei Spalten angeordnet und linksbündig ausgerichtet.
    • Nginx-Konfiguration (/etc/nginx/sites-available/default): Angepasst, um index.html als Standardseite zu priorisieren.

5. Backend-API (Benutzerregistrierung & KI-Extraktion)
Ziel: Bereitstellung eines API-Endpunkts für die Benutzerregistrierung und die KI-gestützte Datenextraktion aus E-Mails.
    • Technologie: Python mit FastAPI.
    • Installation: pip install fastapi uvicorn 'passlib[bcrypt]' mysql-connector-python google-generativeai requests.
    • API-Datei: backend_app.py (Code erstellt und angepasst für MySQL-Verbindung, Passwort-Hashing und Gemini-Integration).
    • Endpunkte:
        ◦ POST /api/register: Für die Benutzerregistrierung.
        ◦ POST /api/process-email-for-client: Empfängt E-Mail-Inhalt und ruft Gemini zur Datenextraktion auf.
    • Logik:
        ◦ Validierung (Passwortübereinstimmung, Mindestlänge).
        ◦ Passworthashing (bcrypt).
        ◦ E-Mail-Eindeutigkeitsprüfung (via Datenbankabfrage).
        ◦ Datenbank-Insertion in tbl_begleiter.
        ◦ Gemini-Integration zur Datenextraktion aus Freitext (mittels google-generativeai).
        ◦ Fehlerbehandlung (z.B. HTTPException für Passwort-Mismatch, E-Mail existiert, interne Fehler).
    • Start: python3 -m uvicorn backend_app:app --host 0.0.0.0 --port 8000.
    • Status: API läuft und ist über Port 8000 erreichbar! 🎉

6. E-Mail-Verarbeitung für Kundenanlage (Architekturwechsel & Aktueller Stand)
6.1 Herausforderungen und Begründung für den Strategiewechsel
Die ursprüngliche Implementierung der E-Mail-Verarbeitung über N8N auf der VM stieß auf anhaltende und fundamentale Probleme, die die Stabilität des Systems gefährdeten und den Fortschritt blockierten. Zu den Hauptproblemen gehörten:
    • Ressourcenmangel und Instabilität von N8N: Trotz der e2-medium VM gab es Probleme beim npm-Build-Prozess und Instabilitäten (Received SIGINT, Portbelegung), die eine zuverlässige Ausführung von N8N verhinderten.
    • Komplexität des N8N-Builds: Der Build aus dem Monorepo war zu fehleranfällig für die VM-Umgebung. Die globale npm-Installation von N8N als Paket war zwar erfolgreich, aber der Dienst selbst blieb instabil.
    • OAuth-Client-Erstellungsprobleme: Die Google Cloud Console akzeptierte keine IP-Adressen als Weiterleitungs-URIs für OAuth-Clients, was den Gmail-Trigger unmöglich machte. Der IMAP-Trigger mit App-Passwort scheiterte ebenfalls.
Aufgrund dieser wiederholten und schwerwiegenden Hindernisse wurde die Entscheidung getroffen, die E-Mail-Verarbeitung von der VM zu entkoppeln und auf eine serverlose Architektur umzustellen.
6.2 Neuer serverloser Ansatz mit Google Cloud Storage & Cloud Run
    • Ziel: Automatisierte, stabile und kostengünstige E-Mail-Verarbeitung für neue Klienten ohne VM-spezifische Instabilität.
    • Implementierung:
        ◦ E-Mail-Empfang: Eingehende E-Mails von Vermittlungsstellen werden über einen externen E-Mail-Provider (z.B. SendGrid, Mailgun) an einen Google Cloud Storage Bucket (pear-email-inbox-raw) weitergeleitet. Fokus liegt hierbei nur auf dem E-Mail-Text-Body, Anlagen werden ignoriert.
        ◦ Trigger: Das Speichern einer neuen E-Mail-Datei im Cloud Storage Bucket löst automatisch einen Google Cloud Run-Dienst aus.
        ◦ Verarbeitung: Der Cloud Run-Dienst liest die E-Mail aus dem Bucket, ruft den bestehenden FastAPI-Endpunkt POST /api/process-email-for-client auf der VM zur KI-gestützten Datenextraktion auf und verarbeitet die Daten in der MySQL-Datenbank auf der VM.
        ◦ Automatisierte E-Mails: Versand von Bestätigungs- und Rückfrage-E-Mails (SMTP-Client in Cloud Run oder separater Dienst).
    • Vorteile: Serverlos, wartungsfrei, hochgradig skalierbar, extrem kosteneffizient (nutzt Free-Tier-Kontingente für minimale Nutzung), umgeht die Probleme der N8N-Installation.
    • Status:
        ◦ Cloud Storage Bucket pear-email-inbox-raw ist erstellt und bereit.
        ◦ Docker-Image-Build: Das Docker-Image für die E-Mail-Verarbeitungsfunktion wurde erfolgreich gebaut (us-central1-docker.pkg.dev/1090307551330/pear-images/email-processor:latest).
        ◦ Docker-Image-Push: Der Push des Docker-Images zur Artifact Registry schlägt fehl mit Permission "artifactregistry.repositories.uploadArtifacts" denied. Dies ist das aktuelle Problem.
            ▪ Ursache: Trotz Zuweisung der Rolle Artifact Registry Create-on-Push Writer an das Benutzerkonto (hystdev2019@gmail.com) und das Dienstkonto der VM, und trotz aggressiver Resets der Authentifizierung (gcloud init, docker login, Docker Desktop Factory Reset), bleibt der Fehler bestehen. Dies deutet auf ein tieferliegendes, hartnäckiges Authentifizierungsproblem im Zusammenspiel zwischen dem lokalen Docker-Client und der Google Cloud Artifact Registry hin.

7. Versionsmanagement & Deployment (Frontend)
Ziel: Automatisiertes und sauberes Hochladen von Code-Änderungen.
    • Versionskontrolle: Git.
    • Remote Repository: GitHub (Public HystDevTV/PEARv2).
    • Lokale Versionierung: package.json ("version": "0.1.1").
    • Automatisches Deployment-Skript auf VM (deploy_all.sh): Holt Code von GitHub, kopiert Dateien nach /var/www/html/, setzt Berechtigungen, startet Nginx neu.

8. Nicht-Funktionale Anforderungen (Lastenheft & Pflichtenheft)
Anforderungen an das System, die sich nicht direkt auf Funktionen, sondern auf Qualität, Sicherheit, Performance etc. beziehen.
    • NF-SI-001 (Sicherheit):
        ◦ NF-SI-001a (Authentifizierung & Autorisierung):
            ▪ Alle Zugriffe auf das System und die Daten müssen authentifiziert (Login) und autorisiert (Rollen/Rechte) sein.
            ▪ Passwörter müssen gehasht und gesalzen gespeichert werden.
            ▪ Sichere Kommunikation über HTTPS/SSL für alle Web- und API-Verbindungen.
        ◦ NF-SI-001b (Datensicherheit):
            ▪ Alle sensiblen Klientendaten müssen Ende-zu-Ende verschlüsselt sein (Datenübertragung und ruhende Daten auf der Datenbank/Speicher).
            ▪ Regelmäßige, automatisierte und verschlüsselte Backups der Datenbank und der abgelegten Dateien (MySQL Backups, Cloud Storage).
            ▪ Zugriff auf die VM und Datenbank nur über SSH-Schlüssel/interne IPs (kein direkter Root-Login über Passwort).
            ▪ Firewall-Regeln restriktiv konfigurieren (nur notwendige Ports öffnen).
        ◦ NF-SI-001c (Anonymität/VPN - spezifische Anfragen):
            ▪ VPN-Konfiguration für Alltagsbegleiter, die anonymen Internetzugang über die VM wünschen (optional, kann als separate Komponente implementiert werden).
            ▪ Sichere Navigation im Darknet (spezifische Beratungsanfrage, nicht direkt Teil der App-Funktionalität).
    • NF-DL-001 (Datenschutz & DSGVO-Konformität):
        ◦ Das System muss von Grund auf DSGVO-konform entwickelt werden.
        ◦ Einwilligung der Klienten zur Datenverarbeitung muss organisatorisch sichergestellt sein.
        ◦ Auftragsverarbeitungsvereinbarungen (AVVs) mit allen Cloud-Dienstleistern (Google Cloud, Gemini API, externe E-Mail-Provider) müssen vorhanden sein.
        ◦ Umsetzung der Betroffenenrechte (Auskunft, Berichtigung, Löschung).
        ◦ Datenminimierung und Zweckbindung.
    • NF-VE-001 (Verfügbarkeit):
        ◦ Das System muss 24/7 erreichbar sein (Webserver, API, Datenbank). Mindestens 99,5% Verfügbarkeit.
        ◦ Automatische Neustarts bei Fehlern (systemd für Dienste).
    • NF-SC-001 (Skalierbarkeit):
        ◦ Das System muss in der Lage sein, mit einer wachsenden Anzahl von Klienten (bis zu 1000) und Alltagsbegleitern (bis zu 50) umzugehen.
        ◦ Kurzfristige Hochskalierung der VM für rechenintensive Aufgaben. Serverlose Komponenten (Cloud Functions/Run) skalieren automatisch.
    • NF-PF-001 (Performance):
        ◦ Ladezeiten der Webseiten unter 3 Sekunden.
        ◦ API-Antwortzeiten unter 1 Sekunde für Standardabfragen.
        ◦ Automatisierte Prozesse (E-Mail-Verarbeitung, Rechnungserstellung) sollen effizient und zeitnah ablaufen.
    • NF-BE-001 (Benutzerfreundlichkeit):
        ◦ Intuitive und leicht bedienbare Oberfläche.
        ◦ Responsives Design für Desktop, Tablet und Smartphone.
        ◦ Klare Fehlermeldungen und Rückmeldungen an den Benutzer.
    • NF-WF-001 (Wartbarkeit & Erweiterbarkeit):
        ◦ Modulares Design (Backend-API, Frontend, serverlose Services) für einfache Erweiterung und Wartung.
        ◦ Clean Code und gute Dokumentation.
        ◦ Automatisierte Deployment-Prozesse (Git-basiert).
    • NF-KO-001 (Kostenkontrolle):
        ◦ Nutzung von Free-Tier-Kontingenten, wo immer möglich.
        ◦ Kostenbewusstes Design der Infrastruktur (z.B. Pay-per-Use für Spitzenlasten, serverlos für Ereignis-basierte Aufgaben).
        ◦ Transparentes Kosten-Monitoring.

# Backend-Entwickler Taskliste - PEARv2 Projekt

## Projektübersicht
Dieses Dokument enthält eine vollständige Liste aller Dateien und Komponenten, die der Backend-Entwickler erstellen kann, basierend auf der aktuellen Projektstruktur und den definierten Anforderungen.

**Zugewiesen an:** Backend-Entwickler  
**Übergabe an:** Projektleiter  
**Erstellungsdatum:** 2025-07-22

---

## 1. FastAPI Backend-Struktur

### 1.1 Haupt-Backend-Dateien (`/pear-backend/`)

- [ ] **`main.py`** - Haupt-FastAPI-Anwendung
  - FastAPI-App-Initialisierung
  - Middleware-Konfiguration
  - Router-Einbindung
  - CORS-Konfiguration

- [ ] **`config.py`** - Konfigurationsdatei
  - Umgebungsvariablen
  - Datenbankverbindung
  - API-Schlüssel
  - Cloud-Services-Konfiguration

- [ ] **`requirements.txt`** - Backend-Abhängigkeiten
  - FastAPI
  - SQLAlchemy
  - Pydantic
  - Google Cloud SDK
  - Weitere benötigte Packages

### 1.2 API-Endpunkte (`/pear-backend/api/`)

- [ ] **`__init__.py`** - Package-Initialisierung
- [ ] **`auth.py`** - Authentifizierungs-Endpunkte
  - POST /api/register
  - POST /api/login
  - POST /api/logout
  - Token-Validierung

- [ ] **`clients.py`** - Client-Management-Endpunkte
  - GET /api/clients
  - POST /api/clients
  - PUT /api/clients/{id}
  - DELETE /api/clients/{id}

- [ ] **`email_processing.py`** - E-Mail-Verarbeitungs-Endpunkte
  - POST /api/process-email-for-client
  - GET /api/email-status/{id}
  - GET /api/processed-emails

- [ ] **`invoices.py`** - Rechnungs-Endpunkte
  - GET /api/invoices
  - POST /api/invoices
  - PUT /api/invoices/{id}
  - GET /api/invoices/{id}/pdf

### 1.3 Datenmodelle (`/pear-backend/models/`)

- [ ] **`__init__.py`** - Package-Initialisierung
- [ ] **`user.py`** - Benutzer-Datenmodell
  - User-Klasse
  - Authentifizierungs-Felder
  - Beziehungen

- [ ] **`client.py`** - Client-Datenmodell
  - Client-Klasse
  - Kontaktinformationen
  - Beziehungen zu Rechnungen

- [ ] **`invoice.py`** - Rechnungs-Datenmodell
  - Invoice-Klasse
  - Rechnungspositionen
  - Status-Tracking

- [ ] **`email_log.py`** - E-Mail-Log-Datenmodell
  - EmailLog-Klasse
  - Verarbeitungsstatus
  - Fehlerbehandlung

### 1.4 Pydantic-Schemas (`/pear-backend/schemas/`)

- [ ] **`__init__.py`** - Package-Initialisierung
- [ ] **`user_schemas.py`** - Benutzer-Validierungsschemas
  - RegisterUser
  - LoginUser
  - UserResponse

- [ ] **`client_schemas.py`** - Client-Validierungsschemas
  - ClientCreate
  - ClientUpdate
  - ClientResponse

- [ ] **`invoice_schemas.py`** - Rechnungs-Validierungsschemas
  - InvoiceCreate
  - InvoiceUpdate
  - InvoiceResponse

- [ ] **`email_schemas.py`** - E-Mail-Validierungsschemas
  - EmailProcessRequest
  - EmailProcessResponse
  - EmailStatusResponse

### 1.5 Services (`/pear-backend/services/`)

- [ ] **`__init__.py`** - Package-Initialisierung
- [ ] **`auth_service.py`** - Authentifizierungs-Services
  - JWT-Token-Generierung
  - Passwort-Hashing
  - Benutzer-Validierung

- [ ] **`email_service.py`** - E-Mail-Verarbeitungs-Services
  - Integration mit Cloud Function
  - Gemini AI-Integration
  - Datenextraktion

- [ ] **`database_service.py`** - Datenbank-Services
  - CRUD-Operationen
  - Transaktionsmanagement
  - Abfrage-Optimierung

- [ ] **`pdf_service.py`** - PDF-Generierungs-Services
  - Rechnungs-PDF-Erstellung
  - Template-Management
  - Formatierung

### 1.6 Datenbank (`/pear-backend/database/`)

- [ ] **`__init__.py`** - Package-Initialisierung
- [ ] **`connection.py`** - Datenbankverbindung
  - SQLAlchemy-Engine
  - Session-Management
  - Connection-Pool

- [ ] **`migrations/`** - Alembic-Migrationen
  - Initialisierungs-Migration
  - Tabellen-Erstellung
  - Index-Erstellung

### 1.7 Middleware (`/pear-backend/middleware/`)

- [ ] **`__init__.py`** - Package-Initialisierung
- [ ] **`auth_middleware.py`** - Authentifizierungs-Middleware
  - JWT-Token-Validierung
  - Berechtigungsprüfung
  - Rate-Limiting

- [ ] **`logging_middleware.py`** - Logging-Middleware
  - Request/Response-Logging
  - Error-Tracking
  - Performance-Monitoring

### 1.8 Utilities (`/pear-backend/utils/`)

- [ ] **`__init__.py`** - Package-Initialisierung
- [ ] **`email_parser.py`** - E-Mail-Parser-Utilities
  - E-Mail-Format-Erkennung
  - Anhang-Extraktion
  - Text-Bereinigung

- [ ] **`validators.py`** - Validierungs-Utilities
  - E-Mail-Validierung
  - Telefonnummer-Validierung
  - Adress-Validierung

- [ ] **`formatters.py`** - Formatierungs-Utilities
  - Datum-Formatierung
  - Währungs-Formatierung
  - Text-Formatierung

---

## 2. Cloud Functions Integration

### 2.1 Cloud Function Updates (`/pear-email-processor-function/`)

- [ ] **`main.py`** - Erweiterte Cloud Function
  - Integration mit FastAPI-Backend
  - Fehlerbehandlung
  - Retry-Logik

- [ ] **`requirements.txt`** - Cloud Function Abhängigkeiten
- [ ] **`config.yaml`** - Cloud Function Konfiguration

---

## 3. Tests

### 3.1 Backend-Tests (`/pear-backend/tests/`)

- [ ] **`__init__.py`** - Test-Package-Initialisierung
- [ ] **`conftest.py`** - Pytest-Konfiguration
- [ ] **`test_auth.py`** - Authentifizierungs-Tests
- [ ] **`test_clients.py`** - Client-Management-Tests
- [ ] **`test_email_processing.py`** - E-Mail-Verarbeitungs-Tests
- [ ] **`test_invoices.py`** - Rechnungs-Tests
- [ ] **`test_database.py`** - Datenbank-Tests

---

## 4. Docker und Deployment

### 4.1 Container-Konfiguration

- [ ] **`/pear-backend/Dockerfile`** - Backend-Container
  - Python-Base-Image
  - Abhängigkeiten-Installation
  - App-Konfiguration

- [ ] **`/pear-backend/.dockerignore`** - Docker-Ignore-Datei
- [ ] **`docker-compose.yml`** - Multi-Container-Setup (Root-Verzeichnis)
  - Backend-Service
  - Datenbank-Service
  - Redis-Service (optional)

### 4.2 Cloud Build

- [ ] **`/pear-backend/cloudbuild.yaml`** - Backend-spezifische Cloud Build
- [ ] Aktualisierung der Root-`cloudbuild.yaml` für Backend-Integration

---

## 5. Dokumentation

### 5.1 API-Dokumentation

- [ ] **`/pear-backend/README.md`** - Backend-spezifische Dokumentation
  - Setup-Anleitung
  - API-Endpunkt-Übersicht
  - Umgebungsvariablen

- [ ] **`/pear-backend/API.md`** - Detaillierte API-Dokumentation
  - Endpunkt-Beschreibungen
  - Request/Response-Beispiele
  - Authentifizierung

### 5.2 Entwickler-Dokumentation

- [ ] **`/pear-backend/DEVELOPMENT.md`** - Entwicklungsrichtlinien
  - Coding-Standards
  - Testing-Richtlinien
  - Deployment-Prozess

---

## 6. Konfigurationsdateien

- [ ] **`/pear-backend/.env.example`** - Beispiel-Umgebungsvariablen
- [ ] **`/pear-backend/alembic.ini`** - Alembic-Konfiguration
- [ ] **`/pear-backend/pytest.ini`** - Pytest-Konfiguration
- [ ] **`/pear-backend/.gitignore`** - Backend-spezifische Git-Ignore

---

## 7. Prioritäten und Reihenfolge

### Phase 1 (Hochpriorität)
1. FastAPI-Grundstruktur (`main.py`, `config.py`)
2. Basis-Datenmodelle (`user.py`, `client.py`)
3. Authentifizierungs-API (`auth.py`)
4. Datenbankverbindung (`connection.py`)

### Phase 2 (Mittlere Priorität)
1. E-Mail-Verarbeitungs-API (`email_processing.py`)
2. Client-Management-API (`clients.py`)
3. E-Mail-Service-Integration (`email_service.py`)
4. Basis-Tests

### Phase 3 (Niedrige Priorität)
1. Rechnungs-Management (`invoices.py`)
2. PDF-Generierung (`pdf_service.py`)
3. Erweiterte Tests
4. Performance-Optimierung

---

## 8. Technische Anforderungen

### Datenbank
- PostgreSQL oder SQLite für Entwicklung
- SQLAlchemy ORM
- Alembic für Migrationen

### API-Framework
- FastAPI mit automatischer OpenAPI-Dokumentation
- Pydantic für Datenvalidierung
- JWT für Authentifizierung

### Cloud-Integration
- Google Cloud Storage für E-Mail-Dateien
- Google Cloud Functions für E-Mail-Verarbeitung
- Gemini AI für Datenextraktion

### Testing
- Pytest für Unit-Tests
- TestClient für API-Tests
- Factory-Pattern für Test-Daten

---

## 9. Abhängigkeiten zu anderen Teams

### Frontend-Team
- API-Endpunkt-Definitionen
- Response-Schema-Definitionen
- Authentifizierungs-Flow

### DevOps-Team
- Docker-Container-Spezifikationen
- Umgebungsvariablen-Definitionen
- Cloud-Deployment-Konfiguration

### Data/AI-Team
- Gemini AI-Integration-Spezifikationen
- E-Mail-Parsing-Anforderungen
- Datenextraktion-Schemas

---

**Hinweis:** Diese Taskliste ist vollständig und kann sofort vom Backend-Entwickler umgesetzt werden. Alle aufgeführten Dateien basieren auf der bestehenden Projektstruktur und den definierten Teamrollen.

**Status:** Bereit zur Übergabe an Projektleiter
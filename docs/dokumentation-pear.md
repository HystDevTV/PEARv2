# PEAR v2 - Cloud Build IAM Rechte - Detaillierte Analyse

## Übersicht

Diese Dokumentation beschreibt die erforderlichen IAM-Berechtigungen für den Cloud Build-Prozess in dem PEAR v2 Projekt. Das Projekt nutzt Google Cloud Build zur automatischen Erstellung und Bereitstellung von Docker-Images über Cloud Run.

## Cloud Build Konfiguration

Die Cloud Build-Konfiguration ist in `cloudbuild.yaml` definiert und umfasst folgende Schritte:

1. **Docker Image Build**: Erstellt ein Docker-Image für den E-Mail-Prozessor
2. **Docker Image Push**: Lädt das Image in die Google Artifact Registry hoch
3. **Cloud Run Deployment**: Stellt den Service auf Cloud Run bereit

## Erforderliche IAM-Berechtigungen

### 1. Cloud Build Service Account Grundberechtigungen

Das Cloud Build-Service-Konto benötigt folgende Basis-Rollen:

```
roles/cloudbuild.builds.builder
```

### 2. Artifact Registry Berechtigungen

Für den Push von Docker-Images in die Artifact Registry:

```
roles/artifactregistry.writer
```

**Spezifische Berechtigungen:**
- `artifactregistry.dockerimages.push`
- `artifactregistry.dockerimages.get`
- `artifactregistry.repositories.uploadArtifacts`

**Repository-Ziel:** `us-central1-docker.pkg.dev/$PROJECT_ID/pear-images/`

### 3. Cloud Run Berechtigungen

Für das Deployment auf Cloud Run:

```
roles/run.developer
```

**Spezifische Berechtigungen:**
- `run.services.create`
- `run.services.update`
- `run.services.get`
- `run.services.delete`
- `run.operations.get`

**Service-Ziel:** `process-pear-emails` in Region `us-central1`

### 4. Logging Berechtigungen

Da die Build-Konfiguration `CLOUD_LOGGING_ONLY` verwendet:

```
roles/logging.logWriter
```

**Spezifische Berechtigungen:**
- `logging.logEntries.create`
- `logging.logEntries.route`

### 5. Service Account Berechtigungen

Falls ein dediziertes Service-Konto für Cloud Run verwendet wird:

```
roles/iam.serviceAccountUser
```

**Spezifische Berechtigungen:**
- `iam.serviceAccounts.actAs`

## Sicherheits-Best-Practices

### Prinzip der minimalen Berechtigung

1. **Dediziertes Service-Konto erstellen:**
```bash
gcloud iam service-accounts create pear-cloudbuild-sa \
    --display-name="PEAR Cloud Build Service Account"
```

2. **Nur erforderliche Rollen zuweisen:**
```bash
# Artifact Registry Writer
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:pear-cloudbuild-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.writer"

# Cloud Run Developer
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:pear-cloudbuild-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.developer"

# Logging Writer
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:pear-cloudbuild-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/logging.logWriter"
```

3. **Cloud Build Konfiguration anpassen:**
```yaml
options:
  logging: CLOUD_LOGGING_ONLY
  substitution_option: ALLOW_LOOSE
serviceAccount: 'projects/$PROJECT_ID/serviceAccounts/pear-cloudbuild-sa@$PROJECT_ID.iam.gserviceaccount.com'
```

### Ressourcen-spezifische Berechtigungen

Statt projekt-weiter Berechtigungen können Sie ressourcen-spezifische Berechtigungen verwenden:

1. **Artifact Registry Repository-Level:**
```bash
gcloud artifacts repositories add-iam-policy-binding pear-images \
    --location=us-central1 \
    --member="serviceAccount:pear-cloudbuild-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.writer"
```

2. **Cloud Run Service-Level (nach der ersten Erstellung):**
```bash
gcloud run services add-iam-policy-binding process-pear-emails \
    --region=us-central1 \
    --member="serviceAccount:pear-cloudbuild-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.developer"
```

## Troubleshooting

### Häufige Berechtigungsfehler

1. **Fehler beim Docker Push:**
   - Überprüfen Sie `roles/artifactregistry.writer`
   - Stellen Sie sicher, dass das Repository existiert
   - Kontrollieren Sie die Repository-URL in `cloudbuild.yaml`

2. **Fehler beim Cloud Run Deployment:**
   - Überprüfen Sie `roles/run.developer`
   - Stellen Sie sicher, dass die Region verfügbar ist
   - Kontrollieren Sie Service-Account-Berechtigungen

3. **Logging-Probleme:**
   - Überprüfen Sie `roles/logging.logWriter`
   - Kontrollieren Sie die Logging-Konfiguration

### Berechtigungen überprüfen

```bash
# Service-Account-Berechtigungen auflisten
gcloud projects get-iam-policy $PROJECT_ID \
    --flatten="bindings[].members" \
    --format="table(bindings.role)" \
    --filter="bindings.members:pear-cloudbuild-sa@$PROJECT_ID.iam.gserviceaccount.com"

# Cloud Build Trigger-Berechtigungen überprüfen
gcloud builds triggers describe $TRIGGER_NAME
```

## Monitoring und Auditing

### Cloud Audit Logs

Aktivieren Sie Audit-Logs für folgende Services:
- Cloud Build API
- Artifact Registry API
- Cloud Run API
- IAM API

### Empfohlene Monitoring-Metriken

1. **Build-Erfolgsrate:** `cloudbuild.googleapis.com/build/count`
2. **Build-Dauer:** `cloudbuild.googleapis.com/build/duration`
3. **IAM-Richtlinien-Verletzungen:** Cloud Security Command Center

## Zusammenfassung

Für eine sichere und funktionsfähige Cloud Build-Pipeline benötigen Sie:

1. **Minimal erforderliche Rollen:**
   - `roles/artifactregistry.writer`
   - `roles/run.developer`
   - `roles/logging.logWriter`

2. **Empfohlene Sicherheitsmaßnahmen:**
   - Dediziertes Service-Konto verwenden
   - Ressourcen-spezifische Berechtigungen
   - Regelmäßige Audit-Log-Überprüfung

3. **Monitoring:**
   - Build-Metriken überwachen
   - Audit-Logs aktivieren
   - Sicherheitswarnungen einrichten

Diese Konfiguration stellt sicher, dass Ihr Cloud Build-Prozess sicher und mit minimalen Berechtigungen funktioniert.
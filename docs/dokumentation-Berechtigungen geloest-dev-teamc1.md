🚀 GCP Cloud Build Trigger mit eigenem Service Account – Schritt-für-Schritt

1. Ziel

Automatisierte Builds in GCP mit einem eigenen, minimal berechtigten Service Account für maximale Sicherheit und Kontrolle.

2. Voraussetzungen

Du hast Zugriff auf das GCP-Projekt als „Inhaber“ oder mit passenden IAM-Rechten.

Cloud Build API & Artifact Registry sind aktiviert.

Dein Quell-Repo (z. B. GitHub) ist verbunden.

3. Schritte im Detail

A. Eigenen Service Account anlegen

Navigation:Google Cloud Console → IAM & Verwaltung → Dienstkonten

Neues Dienstkonto erstellen

Name: z. B. build-trigger

ID: z. B. build-trigger

Beschreibung: z. B. Service Account für Cloud Build Trigger

(Optional) Mitglieder als „Dienstkontonutzer“ eintragen

Trage dich selbst (und ggf. andere Teammitglieder) direkt beim Erstellen als Dienstkontonutzer ein.

Deine E-Mail (z. B. dein.name@gmail.com).

B. Benötigte Rollen zuweisen

Entweder direkt beim Anlegen des Service Accounts oder im Anschluss unter „IAM & Verwaltung > IAM“.

Dem neuen Service Account folgende Rollen geben:

roles/cloudbuild.builds.builder (Cloud-Build-Dienstkonto)

roles/artifactregistry.writer (Artifact Registry Writer)

roles/storage.objectViewer (Storage-Objekt-Betrachter)

roles/iam.serviceAccountUser (Dienstkontonutzer)(Wichtig: Dir selbst auf dieses Konto zuweisen!)

Je nach Bedarf:

roles/secretmanager.secretAccessor (falls Zugriff auf Secrets)

Repository-spezifische Rollen, z. B. roles/source.reader oder „Secure Source Manager Repository Reader“ für Zugriff auf dein GitHub-Repo

C. Build Trigger anlegen

Empfohlene Variante (empfohlen für Logs-Bucket & maximale Flexibilität):

1. cloudbuild.yaml im Repo anlegen (Beispiel: vollständige Pipeline mit Logs-Bucket!)

steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'us-central1-docker.pkg.dev/$PROJECT_ID/pear-images/email-processor:latest', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'us-central1-docker.pkg.dev/$PROJECT_ID/pear-images/email-processor:latest']
  - name: 'gcr.io/cloud-builders/gcloud'
    id: 'Deploy Cloud Run Service'
    args:
      - 'run'
      - 'deploy'
      - 'process-pear-emails'
      - '--image'
      - 'us-central1-docker.pkg.dev/$PROJECT_ID/pear-images/email-processor:latest'
      - '--platform'
      - 'managed'
      - '--region'
      - 'us-central1'
      - '--allow-unauthenticated'
      - '--set-env-vars'
      - 'FASTAPI_API_URL=http://34.46.6.30:8000'
      - '--no-cpu-throttling'
      - '--min-instances'
      - '0'
      - '--max-instances'
      - '1'
images:
  - 'us-central1-docker.pkg.dev/$PROJECT_ID/pear-images/email-processor:latest'
options:
  logging: CLOUD_LOGGING_ONLY
logsBucket: gs://build-team-storage

(Pfad, Tag, Cloud Run Name, und Umgebungsvariablen ggf. anpassen!)

2. Build Trigger im UI anlegen

Trigger-Typ: Cloud Build-Konfigurationsdatei (YAML oder JSON)

Datei: Pfad zu deiner cloudbuild.yaml

Dienstkonto: build-trigger@pear-dev-teamv1.iam.gserviceaccount.com

Jetzt erscheint das Feld fürs Logs-Bucket oder es wird über logsBucket: in der YAML gesetzt.

3. Trigger speichern und testen

Commit auf main (oder anderen Branch)

Build läuft, Logs landen im angegebenen GCS-Bucket

D. Build testen

Push in den konfigurierten Branch machen

Trigger sollte automatisch laufen, das Image wird gebaut und in die Artifact Registry gepusht.

4. Vorteile dieses Vorgehens

Sicherheit: Kein Overprovisioning – nur explizit zugewiesene Rechte

Nachvollziehbarkeit: Auditierbar, wer und was Aktionen im Build ausgeführt hat

Skalierbarkeit: Eigenes Konto für Builds – leichter zu rotieren, entfernen, automatisieren

5. Troubleshooting

Dienstkonto nicht auswählbar:→ Eigenes Konto erstellen (kein „Google managed“), dir selbst als Dienstkontonutzer eintragen, Seite ggf. neuladen.

Berechtigungsfehler beim Build:→ Fehlende Rolle beim Service Account nachtragen (z. B. Artifact Registry Writer, Secret Accessor).

Fehler bei Nutzung eines eigenen Service Accounts:→ Fehlermeldung: "if 'build.service_account' is specified, the build must either (a) specify 'build.logs_bucket', (b) use the REGIONAL_USER_OWNED_BUCKET build.options.default_logs_bucket_behavior option, or (c) use either CLOUD_LOGGING_ONLY / NONE logging options"

2. Alternativ: Eigenes GCS-Bucket für Logs anlegen

Eigenes Bucket erstellen:

Google Cloud Console → Cloud Storage → Buckets → "Bucket erstellen"

Einen aussagekräftigen Namen vergeben (z. B. build-logs-<projektname>)

Region passend zur Build-Region auswählen

Dem Service Account Berechtigung auf das Bucket geben:

Rolle: roles/storage.objectAdmin oder mindestens roles/storage.objectCreator für das Log-Bucket

Entweder via Console unter "Berechtigungen" oder per gcloud:

gcloud storage buckets add-iam-policy-binding gs://build-logs-<projektname> \
  --member="serviceAccount:build-trigger@<PROJECT_ID>.iam.gserviceaccount.com" \
  --role="roles/storage.objectCreator"

Im Build-Trigger das Logs Bucket angeben:

Im Build-Trigger unter "Erweiterte Einstellungen" ("advanced options") das Feld logs bucket auf das neue Bucket setzen, z. B.: gs://build-logs-<projektname>

Trigger speichern und testen!

Optional: CLI-Snippet für Profis

gcloud iam service-accounts create build-trigger --display-name="Build Trigger Service Account"

gcloud projects add-iam-policy-binding <PROJECT_ID> \
  --member="serviceAccount:build-trigger@<PROJECT_ID>.iam.gserviceaccount.com" \
  --role="roles/cloudbuild.builds.builder"

gcloud projects add-iam-policy-binding <PROJECT_ID> \
  --member="serviceAccount:build-trigger@<PROJECT_ID>.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding <PROJECT_ID> \
  --member="serviceAccount:build-trigger@<PROJECT_ID>.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"

gcloud iam service-accounts add-iam-policy-binding build-trigger@<PROJECT_ID>.iam.gserviceaccount.com \
  --member="user:deine@email.de" \
  --role="roles/iam.serviceAccountUser"

Diese Anleitung kannst du direkt ins Wiki oder als PDF speichern. Melde dich, wenn du noch Textbausteine für die Team-Schulung brauchst oder noch weitere Automatisierungsschritte möchtest!


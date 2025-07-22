# 🚀 GCP Cloud Build Trigger mit eigenem Service Account – Schritt-für-Schritt

---

## 1. Ziel

Automatisierte Builds in GCP mit einem eigenen, minimal berechtigten Service Account für maximale Sicherheit und Kontrolle.

---

## 2. Voraussetzungen

- Du hast Zugriff auf das GCP-Projekt als „Inhaber“ oder mit passenden IAM-Rechten.
- Cloud Build API & Artifact Registry sind aktiviert.
- Dein Quell-Repo (z. B. GitHub) ist verbunden.

---

## 3. Schritte im Detail

---

### A. Eigenen Service Account anlegen

1. **Navigation:**\
   Google Cloud Console → IAM & Verwaltung → Dienstkonten

2. **Neues Dienstkonto erstellen**

   - Name: z. B. build-trigger
   - ID: z. B. build-trigger
   - Beschreibung: z. B. Service Account für Cloud Build Trigger

3. **(Optional) Mitglieder als „Dienstkontonutzer“ eintragen**

   - Trage dich selbst (und ggf. andere Teammitglieder) direkt beim Erstellen als Dienstkontonutzer ein.
   - Deine E-Mail (z. B. [dein.name@gmail.com](mailto\:dein.name@gmail.com)).

---

### B. Benötigte Rollen zuweisen

> Entweder direkt beim Anlegen des Service Accounts oder im Anschluss unter „IAM & Verwaltung > IAM“.

**Dem neuen Service Account folgende Rollen geben:**

- roles/cloudbuild.builds.builder (**Cloud-Build-Dienstkonto**)
- roles/artifactregistry.writer (**Artifact Registry Writer**)
- roles/storage.objectViewer (**Storage-Objekt-Betrachter**)
- roles/iam.serviceAccountUser (**Dienstkontonutzer**)\
  (Wichtig: Dir selbst auf dieses Konto zuweisen!)
- Je nach Bedarf:
  - roles/secretmanager.secretAccessor (falls Zugriff auf Secrets)
  - Repository-spezifische Rollen, z. B. roles/source.reader oder „Secure Source Manager Repository Reader“ für Zugriff auf dein GitHub-Repo

---

### C. Build Trigger anlegen

1. **Navigation:**\
   Cloud Build → Trigger → Trigger erstellen

2. **Trigger konfigurieren:**

   - Quell-Repo auswählen (z. B. GitHub, Cloud Source Repository)
   - Trigger-Bedingung: z. B. Push auf main oder dev Branch
   - Build-Konfiguration: Dockerfile/Cloudbuild.yaml angeben

3. **Dienstkonto auswählen:**

   - Im Dropdown Dienstkonto:\
     Jetzt build-trigger\@...iam.gserviceaccount.com auswählen (neues eigenes Konto)
   - Falls nicht sichtbar: Seite neu laden oder kurz ab-/anmelden.

---

### D. Build testen

- Push in den konfigurierten Branch machen
- Trigger sollte automatisch laufen, das Image wird gebaut und in die Artifact Registry gepusht.

---

## 4. Vorteile dieses Vorgehens

- Sicherheit: Kein Overprovisioning – nur explizit zugewiesene Rechte
- Nachvollziehbarkeit: Auditierbar, wer und was Aktionen im Build ausgeführt hat
- Skalierbarkeit: Eigenes Konto für Builds – leichter zu rotieren, entfernen, automatisieren

---

## 5. Troubleshooting

- Dienstkonto nicht auswählbar:\
  → Eigenes Konto erstellen (kein „Google managed“), dir selbst als Dienstkontonutzer eintragen, Seite ggf. neuladen.
- Berechtigungsfehler beim Build:\
  → Fehlende Rolle beim Service Account nachtragen (z. B. Artifact Registry Writer, Secret Accessor).

---

## Optional: CLI-Snippet für Profis

```bash
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
```

---

**Diese Anleitung kannst du direkt ins Wiki oder als PDF speichern.** Melde dich, wenn du noch Textbausteine für die Team-Schulung brauchst oder noch weitere Automatisierungsschritte möchtest!


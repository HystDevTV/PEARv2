# PEAR Scripts Directory

Diese Verzeichnis enthält Hilfsskripte für die PEAR-Automatisierung.

## Scripts

### `demo_workflow_test.py`

**Zweck:** Demonstriert und testet die Funktionalität des PEAR Demo-Workflows.

**Verwendung:**
```bash
python scripts/demo_workflow_test.py
```

**Funktionalität:**
- Fügt automatisch einen neuen Eintrag zur Projektdokumentation (`docs/dokumentation-pear.md`) hinzu
- Verwendet aktuelle Zeitstempel für nachvollziehbare Einträge
- Kann sowohl lokal als auch in GitHub Actions verwendet werden
- Bietet benutzerfreundliche Ausgabe mit Emojis und Statusmeldungen

**Integration:** Wird vom GitHub Actions Workflow `.github/workflows/demo_pear_workflow.yml` verwendet.

## Workflow-Automatisierung

Der Demo-Workflow zeigt, wie PEAR-Aufgaben automatisiert dokumentiert werden können:

1. **Automatische Dokumentation:** Neue Einträge werden mit Zeitstempel versehen
2. **Git-Integration:** Änderungen werden automatisch committed und gepusht
3. **Nachvollziehbarkeit:** Alle Automatisierungsschritte sind dokumentiert
4. **Skalierbarkeit:** Das Muster kann für alle PEAR-Aufgaben übernommen werden

## Verwendung für Project Leader

Um den Demo-Workflow zu starten:

1. Gehen Sie zu GitHub Actions im Repository
2. Wählen Sie "PEAR Demo Workflow"
3. Klicken Sie "Run workflow"
4. Der Workflow fügt automatisch einen neuen Eintrag zur Dokumentation hinzu

Dies demonstriert die automatisierte PEAR-Arbeitsweise für alle Entwicklungsschritte.
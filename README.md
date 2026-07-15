# ECS Pipeline

Synct Close CRM Opportunities alle 15 Minuten in eine JSON Datei.
Der Close API Key liegt als Github Secret, nie im Code.

## Setup

### 1. Repo anlegen

Neues Repo auf Github erstellen, z.B. `escoerfan/ecs-pipeline`.
Diese Dateien hochladen (Struktur unten).

### 2. Secret hinterlegen

Im Repo: Settings -> Secrets and variables -> Actions -> New repository secret

Name: `CLOSE_API_KEY`
Value: dein Close API Key (aus Close: Settings -> API Keys)

### 3. Workflow aktivieren

Der Workflow läuft automatisch alle 15 Minuten (Cron in `.github/workflows/sync-opportunities.yml`).
Erster Lauf: Actions Tab im Repo öffnen, "Sync Close Opportunities" auswählen, "Run workflow" klicken.

Github Actions Cron ist nicht exakt auf die Minute, kann ein paar Minuten Verzug haben. Für ECS unkritisch.

### 4. JSON URL fürs Board

Nach dem ersten erfolgreichen Lauf liegt die Datei unter:

```
https://raw.githubusercontent.com/escoerfan/ecs-pipeline/main/data/opportunities.json
```

Diese URL nutzt das HTML Board zum Laden der Daten. Kein API Key im Frontend nötig.

## Struktur

```
ecs-pipeline/
  .github/workflows/sync-opportunities.yml
  scripts/fetch_opportunities.py
  data/opportunities.json   (wird automatisch erzeugt)
  README.md
```

## Manuell testen

```
export CLOSE_API_KEY="dein_key"
pip install --break-system-packages requests
python scripts/fetch_opportunities.py
```

Erzeugt `data/opportunities.json` lokal zum Prüfen, bevor es über Github läuft.

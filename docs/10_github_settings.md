# GitHub-Einstellungen

## Repository-Konfiguration

### Default Branch

- Name: `main`
- Geschützt durch Branch-Protection-Rules

### Branch Protection Rules (main)

Empfohlene Einstellungen für `main`:

```yaml
Require a pull request before merging: true
  - Require approvals: 1
  - Dismiss stale reviews: true
  - Require review from code owners: optional

Require status checks to pass:
  - Require branches to be up to date: true
  - Required checks:
    - lint
    - test (3.11)
    - test (3.12)

Require conversation resolution: true
Do not allow bypassing: true (für Teams)
```

### Manuelle Einrichtung

1. Settings → Branches → Add branch protection rule
2. Branch name pattern: `main`
3. Checkboxen wie oben aktivieren

## GitHub Actions

CI-Workflow in `.github/workflows/ci.yml`:

- Trigger: Push auf main, Pull Requests
- Jobs: lint, test
- Matrix: Python 3.11, 3.12

### Secrets

Für PyPI-Upload (optional):
- `PYPI_API_TOKEN`: PyPI API Token

## Templates

### Pull Request Template

`.github/pull_request_template.md`

Enthält:
- Beschreibung
- Art der Änderung
- Checkliste
- Zugehörige Issues

### Issue Templates

`.github/ISSUE_TEMPLATE/`

- `bug_report.md`: Bug-Reports
- `feature_request.md`: Feature-Anfragen

## Labels

Empfohlene Labels:

| Label | Farbe | Beschreibung |
|-------|-------|--------------|
| bug | #d73a4a | Fehler/Bugs |
| enhancement | #a2eeef | Neue Features |
| documentation | #0075ca | Dokumentation |
| good first issue | #7057ff | Für Einsteiger |
| help wanted | #008672 | Hilfe erwünscht |
| wontfix | #ffffff | Wird nicht behoben |
| duplicate | #cfd3d7 | Duplikat |

## Projects (optional)

Kanban-Board für Issue-Tracking:

Spalten:
1. Backlog
2. To Do
3. In Progress
4. Review
5. Done

## Automatisierung

### Dependabot

`.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Stale Issues

Optional: `.github/workflows/stale.yml` für automatisches Schließen inaktiver Issues.

## CODEOWNERS (optional)

`.github/CODEOWNERS`:

```
# Default owners
* @team-lead

# Specific paths
/src/pmtool/ui/ @ui-team
/docs/ @docs-team
```

# Packaging & Release

## Versionierung

PMTool folgt [Semantic Versioning](https://semver.org/):

- **MAJOR**: Inkompatible API-Änderungen
- **MINOR**: Neue Features, abwärtskompatibel
- **PATCH**: Bugfixes, abwärtskompatibel

Version wird definiert in:
- `pyproject.toml`: `version = "0.1.0"`
- `src/pmtool/__init__.py`: `__version__ = "0.1.0"`

## Build-System

PMTool verwendet **hatchling** als Build-Backend.

### Wheel erstellen

```bash
pip install build
python -m build
```

Erzeugt:
- `dist/pmtool-0.1.0-py3-none-any.whl`
- `dist/pmtool-0.1.0.tar.gz`

### Installation aus Wheel

```bash
pip install dist/pmtool-0.1.0-py3-none-any.whl
```

## PyPI-Veröffentlichung

### TestPyPI (zum Testen)

```bash
pip install twine
twine upload --repository testpypi dist/*
```

### PyPI (Produktion)

```bash
twine upload dist/*
```

## Standalone-Executable

Für Desktop-Distribution kann PyInstaller verwendet werden:

```bash
pip install pyinstaller
pyinstaller --name PMTool --windowed src/pmtool/app.py
```

Erzeugt ausführbare Datei in `dist/PMTool/`.

### macOS App Bundle

```bash
pyinstaller --name PMTool --windowed --onefile \
    --icon=resources/icon.icns \
    src/pmtool/app.py
```

### Windows Executable

```bash
pyinstaller --name PMTool --windowed --onefile \
    --icon=resources/icon.ico \
    src/pmtool/app.py
```

## Release-Prozess

1. **Version aktualisieren**
   - `pyproject.toml`
   - `src/pmtool/__init__.py`

2. **CHANGELOG aktualisieren**
   - Neue Version mit Datum
   - Änderungen dokumentieren

3. **Tests durchführen**
   ```bash
   pytest --cov=pmtool
   ruff check src tests
   ```

4. **Commit & Tag**
   ```bash
   git add .
   git commit -m "Release v0.1.0"
   git tag v0.1.0
   git push origin main --tags
   ```

5. **Build erstellen**
   ```bash
   python -m build
   ```

6. **Veröffentlichen**
   ```bash
   twine upload dist/*
   ```

## Release-Checkliste

- [ ] Alle Tests bestehen
- [ ] Linting fehlerfrei
- [ ] Version aktualisiert (pyproject.toml, __init__.py)
- [ ] CHANGELOG aktualisiert
- [ ] Dokumentation aktuell
- [ ] Git-Tag erstellt
- [ ] Build erfolgreich
- [ ] Upload zu PyPI erfolgreich

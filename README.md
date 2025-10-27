# Playwright Python smoke test

This repository contains a minimal Playwright + pytest setup in Python.

Quick start

1. Create and activate a virtual environment (recommended).

   PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Install Playwright browsers:

   ```powershell
   playwright install
   # or for CI/debian-based: playwright install --with-deps
   ```

4. Run tests:

   ```powershell
   python -m pytest -q
   ```

Notes

- Tests are under `tests/` and use the `page` fixture from `pytest-playwright`.
- CI workflow is included at `.github/workflows/ci.yml` as an example.

Windows / Troubleshooting

- If `python --version` prints a path under `C:\Users\...\WindowsApps`, that is often the Microsoft Store stub. Install an official Python distribution from https://www.python.org/downloads/ (choose "Windows installer") then reopen your terminal.
- If `python -m venv .venv` fails, verify you have the correct Python installer (the official installer adds the venv module). Re-run the installer and ensure "Add Python to PATH" is selected or use the full path to python.exe.
- If you see `playwright: command not found`, use the module entrypoint:

```powershell
python -m playwright install
```

CI notes

- The included GitHub Actions workflow (in `.github/workflows/ci.yml`) runs tests on Ubuntu with a small matrix for Python versions. It also caches pip and Playwright browser downloads to speed up runs.
- Test results are written to `reports/junit.xml` and uploaded as a workflow artifact.

Next steps you may want me to do for you:

- Add more example tests (forms, login flows), and common helper fixtures (auth, test-data).
- Add test report HTML generation (pytest-html) and upload the HTML as an artifact.
- Configure Playwright to run against a local dev server by adding `BASE_URL` env var to CI.

Convenience scripts

Two helper PowerShell scripts are included in `scripts/` to simplify local setup and test runs on Windows:

- `scripts/setup.ps1` — Creates a `.venv` virtual environment (if missing), installs Python requirements from `requirements.txt`, and runs `playwright install --with-deps` to download browser binaries.
- `scripts/run-tests.ps1` — Ensures a `reports/` directory exists and runs `pytest` using the virtualenv python.

Usage (PowerShell):

```powershell
# From the repo root
.\scripts\setup.ps1
.\scripts\run-tests.ps1
```

If you prefer to activate the venv manually, run:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest -q
```

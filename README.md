# Enterprise Threat Detection & Response Platform

A lightweight prototype that combines:

- **Simulated EDR/SIEM telemetry generation** using `psutil` + random events.
- A **Flask web dashboard** for login, live logs, alerts, and AI risk score.
- A **Tkinter desktop interface** with tabbed views for overview, logs, alerts, and settings.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install flask psutil
python app.py
```

## Default web login

- Username: `admin`
- Password: `admin123`

## Notes

- The web server runs on `http://127.0.0.1:5000`.
- The desktop UI and web server start together from the same process.

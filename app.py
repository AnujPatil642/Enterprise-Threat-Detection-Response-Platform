import datetime
import random
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

import psutil
from flask import Flask, redirect, render_template_string, request, session

# =============================
# GLOBAL DATA
# =============================

logs = []
alerts = []
risk_score = 0
auto_response_enabled = False

# =============================
# SIMULATED AI + EDR MONITOR
# =============================


def monitor_system():
    global risk_score

    while True:
        cpu = psutil.cpu_percent()
        event = random.choice(
            [
                "Process Started",
                "File Modified",
                "Network Connection",
                "Registry Access",
            ]
        )
        status = "Normal"

        if cpu > 70:
            status = "Suspicious"
            alerts.append(
                {
                    "time": datetime.datetime.now().strftime("%H:%M:%S"),
                    "threat": "High CPU Usage",
                    "severity": "High",
                }
            )

        logs.append(
            {
                "time": datetime.datetime.now().strftime("%H:%M:%S"),
                "event": event,
                "status": status,
            }
        )

        if len(logs) > 50:
            logs.pop(0)

        risk_score = random.randint(10, 95)

        time.sleep(3)


# =============================
# FLASK WEB DASHBOARD
# =============================

app = Flask(__name__)
app.secret_key = "secret"


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["user"] = "admin"
            return redirect("/dashboard")
        return "Invalid Credentials"

    return render_template_string(login_html)


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return render_template_string(dashboard_html, logs=logs, alerts=alerts, risk=risk_score)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# =============================
# TKINTER DESKTOP APP
# =============================


def start_desktop_app():
    root = tk.Tk()
    root.title("AI EDR + SIEM Desktop")
    root.geometry("700x500")
    root.configure(bg="#0f172a")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Overview Tab
    overview = tk.Frame(notebook, bg="#0f172a")
    notebook.add(overview, text="Overview")

    risk_label = tk.Label(
        overview,
        text="AI Risk Score: 0%",
        fg="white",
        bg="#0f172a",
        font=("Arial", 20),
    )
    risk_label.pack(pady=20)

    def update_risk():
        risk_label.config(text=f"AI Risk Score: {risk_score}%")
        root.after(2000, update_risk)

    update_risk()

    # Logs Tab
    logs_tab = tk.Frame(notebook)
    notebook.add(logs_tab, text="Live Logs")

    log_box = tk.Text(logs_tab)
    log_box.pack(fill="both", expand=True)

    def update_logs():
        log_box.delete(1.0, tk.END)
        for log in logs:
            log_box.insert(tk.END, f"{log['time']} | {log['event']} | {log['status']}\n")
        root.after(3000, update_logs)

    update_logs()

    # Alerts Tab
    alerts_tab = tk.Frame(notebook)
    notebook.add(alerts_tab, text="Threat Alerts")

    alert_box = tk.Text(alerts_tab)
    alert_box.pack(fill="both", expand=True)

    def update_alerts():
        alert_box.delete(1.0, tk.END)
        for alert in alerts:
            alert_box.insert(
                tk.END,
                f"{alert['time']} | {alert['threat']} | {alert['severity']}\n",
            )
        root.after(4000, update_alerts)

    update_alerts()

    # Settings Tab
    settings_tab = tk.Frame(notebook)
    notebook.add(settings_tab, text="System Settings")

    def toggle_auto():
        global auto_response_enabled

        auto_response_enabled = not auto_response_enabled
        messagebox.showinfo("System", f"Auto Response: {auto_response_enabled}")

    btn = tk.Button(settings_tab, text="Toggle Auto Response", command=toggle_auto)
    btn.pack(pady=20)

    root.mainloop()


# =============================
# HTML TEMPLATES
# =============================

login_html = """
<!DOCTYPE html>
<html>
<body style="background:#0f172a;color:white;text-align:center;padding-top:150px;font-family:Arial;">
<h2>AI Enterprise Threat Platform</h2>
<form method="POST">
<input name="username" placeholder="Username" required><br><br>
<input name="password" type="password" placeholder="Password" required><br><br>
<button type="submit">Login</button>
</form>
</body>
</html>
"""

dashboard_html = """
<!DOCTYPE html>
<html>
<body style="background:#0f172a;color:white;font-family:Arial;">
<h2>Enterprise Dashboard</h2>
<h3>AI Risk Score: {{risk}}%</h3>

<h3>Live Logs</h3>
{% for log in logs %}
<p>{{log.time}} | {{log.event}} | {{log.status}}</p>
{% endfor %}

<h3>Threat Alerts</h3>
{% for alert in alerts %}
<p>{{alert.time}} | {{alert.threat}} | {{alert.severity}}</p>
{% endfor %}

<br><a href="/logout">Logout</a>
</body>
</html>
"""


# =============================
# MAIN EXECUTION
# =============================

if __name__ == "__main__":
    threading.Thread(target=monitor_system, daemon=True).start()
    threading.Thread(target=lambda: app.run(debug=False, use_reloader=False), daemon=True).start()
    start_desktop_app()

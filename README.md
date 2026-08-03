# Infrastructure Monitoring & Self-Healing Automation Platform

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python\&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-E95420?logo=ubuntu\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

A Python-based infrastructure monitoring platform that continuously monitors multiple Linux servers over SSH, detects failures, performs automated recovery, generates alerts, and generates HTML dashboards and incident reports.

---

# Overview

This project automates infrastructure health monitoring for Linux servers using SSH. It periodically collects system metrics, verifies service availability, performs automatic recovery when failures are detected, stores historical metrics, and generates dashboards and reports for system administrators.

---

# Features

* Multi-server SSH monitoring
* Concurrent monitoring using ThreadPoolExecutor
* CPU monitoring
* Memory monitoring
* Disk monitoring
* Network monitoring
* Port scanning
* Service monitoring
* Automatic service recovery
* Alert generation
* Log analysis
* Incident report generation
* HTML dashboard
* Historical metrics
* Scheduled execution

---

# Architecture

## System Overview

```mermaid
graph TD

A[Scheduler / Main Program]

A --> B[Configuration Loader]

B --> C[Server Inventory]

A --> D[Monitoring Engine]

D --> E[SSH Connection]

E --> F[Linux Servers]

F --> G[Metrics Collection]

G --> H[Health Analysis]

H --> I[Recovery Engine]

I --> J[Alert Engine]

J --> K[Dashboard Generator]

K --> L[HTML Dashboard]

J --> M[Incident Reports]
```

---

## Monitoring Flow

```mermaid
graph LR

Start --> Load_Config

Load_Config --> Connect_SSH

Connect_SSH --> CPU

CPU --> Memory

Memory --> Disk

Disk --> Network

Network --> Ports

Ports --> Services

Services --> Save_Metrics

Save_Metrics --> Finish
```

---

## Recovery Flow

```mermaid
graph TD

Service_Check --> Healthy

Healthy -- Yes --> Continue

Healthy -- No --> Restart_Service

Restart_Service --> Verify

Verify -- Success --> Recovery_Log

Verify -- Failed --> Generate_Alert

Generate_Alert --> Incident_Report
```

---

## Dashboard Flow

```mermaid
graph LR

Collected_Metrics

Collected_Metrics --> JSON

JSON --> Dashboard_Generator

Dashboard_Generator --> HTML_Dashboard

HTML_Dashboard --> Browser
```

---

## Reporting Flow

```mermaid
graph TD

Monitoring_Data

Monitoring_Data --> Metrics_JSON

Metrics_JSON --> Incident_Report

Metrics_JSON --> Daily_Report

Metrics_JSON --> Weekly_Report

Metrics_JSON --> Monthly_Report

Incident_Report --> Dashboard
```

---

## Technologies Used

| Category         | Technologies        |
| ---------------- | ------------------- |
| Programming      | Python 3            |
| SSH              | Paramiko            |
| Concurrency      | ThreadPoolExecutor  |
| Configuration    | YAML, JSON          |
| Logging          | Python Logging      |
| Linux Tools      | Systemd, Journalctl |
| Networking       | Requests            |
| Dashboard        | HTML                |
| Operating System | Ubuntu Server       |

---

# Repository Layout

```text
infra-monitor-platform/
│
├── README.md
├── LICENSE
├── requirements.txt
│
├── src/
│   ├── main.py
│   ├── monitor.py
│   ├── recovery.py
│   ├── dashboard.py
│   ├── reports.py
│   ├── alerts.py
│   └── scheduler.py
│
├── config/
│   └── config.yaml
│
├── inventory/
│   └── servers.yaml
│
├── dashboard/
│   └── dashboard.html
│
├── reports/
│   ├── incident_report.html
│   ├── metrics.json
│   ├── history_server1.json
│   └── alerts.log
│
├── logs/
│   └── monitoring.log
│
├── screenshots/
│   ├── dashboard.png
│   ├── incident-report.png
│   ├── alerts.png
│   └── recovery.png
│
└── tests/
    ├── test_monitor.py
    ├── test_recovery.py
    └── test_alerts.py
```

---

# Installation

```bash
git clone https://github.com/yourusername/infra-monitor-platform.git

cd infra-monitor-platform

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

---

# Configuration

Configure monitored servers:

```text
inventory/servers.yaml
```

Application settings:

```text
config/config.yaml
```

---

# Running

```bash
python src/main.py
```

---

# Scheduler

```bash
python src/scheduler.py
```

---

# Dashboard

Generated dashboard:

```text
dashboard/dashboard.html
```

Dashboard includes:

* CPU usage
* Memory usage
* Disk usage
* Network statistics
* Service status
* Alerts
* Historical metrics

---

# Reports

Generated reports include:

* incident_report.html
* metrics.json
* history_server1.json
* alerts.log
* Daily reports
* Weekly reports
* Monthly reports

---

# Stress Testing

The platform has been tested with the following scenarios:

* Stop Nginx service
* High CPU utilization
* Memory stress
* Disk full simulation
* HTTP endpoint failure
* SSH connection failure
* Automatic recovery verification

---

# Sample Output

```text
[INFO] Connecting to server1...

[INFO] CPU Usage: 24%

[INFO] Memory Usage: 47%

[WARNING] nginx service is DOWN

[ACTION] Restarting nginx...

[SUCCESS] nginx restarted successfully.

[INFO] Dashboard updated.

[INFO] Incident report generated.
```

---

# Screenshots

Add screenshots inside the **screenshots/** directory.

* Dashboard
* Incident Report
* Project Structure
* Recovery Logs
* Alert Notifications

---

# Future Improvements

* Email alerts
* Telegram notifications
* Slack integration
* Prometheus exporter
* Grafana dashboards
* Docker deployment
* Kubernetes support
* REST API
* Database backend
* Authentication & Role-Based Access Control

---

# Skills Demonstrated

* Linux Administration
* Networking Fundamentals
* SSH Automation
* Python Programming
* Concurrent Programming (ThreadPoolExecutor)
* Infrastructure Monitoring
* System Health Monitoring
* Automated Service Recovery
* Incident Detection & Response
* Structured Logging
* HTML Dashboard Generation
* Configuration Management (YAML & JSON)
* Git Version Control
* Software Architecture
* Infrastructure Automation

---

# Lessons Learned

* SSH automation with Paramiko
* Concurrent programming in Python
* Linux system administration
* Infrastructure monitoring
* Automated incident response
* Structured logging
* Modular software architecture
* Infrastructure automation best practices

---

# License

This project is licensed under the **MIT License**. See the **LICENSE** file for details.

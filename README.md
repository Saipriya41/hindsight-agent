# hindsight-agent
# OpsMind AI (Hindsight Agent)

An advanced, AI-powered DevOps Incident Response dashboard designed to monitor server errors, recall past incidents from memory, and execute automated mitigation runbooks.

## Features
* *Real-time Error Monitoring:* Instantly catches critical server errors like DB connection timeouts and Redis OOM (Out of Memory).
* *Hindsight Memory Recall:* Automatically matches current anomalies with historical incidents to find the confidence score and root cause.
* *Automated Runbook Execution:* Streamlined UI with one-click mitigation strategies for rapid incident resolution.
* *Modern MNC-Level UI:* Sleek, terminal-like logs, glow effects, and pulse status indicators built with a custom HTML/CSS frontend integrated into Streamlit.

## Tech Stack
* *Frontend:* HTML5, CSS3 (Custom Dashboard Design)
* *Backend:* Python, Streamlit, AI Agent Logic
* *Infrastructure:* Docker, Docker Compose, Makefile
* **LLM / AI Engine**: Grok API
**Memory Framework**: Hindsight Memory
  **Environment Management**: `python-dotenv`
  **Version Control**: Git & GitHub

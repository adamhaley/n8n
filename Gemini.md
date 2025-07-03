## Project Architecture Analysis

### Main Modules & Responsibilities:
*   **`workflows/`**: Contains `n8n` workflow definitions (JSON files) for various automation tasks (e.g., AI chat, resume generation, web scraping).
*   **`config/`**: Holds Docker and Apache configurations (`docker-compose.yml`, `httpd.conf`) for self-hosting `n8n`.
*   **`speech/`**: A Python-based Flask server for speech-to-text (OpenAI Whisper) and text-to-speech (Cartesia), intended to support `n8n` workflows.
*   **Other Services**: The `README.md` mentions other custom services, likely invoked via HTTP by `n8n`.

### Data Flow & Dependencies:
*   `n8n` workflows orchestrate tasks, interacting with external APIs and internal custom services (like the speech server) via HTTP.
*   The speech server depends on OpenAI and Cartesia APIs.
*   Apache/Docker provides the hosting infrastructure.

### Design Patterns:
*   **Orchestration**: `n8n` acts as the central orchestrator.
*   **Microservices (implied)**: Custom services suggest a microservices approach.
*   **Configuration as Code**: Docker and Apache configurations are defined as code.

## Deployment Environments

*   **Local Development:** The application is run manually from the command line using `python3 support/app.py`.
*   **VPS (Production):** The application is managed as a daemon using the `support/n8n-support.service` systemd service file. The service file is configured for the production environment and should not be used for local development.
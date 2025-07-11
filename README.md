This repository is to store all things related to my n8n automation life:

1) n8n workflows

2) working apache / docker config for self-hosted n8n

3) speech-to-text and text-to-speech server in Flask that uses openai Whisper for transcribing and cartesia for  TTS

4) random services I think up to support n8n workflows, usually invoked by the http node

You may say I'm a dreamer. But I'm not the only one

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
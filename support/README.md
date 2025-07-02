# N8N Workflow Support Server

This directory contains a Flask-based support server designed to provide various services to n8n workflows. The server is structured into modular services using Flask Blueprints, making it easy to extend and maintain.

## Refactoring Approach

The primary goal of the refactoring was to create a more organized and maintainable application structure. The following key decisions were made:

1.  **Microservices-oriented Architecture with Flask Blueprints:** The application is divided into smaller, independent services, each encapsulated within a Flask Blueprint. This approach offers several advantages:
    *   **Modularity:** Each service (e.g., `speech`, `name_generator`, `google_search`) has its own dedicated file, making the codebase easier to understand and navigate.
    *   **Scalability:** Services can be developed and deployed independently, allowing for more granular scaling based on demand.
    *   **Maintainability:** Isolating services simplifies debugging and testing, as changes to one service are less likely to impact others.

2.  **Centralized Application Factory:** The main `app.py` file acts as an application factory. It initializes the Flask app, registers the blueprints, and sets up basic configurations. This pattern promotes a clean and organized application structure.

3.  **Dependency Management:** All Python dependencies are listed in the `requirements.txt` file. This ensures that the application environment is reproducible.

4.  **Configuration Management:** The application uses a `.env` file to manage environment variables, such as API keys. This is a security best practice that keeps sensitive information out of the codebase.

5.  **Systemd Integration:** The `n8n-support.service` file is provided to allow the application to be run as a systemd service. This ensures that the server runs reliably in the background and is automatically restarted on failure.

## Services

The following services are currently available:

*   **Speech Service (`services/speech_service.py`):**
    *   `/transcribe`: Transcribes audio files to text using OpenAI's Whisper-1 model.
    *   `/tts`: Converts text to speech using Cartesia's TTS service.

*   **Name Generator Service (`services/name_generator_service.py`):**
    *   `/generate-name`: Generates a random, human-readable name.

*   **Google Search Service (`services/google_search_service.py`):**
    *   `/google`: Performs a Google Custom Search.

## How to Run

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Create a `.env` file:**
    Create a `.env` file in the `support` directory and add the following environment variables:
    ```
    OPENAI_API_KEY=your_openai_api_key
    CARTESIA_API_KEY=your_cartesia_api_key
    CARTESIA_VOICE_ID=your_cartesia_voice_id
    GOOGLE_API_KEY=your_google_api_key
    CX=your_google_custom_search_engine_id
    ```

3.  **Run the Server:**
    ```bash
    python app.py
    ```
    The server will be available at `http://0.0.0.0:8000`.
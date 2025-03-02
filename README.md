# Papier Plane (Back-End)

Papier Plane is an AI-powered writing assistant built specifically for journalists. It streamlines your creative process and helps you craft compelling stories with ease.

## Features

- **AI-Driven Assistance:** Enhance your storytelling with intelligent content suggestions.
- **Tailored for Journalists:** Designed to meet the unique needs of professional journalism.
- **Real-Time Updates:** Uses Server-Sent Events (SSE) for live prompt responses.

## Getting Started

### Prerequisites

- **Python 3.8+** – Ensure you have Python installed.
- **Uvicorn** – An ASGI server for running the application.

### Installation

1. **Clone the Repository:**

```bash
git clone git@github.com:ahafidi/papier-plane-back.git
cd papier-plane-back
```

2. **Install Dependencies:**

Run the following command to install required dependencies:

```bash
pip install fastapi uvicorn mistralai python-dotenv
```

3. **Configure Your Environment:**

Copy the example environment file and update it with your configuration values:

```bash
cp .env.example .env
```

4. **Run the Server:**

Start the application using Uvicorn:

```bash
uvicorn src.main:app --reload
```

## Usage

Once the server is running, access the SSE endpoint to interact with the AI writing assistant. Send your prompt as a query parameter:

`http://localhost:8000/ai?prompt=<your_prompt_here>`

Replace `<your_prompt_here>` with the text you want the AI to process.

The server responds using Server-Sent Events (SSE), meaning the AI-generated content will be streamed to the client in real time as it is being generated.

## Contributing

Contributions are welcome! If you have suggestions, feature requests, or improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

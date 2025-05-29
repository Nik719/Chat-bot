# WAChatbotAI - WhatsApp AI Assistant

A versatile WhatsApp chatbot powered by multiple AI providers (Azure OpenAI and Phi) for intelligent conversations and assistance.

## Project Overview

WAChatbotAI is a Flask-based application that integrates WhatsApp's Cloud API with multiple AI providers (Azure OpenAI and Phi) to create an intelligent assistant. The bot can understand and respond to various queries through WhatsApp with support for different AI models and services.

## Features

- Multi-provider AI integration (Azure OpenAI, Phi)
- WhatsApp message webhook integration
- Secure webhook verification with signature validation
- Asynchronous message handling
- Modular service architecture
- Environment-based configuration
- Request/response logging
- Error handling and validation
- Support for different AI models and configurations

## Tech Stack

- Python 3.13+
- Flask (Web Framework)
- Azure OpenAI
- Phi AI models
- WhatsApp Cloud API
- Pydantic (Data validation)
- python-dotenv (Environment management)
- Requests (HTTP client)
- Logging (Built-in Python logging)

## Project Structure

```
WAChatbotAI/
├── app/
│   ├── decorators/
│   │   ├── __init__.py
│   │   └── security.py         # Security decorators for webhook
│   ├── services/
│   │   ├── __init__.py
│   │   ├── azura_service.py    # Azure OpenAI integration
│   │   ├── meta_service.py     # Meta/WhatsApp service
│   │   ├── openai_service.py   # OpenAI service
│   │   └── phi_service.py      # Phi AI integration
│   ├── utils/
│   │   ├── __init__.py
│   │   └── whatsapp_utils.py   # WhatsApp message handling
│   ├── __init__.py             # App initialization
│   ├── config.py               # App configuration
│   └── views.py                # Route handlers
├── start/
│   ├── assist_Azura.py         # Azure OpenAI test script
│   ├── assistants_quickstart.py # Quickstart example
│   └── whatsapp_quickstart.py   # WhatsApp example
├── tests/
│   └── test_*.py             # Test files
├── .env                        # Environment variables
├── config.py                   # Global configuration
├── requirements.txt            # Project dependencies
├── run.py                      # Application entry point
└── README.md                   # Project documentation
```

## Setup

### Prerequisites

- Python 3.13 or higher
- WhatsApp Business Account with API access
- Azure OpenAI service (for Azure integration)
- Phi model setup (for local Phi integration)

### Installation

1. Clone the repository
    ```bash
    git clone https://github.com/ProDharm/WAChatbotAI.git
    cd WAChatbotAI
    ```

2. Create and activate a virtual environment (recommended)
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

4. Configure environment variables
    Create a `.env` file with the following variables:
    ```env
    # WhatsApp Configuration
    WHATSAPP_ACCESS_TOKEN=your_whatsapp_access_token
    WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
    WHATSAPP_VERIFY_TOKEN=your_webhook_verify_token
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_ENDPOINT=your_azure_endpoint
    AZURE_OPENAI_API_KEY=your_azure_api_key
    AZURE_OPENAI_DEPLOYMENT=your_azure_deployment
    
    # Phi Configuration (if using local Phi models)
    PHI_MODEL_PATH=path/to/phi/model
    
    # App Configuration
    FLASK_APP=run.py
    FLASK_ENV=development
    DEBUG=True
    ```

5. Run the application
    ```bash
    python run.py
    ```

    Or in development mode with auto-reload:
    ```bash
    flask run --debug
    ```

## API Endpoints

- `GET /webhook`: WhatsApp webhook verification endpoint
- `POST /webhook`: WhatsApp message handling endpoint
- `GET /health`: Health check endpoint

## Security

- Webhook verification using Meta's signature validation
- Environment variable protection
- Request signature validation
- Input sanitization
- Rate limiting (via Flask-Limiter)
- CORS protection
- Secure headers

## Current Progress

### Implemented Features
- ✅ Multi-provider AI integration (Azure OpenAI, Phi)
- ✅ WhatsApp Cloud API integration
- ✅ Asynchronous message processing
- ✅ Modular service architecture
- ✅ Environment-based configuration
- ✅ Request/response logging
- ✅ Error handling and validation
- ✅ Health check endpoint

### In Progress
- 🚧 Conversation context management
- 🚧 Integration tests
- 🚧 Performance optimization

### Planned Features
- 📝 Enhanced conversation memory
- 📝 Support for more AI providers
- 📝 Advanced analytics dashboard
- 📝 User authentication and management
- 📝 Multi-language support

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
This project follows PEP 8 style guidelines. Please format your code using `black` and `isort`:

```bash
black .
isort .
```

### Pre-commit Hooks
Install pre-commit hooks to ensure code quality:

```bash
pip install pre-commit
pre-commit install
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code includes appropriate tests and documentation.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

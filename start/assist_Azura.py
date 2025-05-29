import os
import base64
from openai import AzureOpenAI

endpoint = os.getenv("ENDPOINT_URL", "https://dharm-mb6cjd2l-eastus2.cognitiveservices.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "chatbotAItest")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "EHUiBdOARkJnsBobHVVzMdRYjv79SbZIcj1gghEse4ENxxCzykApJQQJ99BEACHYHv6XJ3w3AAAAACOGknIB")

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "what is best diet for healthy bons",
        }
    ],
    max_completion_tokens=100000,
    model=deployment
)

print(response.choices[0].message.content)
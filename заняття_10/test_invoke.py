import boto3
import json

client = boto3.client('bedrock-runtime', region_name='us-east-1')

prompt = "Write a one-sentence bedtime story about a unicorn."

body = json.dumps({
    "messages": [
        {
            "role": "user",
            "content": [{"text": prompt}]
        }
    ],
    "inferenceConfig": {
        "maxTokens": 8192,
        "stopSequences": [],
        "temperature": 0,
        "topP": 0.9,
    }
})

response = client.invoke_model(body=body, modelId="amazon.nova-lite-v1:0")

print(response)
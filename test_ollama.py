from ollama import chat

response = chat(
    model="qwen2.5:0.5b",
    messages=[
        {"role": "user", "content": "Say hello"}
    ]
)

print(response)
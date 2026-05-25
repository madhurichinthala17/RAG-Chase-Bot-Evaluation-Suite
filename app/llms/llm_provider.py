from langchain_ollama import ChatOllama

# Instantiating the model with the specified parameters
chatmodel = ChatOllama(
    model="qwen2.5:latest",
    temperature=0.8,
)

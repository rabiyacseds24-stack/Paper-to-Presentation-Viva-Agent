from langchain_ollama import ChatOllama
llm = ChatOllama(
    model="llama3.2",
    temperature=0.3
)
response = llm.invoke(
    "Explain artificial intelligence in simple words."
)
print(response.content)
from langchain_ollama import ChatOllama

client = ChatOllama(
    model="llama3.1",
    temperature=0,
    # other params...
)

def Response_gen(prompt):
    if prompt:
        return client.invoke(prompt).content
    else:
        return "hello"
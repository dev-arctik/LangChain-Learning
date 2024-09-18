import langchain
# from langchain_openai import OpenAi
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0.9)

output = llm.invoke("What is google?")

print(output)
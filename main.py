import langchain
# from langchain_openai import OpenAi
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class technical coder."),
    ("user", "Explain the concepts to me like I am 5 year old"),
    ("system", "I will explain code like I am explaining to 5 year old"),
    ("user", "also explain in just 20 words"),
    ("user", "{input}")
])

llm = ChatOpenAI(temperature=0.9)

chain = prompt | llm

output = chain.invoke({"input":"what is internet?"})

print(output)
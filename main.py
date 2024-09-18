import langchain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class technical coder."),
    ("user", "Explain the concepts to me like I am 5 year old"),
    ("system", "I will explain code like I am explaining to 5 year old"),
    ("user", "also explain in just 20 words"),
    ("user", "{input}")
])

llm = ChatOpenAI(temperature=0.9)

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

output = chain.invoke({"input":"what is internet?"})

print(output)
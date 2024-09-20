# The below code is from https://python.langchain.com/docs/tutorials/retrievers/

# Vector stores and retrievers
# This tutorial will familiarize you with LangChain's vector store and retriever abstractions. These abstractions are designed to support retrieval of data-- from (vector) databases and other sources-- for integration with LLM workflows. They are important for applications that fetch data to be reasoned over as part of model inference, as in the case of retrieval-augmented generation, or RAG


# Lets create an llm first
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(temperature=0.9)

# We are craeting a smaple document
from langchain_core.documents import Document

documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are stupid.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Goldfish are popular pets for beginners, requiring relatively simple care.",
        metadata={"source": "fish-pets-doc"},
    ),
    Document(
        page_content="Parrots are intelligent birds capable of mimicking human speech.",
        metadata={"source": "bird-pets-doc"},
    ),
    Document(
        page_content="Rabbits are social animals that need plenty of space to hop around.",
        metadata={"source": "mammal-pets-doc"},
    ),
]

# Creating embedding of the document and the using chroma we will store the vector
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

vectorstore = Chroma.from_documents(documents, embeddings)


# Now to use this vectors we will use retrievers
from langchain_core.runnables import RunnableLambda

# k=5 means you will retrieve the top 5 most similar documents based on the query.
retriever = RunnableLambda(vectorstore.similarity_search).bind(k=1) # select top result

# retriever = vectorstore.as_retriever(
#     search_type="similarity",
#     search_kwargs={"k": 1},
# )

## Difference between RunnableLambda and as_retriever
# RunnableLamda: The RunnableLambda creates a runnable object, which is more flexible and can be embedded in complex pipelines or chains, allowing for functional programming-like execution.
# as_retriever: as_retriever() generates a standard retriever interface specifically designed for retrieval tasks, making it more structured but less flexible for chaining with other operations.


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

message = """
Answer this question using the provided context only.

{question}

Context:
{context}
"""

prompt = ChatPromptTemplate.from_messages([("human", message)])

rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm

# now to check the result
response = rag_chain.invoke("tell me about cats")

print(response.content)
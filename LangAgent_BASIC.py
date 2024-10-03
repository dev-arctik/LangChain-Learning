from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# For tools
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Union


# Define tools for calculator functions
class CalculatorInput(BaseModel):
    a: int = Field(description="First number")
    b: int = Field(description="Second number")


@tool('addition_tool', args_schema=CalculatorInput, return_direct=False)
def addition(a: int, b: int) -> int:
    ''' Adding two numbers '''
    return a + b

@tool('subtraction_tool', args_schema=CalculatorInput, return_direct=False)
def subtraction(a: int, b: int) -> int:
    ''' Subtracting second number from first '''
    return a - b

@tool('multiplication_tool', args_schema=CalculatorInput, return_direct=False)
def multiplication(a: int, b: int) -> int:
    ''' Multiplying two numbers '''
    return a * b

@tool('division_tool', args_schema=CalculatorInput, return_direct=False)
def division(a: int, b: int) -> Union[int, str]:
    ''' Dividing first number by second '''
    if b == 0:
        return "Cannot divide by zero"
    return a / b

@tool('percentage_tool', args_schema=CalculatorInput, return_direct=False)
def percentage(a: int, b: int) -> float:
    ''' Calculating the percentage of a from b. example a=5 percentage of b=20 is 1 '''
    if b == 0:
        return "Cannot calculate percentage with zero denominator"
    return (a / b) * 100


memory = MemorySaver()
model = ChatOpenAI()
tools = [addition, subtraction, multiplication, division, percentage]
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Conversational loop
user_session = input('Enter a session id \n')
print("\nStarting Conversation ... \n\n")

# Limit conversation to 5 rounds
for i in range(5):
    user_msg = input("User: ")
    # # To print in details
    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content=user_msg)]}, 
        config={"configurable": {"thread_id": user_session}}
    ):
        print(f"AI: {chunk}")

  

    ##### FAILED TESTS BELOW #####
    # chunks = agent_executor.invoke({"messages": [HumanMessage(content=user_msg)]}, config={"configurable": {"thread_id": user_session}})
    # print(chunks)
    # print("||||||||||||||||||||||||||||||||||||||||")
    # ai_message = chain.invoke({"input":chunks}, config={"configurable": {"thread_id": user_session}})
    # print(f"AI: {ai_message}")

    # for chunk in agent_executor.stream(
    #     {"messages": [HumanMessage(content=user_msg)]}, 
    #     config={"configurable": {"thread_id": user_session}}
    # ):
    #     print(chunk)
    #     print("||||||||||||||||||||||||||||||||||||||||")
    #     ai_message = chain.invoke({"input":chunk}, config={"configurable": {"thread_id": user_session}})
    #     print(f"AI: {ai_message}")

        
    print("----")

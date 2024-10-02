from langchain_core.tools import tool
from pydantic import BaseModel, Field

# define tool using decorator
@tool
def multiply(a: int, b: int) -> int:
    ''' Multiply two numbers '''
    return a*b

# Let's inspect some of the attributes associated with the tool.
print(multiply.name)
print(multiply.description)
print(multiply.args)


# async tool
@tool
async def subtraction(a: int, b: int) -> int:
    ''' Subtracting two numbers '''
    return a-b

print(subtraction.name)
print(subtraction.description)
print(subtraction.args)


# We can also define args using BaseModel
class CalculatorInput(BaseModel):
    a: int = Field(description="First number given by user")
    b: int = Field(description="Second number given by user")

@tool('Addition tool', args_schema=CalculatorInput, return_direct=True)
def addition(a: int, b: int) -> int:
    ''' Adding two number '''
    return a+b

print(addition.name)
print(addition.description)
print(addition.args)
print(addition.return_direct)
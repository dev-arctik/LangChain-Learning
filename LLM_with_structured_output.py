from langchain_openai import ChatOpenAI
from typing import Optional, Union
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

import json

llm = ChatOpenAI()


## Reponse based on structure
# Response: setup='Why was the cat sitting on the computer?' punchline='To keep an eye on the mouse.' rating=8
class Joke(BaseModel):
    """Joke to tell user."""

    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: Optional[int] = Field(
        default=None, description="How funny the joke is, from 1 to 10"
    )
structured_llm = llm.with_structured_output(Joke)
response1 = structured_llm.invoke("Tell me a joke about cats")


## Simple way to get JSON output
# Response: {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'He wanted to keep an eye on the mouse!'}
structured_llm = llm.with_structured_output(None, method="json_mode")
response2 = structured_llm.invoke(
    "Tell me a joke about cats, respond in JSON with `setup` and `punchline` keys"
)

## To get desired JSON format
# Response: {'setup': 'Why was the cat sitting on the computer?', 'punchline': 'To keep an eye on the mouse!', 'fact': 'Cats have a natural instinct to hunt mice and other small rodents.', 'rating': 7}
json_schema = {
    "title": "joke",
    "description": "Joke to tell user.",
    "type": "object",
    "properties": {
        "setup": {
            "type": "string",
            "description": "The setup of the joke",
        },
        "punchline": {
            "type": "string",
            "description": "The punchline to the joke",
        },
        "rating": {
            "type": "integer",
            "description": "How funny the joke is, from 1 to 10",
            "default": None,
        },
        "fact": {
            "type": "string",
            "description": "facts about the joke"
        }
    },
    "required": ["setup", "punchline", "fact"],
}
structured_llm = llm.with_structured_output(json_schema)

response3 = structured_llm.invoke("Tell me a joke about cats")


## From a defined template 
# Response: {'setup': 'Wooden shoe', 'punchline': 'Wooden shoe like to hear another woodpecker joke?', 'rating': 8}
system = """You are a hilarious comedian. Your specialty is knock-knock jokes. \
Return a joke which has the setup (the response to "Who's there?") and the final punchline (the response to "<setup> who?").

Here are some examples of jokes and its json output:

example_user: Tell me a joke about planes
example_assistant: {{"query": "Tell me a joke about planes", "setup": "Why don't planes ever get tired?", "punchline": "Because they have rest wings!", "rating": 2}}

example_user: Tell me another joke about planes
example_assistant: {{"query": "Tell me another joke about planes", "setup": "Cargo", "punchline": "Cargo 'vroom vroom', but planes go 'zoom zoom'!", "rating": 10}}

example_user: Now about caterpillars
example_assistant: {{"query": "Now about caterpillars", "setup": "Caterpillar", "punchline": "Caterpillar really slow, but watch me turn into a butterfly and steal the show!", "rating": 5}}"""

prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "{input}")])

structured_llm = llm.with_structured_output(None, method="json_mode")

few_shot_structured_llm = prompt | structured_llm
response4 = few_shot_structured_llm.invoke("Tell me a joke about cats")


def pretty_print(title, response):
    print(f"\n{'=' * 50}")
    print(f"{title}")
    print(f"{'=' * 50}")
    if isinstance(response, str):
        # Try to load as JSON if it's a JSON string, otherwise print as is
        try:
            response = json.loads(response)
        except json.JSONDecodeError:
            pass
    # Pretty print dictionary or JSON response
    if isinstance(response, dict):
        print(json.dumps(response, indent=4))
    else:
        print(response)
    print(f"{'=' * 50}\n")


# Print all responses
pretty_print("Response 1 - Structured Joke (Joke Model)", response1)
pretty_print("Response 2 - Simple JSON Mode", response2)
pretty_print("Response 3 - Custom JSON Schema", response3)
pretty_print("Response 4 - Few Shot Knock-Knock Template", response4)
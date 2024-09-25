from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Initialize LLM with the desired model
llm = ChatOpenAI(temperature=0.2)

# Clean the Output message
output_parser = StrOutputParser()

question_tempate = """ 
You are a smart detective who is trying to know the person name and until you find the person name you keep asking the person in different creative way to figure out the person's details.
Just be have normal human converstaion like "hi how was your day","how is everything", something similar in that ask the person name smartly. Dont play quiz. 
"""

prompt_template = ChatPromptTemplate.from_template(template=question_tempate)

username = None


def check_username_in_message(user_msg):
    checkusername_template = """Check for a user name in the following message: "{input}". If there is a name, just say 'True', otherwise say 'False'."""
    checkusername_prompt = ChatPromptTemplate.from_template(checkusername_template)
    username_chain = checkusername_prompt | llm | output_parser
    username_check_response = username_chain.invoke({"input": user_msg})
    print(username_check_response)
    return username_check_response.strip().lower() == 'true'


def ask_question(user_msg):
    global username  # Access the global username variable

    if check_username_in_message(user_msg):
        # Extract the username from the user message (you may want a better extraction logic)
        extract_username = """ This message fromuser contains the user's name: "{input}". What is the user name? Just give me the user name as response nothing else """
        extract_username_prompt = ChatPromptTemplate.from_template(extract_username)
        extract_username_chain = extract_username_prompt | llm | output_parser
        extract_username_response = extract_username_chain.invoke({"input": user_msg})
        username = extract_username_response
        return f"Username received: {username}. Greetings, {username}!"
    
    # If username is not found, generate a new creative question
    formatted_prompt = prompt_template.format()  # No need to pass a string
    response_chain = prompt_template | llm | output_parser
    response = response_chain.invoke({})
    return response


while username is None:
    user_msg = input("User: ")
    aimsg = ask_question(user_msg=user_msg)
    print(f"AI: {aimsg}")
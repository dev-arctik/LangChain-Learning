import os
import langchain
from langchain_openai import ChatOpenAi
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")
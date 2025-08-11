import getpass
import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI

load_dotenv()

def get_model() :
    if os.getenv("DEEPSEEK_API_KEY"):
        return  ChatDeepSeek(model="deepseek-chat", temperature=0.5)
    if os.getenv("OPENAI_API_KEY") :
        return ChatOpenAI(temperature=0.5)

reasoner_model = ChatDeepSeek(model="deepseek-reasoner", temperature=0.1)


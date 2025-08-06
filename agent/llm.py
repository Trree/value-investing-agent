import getpass
import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek

load_dotenv()
if not os.getenv("DEEPSEEK_API_KEY"):
    os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter your DeepSeek API key: ")

model =  ChatDeepSeek(model="deepseek-chat", temperature=0)




import getpass
import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek

load_dotenv()

def get_model() :
    if os.getenv("DEEPSEEK_API_KEY"):
        model =  ChatDeepSeek(model="deepseek-chat", temperature=0.5)
    if os.getenv("OPENAI_MODEL") && os.getenv("OPENAI_APK_KEY"):
        model = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL"),
            temperature=0.5,
            base_url="https://api.openai.com/v1/",
            if os.getenv("OPENAI_BASE_URL"):
                base_url = os.getenv("OPENAI_BASE_URL")
            api_key=os.getenv("OPENAI_APK_KEY")
        )

reasoner_model = ChatDeepSeek(model="deepseek-reasoner", temperature=0.1)


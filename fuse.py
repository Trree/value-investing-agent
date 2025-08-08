from dotenv import load_dotenv
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

load_dotenv()
langfuse = Langfuse()
langfuse_handler = CallbackHandler()

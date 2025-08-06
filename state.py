from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Optional

class State(TypedDict):
    input_data: str
    code: str
    code_info: Optonal[str]

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

from agent.qeury_code import query_code_agent
from tool.pe_tool import get_stock_pe


class State(TypedDict):
    input_key: str
    code: str
    code_info: str

def query_code(state: State):
    input_key = state.get("input_key")
    code = query_code_agent(input_key)
    return {"code": code}

def query_code_info(state: State):
    code = state.get("code")
    code_info = get_stock_pe(code)
    return {"code_info": code_info}


# 构建图表
builder = StateGraph(State)
builder.add_node("query_code", query_code)
builder.add_node("query_code_info", query_code_info)

# 连接逻辑
builder.add_edge(START, "query_code")
builder.add_edge("query_code", "query_code_info")
builder.add_edge("query_code_info", END)

# 编译
graph = builder.compile()
result = graph.invoke({"input_key" : "中远海控"})
print(result)

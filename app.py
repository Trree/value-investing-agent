from typing_extensions import TypedDict
import random
from typing import Literal
from langgraph.graph import StateGraph, START, END

# 构建图表
builder = StateGraph(State)
builder.add_node("query_code_info", query_code_info)

# 连接逻辑
builder.add_edge(START, "query_code_info")
builder.add_edge("query_code_info", END)

# 编译
graph = builder.compile()
graph.invoke({"input_key" : "中远海控"})

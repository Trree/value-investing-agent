from typing_extensions import TypedDict
import random
from typing import Literal
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    graph_state: str

def node_1(state):
    print("---Node 1---")
    return {"graph_state": state['graph_state'] +" I am"}

def node_2(state):
    print("---Node 2---")
    return {"graph_state": state['graph_state'] +" happy!"}

def node_3(state):
    print("---Node 3---")
    return {"graph_state": state['graph_state'] +" sad!"}


def decide_mood(state) -> Literal["node_2", "node_3"]:
    # 通常我们会根据状态决定下一个节点
    user_input = state['graph_state']

    # 这里我们在节点2和节点3之间简单实现 50/50 的概率分配
    if random.random() < 0.5:
        # 50% 时间， 我们返回节点2
        return "node_2"

    # 50% 时间， 我们返回节点3
    return "node_3"



# 构建图表
builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# 连接逻辑
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# 编译
graph = builder.compile()
graph.invoke({"graph_state" : "Hi, this is Lance."})
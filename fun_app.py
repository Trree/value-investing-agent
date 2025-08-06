from langgraph.func import entrypoint

from agent.qeury_code import query_code_agent
from tool.pe_tool import get_stock_pe


@entrypoint()
def orchestrator_worker(topic: str):
    sections = query_code_agent(topic).result()
    result = get_stock_pe(sections)
    return result

report = orchestrator_worker.invoke("中远海控")
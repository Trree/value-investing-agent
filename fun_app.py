from langgraph.func import entrypoint
from agent.ben_graham import ben_graham_analyst
from agent.query_code import query_code_agent
from agent.risk_management import risk_management_analyze
from tool.pe_tool import get_stock_pe


@entrypoint()
def orchestrator_worker(topic: str):
    sections = query_code_agent(topic).result()
    code_info = get_stock_pe(sections).result()
    ben_analyze = risk_management_analyze(code_info)
    buffett_analyze = ben_graham_analyst(code_info)
    risk_analyze = risk_management_analyze(topic)
    print(code_info)
    print(ben_analyze)
    print(buffett_analyze)
    print(risk_analyze)
    return ben_analyze

from dotenv import load_dotenv
from langgraph.func import entrypoint

from agent.ben_graham import ben_graham_analyst
from agent.investment_advisor import investment_advisor_analyze
from agent.query_code import query_code_agent
from agent.risk_management import risk_management_analyze
from agent.warren_buffett import warren_buffett_analyze
from tool.pe_tool import get_stock_pe

load_dotenv()

@entrypoint()
def orchestrator_worker(topic: str):
    sections = query_code_agent(topic).result()
    code_info = get_stock_pe(sections).result()
    ben_analyze = ben_graham_analyst(topic, code_info)
    buffett_analyze = warren_buffett_analyze(topic, code_info)
    risk_analyze = risk_management_analyze(topic)

    analyze_result = investment_advisor_analyze(topic, code_info, ben_analyze, buffett_analyze, risk_analyze).result();
    return analyze_result

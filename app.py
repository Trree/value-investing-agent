from dotenv import load_dotenv
from langgraph.func import entrypoint
import json

from agent.ben_graham import ben_graham_analyst
from agent.investment_advisor import investment_advisor_analyze
from agent.query_code import query_code_agent
from agent.risk_management import risk_management_analyze
from agent.warren_buffett import warren_buffett_analyze
from tool.akshare_tool import get_skshare_info

load_dotenv()

@entrypoint()
def orchestrator_worker(topic: str):
    sections = query_code_agent(topic).result()
    code_info = get_skshare_info(sections).result()
    all_code_info = json.dumps(code_info, ensure_ascii=False)
    print(all_code_info)
    ben_analyze = ben_graham_analyst(topic, all_code_info)
    buffett_analyze = warren_buffett_analyze(topic, all_code_info)
    risk_analyze = risk_management_analyze(topic, all_code_info)

    analyze_result = investment_advisor_analyze(topic, ben_analyze.result(), 
            buffett_analyze.result(), risk_analyze.result()).result()
    return analyze_result


if __name__ == '__main__':
    print(orchestrator_worker.invoke("中远海控"))

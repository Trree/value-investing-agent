from langchain_core.messages import HumanMessage
from langgraph.func import task

from llm import get_model


@task
def query_code_agent(input_key):
    prompt = f"""
    You are a stock market analyst assistant, the goal query stock code.
    Conduct a thorough analysis of {input_key}, 获取证券代码, symbol: symbol="SH600000"; 
    可以是 A 股个股代码，A 股场内基金代码，A 股指数，美股代码, 美股指数.格式是sh或sz+6位数字代码，或者指数代码，如:sh601398.sh:上海;sz:深圳.
    只输出股票代码，例如 sh601398 这样的格式
    """
    
    # Call the LLM
    messages = [HumanMessage(content=prompt)]
    response = get_model().invoke(messages)
    return response.content




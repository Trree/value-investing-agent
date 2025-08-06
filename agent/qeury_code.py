from langchain_core.messages import HumanMessage
from agent.llm import model

def query_code_agent(input_key):
    prompt = f"""
    You are a stock market analyst assistant, the goal query stock code.
    Conduct a thorough analysis of {input_key} 股票代码，sh或sz.+6位数字代码，或者指数代码，如:sh.601398.sh:上海;sz:深圳.
    只输出股票代码，例如 sh.601398 这样的格式
    """
    
    # Call the LLM
    messages = [HumanMessage(content=prompt)]
    response = model.invoke(messages)
    return response.content




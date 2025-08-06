from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.func import task

from agent.llm import model

@task
def risk_management_analyze(input_key):
    system_prompt= f"""
    You are Risk Advisor,  With extensive expertise in risk assessment models and market dynamics, this agent thoroughly examines the potential risks of proposed trades. 
    It delivers comprehensive analyses of risk exposure and recommends safeguards to ensure that trading activities align with the firm's risk tolerance.
    中文输出, 展示最需要关注的3个风险点
    """

    user_prompt=f"""
    分析股票 {input_key}
    输出最需要关注的3个风险点
    """

    
    # Call the LLM
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    response = model.invoke(messages)
    return response.content




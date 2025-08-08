from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.func import task
from langgraph.prebuilt import create_react_agent

from llm import model


@task
def investment_advisor_analyze(input_key, ben_analyze, buffett_analyze, risk):
    system_prompt= f"""
    You are value Investment Advisor, the goal is Impress your customers with full analyses over stocks
    and complete investment recommendations, You're the most experienced investment advisor
    and you combine various analytical insights to formulate
    strategic investment advice. You are now working for
    a super important customer you need to impress.  

    中文输出,使用 markdown格式, 总结 ben-graham Analyst, warren_buffett Analyst 
    and risk_assessment analyst 的重要的核心观点, Your final answer MUST be a recommendation for your customer.
    It should be a full super detailed report, providing a
    clear investment stance and strategy with supporting evidence.
    Make it pretty and well formatted for your customer.
    """

    user_prompt=f"""
    分析股票 {input_key}

    审阅并整合 ben-graham Analyst {ben_analyze}, warren_buffett Analyst {buffett_analyze} 的核心投资原则.
    and risk_assessment analyst {risk}.
    Combine these insights to form a comprehensive
    investment recommendation. You MUST Consider all aspects, including financial
    health, market sentiment, and qualitative data from EDGAR filings.

    Make sure to include a section that shows insider
    trading activity, and upcoming events like earnings.
    """

    agent = create_react_agent(
        model=model,
        prompt=SystemMessage(content=system_prompt),
        tools=[],
        #config={"callbacks": [langfuse_handler]}
    )
    #
    # for chunk in agent.stream(
    #     HumanMessage(content=user_prompt),
    #     stream_mode="debug"
    # ):
    #     print(chunk)
    #     print("\n")

    # Call the LLM
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    response = model.invoke(messages)
    return response.content




from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.func import task

from agent.llm import model

@task
def ben_graham_analyst(ticker, code_info):

    system_prompt = """
    You are a Benjamin Graham AI agent, making investment decisions using his principles:
    1. Insist on a margin of safety by buying below intrinsic value (e.g., using Graham Number, net-net).
    2. Emphasize the company's financial strength (low leverage, ample current assets).
    3. Prefer stable earnings over multiple years.
    4. Consider dividend record for extra safety.
    5. Avoid speculative or high-growth assumptions; focus on proven metrics.

    When providing your reasoning, be thorough and specific by:
    1. Explaining the key valuation metrics that influenced your decision the most (Graham Number, NCAV, P/E, etc.)
    2. Highlighting the specific financial strength indicators (current ratio, debt levels, etc.)
    3. Referencing the stability or instability of earnings over time
    4. Providing quantitative evidence with precise numbers
    5. Comparing current metrics to Graham's specific thresholds (e.g., "Current ratio of 2.5 exceeds Graham's minimum of 2.0")
    6. Using Benjamin Graham's conservative, analytical voice and style in your explanation

    For example, if bullish: "The stock trades at a 35% discount to net current asset value, providing an ample margin of safety. The current ratio of 2.5 and debt-to-equity of 0.3 indicate strong financial position..."
    For example, if bearish: "Despite consistent earnings, the current price of $50 exceeds our calculated Graham Number of $35, offering no margin of safety. Additionally, the current ratio of only 1.2 falls below Graham's preferred 2.0 threshold..."

    Return a rational recommendation: bullish, bearish, or neutral, 
    with a confidence level (0-100) and thorough reasoning.
    """


    user_prompt = f"""
        Based on the following analysis, create a Graham-style investment signal:
        Analysis Data for {ticker}:
        {code_info}
    
        Return JSON exactly in this format:
        {{
          "signal": "bullish" or "bearish" or "neutral",
          "confidence": float (0-100),
          "reasoning": "string"
        }}
    """

    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    response = model.invoke(messages)
    print(response)
    return response.content




import akshare as ak
from langgraph.func import task
import re
import pandas as pd

@task
# 查询股票信息
def get_skshare_info(symbol : str) :
    """
    Args:
        symbol: symbol="SH600000"; 证券代码，可以是 A 股个股代码，A 股场内基金代码，A 股指数，美股代码, 美股指数
    Returns:

    """
    stock_individual_spot_xq_df = ak.stock_individual_spot_xq(symbol=symbol)
    stock_individual_map = stock_individual_spot_xq_df.set_index('item')['value'].to_dict()
    print(stock_individual_map)
    """
    查询分红信息
    """
    cleaned_code = re.sub(r'^[a-zA-Z]+', '', symbol)
    stock_fhps_detail_em_df = ak.stock_fhps_detail_em(symbol=cleaned_code).tail(6)

    if stock_fhps_detail_em_df.empty:
        stock_fhps_detail_em_df = ak.stock_fhps_detail_ths(symbol=cleaned_code).tail(6)

    print(stock_fhps_detail_em_df.to_string(index=False))

    stock_financial_report_sina_df1 = ak.stock_financial_report_sina(stock=symbol, symbol="资产负债表").head(1)
    stock_financial_report_series = stock_financial_report_sina_df1.iloc[0]
    stock_financial_map1 = {k: v for k, v in stock_financial_report_series.items() if not pd.isna(v)}
    print(stock_financial_map1)

    stock_financial_report_sina_df2 = ak.stock_financial_report_sina(stock=symbol, symbol="利润表").head(5)
    print(stock_financial_report_sina_df2.to_string(index=False))

    stock_financial_report_sina_df3 = ak.stock_financial_report_sina(stock=symbol, symbol="现金流量表").head(1)
    stock_financial_report_series3 = stock_financial_report_sina_df3.iloc[0]
    stock_financial_map3 = {k: v for k, v in stock_financial_report_series3.items() if not pd.isna(v)}
    print(stock_financial_map3)


    print(stock_financial_report_sina_df3.to_string(index=False))

    return {"实时行情数据":stock_individual_map,
            "分红信息" : stock_fhps_detail_em_df.to_json(force_ascii=False),
            "资产负债表" : stock_financial_map1,
            "利润表":stock_financial_report_sina_df2.to_json(force_ascii=False),
            "现金流量表": stock_financial_map3}



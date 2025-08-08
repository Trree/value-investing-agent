import akshare as ak
from langgraph.func import task


@task
# 查询股票信息
def get_skshare_info(symbol : str) :
    """
    Args:
        symbol: symbol="SH600000"; 证券代码，可以是 A 股个股代码，A 股场内基金代码，A 股指数，美股代码, 美股指数
    Returns:

    """
    stock_individual_spot_xq_df = ak.stock_individual_spot_xq(symbol="SH601919")


    """
    查询分红信息
    """
    stock_fhps_detail_em_df = ak.stock_fhps_detail_em(symbol="601919")
    print(stock_fhps_detail_em_df.to_string(index=False))

    if stock_fhps_detail_em_df.empty:
        stock_fhps_detail_em_df = ak.stock_fhps_detail_ths(symbol="601919")

    print(stock_fhps_detail_em_df.to_string(index=False))

    stock_financial_report_sina_df1 = ak.stock_financial_report_sina(stock="sh601919", symbol="资产负债表").head(10)
    print(stock_financial_report_sina_df1.to_string(index=False))

    stock_financial_report_sina_df2 = ak.stock_financial_report_sina(stock="sh601919", symbol="利润表").head(10)
    print(stock_financial_report_sina_df2.to_string(index=False))

    stock_financial_report_sina_df3 = ak.stock_financial_report_sina(stock="sh601919", symbol="现金流量表").head(10)
    print(stock_financial_report_sina_df3.to_string(index=False))

    return {"当日行情":stock_individual_spot_xq_df.to_json(force_ascii=False),
            "分红信息" : stock_fhps_detail_em_df.to_json(force_ascii=False),
            "资产负债表" :stock_financial_report_sina_df1.to_json(force_ascii=False),
            "利润表":stock_financial_report_sina_df2.to_json(force_ascii=False),
            "现金流量表":stock_financial_report_sina_df3.to_json(force_ascii=False)}



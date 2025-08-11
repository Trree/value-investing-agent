import re
from functools import lru_cache

import akshare as ak
import pandas as pd
from langgraph.func import task


@lru_cache(maxsize=128)
@task
# 查询股票信息
def get_akshare_info(symbol : str) :
    """
    Args:
        symbol: symbol="SH600000"; 证券代码，可以是 A 股个股代码，A 股场内基金代码，A 股指数，美股代码, 美股指数
    Returns:
    """
    df_30_minute = ak.stock_zh_a_minute(symbol=symbol, period="30", adjust="")
    latest_price = df_30_minute.iloc[-1].to_dict()
    print(latest_price)

    stock_individual_spot_xq_df = ak.stock_individual_spot_xq(symbol=symbol, timeout=3)
    stock_individual_map = stock_individual_spot_xq_df.set_index('item')['value'].to_dict()
    print(stock_individual_map)
    """
    查询分红信息
    """
    cleaned_code = re.sub(r'^[a-zA-Z]+', '', symbol)
    stock_fhps_detail_em_df = ak.stock_fhps_detail_em(symbol=cleaned_code).tail(6)
    if stock_fhps_detail_em_df.empty:
        stock_fhps_detail_em_df = ak.stock_fhps_detail_ths(symbol=cleaned_code).tail(6)

    selected_columns = [
        '报告期',
        '现金分红-现金分红比例',
        '现金分红-现金分红比例描述',
        '现金分红-股息率'
    ]

    fhps_detail_df = stock_fhps_detail_em_df[selected_columns]
    print(fhps_detail_df.to_string(index=False))

    stock_financial_report_sina_df1 = ak.stock_financial_report_sina(stock=symbol, symbol="资产负债表").head(1)
    stock_financial_report_series = stock_financial_report_sina_df1.iloc[0]
    stock_financial_map1 = {k: v for k, v in stock_financial_report_series.items() if not pd.isna(v)}
    print(stock_financial_map1)

    stock_financial_report_sina_df2 = ak.stock_financial_report_sina(stock=symbol, symbol="利润表").head(5)
    financial_selected_columns = [
        '报告日',
        '营业总收入',
        '营业总成本',
        '营业利润',
        '利润总额',
        '净利润',
        '归属于母公司所有者的净利润',
        '基本每股收益',
        '稀释每股收益',
        '综合收益总额'
    ]
    stock_financial2 = stock_financial_report_sina_df2[financial_selected_columns]
    print(stock_financial2.to_string(index=False))
        

    stock_financial_report_sina_df3 = ak.stock_financial_report_sina(stock=symbol, symbol="现金流量表").head(1)
    important_columns = [
        '报告日',
        '销售商品、提供劳务收到的现金',  # 核心收入来源
        '经营活动产生的现金流量净额',    # 主营业务的造血能力
        '购买商品、接受劳务支付的现金',  # 主要成本支出
        '投资活动产生的现金流量净额',    # 投资活动状况
        '筹资活动产生的现金流量净额',    # 融资能力
        '购建固定资产、无形资产和其他长期资产所支付的现金', # 资本性支出
        '期末现金及现金等价物余额',      # 资金储备
        '支付的各项税费',              # 税务负担
        '支付给职工以及为职工支付的现金'  # 人力成本
    ]
    stock_financial3 = stock_financial_report_sina_df3[important_columns]
    stock_financial_report_series3 = stock_financial3.iloc[0]
    stock_financial_map3 = {k: v for k, v in stock_financial_report_series3.items() if not pd.isna(v)}
    print(stock_financial_map3)


    print(stock_financial_report_sina_df3.to_string(index=False))

    return {
        "最新价格": latest_price,
        "实时行情数据":stock_individual_map,
        "分红信息" : fhps_detail_df.to_markdown(index=False),
        "资产负债表" : stock_financial_map1,
        "利润表":stock_financial2.to_markdown(index=False),
        "现金流量表": stock_financial_map3}



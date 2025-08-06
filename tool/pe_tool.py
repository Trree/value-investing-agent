import json
from datetime import datetime, timedelta

import baostock as bs


def get_recent_quarter(which_quarter):
    today = datetime.now()
    current_year = today.year
    current_month = today.month
    current_quarter = (current_month - 1) // 3 + 1
    if which_quarter == 1:
        if current_quarter == 1:
            return current_year - 1, 4
        else:
            return current_year, current_quarter - 1
    elif which_quarter == 2:
        if current_quarter == 1:
            return current_year - 1, 3
        if current_quarter == 2:
            return current_year - 1, 4
        else:
            return current_year, current_quarter - 2
    else:
        raise ValueError("exception para")

def get_current_and_last_year():
    current_year = datetime.now().year
    last_year = current_year - 1
    return current_year, last_year

# 查询股票信息
def get_stock_pe(code : str) -> str:
    """
    查询股票相关信息.
    Args:
        code: 股票代码
    """

    lg = bs.login()
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    yesterday_date = yesterday.strftime("%Y-%m-%d")
    today_date = today.strftime("%Y-%m-%d")
    #### 获取沪深A股估值指标(日频)数据 ####
    # peTTM    滚动市盈率
    # psTTM    滚动市销率
    # pcfNcfTTM    滚动市现率
    # pbMRQ    市净率

    """
    | 参数名称      | 参数描述            | 说明                                                                 |
    |---------------|------------------|----------------------------------------------------------------------|
    | date          | 交易所行情日期      | 格式：YYYY-MM-DD                                                    |
    | code          | 证券代码           | 格式：sh.600000（sh：上海，sz：深圳）                               |
    | open          | 今开盘价格         | 精度：小数点后4位；单位：人民币元                                   |
    | high          | 最高价            | 精度：小数点后4位；单位：人民币元                                   |
    | low           | 最低价            | 精度：小数点后4位；单位：人民币元                                   |
    | close         | 今收盘价          | 精度：小数点后4位；单位：人民币元                                   |
    | preclose      | 昨日收盘价        | 精度：小数点后4位；单位：人民币元                                   |
    | volume        | 成交数量          | 单位：股                                                            |
    | amount        | 成交金额          | 精度：小数点后4位；单位：人民币元                                   |
    | adjustflag    | 复权状态          | 不复权、前复权、后复权                                              |
    | turn          | 换手率            | 精度：小数点后6位；单位：%                                          |
    | tradestatus   | 交易状态          | 1：正常交易 0：停牌                                                 |
    | pctChg        | 涨跌幅（百分比）   | 精度：小数点后6位                                                   |
    | peTTM         | 滚动市盈率        | 精度：小数点后6位                                                   |
    | psTTM         | 滚动市销率        | 精度：小数点后6位                                                   |
    | pcfNcfTTM     | 滚动市现率        | 精度：小数点后6位                                                   |
    | pbMRQ         | 市净率           | 精度：小数点后6位                                                   |
    | isST          | 是否ST          | 1是，0否                                                            |
    """
    filed = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST"
    rs = bs.query_history_k_data_plus(code, filed,
                                      start_date=yesterday_date, end_date=today_date,
                                      frequency="d", adjustflag="3")

    filed_list = filed.split(",")
    rs_result = dict(zip(filed_list, rs.data[-1]))

    balance_list = []
    year, quarter = get_recent_quarter(1)
    """
    +---------------------+--------------------------------------------------------+----------------------------------------------------------------+
    | 参数名称            | 参数描述                                                | 算法说明                                                      |
    +---------------------+--------------------------------------------------------+----------------------------------------------------------------+
    | code                | 证券代码                                               |                                                                |
    | pubDate             | 公司发布财报的日期                                     |                                                                |
    | statDate            | 财报统计的季度的最后一天                               | 比如2017-03-31, 2017-06-30                                   |
    | currentRatio        | 流动比率                                               | 流动资产/流动负债                                            |
    | quickRatio          | 速动比率                                               | (流动资产-存货净额)/流动负债                                 |
    | cashRatio           | 现金比率                                               | (货币资金+交易性金融资产)/流动负债                           |
    | YOYLiability        | 总负债同比增长率                                       | (本期总负债-上年同期总负债)/上年同期中负债的绝对值*100%      |
    | liabilityToAsset    | 资产负债率                                             | 负债总额/资产总额                                            |
    | assetToEquity       | 权益乘数                                               | 资产总额/股东权益总额=1/(1-资产负债率)                       |
    +---------------------+--------------------------------------------------------+----------------------------------------------------------------+
    """
    rs_balance = bs.query_balance_data(code, year=year, quarter=quarter)
    while (rs_balance.error_code == '0') & rs_balance.next():
        balance_list.append(rs_balance.get_row_data())
    if len(balance_list) == 0:
        year, quarter = get_recent_quarter(2)
        rs_balance = bs.query_balance_data(code, year=year, quarter=quarter)
        while (rs_balance.error_code == '0') & rs_balance.next():
            balance_list.append(rs_balance.get_row_data())

    balance_result = {}
    dividend_result = {}
    if balance_list:
        balance_result = dict(zip(rs_balance.fields, balance_list[0]))

    dividend_list = []
    current_year, last_year = get_current_and_last_year()
    rs_dividend = bs.query_dividend_data(code, year=current_year, yearType="report")
    while (rs_dividend.error_code == '0') & rs_dividend.next():
        dividend_list.append(rs_dividend.get_row_data())
    if len(dividend_list) == 0:
        rs_dividend = bs.query_dividend_data(code, year=last_year, yearType="report")
        while (rs_dividend.error_code == '0') & rs_dividend.next():
            dividend_list.append(rs_dividend.get_row_data())
    if dividend_list:
        dividend_result = dict(zip(rs_dividend.fields, dividend_list[0]))
    merged_map = {**rs_result, **balance_result, **dividend_result}
    print(merged_map)
    #### 登出系统 ####
    bs.logout()
    return json.dumps(merged_map, ensure_ascii=False)
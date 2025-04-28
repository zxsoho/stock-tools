import akshare as ak
import pandas as pd
from datetime import datetime
import argparse

def get_limit_up_stocks(date=None):
    """
    获取涨停股票数据
    :param date: 日期字符串，格式：YYYYMMDD，默认为当天
    """
    try:
        print("正在获取涨停股票数据...")
        # 如果没有指定日期，使用当天日期
        if not date:
            date = datetime.now().strftime("%Y%m%d")
            
        # 获取涨停股票数据
        limit_up_df = ak.stock_zt_pool_em(date=date)
        print(f"获取到涨停股票数据，共 {len(limit_up_df)} 条记录")
        
        if limit_up_df.empty:
            print("未获取到涨停股票数据")
            return pd.DataFrame()
            
        # 选择需要的列
        selected_columns = [
            '序号', '代码', '名称', '涨跌幅', '最新价', '成交额', '流通市值',
            '封板资金', '首次封板时间', '最后封板时间', '炸板次数', '连板数', '所属行业'
        ]
        
        result = limit_up_df[selected_columns].copy()
        
        # 重命名列
        result = result.rename(columns={
            '序号': 'index',
            '代码': 'stock_code',
            '名称': 'name',
            '涨跌幅': 'pct_chg',
            '最新价': 'price',
            '成交额': 'amount',
            '流通市值': 'market_cap',
            '封板资金': 'limit_up_amount',
            '首次封板时间': 'first_limit_up_time',
            '最后封板时间': 'last_limit_up_time',
            '炸板次数': 'break_limit_times',
            '连板数': 'continuous_limit_up',
            '所属行业': 'industry'
        })
        
        return result
        
    except Exception as e:
        print(f"获取数据时发生错误: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        if isinstance(e, KeyError):
            print("列名不匹配，实际列名为:")
            print(limit_up_df.columns.tolist())
        print("请确保网络连接正常")
        return pd.DataFrame()

def format_number(num):
    """
    格式化数字显示（将大数字转换为亿、万单位）
    """
    if pd.isna(num):
        return "-"
    if isinstance(num, str):
        return num
    if num >= 100000000:
        return f"{num/100000000:.2f}亿"
    elif num >= 10000:
        return f"{num/10000:.2f}万"
    else:
        return f"{num:.2f}"

def get_hour_from_time_str(time_str):
    """
    从时间字符串中提取小时
    """
    try:
        return int(time_str[:2])
    except:
        return None

def print_simple_info(limit_up_stocks):
    """
    打印简要信息
    """
    if not limit_up_stocks.empty:
        print(f"\n今日涨停股票数量: {len(limit_up_stocks)}")
        print("\n涨停股票列表:")
        simple_info = limit_up_stocks[['stock_code', 'name', 'industry', 'continuous_limit_up', 'break_limit_times']]
        print(simple_info.to_string(index=False))

def print_stats_info(limit_up_stocks):
    """
    打印统计信息
    """
    if not limit_up_stocks.empty:
        print(f"\n今日涨停股票数量: {len(limit_up_stocks)}")
        
        print("\n行业分布:")
        industry_stats = limit_up_stocks['industry'].value_counts()
        print(industry_stats.to_string())
        
        print("\n连板数统计:")
        continuous_stats = limit_up_stocks['continuous_limit_up'].value_counts().sort_index()
        print(continuous_stats.to_string())
        
        print("\n首次封板时间分布:")
        hour_stats = limit_up_stocks['first_limit_up_time'].apply(get_hour_from_time_str).value_counts().sort_index()
        for hour, count in hour_stats.items():
            if hour is not None:
                print(f"{hour:02d}点: {count}个")
        
        print("\n炸板次数统计:")
        break_stats = limit_up_stocks['break_limit_times'].value_counts().sort_index()
        print(break_stats.to_string())

def print_all_info(limit_up_stocks):
    """
    打印所有信息
    """
    if not limit_up_stocks.empty:
        # 格式化金额显示
        limit_up_stocks['amount'] = limit_up_stocks['amount'].apply(format_number)
        limit_up_stocks['market_cap'] = limit_up_stocks['market_cap'].apply(format_number)
        limit_up_stocks['limit_up_amount'] = limit_up_stocks['limit_up_amount'].apply(format_number)
        
        print(f"\n今日涨停股票数量: {len(limit_up_stocks)}")
        print("\n涨停股票列表:")
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        print(limit_up_stocks.to_string(index=False))
        
        # 打印统计信息
        print_stats_info(limit_up_stocks)

def main():
    try:
        # 解析命令行参数
        parser = argparse.ArgumentParser(description='获取涨停股票信息')
        parser.add_argument('--date', type=str, help='查询日期，格式：YYYYMMDD，默认为当天')
        parser.add_argument('--type', type=str, default='all', choices=['all', 'simple', 'stats'],
                          help='显示类型：all-全部信息，simple-简要信息，stats-仅统计信息')
        args = parser.parse_args()
        
        now = datetime.now()
        print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 获取涨停股票
        limit_up_stocks = get_limit_up_stocks(args.date)
        
        if not limit_up_stocks.empty:
            if args.type == 'simple':
                print_simple_info(limit_up_stocks)
            elif args.type == 'stats':
                print_stats_info(limit_up_stocks)
            else:  # 'all'
                print_all_info(limit_up_stocks)
        else:
            print("未获取到涨停股票数据")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        print(f"错误类型: {type(e).__name__}")

if __name__ == "__main__":
    main() 
// stock_limit_up.ts - 获取涨停板股票信息
import { parse } from "https://deno.land/std/flags/mod.ts";

// 解析命令行参数
const args = parse(Deno.args);
const date = args.date || new Date().toISOString().split('T')[0]; // 默认当天
const market = args.market || 'A'; // 默认A股市场

console.log(`正在获取${date}的${market}股涨停板数据...`);

// 股票API接口地址
const API_URL = `https://api.example.com/stocks/limitup?date=${date}&market=${market}`;

async function fetchLimitUpStocks() {
  try {
    const response = await fetch(API_URL);
    
    if (!response.ok) {
      throw new Error(`API请求失败: ${response.status}`);
    }
    
    const data = await response.json();
    
    console.log("\n====== 涨停板股票列表 ======");
    console.table(data.stocks.map((stock: any) => ({
      代码: stock.code,
      名称: stock.name,
      现价: stock.price,
      涨幅: `${stock.changePercent}%`,
      封板时间: stock.limitTime,
      封板次数: stock.limitCount
    })));
    
    console.log(`\n总计: ${data.stocks.length}只涨停股`);
  } catch (error) {
    console.error(`获取数据失败: ${error.message}`);
  }
}

await fetchLimitUpStocks();

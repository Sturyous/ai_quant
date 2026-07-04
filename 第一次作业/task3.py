import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys

# ---------------------------------------------------------
# 1. 初始化设置与参数配置
# ---------------------------------------------------------
# 设置中文字体，防止图表中文显示为方块
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS'] 
plt.rcParams['axes.unicode_minus'] = False

# 新浪接口的股票代码要求携带市场前缀（如沪市为 sh，深市为 sz）
stock_symbol = "sh600519" 
stock_code_pure = "600519"
stock_name = "贵州茅台"

# 计算过去一年的时间区间，并格式化为 YYYYMMDD（新浪接口要求的日期格式）
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=365)
start_str = start_date.strftime('%Y%m%d')
end_str = end_date.strftime('%Y%m%d')

print(f"正在通过新浪财经接口获取 {stock_name}({stock_code_pure}) 从 {start_str} 到 {end_str} 的历史行情数据...")

# ---------------------------------------------------------
# 2. 获取数据 (使用 stock_zh_a_daily 接口)
# ---------------------------------------------------------
try:
    # 采用量化研究中普遍使用的后复权(hfq)数据
    stock_data = ak.stock_zh_a_daily(
        symbol=stock_symbol, 
        start_date=start_str, 
        end_date=end_str, 
        adjust="hfq"
    )
    
    if stock_data is None or stock_data.empty:
        print("未获取到数据，请检查网络连接或股票代码是否正确。")
        sys.exit()
        
    print(f"成功获取到 {len(stock_data)} 个交易日的数据！正在生成图表和文件...")

except Exception as e:
    print(f"获取数据时发生错误: {e}")
    sys.exit()

# ---------------------------------------------------------
# 3. 数据处理与可视化绘制
# ---------------------------------------------------------
# 将返回的 'date' 字段转换为 datetime 格式以便画图
stock_data['date'] = pd.to_datetime(stock_data['date'])

plt.figure(figsize=(10, 5))
# 根据接口文档，收盘价字段名为 'close'
plt.plot(stock_data['date'], stock_data['close'], color='red', label='收盘价(后复权)', linewidth=1.5)
plt.title(f"{stock_name} ({stock_code_pure}) 过去一年每日收盘价走势图")
plt.xlabel("日期")
plt.ylabel("收盘价 (元)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()

# 导出曲线图为图片
img_filename = "close_price_chart.png"
plt.savefig(img_filename, dpi=150)
print(f"图表已成功保存为: {img_filename}")

# ---------------------------------------------------------
# 4. 导出 CSV 数据文件
# ---------------------------------------------------------
csv_filename = f"{stock_code_pure}_history_data.csv"
# 直接将包含 date, open, high, low, close, volume 等字段的 DataFrame 导出
stock_data.to_csv(csv_filename, index=False, encoding='utf-8-sig')
print(f"CSV 数据已成功保存为: {csv_filename}")

# ---------------------------------------------------------
# 5. 生成提交用的 HTML 网页文档
# ---------------------------------------------------------
html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>量化交易基础 - 数据获取报告</title>
    <style>
        body {{ font-family: '微软雅黑', sans-serif; background-color: #f4f4f9; padding: 20px; }}
        .container {{ max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1, h2 {{ color: #333; }}
        .info-box {{ background-color: #eef2f5; padding: 15px; border-left: 4px solid #0056b3; margin-bottom: 20px; }}
        img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; margin-top: 10px; }}
        .footer {{ margin-top: 40px; text-align: center; color: #777; font-size: 14px; border-top: 1px solid #eee; padding-top: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>量化交易作业：获取与可视化交易数据</h1>
        
        <div class="info-box">
            <p><strong>股票名称：</strong>{stock_name} ({stock_code_pure})</p>
            <p><strong>数据时间段：</strong>{stock_data['date'].min().strftime('%Y-%m-%d')} 至 {stock_data['date'].max().strftime('%Y-%m-%d')}</p>
            <p><strong>交易日天数：</strong>共 {len(stock_data)} 天</p>
            <p><strong>复权方式：</strong>后复权 (hfq)</p>
        </div>

        <h2>1. 每日收盘价曲线图</h2>
        <p>以下是通过 Python 绘制的过去一年收盘价走势图：</p>
        <img src="{img_filename}" alt="收盘价走势图">

        <h2>2. 数据存储说明</h2>
        <p>数据已成功利用 <code>akshare</code> 的 <code>stock_zh_a_daily</code> 接口获取，并完整保存至 <strong><a href="{csv_filename}">{csv_filename}</a></strong> 文件中。提取的字段包括：</p>
        <table>
            <tr>
                <th>date (交易日)</th>
                <th>open (开盘价)</th>
                <th>high (最高价)</th>
                <th>low (最低价)</th>
                <th>close (收盘价)</th>
                <th>volume (成交量)</th>
            </tr>
            <tr>
                <td>包含</td>
                <td>包含</td>
                <td>包含</td>
                <td>包含</td>
                <td>包含</td>
                <td>包含</td>
            </tr>
        </table>
        
        <div class="footer">
            <p>作业提交至 GitHub: <a href="https://github.com/Sturyous/ai_quant.git">Sturyous/ai_quant</a></p>
        </div>
    </div>
</body>
</html>
"""

html_filename = "index.html"
with open(html_filename, 'w', encoding='utf-8') as f:
    f.write(html_content)
    
print(f"HTML 网页报告已成功生成: {html_filename}")
print("\n所有任务执行完毕！现在可以将生成的文件推送到 GitHub 仓库了。")
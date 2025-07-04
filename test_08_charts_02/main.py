import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 读取数据
file_path = r'C:\Users\Grand_Caster\Desktop\test_01\test_01.xlsx'
df = pd.read_excel(file_path)

# 确保日期列是日期类型
df['日期'] = pd.to_datetime(df['日期'], format='%Y年%m月%d日')

# 提取年份和月份
df['年'] = df['日期'].dt.year
df['月'] = df['日期'].dt.month

# 去除温度的“℃”符号并转换为数值类型
df['最高温度'] = df['最高温度'].str.replace('℃', '').astype(float)
df['最低温度'] = df['最低温度'].str.replace('℃', '').astype(float)

# 计算每个月的平均最高温度和平均最低温度
monthly_avg_temps = df.groupby(['月'])[['最高温度', '最低温度']].mean().reset_index()

# 设置月份标签
monthly_avg_temps['月份'] = monthly_avg_temps['月'].astype(str) + '月'
monthly_avg_temps.set_index('月份', inplace=True)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体（SimHei）字体
plt.rcParams['axes.unicode_minus'] = False   # 解决负号显示问题

# 绘制折线图
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_avg_temps, x=monthly_avg_temps.index, y='最高温度', label='三年平均最高温度', marker='o', color='orange')
sns.lineplot(data=monthly_avg_temps, x=monthly_avg_temps.index, y='最低温度', label='三年平均最低温度', marker='o', color='blue')

# 设置图表标签和标题
plt.title('近三年月平均气温变化图', fontsize=16)
plt.xlabel('月份', fontsize=14)
plt.ylabel('温度 (℃)', fontsize=14)
plt.xticks(rotation=45)
plt.legend(title='气温类型')

# 保存图表到指定路径
output_path = r'C:\Users\Grand_Caster\Desktop\test_01\monthly_avg_temperature_trend.png'  # 指定保存路径
plt.tight_layout()  # 自动调整布局
plt.savefig(output_path, dpi=300)  # 保存图片，设置图片分辨率为300dpi

# 显示图表
plt.show()

print(f"图表已保存至: {output_path}")

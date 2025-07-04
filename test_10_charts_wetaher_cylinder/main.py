import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 读取数据
file_path = r'C:\Users\Grand_Caster\Desktop\test_01\test_01.xlsx'
df = pd.read_excel(file_path)

# 确保日期列是日期类型
df['日期'] = pd.to_datetime(df['日期'], format='%Y年%m月%d日')

# 提取白天和夜间天气状况
df['月'] = df['日期'].dt.month
df['白天天气'] = df['白天天气'].apply(lambda x: x.strip())  # 去除多余空格
df['夜间天气'] = df['夜间天气'].apply(lambda x: x.strip())  # 去除多余空格

# 统计每个月白天天气和夜间天气的分布
weather_counts = df.groupby(['月'])['白天天气'].value_counts().unstack(fill_value=0)
night_weather_counts = df.groupby(['月'])['夜间天气'].value_counts().unstack(fill_value=0)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体（SimHei）字体
plt.rcParams['axes.unicode_minus'] = False   # 解决负号显示问题

# 创建一个子图来同时展示白天和夜间天气的分布
fig, ax = plt.subplots(figsize=(14, 7))

# 绘制柱状图
weather_counts.plot(kind='bar', stacked=True, ax=ax, position=1, width=0.4)
night_weather_counts.plot(kind='bar', stacked=True, ax=ax, position=0, width=0.4)

# 设置标题和标签
plt.title('近三年每月天气状况分布', fontsize=16)
plt.xlabel('月份', fontsize=14)
plt.ylabel('出现的天数', fontsize=14)
plt.xticks(rotation=45)
plt.legend(title='天气状况', bbox_to_anchor=(1.05, 1), loc='upper left')

# 保存图表到指定路径
output_path = r'C:\Users\Grand_Caster\Desktop\test_01\monthly_weather_distribution.png'
plt.tight_layout()  # 自动调整布局
plt.savefig(output_path, dpi=300)  # 保存图片，设置图片分辨率为300dpi

# 显示图表
plt.show()

print(f"图表已保存至: {output_path}")

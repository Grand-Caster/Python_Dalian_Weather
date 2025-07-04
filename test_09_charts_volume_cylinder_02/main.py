import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# 读取数据
file_path = r'C:\Users\Grand_Caster\Desktop\test_01\test_01.xlsx'
df = pd.read_excel(file_path)

# 确保日期列是日期类型
df['日期'] = pd.to_datetime(df['日期'], format='%Y年%m月%d日')

# 提取风力等级（白天和夜间风力）
def extract_wind_level(wind_str):
    # 使用正则表达式提取风力等级
    match = re.search(r'(\d+-\d+)级', wind_str)
    if match:
        return match.group(1)
    return None

# 提取白天和夜间风力等级
df['白天风力等级'] = df['白天风力'].apply(extract_wind_level)
df['夜间风力等级'] = df['夜间风力'].apply(extract_wind_level)

# 合并白天和夜间风力等级
df['风力等级'] = df['白天风力等级'].fillna('无数据') + ' / ' + df['夜间风力等级'].fillna('无数据')

# 统计每个月不同风力等级出现的天数
df['月'] = df['日期'].dt.month
wind_level_counts = df.groupby(['月', '风力等级']).size().unstack(fill_value=0)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体（SimHei）字体
plt.rcParams['axes.unicode_minus'] = False   # 解决负号显示问题

# 绘制柱状图
plt.figure(figsize=(12, 6))

# 每个风力等级的统计数据
wind_level_counts.plot(kind='bar', stacked=True, figsize=(14, 7))

# 设置标题和标签
plt.title('近三年每月风力等级分布情况', fontsize=16)
plt.xlabel('月份', fontsize=14)
plt.ylabel('出现的天数', fontsize=14)
plt.xticks(rotation=45)
plt.legend(title='风力等级')

# 保存图表到指定路径
output_path = r'C:\Users\Grand_Caster\Desktop\test_01\monthly_wind_level_distribution.png'
plt.tight_layout()  # 自动调整布局
plt.savefig(output_path, dpi=300)  # 保存图片，设置图片分辨率为300dpi

# 显示图表
plt.show()

print(f"图表已保存至: {output_path}")

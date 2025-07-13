import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# === 读取主数据文件（2022-2024） ===
file_path = r'C:\Users\Grand_Caster\Desktop\Python_大连市天气作业\test_01\test_01.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')

# 数据预处理
df['日期'] = pd.to_datetime(df['日期'], format='%Y年%m月%d日')
df['年'] = df['日期'].dt.year
df['月'] = df['日期'].dt.month
df['最高温度'] = df['最高温度'].apply(lambda x: int(str(x).replace('℃', '')) if isinstance(x, str) else x)

# 按年和月计算每月平均最高温度
monthly_avg_temp = df.groupby(['年', '月'])['最高温度'].mean().reset_index()

# 特征构造
X = monthly_avg_temp[['年', '月']]
y = monthly_avg_temp['最高温度']
X['月_sin'] = np.sin(2 * np.pi * X['月'] / 12)
X['月_cos'] = np.cos(2 * np.pi * X['月'] / 12)

# 划分训练集（<2025）用于预测
X_train = X[X['年'] < 2025]
y_train = y[X['年'] < 2025]

# 模型训练
model = LinearRegression()
model.fit(X_train[['月_sin', '月_cos']], y_train)

# === 构造 2025 年的预测月份数据 ===
months_2025 = pd.DataFrame({'年': [2025]*12, '月': range(1, 13)})
months_2025['月_sin'] = np.sin(2 * np.pi * months_2025['月'] / 12)
months_2025['月_cos'] = np.cos(2 * np.pi * months_2025['月'] / 12)

# 预测结果
y_pred_2025 = model.predict(months_2025[['月_sin', '月_cos']])

# === 从 Excel 读取真实 2025 年 1~6 月爬虫数据 ===
real_file_path = r'C:\Users\Grand_Caster\Desktop\Python_大连市天气作业\test_01\test_01_2025_1_7.xlsx'
df_real = pd.read_excel(real_file_path, engine='openpyxl')
df_real['日期'] = pd.to_datetime(df_real['日期'], format='%Y年%m月%d日')
df_real['年'] = df_real['日期'].dt.year
df_real['月'] = df_real['日期'].dt.month
df_real['最高温度'] = df_real['最高温度'].apply(lambda x: int(str(x).replace('℃', '')) if isinstance(x, str) else x)

# 计算 2025 年前 6 月的平均最高温度
monthly_avg_real = df_real[df_real['年'] == 2025].groupby('月')['最高温度'].mean().loc[1:6]
real_data_2025 = monthly_avg_real.tolist()

# === 绘图对比 ===
plt.figure(figsize=(10, 6))
plt.plot(months_2025['月'], y_pred_2025, label='预测温度', marker='o', color='blue')
plt.plot(range(1, 7), real_data_2025, label='真实温度（爬虫数据）', marker='o', color='red')

# 图表细节
plt.xlabel('月份')
plt.ylabel('平均最高温度 (℃)')
plt.title('2025年温度预测与2025年1月至6月真实温度对比')
plt.legend()
plt.grid(True)

# 保存图像
plt.savefig(r'C:\Users\Grand_Caster\Desktop\Python_大连市天气作业\test_01\temperature_prediction_2025_full_year.png')
plt.show()

# 输出预测结果
for month, temp in zip(range(1, 13), y_pred_2025):
    print(f"2025年{month}月预测平均最高温度为: {temp:.2f}℃")

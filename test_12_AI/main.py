import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 读取数据
file_path = r'C:\\Users\\Grand_Caster\\Desktop\\test_01\\test_01.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')

# 数据预处理：提取日期中的年、月信息
df['日期'] = pd.to_datetime(df['日期'], format='%Y年%m月%d日')
df['年'] = df['日期'].dt.year
df['月'] = df['日期'].dt.month

# 转换 "最高温度" 列为数值类型，并去掉 "℃"
df['最高温度'] = df['最高温度'].apply(lambda x: int(x.replace('℃', '')) if isinstance(x, str) else x)

# 按年和月计算每月的平均最高温度
monthly_avg_temp = df.groupby(['年', '月'])['最高温度'].mean().reset_index()

# 特征和标签准备
X = monthly_avg_temp[['年', '月']]  # 年份和月份作为特征
y = monthly_avg_temp['最高温度']    # 平均最高温度作为标签

# 将月份转换为周期性特征：使用正弦和余弦
X['月_sin'] = np.sin(2 * np.pi * X['月'] / 12)  # 使用正弦函数表示月份
X['月_cos'] = np.cos(2 * np.pi * X['月'] / 12)  # 使用余弦函数表示月份

# 划分训练集和测试集（这里只用前三年训练）
X_train = X[X['年'] < 2025]  # 只用2022和2023年的数据
y_train = y[X['年'] < 2025]
X_test = X[X['年'] == 2024]  # 用2024年数据来测试
y_test = y[X['年'] == 2024]

# 训练线性回归模型
model = LinearRegression()
model.fit(X_train[['月_sin', '月_cos']], y_train)  # 使用周期性特征训练模型

# 预测2025年1月到12月的温度
months_2025 = pd.DataFrame({'年': [2025]*12, '月': range(1, 13)})
months_2025['月_sin'] = np.sin(2 * np.pi * months_2025['月'] / 12)
months_2025['月_cos'] = np.cos(2 * np.pi * months_2025['月'] / 12)

y_pred_2025 = model.predict(months_2025[['月_sin', '月_cos']])

# 获取真实数据：2025年1月到6月的真实数据（暂时没有，但可以在实际中替换成爬取的结果）
real_data_2025 = [7, 8, 10, 12, 14, 16]  # 这是一个示例，实际需要从爬虫中获得

# 合并预测数据和真实数据
predicted_real_data = y_pred_2025[:6]
real_data_combined = list(zip(range(1, 7), predicted_real_data, real_data_2025))

# 绘制预测结果和真实结果对比的折线图
plt.figure(figsize=(10, 6))
plt.plot(months_2025['月'], y_pred_2025, label='预测温度', marker='o', color='blue')
plt.plot(range(1, 7), real_data_2025, label='真实温度（爬虫数据）', marker='o', color='red')

# 设置标签和标题
plt.xlabel('月份')
plt.ylabel('平均最高温度 (℃)')
plt.title('2025年温度预测与2025年1月至6月真实温度对比')

# 添加图例
plt.legend()

# 显示网格
plt.grid(True)

# 保存图表
plt.savefig(r'C:\\Users\\Grand_Caster\\Desktop\\test_01\\temperature_prediction_2025_full_year.png')  # 保存图表
plt.show()

# 输出预测结果
for month, temp in zip(range(1, 13), y_pred_2025):
    print(f"2025年{month}月预测平均最高温度为: {temp:.2f}℃")

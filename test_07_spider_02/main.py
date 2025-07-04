from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# 存储所有天气数据
all_data = []

# 启动 Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # headless=True 表示无界面启动
    page = browser.new_page()

    # 网站的基本链接
    base_url = 'https://www.tianqihoubao.com/lishi/dalian/month/'

    # 生成2022-2024的月份URL
    months = [f"{year}{str(month).zfill(2)}" for year in range(2022, 2025) for month in range(1, 13)]

    # 遍历每个月
    for month in months:
        url = f"{base_url}{month}.html"
        print(f"正在爬取: {url}")
        page.goto(url)

        # 等待页面加载
        page.wait_for_timeout(5000)  # 等待5秒，确保页面加载完成

        # 解析页面内容
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

        # 查找所有天气数据行
        rows = soup.find_all('tr')

        for row in rows:
            # 获取日期
            date = row.find('a')
            if date:
                date = date.get_text().strip()

                # 获取天气状况（白天/夜间）
                weather = row.find_all('td')[1].get_text().strip().split(" / ")

                # 获取温度（最高/最低）
                temp = row.find_all('td')[2].get_text().strip().split(" / ")

                # 获取风力情况（白天/夜间）
                wind = row.find_all('td')[3].get_text().strip().split(" / ")

                # 存储数据
                all_data.append([date, weather[0], weather[1], temp[0], temp[1], wind[0], wind[1]])

    # 将数据保存到 Excel 文件
    df = pd.DataFrame(all_data, columns=['日期', '白天天气', '夜间天气', '最高温度', '最低温度', '白天风力', '夜间风力'])
    file_path = r'C:\Users\Grand_Caster\Desktop\test_01\test_01.xlsx'
    df.to_excel(file_path, index=False, engine='openpyxl')

    print(f"数据已保存到 {file_path}")

    # 关闭浏览器
    browser.close()

import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 创建一个Chrome选项对象
chrome_options = Options()
# 设置User-Agent
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36")

# 设置浏览器窗口大小
chrome_options.add_argument("--window-size=1920,1080")

# 设置代理IP
proxy = "127.0.0.1:7890"  # 替换为代理IP地址和端口号
chrome_options.add_argument(f'--proxy-server=http://{proxy}')

# 初始化WebDriver，这里以Chrome为例
driver = webdriver.Chrome(options=chrome_options)

# 打开网页
driver.get("https://www.csgoob.com/goods?name=%E6%A0%BC%E6%B4%9B%E5%85%8B%2018%20%E5%9E%8B%20%7C%20%E8%BF%9C%E5%85%89%E7%81%AF%20(%E5%B4%AD%E6%96%B0%E5%87%BA%E5%8E%82)")

# 随机等待一段时间，模拟人类操作
time.sleep(random.uniform(2, 5))

# 暂停程序，直到按下回车键
input("按下回车键以退出程序...")

# 关闭WebDriver
driver.quit()

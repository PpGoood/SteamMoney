import time
import random

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from ItemInfo import ItemInfo


def open_browser():
    uu_main_url = "https://www.youpin898.com/"
    steam_main_url = "https://steamcommunity.com/login"

    # 创建一个Chrome选项对象
    chrome_options = Options()
    # 设置User-Agent
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36")
    # 禁用 ChromeDriver 日志输出
    chrome_options.add_argument("--log-level=3")
    # 初始化WebDriver，这里以Chrome为例
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1288, 1100)
    #打开uu登录
    driver.get(uu_main_url)
    time.sleep(random.uniform(2, 5))
    input("请完成uu登陆后按下回车键...")

    #打开steam登录
    driver.get(steam_main_url)
    time.sleep(random.uniform(2, 5))
    input("请完成steam登陆后按下回车键...")

    count = input("请输入要爬取的最小销售额后按下回车键...\n")
    print("制作人pp，如有问题或者建议反馈：928826801，使用愉快❥(^_-)")
    process_data(driver,count)


def process_data(driver,count):
    iflow_url = f"https://www.iflow.work/cn?platform=buff-uuyp&game=csgo&order=sell&pagenum=1&min_price=1.0&max_price=5000.0&min_volume={count}"
    #iflow_url = "https://www.iflow.work/cn?platform=buff-uuyp&game=dota2&order=sell&pagenum=1&min_price=1.0&max_price=5000.0&min_volume=200"
    driver.get(iflow_url)
    dataDict = {}
    # 获取当前窗口句柄
    main_window = driver.current_window_handle

    count = 20
    # 循环点击不同元素，打开新窗口
    for i in range(1, count):
        try:
            platform_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            f"body > div > div.table-container > table > tbody > tr:nth-child({2*(i-1)+1}) > td:nth-child(9) > a"))
            )
            item_name_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            f"body > div > div.table-container > table > tbody > tr:nth-child({2*(i-1)+1}) > td:nth-child(2)"))
            )
            cur_item_name = item_name_element.text
            print("正在读取物品数据", item_name_element.text, f"当前进度：{i * 100 / count:.2f}%")
            dataDict[item_name_element.text] = ItemInfo(0,0,0)
            platform_element.click()
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            new_window = [window for window in driver.window_handles if window != main_window][0]
            driver.switch_to.window(new_window)
            # 获取新页面的数据
            new_window_url = driver.current_url
            if new_window_url.startswith("https://www.youpin898.com/"):
                sell_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                "#__layout > div > div.goodInfo > div.w1200.game-box > div.tabsNavBar.flex-b > div > div.ant-tabs-bar.ant-tabs-top-bar.ant-tabs-large-bar > div > div > div > div > div:nth-child(1) > div:nth-child(1)"))
                )
                sell_element.click()
                price_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                "#__layout > div > div.goodInfo > div.w1200.game-box > div:nth-child(10) > ul:nth-child(1) > li:nth-child(1) > div.t-4.price-wrapper > span > span"))
                )
                dataDict[cur_item_name].itemPrice = float(price_element.text)
                print("uu价格", dataDict[cur_item_name].itemPrice)
            elif new_window_url.startswith("https://buff.163.com/"):
                price_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                "#market-selling-list > tbody > tr:nth-child(2) > td:nth-child(5) > div:nth-child(1)"))
                )
                dataDict[cur_item_name].itemPrice = float(price_element.text.strip()[2:])
                print("buff价格",dataDict[cur_item_name].itemPrice)
            driver.close()
            driver.switch_to.window(main_window)
            time.sleep(2)


            steam_element =  WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            f"body > div > div.table-container > table > tbody > tr:nth-child({2*(i-1)+1}) > td:nth-child(10) > a"))
            )
            steam_element.click()
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            new_window = [window for window in driver.window_handles if window != main_window][0]
            driver.switch_to.window(new_window)

            try:
                max_attempts = 10  # 设置最大尝试次数
                attempts = 0  # 记录当前尝试次数
                while attempts < max_attempts:
                    try:
                        # 尝试使用第一种结构找到元素
                        steam_price1_element = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                        f"#searchResultsTable > div:nth-child(2) > div:nth-child({2 + attempts}) > div.market_listing_price_listings_block > div.market_listing_right_cell.market_listing_their_price > span > span.market_listing_price.market_listing_price_with_fee"))
                        )
                        steam_price_float = float(steam_price1_element.text.strip()[2:])
                        dataDict[cur_item_name].steamPrice = steam_price_float
                        break  # 转换成功，退出循环
                    except ValueError:
                        attempts += 1
                        if attempts < max_attempts:
                            time.sleep(2)
                            driver.refresh()  # 刷新页面
                            print("转换失败，正在尝试重新获取价格...")
                        else:
                            print("无法获取价格，请检查页面结构或网络连接")
            except TimeoutException:
                # 如果第一种结构找不到元素，尝试使用第二种结构
                try:
                    steam_price2_element = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "#market_commodity_forsale > span:nth-child(2)"))
                    )
                    dataDict[cur_item_name].steamPrice = float(steam_price2_element.text.strip()[2:])
                except TimeoutException:
                    print("两种结构都未找到元素")
            print("steam价格：",dataDict[cur_item_name].steamPrice)
            dataDict[cur_item_name].discount = round(
                dataDict[cur_item_name].itemPrice / (dataDict[cur_item_name].steamPrice * 0.87), 2)
            print("折扣：", format(dataDict[cur_item_name].discount, ".2f"))

            driver.close()
            driver.switch_to.window(main_window)
            time.sleep(2)
        except Exception as e:
            pass  # 忽略超时异常
            print(f"点击第 {i} 个元素时出现异常：{e}")

    input("按下回车键以继续...")


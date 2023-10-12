import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests

from qrcode import save_qrcode


# 设置 ChromeDriver 的路径
# https://chromedriver.storage.googleapis.com/index.html?path=114.0.5735.90/
# https://googlechromelabs.github.io/chrome-for-testing/
chromedriver_path = '/Users/xhs/Downloads/chromedriver-mac-arm64/chromedriver'

# 配置 ChromeDriver 选项
chrome_options = Options()
chrome_options.add_argument('--headless')  # 在无界面模式下运行
chrome_options.add_argument('--no-sandbox')  # 禁用沙盒模式
chrome_options.add_argument('--disable-infobars')  # 禁用"Chrome正在受到自动测试软件的控制"提示
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 避免Chrome被识别为自动化测试工具而无法加载页面
# 创建 ChromeDriver 实例
driver = webdriver.Chrome(chromedriver_path, options=chrome_options)

driver.set_window_size(1910, 985)

driver.get('https://mp.weixin.qq.com/')
# 打开网页

wait = WebDriverWait(driver, 20)
driver.get_screenshot_as_file("/tmp/login.png")  # 截取当前窗口，并指定截图图片的保存位置

# 等待二维码图片元素出现
qrcode_img = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, "//img[@class='login__type__container__scan__qrcode']")))
# 打印二维码地址
qrcode_url = qrcode_img.get_attribute('src')
print("qrcode_url:" + qrcode_url)
cookies = driver.get_cookies()
response = requests.get(qrcode_url, cookies={c['name']: c['value'] for c in cookies})
# print(response.text)
# response = requests.get(qrcode_url)
if response.status_code == 200:
    with open('qrcode.png', 'wb') as file:
        file.write(response.content)
        print("二维码已保存为 qrcode.png")
    # 把二维码发到服务端
    save_success = save_qrcode()
    if not save_success:
        print("上传二维码失败")
        exit(1)
else:
    print("无法获取二维码")

# 设置等待时间为20秒
waitLogin = WebDriverWait(driver, 20)
# driver.get_screenshot_as_file("/Users/xhs/go_workspace/wechatmplogin/main.png") # 截取当前窗口，并指定截图图片的保存位置
element1 = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//*[@class='weui-desktop_name']")))

# 获取当前页面的 URL
current_url = driver.current_url

# 打印当前页面的 URL
print("Current URL:", current_url)
params = current_url.split("&")

# 遍历键值对，查找包含 "token=" 的项
token = ""
for param in params:
    if "token=" in param:
        # 使用字符串的 split 方法将键值对按照 "=" 分割，并获取第二部分即 token 值
        token = param.split("=")[1]
        break
print(token)

# 获取当前页面的 cookie
cookies = driver.get_cookies()

cookie_str = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

url = "http://task.xiaohuasheng.cc/api/mp"

headers = {
    "Content-Type": "application/json"
}

data = {
    "headers": {
        "Host": "mp.weixin.qq.com",
        "Connection": "keep-alive",
        "Content-Length": "159",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": "\"macOS\"",
        "Accept": "*/*",
        "Origin": "https://mp.weixin.qq.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://mp.weixin.qq.com/cgi-bin/message?t=message/list&count=20&day=7&token=1262175526&lang=zh_CN",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": cookie_str
    },
    "body": {
        "tofakeid": "oxlcXw9YCql2m3RH0A3xVLw8oFo0",
        "imgcode": "",
        "type": "1",
        "content": "1",
        "out_trade_no": "undefined",
        "appmsg": "",
        "quickreplyid": "464155968",
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1"
    }
}

print(data)
response = requests.post(url, json=data, headers=headers)
print(response.text)
driver.quit()

# 保存到 mp_auth.json
with open('mp_auth.json', 'w') as f:
    f.write(json.dumps(data))
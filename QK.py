import requests

import json
from bs4 import BeautifulSoup

#自动获取cookie部分，建议提前手动登录获取cookie
# 自己手动替换专业号，班级号和年份
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
'''

#这里使用统一身份验证的票据登录

'''
cookies_string = validate_and_get_cookies(username, password)

def fetch_new_cookies(username, password):
    logging.info("#Starting to fetch new cookies...")
    options = Options()
    options.add_argument("--headless")  # Headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    chromedriver_path = r"/usr/bin/chromedriver"

    #请改为你的正确路径，例如
    #chromedriver_path = r"C:\Users\zhang\Desktop\chromedriver_win32\chromedriver.exe"

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://authserver.jsei.edu.cn/authserver/login?service=https%3A%2F%2Fjwpd.jsei.edu.cn%2Fsso%2Fjznewsixlogin")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

        # Enter username and password
        logging.info("#Entering username and password...")
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.CLASS_NAME, "auth_login_btn").click()

        # Wait for redirection
        WebDriverWait(driver, 15).until(EC.url_contains("jwpd.jsei.edu.cn"))

        # Get new cookies
        cookies_string = get_cookies_with_retries(driver)

        #如果需要预存
        # Save cookies to file
        #save_cookies_to_file(username, password, cookies_string)
    finally:
        driver.quit()

    return cookies_string

    

# 获取 Cookies 带重试机制
def get_cookies_with_retries(driver, retries=5, delay=1):
    for attempt in range(1, retries + 1):
        try:
            logging.info(f"#Attempting to retrieve cookies (Attempt {attempt})...")
            cookies = driver.get_cookies()
            if cookies:
                cookies_string = "; ".join(f"{cookie['name']}={cookie['value']}" for cookie in cookies)
                logging.info(f"#Successfully retrieved cookies: {cookies_string}")

                # 检查是否包含 org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=en;
                if "org.springframework.web.servlet.i18n.CookieLocaleResolver." in cookies_string:
                    logging.warning("!!!Account or password error, cookies contain invalid fields")
                    socketio.emit('error', {"error": "Invalid account or password"})  # 向客户端发送错误信息
                    return None  # 返回 None 表示错误

                return cookies_string
            else:
                logging.warning("!!!Failed to retrieve cookies, retrying...")
        except Exception as error:
            logging.error(f"!!!Error while retrieving cookies: {error}")
        time.sleep(delay)

    raise Exception("!!!Failed to retrieve cookies after maximum retry attempts")


    
def validate_and_get_cookies(username, password):
    cookies_string = check_for_valid_cookies(username, password)

    # 如果已有的 Cookies 包含 'org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=en;' 字段，认为账号密码错误
    if cookies_string and "org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=en;" in cookies_string:
        logging.warning(f"!!!Account or password error, cookies contain invalid 'LOCALE=en' field")
        socketio.emit('error', {"error": "Invalid account or password"})
        return None  # Return None to indicate an error

    # 如果 Cookies 无效或不存在，则获取新的 Cookies
    if cookies_string:
        if not are_cookies_valid(cookies_string, username, password):
            logging.info("#Existing cookies are invalid, attempting to retrieve new ones...")
            delete_invalid_cookies(username, password)
            cookies_string = None

    if not cookies_string:
        logging.info("#No valid cookies found, starting to retrieve new cookies...")
        cookies_string = fetch_new_cookies(username, password)

    return cookies_string
'''

####获取个人选课批次号######
#当教务系统开放抢课后会生成一个个人选课批次号，用于后续选课

# 以下是手动提取的 Cookie 字符串，

cookies_string = "JSESSIONID=267F84018E5EA4439FDD31D6C96124DA; route=9e4eecea493e42c3ec7d850aa5b4b0bb"


urlgrxkpch = "https://jwpd.jsei.edu.cn/xsxk/zzxkyzb_cxZzxkYzbIndex.html"
paramsgrxkpch = {
    "gnmkdm": "N253512",
    "layout": "default"
}

headersgrxkpch = {
    "Host": "jwpd.jsei.edu.cn",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Cookie": cookies_string,
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i"
}

try:
    # 发送 GET 请求
    responsegrxkpch = requests.get(urlgrxkpch, headers=headersgrxkpch, params=paramsgrxkpch)
    responsegrxkpch.raise_for_status()  # 检查 HTTP 状态码
    
    # 解析 HTML
    soup = BeautifulSoup(responsegrxkpch.text, 'html.parser')
    
    # 提取隐藏字段值
    hidden_input = soup.find('input', {'name': 'firstXkkzId', 'id': 'firstXkkzId'})
    
    if hidden_input and hidden_input.get('value'):
        xkkz_id = hidden_input['value']
        print(f"提取成功！个人选课批次号隐藏字段值: {xkkz_id}")
        
        # 以下是原始内容输出的两种方式
       # print("\n完整响应内容 (前1000字符):")
        #print(response.text[:1000] + "..." if len(response.text) > 1000 else response.text)
        
        #print("\n格式化后的隐藏字段HTML片段:")
        #print(hidden_input.prettify())
    else:
        print("错误：未找到 firstXkkzId 隐藏字段")

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
except Exception as e:
    print(f"解析错误: {e}")

# 输出 HTTP 状态信息
print("\n调试信息:".center(50, '-'))
print(f"HTTP 状态码: {responsegrxkpch.status_code}")
print(f"响应大小: {len(responsegrxkpch.content)} 字节")
print(f"实际请求 URL: {responsegrxkpch.url}")







#############


#############查询页面
#查询页面


urlcxym = "https://jwpd.jsei.edu.cn/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512"

headerscxym = {
    "Host": "jwpd.jsei.edu.cn",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://jwpd.jsei.edu.cn",
    "Connection": "keep-alive",
    "Referer": "https://jwpd.jsei.edu.cn/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default",
    "Cookie": cookies_string,
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0"
}

# 基础请求参数（不包含分页参数）
base_payload = {
    "rwlx": "2",
    "xklc": "2",
    "xkly": "0",
    "bklx_id": "0",
    "sfkkjyxdxnxq": "0",
    "kzkcgs": "0",
    "xqh_id": "1",
    "jg_id": "03",
    "njdm_id_1": "2024",
    "zyh_id_1": "0319",
    "gnjkxdnj": "0",
    "zyh_id": "0319",
    "zyfx_id": "wfx",
    "njdm_id": "2024",
    "bh_id": "0319241",
    "bjgkczxbbjwcx": "0",
    "xbm": "1",
    "xslbdm": "06",
    "mzm": "01",
    "xz": "3",
    "ccdm": "4",
    "xsbj": "0",
    "sfkknj": "0",
    "sfkkzy": "0",
    "kzybkxy": "0",
    "sfznkx": "0",
    "zdkxms": "0",
    "sfkxq": "0",
    "sfkcfx": "0",
    "kkbk": "0",
    "kkbkdj": "0",
    "sfkgbcx": "0",
    "sfrxtgkcxd": "0",
    "tykczgxdcs": "0",
    "xkxnm": "2024",
    "xkxqm": "12",
    "kklxdm": "10",
    "bbhzxjxb": "0",
    "xkkz_id": "xkkz_id",  # 注意：此处需替换为实际变量值
    "rlkz": "0",
    "xkzgbj": "0",
    "jxbzb": ""
}

page = 1
courses = []  # 存储所有课程信息

while True:
    kspage = str(1 + (page - 1) * 10)
    jspage = str(page * 10)
    
    payload = base_payload.copy()
    payload['kspage'] = kspage
    payload['jspage'] = jspage
    
    response = requests.post(urlcxym, headers=headerscxym, data=payload)
    
    if response.status_code != 200:
        print(f"请求失败（页码 {page}）: 状态码 {response.status_code}")
        break
    
    try:
        data = response.json()
    except json.JSONDecodeError:
        print(f"页码 {page} 的响应格式不正确")
        break
    
    tmp_list = data.get('tmpList', [])
    
    # 收集所有课程
    courses.extend(tmp_list)
    
    if not tmp_list:
        print(f"页码 {page} 无数据，结束请求")
        break
    else:
        page += 1

# 展示所有课程列表供选择
print("\n所有课程列表：")
for idx, course in enumerate(courses, 1):
    jxbmc = course.get('jxbmc', 'N/A')
    kch_id = course.get('kch_id', 'N/A')
    print(f"{idx}. 子课程: {jxbmc}, 课程类型编号: {kch_id}")

# 用户输入选择
while True:
    try:
        selected = input("\n请输入要选择的课程编号（数字）：")
        selected_index = int(selected) - 1  # 转换为0-based索引
        
        if 0 <= selected_index < len(courses):
            kch_id = courses[selected_index]['kch_id']
            print(f"已选择课程类型编号：{kch_id}")
            break
        else:
            print("输入的编号超出范围，请重新输入！")
    except ValueError:
        print("请输入有效的数字！")

# 现在kch_id变量已保存用户选择的课程编号
print(f"最终选择的kch_id是：{kch_id}")
###############处理查询结果结束###################

###############展示课程教学班（展开课程详细）###################
#kch_id=input("课程类型编号")

urlcxxx = "https://jwpd.jsei.edu.cn/xsxk/zzxkyzbjk_cxJxbWithKchZzxkYzb.html?gnmkdm=N253512"

headerscxxx = {
    "Host": "jwpd.jsei.edu.cn",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://jwpd.jsei.edu.cn",
    "Connection": "keep-alive",
    "Referer": "https://jwpd.jsei.edu.cn/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default",
    "Cookie": cookies_string,
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0"
}

payloadcxxx = {
    "rwlx": "2",
    "xkly": "0",
    "bklx_id": "0",
    "sfkkjyxdxnxq": "0",
    "kzkcgs": "0",
    "xqh_id": "1",
    "jg_id": "03",
    "zyh_id": "0319",
    "zyfx_id": "wfx",
    "txbsfrl": "0",
    "njdm_id": "2024",
    "bh_id": "0319241",
    "xbm": "1",
    "xslbdm": "06",
    "mzm": "01",
    "xz": "3",
    "ccdm": "4",
    "xsbj": "0",
    "sfkknj": "0",
    "gnjkxdnj": "0",
    "sfkkzy": "0",
    "kzybkxy": "0",
    "sfznkx": "0",
    "zdkxms": "0",
    "sfkxq": "0",
    "sfkcfx": "0",
    "bbhzxjxb": "0",
    "kkbk": "0",
    "kkbkdj": "0",
    "xkxnm": "2024",
    "xkxqm": "12",
    "xkxskcgskg": "1",
    "rlkz": "0",
    "cdrlkz": "0",
    "rlzlkz": "1",
    "kklxdm": "10",
    "kch_id": kch_id,
    "jxbzcxskg": "0",
    "xklc": "2",
    "xkkz_id": xkkz_id,
    "cxbj": "0",
    "fxbj": "0"
}

responsecxxx = requests.post(urlcxxx, headers=headerscxxx, data=payloadcxxx)

print(f"Status Code: {responsecxxx.status_code}")
#print("Response Content:")
#print(responsecxxx.text)

###############展示课程教学班（展开课程详细）###################

##############处理展示课程教学班请求##################
# 将JSON字符串转换为Python字典
datacxxx = json.loads(responsecxxx.text)

# 遍历列表，并打印每个课程的相关信息
for course in datacxxx:
    kcmc = course.get('kcmc', 'N/A')  # 课程名称可能不存在于提供的JSON数据中
    kklxmc = course.get('kklxmc', 'N/A')  # 课程类型也可能不存在
    jsxx = course.get('jsxx', 'N/A')
    sksj = course.get('sksj', 'N/A')
    jxdd = course.get('jxdd', 'N/A')
    do_jxb_id = course.get('do_jxb_id', 'N/A')
#print(f'课程名称: {kcmc}, 课程类型: {kklxmc}, 教师姓名: {jsxx}, 上课时间: {sksj}, 上课地点: {jxdd}, 班级唯一编号: {do_jxb_id}')

##############处理展示课程教学班请求结束##################

##############选课请求##################
# 获取用户输入的班级号序列（如输入12345代表选择1、2、3、4、5号班级）
import json

# 将JSON字符串转换为Python字典
datacxxx = json.loads(responsecxxx.text)

courses = []  # 存储所有课程的do_jxb_id
#print("可用课程列表：")
for index, course in enumerate(datacxxx, 1):
    kcmc = course.get('kcmc', 'N/A')
    kklxmc = course.get('kklxmc', 'N/A')
    jsxx = course.get('jsxx', 'N/A')
    sksj = course.get('sksj', 'N/A')
    jxdd = course.get('jxdd', 'N/A')
    do_jxb_id = course.get('do_jxb_id', 'N/A')
    courses.append(do_jxb_id)
  #  print(f'序号: {index}, 课程名称: {kcmc}, 课程类型: {kklxmc}, 教师姓名: {jsxx}, 上课时间: {sksj}, 上课地点: {jxdd}, 班级唯一编号: {do_jxb_id}')
    print(f'序号: {index}, 课程名称: {kcmc}, 课程类型: {kklxmc}, 教师姓名: {jsxx}, 上课时间: {sksj}, 上课地点: {jxdd}')

# 用户输入处理
while True:
    try:
        choice = int(input("请输入班级对应的序号："))
        if 1 <= choice <= len(courses):
            selected_id = courses[choice - 1]
            jxb_ids = selected_id  # 将选中的班级编号赋值给jxb_ids
            break
        else:
            print("输入的序号超出范围，请重新输入。")
    except ValueError:
        print("请输入有效的数字。")

# 此时jxb_ids_str即为最终需要的班级编号集合，可直接用于后续操作

##############处理展示课程教学班请求结束##################

##############选课请求##################
#jxb_ids=input("请输入班级号：")

urlxk = "https://jwpd.jsei.edu.cn/xsxk/zzxkyzbjk_xkBcZyZzxkYzb.html?gnmkdm=N253512"

headersxk = {
    "Host": "jwpd.jsei.edu.cn",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://jwpd.jsei.edu.cn",
    "Connection": "keep-alive",
    "Referer": "https://jwpd.jsei.edu.cn/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default",
    "Cookie": cookies_string,
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0"
}

payloadxk = {
    "jxb_ids": jxb_ids,
    "kch_id": kch_id,
    "xkkz_id": xkkz_id,
    "rwlx": "2",
    "rlkz": "0",
    "cdrlkz": "0",
    "rlzlkz": "1",
    "sxbj": "1",
    "xxkbj": "0",
    "qz": "0",
    "cxbj": "0",
    "xkkz_id": "0",
    "njdm_id": "2024",
    "zyh_id": "0319",
    "kklxdm": "10",
    "xklc": "2",
    "xkxnm": "2024",
    "xkxqm": "12",
    "jcxx_id": ""
}
#  #这个参数似乎和选课者批次有关，不同的选课者有不同的值
responsexk = requests.post(urlxk, headers=headersxk, data=payloadxk)

print(f"Status Code: {responsexk.status_code}")
print("Response Content:")
print(responsexk.text)

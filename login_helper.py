import json
import logging
from time import sleep
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from globals import home_url
from utils.file_util import append_data_to_env
from utils.xpath_util import is_xpath_exist

logging.basicConfig(level=logging.INFO)


def init_webdriver_for_gen_cookie_gui():
    chrome_options = Options()
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    s = Service(r"./lib/chromedriver.exe")
    bro = webdriver.Chrome(service=s, chrome_options=chrome_options, options=option)
    chains = ActionChains(bro)
    return bro, chains


def login_manual(bro):
    while is_xpath_exist(bro, '//*[@id="i_cecream"]/div[2]/div[1]/div[1]/ul[2]/li[1]/li/div') is True:
        sleep(1)
    dict_cookies = bro.get_cookies()
    json_cookies = json.dumps(dict_cookies)
    try:
        url = bro.find_element(By.XPATH, '//*[@id="i_cecream"]/div[2]/div[1]/div[1]/ul[2]/li[1]/div[1]/a[1]').get_attribute("href")
    except Exception as e:
        print(e)
    result = urlparse(url)
    id = str(result[2])[1:]
    cookie_path = './cookie/' + id + '.txt'
    with open(cookie_path, 'w') as f:
        f.write(json_cookies)
    # 在my_user_id后面追加新数据，如果原来的my_user_id为空则不添加逗号
    append_data_to_env("my_user_id", id if not id.startswith(",") else id)


def login_gui():
    # 初始化
    bro, chains = init_webdriver_for_gen_cookie_gui()
    bro.get(home_url)
    # 登录
    login_manual(bro)
    bro.quit()

if __name__ == '__main__':
    # 初始化
    bro, chains = init_webdriver_for_gen_cookie_gui()
    bro.get(home_url)
    # 登录
    login_manual(bro)
    bro.quit()
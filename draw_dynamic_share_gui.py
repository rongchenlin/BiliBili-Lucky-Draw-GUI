import json
import logging
import time
import traceback
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import globals
from login_helper import init_webdriver_for_gen_cookie_gui
from utils.customer_logger import error_to_log_more, error_to_log
from utils.file_util import get_value_from_env

logging.basicConfig(level=logging.INFO)
from main import logger


def login_by_cookie(bro, cookie_path):
    """
    根据保存的Cookie信息进行登录
    :param bro:
    :param cookie_path:
    :return:
    """
    try:
        with open(cookie_path, 'r', encoding='utf-8') as f:
            cookies = f.readlines()
        for cookie in cookies:
            cookie = cookie.replace(r'\n', '')
            cookie_li = json.loads(cookie)
            sleep(1)
            for cookie in cookie_li:
                bro.add_cookie(cookie)
            bro.refresh()
        print('使用cookie自动登录成功！')
        sleep(1)
    except Exception as e:
        print(e)
        print('登录失败')

def is_draw(bro, xpath):
    """
    判断是否为抽奖标签
    :param bro:
    :param xpath:
    :return:
    """
    try:
        var = bro.find_element(By.XPATH, xpath).text
        if "抽奖" in var:
            return True
        else:
            return False
    except:
        return False


def do_share(bro, chains,  filtered_links):
    try:

        for new_url in filtered_links:
            try:
                # 如果是已经转发过的，跳过，不转发
                # sql = "SELECT * FROM t_share where dyn_id  = " + dyn_id
                # data = db.select_db(sql)  # 用mysql_operate文件中的db的select_db方法进行查询
                # if len(data) != 0:
                #     break

                # 否则，开始执行下面的转发操作
                bro.get(new_url)
                sleep(3)

                # 移动到头像
                touxiang = bro.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div/div[1]/div[1]/div')
                sleep(3)
                chains.move_to_element(touxiang).perform()
                sleep(3)

                # 点击关注
                follow = bro.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[3]/div[1]')
                follow_text = follow.get_attribute('innerText')
                sleep(2)
                if "已关注" not in follow_text:
                    chains.click(follow).perform()

                sleep(1)
                share_btn = bro.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div/div[1]/div[4]/div[1]/div/i')
                sleep(1)
                chains.click(share_btn).perform()
                sleep(1)
                do_share_btn = bro.find_element(By.XPATH,
                                                '//*[@id="app"]/div[2]/div/div/div[2]/div[1]/div[1]/div/div[2]/div['
                                                '2]/div[2]/button')
                sleep(2)
                chains.click(do_share_btn).perform()
                sleep(2)

                # # 保存记录
                # params = {
                #     'user_id': user_id,
                #     'fans_id': fans_id,
                #     'dyn_id': dyn_id,
                #     'flag': str(1),
                #     'insert_time': str(datetime.now())
                # }
                # db.insert('t_share', params)
                # # 更新t_share的update_time
                # update_params = {'update_time': str(datetime.now())}
                # cond_dict = {'fans_id': fans_id}
                # db.update('t_fans', update_params, cond_dict)
                logger.info('已完成转发的动态链接为: ' + new_url)
            except Exception as e:
                error_to_log_more("start_forward", "转发动态[执行转发or入库]出错：" + traceback.format_exc(), "p1", new_url)
    except Exception as e:
        logging.error(traceback.format_exc())




def start_forward():

    try:
        logger.info('抽奖动态开始转发，当前时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        # 初始化
        bro, chains = init_webdriver_for_gen_cookie_gui()
        my_user_id = get_value_from_env(".env", "my_user_id")
        cookie_path = './cookie/' + my_user_id + '.txt'
        bro.get(globals.home_url)
        login_by_cookie(bro, cookie_path)
        # time.sleep(2)
        # 使用XPath定位元素并获取链接
        bro.get('https://space.bilibili.com/226257459/article')
        time.sleep(1)
        bro.get('https://space.bilibili.com/226257459/article')

        wait = WebDriverWait(bro, 30)  # 最多等待10秒
        link_element = wait.until(EC.presence_of_element_located((By.XPATH, '//h2[@class="article-title"]/a')))
        today_start_link = link_element.get_attribute('href')


        bro.get(today_start_link)
        # 显式等待，等待元素列表出现
        wait2 = WebDriverWait(bro, 10)  # 最多等待10秒
        # 等待元素列表出现
        elements = wait2.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(text(), "网页链接")]')))
        # 获取这些<a>标签的href属性值
        links = [element.get_attribute("href") for element in elements]
        filtered_links = [link for link in links if "t.bilibili." in link]
        # 输出链接列表
        do_share(bro, chains, filtered_links)
    except Exception as e:
        error_to_log("start_forward", "转发动态出错：" + traceback.format_exc(), "p1")
    finally:
        finish_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        logger.info('抽奖动态转发结束，当前时间：' + finish_time)



# if __name__ == '__main__':
#     start_forward()
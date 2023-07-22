import logging
import os
import random
import threading
import time
import tkinter as tk
import webbrowser
from globals import max_checks
from logger_util import TextHandler
from utils.file_util import get_value_from_env

logging.basicConfig(level=logging.INFO)


def open_url(url):
    webbrowser.open(url)

"""
设置主窗口信息
"""
# 创建主窗口
window = tk.Tk()
window.title("BibiBili-Lucky-Draw")
window.geometry("900x600")
# 最大化窗口
# window.state('zoomed')

def do_login_gui():
    from login_helper import login_gui
    thread2 = threading.Thread(target=login_gui)
    thread2.start()

"""
设置登录状态相关组件
"""
def blink_label():
    random_color = random.choice(colors)
    tip_login_label.config(fg=random_color)
    tip_login_label.after(100, blink_label)

tip_login_label = tk.Label(window, text="请先登录到bilibili!", font=("Arial", 32))
tip_login_label.place(x=220, y=100)
colors = ["red", "green", "blue", "purple"]
logined_lab = tk.Label(window, text="您已经成功登录到bilibili啦!")
# login_btn = tk.Button(window, text="点击我，登录bilibili", command=lambda: do_login_gui())
# 调用提醒登录的闪烁组件
blink_label()

"""
设置日志相关组件
"""
log_area = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED)
log_area.place(x=0, y=400, width=900, height=200)
# 设置日志处理器
text_handler = TextHandler(log_area)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
text_handler.setFormatter(formatter)
# 创建Logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)
logger.addHandler(text_handler)

logined_flag = False
"""
当前账号是否登录校验
- 如果登录，才可以显示相关按钮
- 如果没有登录，则提示用户登录
"""
def check_cookie_status(logined_lab, tip_login_label):
    file_name = ''
    flag = 1
    for i in range(max_checks):
        if os.path.exists(os.path.join('./', '.env')):
            # 加载 .env 文件
            my_user_id_value = get_value_from_env(".env", "my_user_id")
            file_name = my_user_id_value + '.txt'
        if os.path.exists(os.path.join('./cookie', file_name)):
            logger.info('登录成功！')
            tip_login_label.destroy()
            logined_lab.pack()
            # TODO 这里开始设置逻辑
            from draw_dynamic_share_gui import start_forward
            start_forward()
            return True;
        else:
            if flag == 1:
                do_login_gui()
                flag = 2
            if flag ==2 or flag == 1:
                logger.warning('请先登录到BiliBili . . .')
        time.sleep(1)


# 日志实时打印
def info_logging_print():
    # 2秒后继续打印日志
    window.after(2000, info_logging_print)


if __name__ == '__main__':
    # 子线程时刻判断登录状态，不影响windows组件的加载
    thread = threading.Thread(target=check_cookie_status, args=( logined_lab, tip_login_label))
    thread.start()
    # 显示日志组件
    info_logging_print()
    window.mainloop()

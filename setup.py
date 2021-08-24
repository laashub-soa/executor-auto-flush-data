import logging
import os
import time

from __init__ import init
from component import mymysql
from config import app_conf

init()
target_db_pool = mymysql.init(app_conf["mysql"])
logger = logging.getLogger('setup')
logger.setLevel(logging.DEBUG)
flush_data_worker = []  # 刷数据的工作者
if __name__ == '__main__':
    # 检查service_data目录中是否有需要文件
    while True:
        time.sleep(5)
        logger.debug("正在检查是否有需要刷数据的任务")
        file_list = os.listdir("service_data")
        print(file_list)

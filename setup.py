import logging
import os
import time
from threading import Thread

from __init__ import init
from timer.auto_flush_data import auto_flush_data

init()
logger = logging.getLogger('setup')
logger.setLevel(logging.DEBUG)
flush_data_worker = {}  # 刷数据的工作者


def check_2_create_worker_thread():
    # logger.debug("正在检查是否有需要刷数据的任务")
    file_list = os.listdir("service_data")
    # 得到SQL文件列表
    sql_file_list = []
    for item in file_list:
        if item.endswith(".sql"):
            sql_file_list.append(item)
    # 创建任务队列
    for item in sql_file_list:
        # TODO 这里同样需要检查线程的执行状态
        if item not in flush_data_worker:
            t = Thread(target=auto_flush_data, args=(item,), name=item)
            flush_data_worker[item] = t  # 先添加数据再启动
            t.start()
            logger.debug("任务队列%s正在运行" % (item,))

    # logger.debug(file_list)


if __name__ == '__main__':
    # 检查service_data目录中是否有需要文件
    while True:
        time.sleep(3)
        check_2_create_worker_thread()

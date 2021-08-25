import logging
import os
import time

from __init__ import project_root_path
from component import mymysql, request_dingding_webhook
from config import app_conf

mysql_config = app_conf["mysql"]


def post_alarm(logger, msg_content, at_mobiles=[]):
    dingding_webhook_access_token = app_conf["dingding_webhook_access_token"][0]
    dingding_resp = request_dingding_webhook.request_dingding_webhook(dingding_webhook_access_token, "自动刷数据",
                                                                      msg_content, at_mobiles)
    logger.debug(dingding_resp)


def do_auto_flush_data(logger, sql_file_name):
    # 检查路径
    sql_file_path = os.path.join(project_root_path, "service_data", sql_file_name)
    sql_db_file_path = os.path.join(project_root_path, "service_data", sql_file_name + ".db")
    if not (os.path.exists(sql_file_path) and os.path.exists(sql_db_file_path)):
        logger.debug("任务的SQL文件或者数据名称声明文件不存在")
        raise Exception("任务的SQL文件或者数据名称声明文件不存在")
    # 数据库名称
    with open(sql_db_file_path, 'r', encoding='utf-8') as f:
        sql_db = f.read()
    mysql_config["database"] = sql_db
    # SQL
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_file_content = f.read()
    # logger.debug(sql_file_content)
    # 查询需要刷的数据的行数
    count_sql = """
    select count(1) as sql_count from (
    %s
    )tristan_t
    """ % sql_file_content
    count_result = mymysql.query(mysql_config, count_sql)
    if len(count_result) < 1:
        logger.debug("并没有需要刷的数据")
        return
    sql_count = count_result[0]["sql_count"]
    if sql_count < 1:
        logger.debug("并没有需要刷的数据")
        return

    actual_flush_data_count = count_result[0]["sql_count"]
    # 查询刷数据的实际update语句行
    actual_update_sql_result = mymysql.query(mysql_config, sql_file_content)
    # 转换为update sql 数组
    update_sql_list = []
    for item in actual_update_sql_result:
        update_sql_item = item["updSql"]
        update_sql_list.append(update_sql_item)
    logger.debug(actual_update_sql_result)
    change_result = mymysql.change(mysql_config, update_sql_list)
    logger.debug(change_result)
    return change_result


def auto_flush_data(sql_file_name):
    logger = logging.getLogger('auto_flush_data-%s' % sql_file_name)
    logger.setLevel(logging.DEBUG)
    is_continue = True
    while is_continue:
        time.sleep(30 * 60)  # 每隔30min钟刷一下数据
        # time.sleep(3)  # 每隔3s钟刷一下数据
        try:
            start_time = int(time.time())
            change_result = do_auto_flush_data(logger, sql_file_name)
            took_time = int(time.time()) - start_time
            if change_result:
                change_result_len = len(change_result)
                post_alarm(logger,
                           "自动刷数据: " + sql_file_name + "-运行成功: 成功自动刷%s条数据动作, 过程花费%s秒钟" % (change_result_len, took_time))
        except Exception as e:
            import traceback, sys
            traceback.print_exc()  # 打印异常信息
            logger.debug("由于文件变动已退出运行")
            post_alarm(logger, "自动刷数据: " + sql_file_name + "-由于文件变动已退出运行")
            # 这里需要
            is_continue = False

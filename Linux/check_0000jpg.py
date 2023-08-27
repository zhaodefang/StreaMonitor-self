import os
import time
import logging
import shutil
import sys
import json
import requests
import datetime
import hmac
import hashlib
import base64
import urllib.parse

# 操作日志
logtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")             # 脚本操作日志时间戳
logLifecycleLog = "log-RunOperation.log"                                    # 脚本的生命周期日志

localpath = os.path.split(os.path.abspath(__file__))[0]                     # 获取当前文件的绝对路径，并使用os.path.split()函数将其分割为目录和文件名，[0]表示取目录部分
logpath = os.path.join(localpath, 'log')                                    # 使用os.path.join()函数将当前路径和子目录名 'log' 连接起来，形成完整的日志路径

# 设置日志文件名和格式
log_filename = os.path.join(logpath, 'log-check_0000jpg.log')  # 使用os.path.join()函数将日志路径和日志文件名连接起来，形成完整的日志文件路径
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(message)s')


# 搜索指定目录下的文件夹
def search_folders(directory):
    for root, dirs, files in os.walk(directory):
        for folder in dirs:
            if folder.endswith('_pics'):
                folder_path = os.path.join(root, folder)
                check_files(folder_path)

# 检查文件夹中的文件
def check_files(folder_path):
    files = os.listdir(folder_path)
    if len(files) == 1 and files[0] == '[0000].jpg':
        folder_size = get_folder_size(folder_path)
        formatted_size = format_size(folder_size)
        log_entry = f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}, Empty folder name with the suffix '_pics': {folder_path},  folder size: {formatted_size}"
        print(log_entry)
        logging.info(log_entry)
        if folder_size > 20 * 1024:
            confirm = input("The folder size exceeds 20KB. Do you want to delete it?(Y/N): ")
            if confirm.lower() == 'n':
                return
        delete_folder(folder_path)

# 删除文件夹及其中的文件
def delete_folder(folder_path):
    try:
        os.remove(os.path.join(folder_path, '[0000].jpg'))
        os.rmdir(folder_path)
        print(f"Deleted folder:{folder_path}")
    except Exception as e:
        print(f"Deleted folder:{folder_path}, Error message:{str(e)}")

# 获取文件夹大小
def get_folder_size(folder_path):
    total_size = 0
    for path, dirs, files in os.walk(folder_path):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.path.getsize(fp)
    return total_size

# 格式化文件夹大小
def format_size(size):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    formatted_size = size

    while formatted_size >= 1024 and unit_index < len(units) - 1:
        formatted_size /= 1024
        unit_index += 1

    formatted_size = round(formatted_size, 2)

    return f"{formatted_size} {units[unit_index]}"

def send_dingtalk_message(webhook_url, secret, title, text):
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    # 调用示例
    webhook_url = webhook_url + '&timestamp={timestamp}&sign={sign}'.format(
        timestamp=timestamp, sign=sign)
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title":title,
            "text": text
        },
    }

    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        print("钉钉消息发送成功")
    except requests.exceptions.RequestException as e:
        print("钉钉消息发送失败:", str(e))


# 调用入口函数
if __name__ == '__main__':
    
    # 将操作日志消息追加到操作日志文件
    with open(os.path.join(logpath,logLifecycleLog),'a+',encoding='utf-8') as file:
        file.write(f"{logtime} ---- 脚本操作：开始运行----check_0000jpg.py 清理空略缩图文件夹\n")
    
    if len(sys.argv) < 2:
        print("Please provide a folder name as a parameter")
        sys.exit(1)
    directory = sys.argv[1]

    # 执行搜索
    search_folders(directory)
    
    # 将操作日志消息追加到操作日志文件
    with open(os.path.join(logpath,logLifecycleLog),'a+',encoding='utf-8') as file:
        file.write(f"{logtime} ---- 脚本操作：运行结束----check_0000jpg.py 清理空略缩图文件夹\n")

    # 发送钉钉通知
    secret = 'SEC6bbb58d2e08ca3cdb9ce79883cc9baa6cbcb01f5cf6bebfb1a38fca7090e903c'
    webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=f3d9971f909edf26843ae6cd0a16aa7892360dcc5c7c146073ff4898f0607db5'
    title = "清理空略缩图文件夹任务已经完成！"
    text = f"清理空略缩图文件夹任务已经完成！\n"
    send_dingtalk_message(webhook_url, secret, title, text)
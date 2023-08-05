import os
import time
import logging
import shutil

# 设置日志文件名和格式
log_filename = 'log-check_0000jpg.txt'
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
    if len(files) == 1 and files[0] == '【0000】.jpg':
        folder_size = get_folder_size(folder_path)
        formatted_size = format_size(folder_size)
        log_entry = f"带有_pics后缀的空文件夹名称: {folder_path}，时间: {time.strftime('%Y-%m-%d %H:%M:%S')}，文件夹大小: {formatted_size}"
        print(log_entry)
        logging.info(log_entry)
        if folder_size > 20 * 1024:
            confirm = input("文件夹大小超过20KB，是否删除？(Y/N): ")
            if confirm.lower() == 'n':
                return
        delete_folder(folder_path)

# 删除文件夹及其中的文件
def delete_folder(folder_path):
    try:
        os.remove(os.path.join(folder_path, '【0000】.jpg'))
        os.rmdir(folder_path)
        print(f"已删除文件夹: {folder_path}")
    except Exception as e:
        print(f"删除文件夹时出错: {folder_path}, 错误信息: {str(e)}")

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

# 入口函数
def main():
    # 填写您需要的参数
    directory = './sync'

    # 执行搜索
    search_folders(directory)

# 调用入口函数
if __name__ == '__main__':
    main()

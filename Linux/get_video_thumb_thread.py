#!/usr/bin/env python 3.10
# -*- coding: UTF-8 -*-
# @date: 2023/8/28 0:03
# @name: get_video_thumb_thread.py
# @author：Ryen
# @webside：www.prlrr.com
# @software: PyCharm
import os

def find_mp4_files(rootpath):
    mp4_files = []

    for root, dirs, files in os.walk(rootpath):
        for file in files:
            if file.endswith('.mp4'):
                mp4_path = os.path.join(root, file)
                pics_folder = os.path.join(root, file[:-4] + '_pics')

                if os.path.isdir(pics_folder):
                    folder_size = os.path.getsize(pics_folder)

                    if folder_size <= 20 * 1024:  # 将20 KB转换为字节
                        mp4_files.append(mp4_path)

    return mp4_files

# 调用示例
rootpath = '/path/to/folder'
mp4_files = find_mp4_files(rootpath)

for file in mp4_files:
    print(file)

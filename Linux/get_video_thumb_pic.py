# !/usr/bin/env python
# -*- coding:utf-8 -*-

# 作者：AMII
# 时间：2022-03-08
# 更新内容：改用OpenCV提高速度，优化遍历方式减轻硬盘压力
# 脚本功能：为视频创建截图，默认间隔2分钟以下：2s，10分钟：5s，30分钟：15s，1小时：30s，其他：60s

import sys
import time
import requests
import json
import os
import re
import cv2
import datetime
from datetime import timedelta
import numpy as np
import hmac
import hashlib
import base64
import urllib.parse
# from PIL import Image, ImageDraw, ImageFont

localpath = os.path.split(os.path.abspath(__file__))[0]                                     # 当前位置
logname = 'log-get_video_pic_log.json'                                                      # 具体的脚本运行日志文件
logpath = os.path.join(localpath, 'log')  # 日志位置
now = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))                # 脚本运行日志时间戳

logtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")                             # 脚本操作日志时间戳
logLifecycleLog = "log-RunOperation.log"                                                    # 脚本的生命周期日志
index_count = 0 # 已处理的视频数量
total_processing_time = 0  # 总处理时间

# 主控制
def thumb_start(path, count_f_l):
    file_list, path_list = get_list(path)                                                   # 获取文件、目录列表

    global index_count, total_processing_time  # 声明使用全局变量
    for f in file_list:
        start = time.time()  # 记录当前视频开始处理的时间
        # 循环文件列表
        index_count += 1                                                                      # 当前执行的文件索引数
        try:

            if get_pic(path, f, count_f_l, start):                                      # 截取截图，如已存在截图则跳过

                end = time.time()  # 记录当前视频处理完成的时间
                processing_time = end - start  # 当前视频的处理时间
                total_processing_time += processing_time
                # 计算平均处理时间
                average_processing_time = total_processing_time / index_count
                # 计算预估剩余时间
                remaining_videos = count_f_l - index_count
                estimated_remaining_time = average_processing_time * remaining_videos
                # 格式化时间为时:分:秒的形式
                # processing_time_formatted = str(timedelta(seconds=processing_time))
                # average_processing_time_formatted = str(timedelta(seconds=average_processing_time))
                estimated_remaining_time_formatted = str(timedelta(seconds=estimated_remaining_time))

                save_log(
                    '[' + str(index_count) + '/' + str(count_f_l) + ']："' + os.path.join(path, f) + '", "跳过, 预估剩余时间:' + estimated_remaining_time_formatted +'秒\n\n')
        except:
            end = time.time()  # 记录当前视频处理完成的时间
            processing_time = end - start  # 当前视频的处理时间
            total_processing_time += processing_time
            # 计算平均处理时间
            average_processing_time = total_processing_time / index_count
            # 计算预估剩余时间
            remaining_videos = count_f_l - index_count
            estimated_remaining_time = average_processing_time * remaining_videos
            # 格式化时间为时:分:秒的形式
            # processing_time_formatted = str(timedelta(seconds=processing_time))
            # average_processing_time_formatted = str(timedelta(seconds=average_processing_time))
            estimated_remaining_time_formatted = str(timedelta(seconds=estimated_remaining_time))

            save_log('[' + str(index_count) + '/' + str(count_f_l) + ']：' + '[----Error----],' + os.path.join(path,
                                                                                                                f) + ', 预估剩余时间:' + estimated_remaining_time_formatted +'秒\n\n')
            print('[' + str(index_count) + '/' + str(count_f_l) + ']：' + '[Error File]',
                  os.path.join(path, f).encode('utf-8'))
    if len(path_list):                                                                      # 如本级有目录则循环递归调用
        for p in path_list:
            thumb_start(p, count_f_l)


# 遍历文件夹内视频文件计数
def count_video_files(path):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mkv', '.mov')):
                count += 1
    return count


# 获取时长时间戳
def get_video_duration(cap):
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 获取视频的总帧数
    fps = cap.get(cv2.CAP_PROP_FPS)                                                         # 获取视频的帧率

    duration = frame_count / fps                                                            # 计算视频的时长（以秒为单位）

    # 将时长转换为时间戳形式
    minutes = int(duration / 60)
    seconds = int(duration % 60)
    milliseconds = int((duration % 1) * 1000)

    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


# 获取视频截图并保存
def get_pic(path, file, count_file_list, start):
    global index_count, total_processing_time  # 声明使用全局变量
    # 视频基础数据获取
    nfile = os.path.splitext(file)[0]                                                       # 视频文件名
    pfile = os.path.join(path, file)                                                        # 视频路径+文件名
    path_pic = os.path.join(path, nfile + '_pics')                                          # 截图存放路径
    temp_pic = os.path.join(path_pic, '[0000].jpg')                                         # 临时文件
    if not os.path.exists(path_pic):                                                        # pics文件夹检测
        os.makedirs(path_pic)
    if (os.path.exists(temp_pic)): return True                                              # 已存在临时文件
    with open(temp_pic, 'w') as f:
        pass                                                                                # 创建临时文件
    cap = cv2.VideoCapture(pfile)                                                           # 读取视频文件
    frames, fps, durations, tim, width, height = get_info(cap)                              # 获取视频信息
    num, jg = get_row(durations)                                                            # 获取截图数量、时间间隔
    if frames == 0: return False                                                            # 帧数为零，返回True
    if (durations < 5): return False                                                        # 时间过短，返回True
    video_duration = get_video_duration(cap)                                                # 获取视频时长
    # print("视频时长:", duration)
    # save_log('"' + os.path.join(path,file) + '",' + str(frames) + ',' + str(fps) + ',' + str(durations) + ',"' + tim + '",' + str(num))
    save_log('[' + str(index_count) + '/' + str(count_file_list) + ']："' + os.path.join(path, file) + '",' + ', FPS：' + str(
        fps) + ', 时长：' + str(video_duration) + '"')

    chk = 2
    print(nfile + '\n[', end="")
    for i in range(num):
        loop_num = 0
        if i and i % 500 == 0:
            save_log('\n')
        name_t = str(datetime.timedelta(seconds=((i + 1) * jg))).replace(":", "-")
        name_t = '0' + name_t if len(name_t) == 7 else name_t  # 文件名时间
        # tmp_name = 'temp__' + str(i) + '.jpg'                                             # 临时文件名
        file_name = '[' + '{:0>4d}'.format(i + 1) + ']' + name_t + '.jpg'                   # 截图文件名
        path_file = os.path.join(path_pic, file_name)                                       # 截图路径加文件名
        # path_tmp = os.path.join(localpath,tmp_name)                                       # 截图路径加临时文件名
        time_fps = int(((i + 1) * jg * fps) // 1)                                           # 时间帧数
        if os.path.exists(path_file):                                                       # 截图存在跳过
            save_log(',跳' + str(i + 1))
            continue
        cap.set(cv2.CAP_PROP_POS_FRAMES, time_fps)                                          # 设置截取帧数
        ret, frame = cap.read()                                                             # 读取帧
        if (time_fps / frames) > 0.5:                                                       # 设定回退or前进固定帧
            up_or_down = -round(fps)                                                        # 回退
        else:
            up_or_down = round(fps)                                                         # 前进
        while not ret:                                                                      # 截图出错回退or前进指定帧
            if loop_num > (jg * 2):                                                         # 回退or前进超过2个间隔退出
                save_log('[----Error----],' + os.path.join(path, file) + '\n')
                print('[Error File]', os.path.join(path, file))
                return True
            time_fps += up_or_down
            save_log('[' + str(int(time_fps)) + ']')
            print('.', end="")
            cap.set(cv2.CAP_PROP_POS_FRAMES, time_fps)
            ret, frame = cap.read()
            loop_num += 1
        if dwidth:
            dheight = int(((dwidth / width) * height) // 1)
            frame = cv2.resize(frame, (dwidth, dheight))                            # 调整长宽
        if rotate:
            frame = rotate_bound(frame, rotate)                                           # 旋转检测
        cv2.imencode('.jpg', frame)[1].tofile(path_file)  # 保存截图
        # cv2.imwrite(path_tmp,frame)                                                     # 保存截图
        # if os.path.exists(path_tmp): shutil.move(path_tmp,path_file)                    # 替换文件名并移动
        # save_log(',' + str(i+1))                                                        # 保存略缩图生成的数量到日志
        if (((i + 1) / num) * 100 > chk):                                                 # 进度条模块
            sn = int((((i + 1) / num) * 100 - chk) / 2)
            for x in range(sn):
                print('■', end="")
            chk += 2 * sn
    end = time.time()  # 记录当前视频处理完成的时间
    processing_time = end - start  # 当前视频的处理时间
    total_processing_time += processing_time
    # 计算平均处理时间
    average_processing_time = total_processing_time / index_count
    # 计算预估剩余时间
    remaining_videos = count_file_list - index_count
    estimated_remaining_time = average_processing_time * remaining_videos
    # 格式化时间为时:分:秒的形式
    #processing_time_formatted = str(timedelta(seconds=processing_time))
    #average_processing_time_formatted = str(timedelta(seconds=average_processing_time))
    estimated_remaining_time_formatted = str(timedelta(seconds=estimated_remaining_time))

    save_log(',Done, 预估剩余时间:' + estimated_remaining_time_formatted +'\n')
    print('] Done~')


# 获取指定类型文件和文件夹列表
def get_list(path):
    file_list = []
    path_list = []
    rule = r"\.(avi|wmv|wmp|wm|asf|mpg|mpeg|mpe|m1v|m2v|mpv2|mp2v|ts|tp|tpr|trp|vob|ogm|ogv|mp4|m4v|m4p|m4b|3gp|3gpp|3g2|3gp2|mkv|rm|ram|rmvb|rpm|flv|swf|mov|qt|nsv|dpg|m2ts|m2t|mts|dvr-ms|k3g|skm|evo|nsr|amv|divx|webm|wtv|f4v|mxf)$"
    lists = os.listdir(path)
    for p in lists:
        if re.search("\$RECYCLE\.BIN|System Volume Information|Recovery", p): continue  # 排除windows系统文件夹
        if os.path.isdir(os.path.join(path, p)):
            path_list.append(os.path.join(path, p))  # 追加文件夹
            continue
        if re.search(rule, p, re.IGNORECASE):
            file_list.append(p)  # 追加文件
    return (file_list, path_list)


# 获取视频基本信息
def get_info(cap):
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))                 # 总帧数
    fps = round(cap.get(cv2.CAP_PROP_FPS), 4)                       # 帧率
    durations = int(frames / fps)  # 时间
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))                  # 宽度
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))                # 高度
    tim = str(datetime.timedelta(seconds=durations))                # 格式化时间
    tim = '0' + tim if len(tim) == 7 else tim                       # 格式化时间前补零
    return (frames, fps, durations, tim, width, height)


# OpenCV旋转图片
def rotate_bound(image, angle):
    (h, w) = image.shape[:2]                                        # 获取图片长宽
    (cX, cY) = (w // 2, h // 2)                                     # 设置旋转中心坐标
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)  # 设置M矩阵
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    return cv2.warpAffine(image, M, (nW, nH))


# 设定并返回图片个数、间隔
def get_row(sec):
    jg, num = (0, 0)
    if (sec <= 121):
        jg = s2  # 2分钟内间隔
    elif (sec <= 601):
        jg = s10  # 10分钟内间隔
    elif (sec <= 1801):
        jg = s30  # 30分钟内间隔
    elif (sec <= 3601):
        jg = s60  # 60分钟内间隔
    else:
        jg = sot  # 大于60分钟间隔
    num = sec // jg
    return (num, jg)


# 保存日志
def save_log(mess):
    with open(os.path.join(logpath, logname), 'a+', encoding='utf-8') as f:
        f.write(mess)


class wechatbot:
    '''
    企业微信机器人
    '''

    def __init__(self, corpid, agentid, secret):
        '''
        corpid: 企业ID
        agentid: 机器人的AgentId
        secret: 机器人的Secret
        '''
        self.corpid = corpid
        self.agentid = agentid
        self.secret = secret

    def get_access_token(self):
        get_token_api = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={self.secret}'
        r = requests.get(get_token_api).json()
        print(r)
        if r["errcode"] == 0:
            self.access_token = r["access_token"]

    def upload_file(self, file_type, file_path, file_name):
        upload_api = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={self.access_token}&type={file_type}'
        files = {'media': (file_name, open(file_path, "rb"), '', {})}

        # headers = {'Content-Type': 'multipart/form-data'}
        r = requests.post(upload_api, files=files).json()
        print(r)
        if r["errcode"] == 0:
            return r["media_id"]

    def send(self, msgtype, content):
        send_message_api = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}'

        message = {
            "agentid": self.agentid,
            "touser": "@all",
            "msgtype": msgtype,
            msgtype: content
        }

        headers = {'Content-Type': 'application/json'}
        r = requests.post(send_message_api, data=json.dumps(message),
                          headers=headers).json()
        print(r)
        return r["errcode"]


def wxworks_main(corpid, agentid, secret):
    '''
            corpid: 企业ID
            agentid: 机器人的AgentId
            secret: 机器人的Secret
            '''
    corpid = corpid
    agentid = agentid
    secret = secret
    bot = wechatbot(corpid, agentid, secret)
    bot.get_access_token()
    news = {
        "articles": [
            {
                "title": title,
                "description": syntax,
                # "url": "https://work.weixin.qq.com/wework_admin/frame#profile/wxPlugin",
                "picurl": "https://www.prlrr.com/pic/wxwork/python.png"
            }
        ]
    }
    bot.send("news", news)

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

if __name__ == '__main__':

    # 将操作日志消息追加到操作日志文件
    if not os.path.exists(logpath):
        os.makedirs(logpath)
    with open(os.path.join(logpath, logLifecycleLog), 'a+', encoding='utf-8') as file:
        file.write(f"{logtime} ---- 脚本操作：开始运行----get_video_thumb_pic.py 生成略缩图\n")

    # 运行命令：python get_video_thumb_pic.py sync 0
    # sync：文件夹名
    # 0：不改变默认参数   1：改变默认参数
    # 检查是否提供了足够的参数
    if len(sys.argv) < 3:
        print("请提供文件夹名作为参数")
        sys.exit(1)
    folder_name = sys.argv[1]

    rootpath = folder_name
    if sys.argv[2] == 1:
        dwidth = int(input('截图宽度：') or 0)
        rotate = int(input('是否逆时针旋转截图（输入度数）：') or 0)
        print('默认间隔2分钟以下：2s，10分钟：5s，30分钟：15s，1小时：30s，其他：45s[输入数字修改，回车跳过]')
        s2 = int(input('2分钟内间隔：') or 2)
        s10 = int(input('10分钟内间隔：') or 5)
        s30 = int(input('30分钟内间隔：') or 15)
        s60 = int(input('60分钟内间隔：') or 30)
        sot = int(input('大于60分钟间隔：') or 45)
    else:
        # dwidth, rotate, s2, s10, s30, s60, s90, s120, s180, s60, s300 = (0, 0, 5, 20, 40, 90, 120, 240, 300, 480, 600)
        dwidth, rotate, s2, s10, s30, s60, sot = (0, 0, 2, 5, 15, 30, 45)
    # print('[■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■] 进度条')
    # stime = time.time()
    save_log(
        '\t' + '===========================================' + '     ' + now + '     ' + rootpath + '     ' + '===========================================' + '\n')

    count_file_list = count_video_files(rootpath)  # 视频文件总数

    start_time = time.time()  # 记录开始时间
    thumb_start(rootpath, count_file_list) # 开始脚本

    end_time = time.time()  # 记录结束时间
    total_time = end_time - start_time  # 总耗时
    total_time_formatted = str(timedelta(seconds=total_time))

    print(f"所有视频处理完成，耗时 {total_time_formatted} ")

    # etime = time.time()
    # print(etime - stime)
    # save_log(str((etime - stime)) + '\n')
    save_log(
        '\t' + '===========================================' + '     ' + '运行结束-耗时 ' + total_time_formatted + '秒 ===========================================' + '\n')
    # 将操作日志消息追加到操作日志文件
    with open(os.path.join(logpath, logLifecycleLog), 'a+', encoding='utf-8') as file:
        file.write(f"{logtime} ---- 脚本操作：运行结束----get_video_thumb_pic.py 生成略缩图----耗时 {total_time_formatted} 秒\n")

    title = '视频略缩图已经生成完成！'
    # 发送企业微信通知
    try:
        corpid = 'ww377bffbd7ed5dd33'
        title = title
        syntax = "" + '共计耗时：' + total_time_formatted + '\n'
        agentid = 1000002
        secret = 'uuqh1Ar95GByhyN52S667uxicVpH2KkLc5FvONRgPsw'
        wxworks_main(corpid, agentid, secret)
        #print('=' * 20)
        print('企业微信通知已发送！')
        #print('=' * 20)
    except:
        #print('=' * 20)
        print('企业微信通知发送失败！')
        #print('=' * 20)


    # 发送钉钉通知
    secret = 'SEC6bbb58d2e08ca3cdb9ce79883cc9baa6cbcb01f5cf6bebfb1a38fca7090e903c'
    webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=f3d9971f909edf26843ae6cd0a16aa7892360dcc5c7c146073ff4898f0607db5'
    title = "视频略缩图已经生成完成！"
    text = f"# 视频略缩图已经生成完成！\n#### 文件夹：{rootpath} \n#### 共计耗时： {total_time_formatted} \n"
    send_dingtalk_message(webhook_url, secret, title, text)
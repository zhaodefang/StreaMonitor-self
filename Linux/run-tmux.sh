#!/bin/bash

# 必须固定这个文件夹
folder="/root/StreaMonitor"
Dfolder="/mnt/mylv/StreaMonitor/downloads"
Sfolder="/mnt/mylv/StreaMonitor/sync"

Dcommand = python3 $folder/Downloader.py

# 输出选项
echo "请选择一个选项:"
echo ""
# 由于暂停或开始全部会识别不到streamers流，采用tmux终端
echo "1. StreaMonitor-开启脚本"
# 控制参数可以直接改config.json，直接运行python
echo "2. StreaMonitor-添加主播"
echo "3. StreaMonitor-删除主播"
echo "4. StreaMonitor-开始特定主播"
echo "5. StreaMonitor-暂停特定主播"
# 流问题只能进入运行的tmux会话中去执行命令
echo "6. StreaMonitor-全部暂停"
echo "7. StreaMonitor-全部开始"
# 控制参数可以直接获取config.json，直接运行python
echo "8. StreaMonitor-录制状态"
# 删除tmux会话
echo "9. StreaMonitor-退出脚本"
echo ""
echo "10. Rclone-Config配置"
echo "11. Rclone-GUI图像界面"
echo ""
# 无交互，使用screen后台任务
echo "12. Downloads-同步文件夹"
echo "13. Downloads-仅删除视频文件"
echo "14. Downloads-生成略缩图"
echo ""
# 无交互，直接运行或使用screen后台任务
echo "15. Sync-移动文件夹"
echo "16. Sync-同步文件夹"
echo "17. Sync-仅删除视频文件"
echo "18. Sync-生成略缩图"
echo "19. Sync-清理文件夹"
echo ""
echo "20. Cancel-Downloads-取消同步任务"
echo "21. Cancel-Sync-取消同步任务"

echo "0. 退出脚本"
echo ""

# 读取用户输入
read -p "请输入选项数字: " option

# 根据选项执行相应的命令操作
case $option in

	# 由于暂停或开始全部会识别不到streamers流，采用tmux终端
	1)
		# 执行StreaMonitor-开启脚本的命令
		echo "执行StreaMonitor-开启脚本的命令"
		# 检查会话是否存在
		if ! tmux has-session -t StreaMonitor-Downloader >/dev/null 2>&1; then
			# 如果会话不存在，则创建会话并执行命令
			echo "会话不存在，创建新会话"
			echo "命令为python3 /root/StreaMonitor/Downloader.py"
			tmux new-session -d -s StreaMonitor-Downloader
			tmux send-keys -t StreaMonitor-Downloader:0 "python3 /root/StreaMonitor/Downloader.py" Enter
		else
			# 如果会话已存在，则发送命令到会话中的窗格
			echo "会话存在，请手动暂停录制、删除会话后，重新启动"
			exit 0
		fi
		;;
		
	# 控制参数可以直接改config.json，直接运行python
	2)
		# 执行StreaMonitor-添加主播的命令
		# 询问主播名
		read -p "请输入添加的主播名: " anchor_name

		# 循环直到选择有效选项
		while true; do
			# 提供选项并读取选择
			echo "请选择直播源:"
			echo "1. sc"
			echo "2. cb"
			read -p "请输入选项: " option

			case $option in
				1)
					# 执行命令：python3 $folder/Controller.py 添加的主播名 sc
					python3 $folder/Controller.py add "$anchor_name" sc
					break  # 选择有效，跳出循环
					;;
				2)
					# 执行命令：python3 $folder/Controller.py 添加的主播名 cb
					python3 $folder/Controller.py add "$anchor_name" cb
					break  # 选择有效，跳出循环
					;;
				*)
					echo "无效的选项，请重新选择"
					;;
			esac
		done
		;;
	3)
		# 执行StreaMonitor-删除主播的命令
		# 询问需要删除的主播名
		read -p "请输入需要删除的主播名: " delete_anchor_name

		# 执行命令：python3 $folder/Controller.py remove 需要删除的主播名
		python3 $folder/Controller.py remove "$delete_anchor_name"
		;;
	4)
		# 执行StreaMonitor-开始特定主播的命令
		# 询问需要开启录制的主播名
		read -p "请输入需要开启录制的主播名: " start_recording_anchor_name

		# 执行命令：python3 $folder/Controller.py start 需要开启录制的主播名
		python3 $folder/Controller.py start "$start_recording_anchor_name"
		;;
	5)
		# 执行StreaMonitor-暂停特定主播的命令
		# 询问需要暂停录制的主播名
		read -p "请输入需要暂停录制的主播名: " pause_recording_anchor_name

		# 执行命令：python3 $folder/Controller.py pause 需要暂停录制的主播名
		python3 $folder/Controller.py pause "$pause_recording_anchor_name"
		;;
	# 流问题只能进入运行的tmux会话中去执行命令
	6)
		# 执行StreaMonitor-全部暂停的命令
		echo "执行StreaMonitor-全部暂停的命令"
		# 执行命令：
		tmux send-keys -t StreaMonitor-Downloader:0 "stop *" Enter
		;;
	7)
		# 执行StreaMonitor-全部开始的命令
		echo "执行StreaMonitor-全部开始的命令"
		# 执行命令：
		tmux send-keys -t StreaMonitor-Downloader:0 "start *" Enter
		;;
	# 控制参数可以直接获取config.json，直接运行python
	8)
		# 执行StreaMonitor-录制状态的命令
		echo "执行StreaMonitor-录制状态的命令"
		# 执行命令：python3 $folder/Controller.py status
		python3 $folder/Controller.py status
		;;
	# 删除tmux会话
	9)
		# 执行StreaMonitor-退出脚本的命令
		echo "执行StreaMonitor-退出脚本的命令"
		# 执行命令：删除StreaMonitor-Downloader会话

		# 检查会话是否存在
		if ! tmux has-session -t StreaMonitor-Downloader >/dev/null 2>&1; then
			# 如果会话不存在，则创建会话并执行命令
			echo "会话不存在，执行失败"
			exit 0
		else
			# 如果会话已存在，则发送命令到会话中的窗格
			echo "成功删除StreaMonitor-Downloader会话"
			tmux kill-session -t StreaMonitor-Downloader
		fi

		
		
		;;
	10)
		# 执行Rclone-Config配置的命令
		echo "执行Rclone-Config配置的命令"
		rclone config
		;;
	11)
		# 执行Rclone-GUI图像界面的命令
		echo "执行Rclone-GUI图像界面的命令"
		echo "为了方便结束进程、再加上使用频率低，不启用后台运行"
		rclone rcd --rc-web-gui --rc-addr :857 --rc-user=admin --rc-pass=1594959462
		echo "Rclone-GUI图像界面参数："
		echo "端口：857"
		echo "账号：admin"
		echo "密码：1594959462"
		;;
	# 无交互，使用screen后台任务
	12)
		# 执行Downloads-同步文件夹的命令
		echo "执行Downloads-同步文件夹的命令"
		# 询问 Rclone 远程配置名称
		read -p "请输入 Rclone 远程配置名称（默认为 scsg）: " rclone_remote_name
		rclone_remote_name=${rclone_remote_name:-scsg}  # 如果用户没有输入，则使用默认值 scsg

		# 询问 Rclone 同步线程数
		read -p "请输入 Rclone 同步线程数（默认为 10）: " rclone_thread_count
		rclone_thread_count=${rclone_thread_count:-10}  # 如果用户没有输入，则使用默认值 10

		# 使用 screen 运行命令：rclone copy "./downloads" Rclone远程配置名称:SC --progress --transfers Rclone线程数，并命名为 "Downloads-Sync"
		screen -dmS Downloads-Sync rclone copy $folder/downloads "$rclone_remote_name:SC" --progress --transfers "$rclone_thread_count"
		;;
	13)
		# 执行Downloads-仅删除视频文件的命令
		echo "执行Downloads-仅删除视频文件的命令"
		# 删除 ./downloads 文件夹中的所有视频文件（包括子文件夹），保留其他文件
		find $folder/downloads -type f \( -name "*.mp4" -o -name "*.avi" -o -name "*.mkv" \) -delete
		;;
	14)
		# 执行Downloads-生成略缩图的命令
		echo "执行Downloads-生成略缩图的命令"
		screen -dmS Downloads-thumb python $folder/get_video_thumb_pic.py downloads 0
		;;
	# 无交互，直接运行或使用screen后台任务
	15)
		# 执行Sync-移动文件夹的命令
		# 将 downloads 文件夹重命名为 sync
		mv $folder/downloads $folder/sync

		# 创建一个新的 downloads 文件夹
		mkdir $folder/downloads
		;;
	16)
		# 执行Sync-同步文件夹的命令
		echo "执行Sync-同步文件夹的命令"
		# 询问 Rclone 远程配置名称
		read -p "请输入 Rclone 远程配置名称（默认为 scsg）: " rclone_remote_name
		rclone_remote_name=${rclone_remote_name:-scsg}  # 如果用户没有输入，则使用默认值 scsg

		# 询问 Rclone 同步线程数
		read -p "请输入 Rclone 同步线程数（默认为 10）: " rclone_thread_count
		rclone_thread_count=${rclone_thread_count:-10}  # 如果用户没有输入，则使用默认值 10

		# 使用 screen 运行命令：rclone copy "./sync" Rclone远程配置名称:SC --progress --transfers Rclone线程数，并命名为 "sync-Sync"
		screen -dmS sync-Sync rclone copy $folder/sync "$rclone_remote_name:SC" --progress --transfers "$rclone_thread_count"
		;;
	17)
		# 执行Sync-仅删除视频文件的命令
		echo "执行Sync-仅删除视频文件的命令"
		find $folder/sync -type f \( -name "*.mp4" -o -name "*.avi" -o -name "*.mkv" \) -delete
		;;
	18)
		# 执行Sync-生成略缩图的命令
		echo "执行Sync-生成略缩图的命令"
		screen -dmS Sync-thumb python $folder/get_video_thumb_pic.py sync 0
		;;		
	19)
		# 执行Sync-清理文件夹的命令
		echo "执行Sync-清理文件夹的命令"
		# 删除 sync 文件夹
		rm -rf $folder/sync
		;;
	20)
		# 执行Cancel-Downloads-取消同步视频任务的命令
		echo "执行Cancel-Downloads-取消同步视频任务的命令"
		# 获取指定任务名的会话 ID
		session_id=$(screen -ls | awk '/\.Downloads-Sync/ {print $1}')

		# 检查是否找到了会话 ID
		if [ -n "$session_id" ]; then
		  # 终止指定的 screen 会话
		  screen -S "$session_id" -X quit
		  echo "已删除会话：$session_id"
		else
		  echo "未找到具有指定任务名的会话"
		fi
		;;
	21)
		# 执行Cancel-Sync-取消同步视频任务的命令
		echo "执行Cancel-Sync-取消同步视频任务的命令"
		# 获取指定任务名的会话 ID
		session_id=$(screen -ls | awk '/\.sync-Sync/ {print $1}')

		# 检查是否找到了会话 ID
		if [ -n "$session_id" ]; then
		  # 终止指定的 screen 会话
		  screen -S "$session_id" -X quit
		  echo "已删除会话：$session_id"
		else
		  echo "未找到具有指定任务名的会话"
		fi
		;;
	0)
		# 退出脚本
		exit 0
		;;
	*)
		echo "无效的选项"
		;;
esac

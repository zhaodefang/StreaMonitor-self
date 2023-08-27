#!/bin/bash

# 必须固定这个文件夹
# python程序所在文件夹
MainFolder="/root/StreaMonitor"
# 挂载硬盘目录，也可为下载文件夹目录
MountFolder="/768"
# 具体的下载目录
DownloadFolder="/768/downloads"
# 一个中转获取略缩图和同步OD的文件夹
SyncFolder="/768/sync"

# 获取当前时间
time=$(date +"%Y-%m-%d %H:%M:%S")
logfile="$MainFolder/log/log-RunOperation.log"

show_menu() {
	# 输出选项
	echo "请选择一个选项:"
	echo ""
	# Docker操作
	echo "1. Docker-钩子失效"
	echo "2. Docker-暂停容器"
	echo "3. Docker-删除容器"

	# 由于暂停或开始全部会识别不到streamers流，采用tmux终端
	echo "4. StreaMonitor-开启容器"
	# 控制参数可以直接改config.json，直接运行python
	echo "5. StreaMonitor-添加主播"
	echo "6. StreaMonitor-删除主播"
	echo "7. StreaMonitor-开始特定主播"
	echo "8. StreaMonitor-暂停特定主播"
	# 流问题只能进入运行的tmux会话中去执行命令
	echo "9. StreaMonitor-全部暂停"
	echo "10. StreaMonitor-全部开始"
	# 控制参数可以直接获取config.json，直接运行python
	echo "11. StreaMonitor-录制状态"
	# 删除tmux会话
	echo "12. StreaMonitor-退出脚本"
	echo ""

	# Rclone
	echo "13. Rclone-Config配置"
	echo "14. Rclone-GUI图像界面"
	echo ""

	# 无交互，使用screen后台任务
	echo "15. Downloads-同步文件夹"
	echo "16. Downloads-仅删除视频文件"
	echo "17. Downloads-生成略缩图"
	echo ""

	# 无交互，直接运行或使用screen后台任务
	echo "18. Sync-移动文件夹"
	echo "19. Sync-同步文件夹"
	echo "20. Sync-仅删除视频文件"
	echo "21. Sync-生成略缩图"
	echo "22. Sync-清理文件夹"
	echo ""
	echo "23. Cancel-Downloads-取消同步任务"
	echo "24. Cancel-Sync-取消同步任务"
	echo ""
	echo "25. Clear-Downloads-删除空白略缩图"
	echo "26. Clear-Sync-删除空白略缩图"
	echo ""
	echo "27. Query-Size-查询文件夹大小"
    echo ""
	echo "0. 退出脚本"
	echo ""

	# 读取用户输入
	read -p "请输入选项数字: " option

	# 根据选项执行相应的命令操作
	case $option in

		# Docker操作
		# 文件夹：/root/StreaMonitor 大写S
		# 容器名：streamonitor  小写s
		# 进入容器：docker exec -it streamonitor /bin/bash
		# 单执行：docker exec streamonitor python Controller.py add ss sc

		1)
			# 执行Docker-运行钩子的命令
			echo "执行 Docker-事件监听和记录日志"
			start_event_logger() {
				while read -r event
				do
					time=$(date +"%Y-%m-%d %H:%M:%S")
					container_name=$(echo "$event" | awk '{print $2}')

					case $event in
						*attach*)
							echo "$time ---- 容器操作：$container_name Container attached" >> "$logfile"
							;;
						*commit*)
							echo "$time ---- 容器操作：$container_name New image committed" >> "$logfile"
							;;
						*create*)
							echo "$time ---- 容器操作：$container_name Container created" >> "$logfile"
							;;
						*die*)
							echo "$time ---- 容器操作：$container_name Container died" >> "$logfile"
							;;
						*kill*)
							echo "$time ---- 容器操作：$container_name Container killed" >> "$logfile"
							;;
						*oom*)
							echo "$time ---- 容器操作：$container_name Out of memory" >> "$logfile"
							;;
						*pause*)
							echo "$time ---- 容器操作：$container_name Container paused" >> "$logfile"
							;;
						*start*)
							echo "$time ---- 容器操作：$container_name Container started" >> "$logfile"
							;;
						*restart*)
							echo "$time ---- 容器操作：$container_name Container restarted" >> "$logfile"
							;;
						*stop*)
							echo "$time ---- 容器操作：$container_name Container stopped" >> "$logfile"
							;;
						*unpause*)
							echo "$time ---- 容器操作：$container_name Container unpaused" >> "$logfile"
							;;
						*update*)
							echo "$time ---- 容器操作：$container_name Container updated" >> "$logfile"
							;;
					esac
				done < <(docker events --filter 'event=attach' --filter 'event=commit' --filter 'event=create' --filter 'event=die' --filter 'event=kill' --filter 'event=oom' --filter 'event=pause' --filter 'event=start' --filter 'event=restart' --filter 'event=stop' --filter 'event=unpause' --filter 'event=update' --format '{{.Time}} {{.ID}}') &
			}

			start_event_logger
			echo "$time ---- 用户操作：执行 Docker-运行钩子的命令" >> "$logfile"
			;;
		2)
			# 执行Docker-暂停容器的命令
			docker stop streamonitor
			echo "$time ---- 用户操作：执行Docker-暂停容器的命令" >> $logfile
			;;
		3)
			# 执行Docker-删除容器的命令
			docker stop streamonitor
			docker rm streamonitor
			echo "$time ---- 用户操作：执行Docker-删除容器的命令" >> $logfile
			;;
			
		# 由于暂停或开始全部会识别不到streamers流，采用tmux终端
		# 由于暂停或开始全部会识别不到streamers流，docker无解
		4)

			# 执行StreaMonitor-开启脚本容器的命令
			echo "执行StreaMonitor-开启脚本容器的命令"
			
			# 检查会话是否存在
			if [[ "$(docker ps -q -f name=streamonitor)" ]]; then
				echo "streamonitor 容器已经存在，正在启动..."
				docker start streamonitor
			else
				echo "streamonitor 容器不存在，正在创建容器..."
				cd "$MainFolder" && docker-compose up -d
			fi
			
			echo "$time ---- 用户操作：执行StreaMonitor-开启脚本容器的命令" >> $logfile
			;;
			
		# 控制参数可以直接改config.json，直接运行python
		5)
			# 单执行：docker exec streamonitor python Controller.py add ss sc
			# 执行StreaMonitor-添加主播的命令
			# 询问主播名
			read -p "请输入添加的主播名: " anchor_name

			# 循环直到选择有效选项
			while true; do
				# 提供选项并读取选择
				echo "请选择直播源:（自定义需要修改sh脚本）"
				echo "1. sc"
				echo "2. cb"
				read -p "请输入选项: " option

				case $option in
					1)
						# 执行命令：python3 Controller.py 添加的主播名 sc
						docker exec streamonitor python3 Controller.py add $anchor_name sc
						break  # 选择有效，跳出循环
						echo "$time ---- 用户操作：执行StreaMonitor-添加SC主播：$anchor_name  的命令" >> $logfile
						;;
					2)
						# 执行命令：python3 Controller.py 添加的主播名 cb
						docker exec streamonitor python3 Controller.py add $anchor_name cb
						break  # 选择有效，跳出循环
						echo "$time ---- 用户操作：执行StreaMonitor-添加CB主播：$anchor_name  的命令" >> $logfile
						;;
					*)
						echo "无效的选项，请重新选择"
						;;
				esac
			done
			
			;;
		6)
			# 执行StreaMonitor-删除主播的命令
			# 询问需要删除的主播名
			read -p "请输入需要删除的主播名: " delete_anchor_name

			# 执行命令：python3 Controller.py remove 需要删除的主播名
			docker exec streamonitor python3 Controller.py remove $delete_anchor_name
			echo "$time ---- 用户操作：执行StreaMonitor-删除主播：$delete_anchor_name  的命令" >> $logfile
			;;
		7)
			# 执行StreaMonitor-开始特定主播的命令
			# 询问需要开启录制的主播名
			read -p "请输入需要开启录制的主播名: " start_recording_anchor_name

			# 执行命令：python3 Controller.py start 需要开启录制的主播名
			docker exec streamonitor python3 Controller.py start $start_recording_anchor_name
			echo "$time ---- 用户操作：执行StreaMonitor-开始特定主播：$start_recording_anchor_name  的命令" >> $logfile
			;;
		8)
			# 执行StreaMonitor-暂停特定主播的命令
			# 询问需要暂停录制的主播名
			read -p "请输入需要暂停录制的主播名: " pause_recording_anchor_name

			# 执行命令：python3 Controller.py pause 需要暂停录制的主播名
			docker exec streamonitor python3 Controller.py pause $pause_recording_anchor_name
			echo "$time ---- 用户操作：执行StreaMonitor-暂停特定主播：$pause_recording_anchor_name  的命令" >> $logfile
			;;
		# 流问题只能进入运行的tmux会话中去执行命令
		9)
			# 执行StreaMonitor-全部暂停的命令
			#echo "执行StreaMonitor-全部暂停的命令"
			# 执行命令：
			#tmux send-keys -t StreaMonitor-Downloader:0 "stop *" Enter
			echo "暂不支持该功能，docker版本不识别streamers流"
			echo "暂停容器同效，已暂停容器"
			docker stop streamonitor
			echo "$time ---- 用户操作：执行StreaMonitor-全部暂停的命令" >> $logfile
			;;
		10)
			# 执行StreaMonitor-全部开始的命令
			#echo "执行StreaMonitor-全部开始的命令"
			# 执行命令：
			#tmux send-keys -t StreaMonitor-Downloader:0 "start *" Enter
			echo "暂不支持该功能，docker版本不识别streamers流"
			echo "开启容器同效，已开启容器"
			docker start streamonitor
			echo "$time ---- 用户操作：执行StreaMonitor-全部开始的命令" >> $logfile
			;;
		# 控制参数可以直接获取config.json，直接运行python
		11)
			# 执行StreaMonitor-录制状态的命令
			echo "执行StreaMonitor-录制状态的命令"
			# 执行命令：python3 Controller.py status
			docker exec streamonitor python3 Controller.py status
			echo "$time ---- 用户操作：执行StreaMonitor-录制状态的命令" >> $logfile
			;;
		# 删除tmux会话
		12)
			# 执行StreaMonitor-退出脚本的命令
			#echo "执行StreaMonitor-退出脚本的命令"
			# 执行命令：删除StreaMonitor-Downloader会话
			echo "暂不支持该功能，docker版本不识别streamers流"
			echo "暂停容器同效，已暂停容器"
			docker stop streamonitor
			echo "$time ---- 用户操作：执行StreaMonitor-退出脚本的命令" >> $logfile
			;;
		13)
			# 执行Rclone-Config配置的命令
			echo "执行Rclone-Config配置的命令"
			rclone config
			echo "$time ---- 用户操作：执行Rclone-Config配置的命令" >> $logfile
			;;
		14)
			# 执行Rclone-GUI图像界面的命令
			echo "执行Rclone-GUI图像界面的命令"
			echo "为了方便结束进程、再加上使用频率低，不启用后台运行"
			rclone rcd --rc-web-gui --rc-addr :857 --rc-user=admin --rc-pass=1594959462
			echo "Rclone-GUI图像界面参数："
			echo "端口：857"
			echo "账号：admin"
			echo "密码：1594959462"
			echo "$time ---- 用户操作：执行Rclone-GUI图像界面的命令" >> $logfile
			;;
		# 无交互，使用screen后台任务
		15)
			# 执行Downloads-同步文件夹的命令
			echo "执行Downloads-同步文件夹的命令"
			# 询问 Rclone 远程配置名称
			read -p "请输入 Rclone 远程配置名称（默认为 scsg3）: " rclone_remote_name
			rclone_remote_name=${rclone_remote_name:-scsg3}  # 如果用户没有输入，则使用默认值 scsg3

			# 询问 Rclone 同步线程数
			read -p "请输入 Rclone 同步线程数（默认为 10）: " rclone_thread_count
			rclone_thread_count=${rclone_thread_count:-10}  # 如果用户没有输入，则使用默认值 10

			# 使用 screen 运行命令：rclone copy "./downloads" Rclone远程配置名称:SC --progress --transfers Rclone线程数，并命名为 "Downloads-Sync"
			screen -dmS Downloads-Sync rclone copy $DownloadFolder "$rclone_remote_name:SC" --progress --transfers "$rclone_thread_count"
			echo "$time ---- 用户操作：Downloads-同步文件夹的命令：(Rclone远程配置名称：$rclone_remote_name, Rclone线程数:$rclone_thread_count)" >> $logfile
			;;
		16)
			# 执行Downloads-仅删除视频文件的命令
			echo "执行Downloads-仅删除视频文件的命令"
			# 删除 ./downloads 文件夹中的所有视频文件（包括子文件夹），保留其他文件
			screen -dmS Downloads-del-video find $DownloadFolder -type f \( -name "*.mp4" -o -name "*.avi" -o -name "*.mkv" \) -delete
			echo "$time ---- 用户操作：执行Downloads-仅删除视频文件的命令" >> $logfile
			;;
		17)
			# 执行Downloads-生成略缩图的命令
			echo "执行Downloads-生成略缩图的命令"
			screen -dmS Downloads-thumb python3 $MainFolder/get_video_thumb_pic.py $DownloadFolder 0
			echo "$time ---- 用户操作：执行Downloads-生成略缩图的命令" >> $logfile
			;;
		# 无交互，直接运行或使用screen后台任务
		18)
			# 执行Sync-移动文件夹的命令
			# 检测 downloads 文件夹是否存在
			if [ -d "$DownloadFolder" ]; then
				# 移动文件到 sync 文件夹 "mv -f /768/downloads/* /768/sync/" 只移动文件夹内的东西，-f强制覆盖目标文件夹已存在文件，不提示
				mv -f $DownloadFolder/* $SyncFolder/
			else
				# 创建 downloads 文件夹
				mkdir $DownloadFolder
			fi
			echo "$time ---- 用户操作：执行Sync-移动文件夹的命令" >> $logfile
			;;
		19)
			# 执行Sync-同步文件夹的命令
			echo "执行Sync-同步文件夹的命令"
			# 询问 Rclone 远程配置名称
			read -p "请输入 Rclone 远程配置名称（默认为 scsg3）: " rclone_remote_name
			rclone_remote_name=${rclone_remote_name:-scsg3}  # 如果用户没有输入，则使用默认值 scsg3

			# 询问 Rclone 同步线程数
			read -p "请输入 Rclone 同步线程数（默认为 10）: " rclone_thread_count
			rclone_thread_count=${rclone_thread_count:-10}  # 如果用户没有输入，则使用默认值 10

			# 使用 screen 运行命令：rclone copy "./sync" Rclone远程配置名称:SC --progress --transfers Rclone线程数，并命名为 "sync-Sync"
			screen -dmS sync-Sync rclone copy $SyncFolder "$rclone_remote_name:SC" --progress --transfers "$rclone_thread_count"
			echo "$time ---- 用户操作：Sync-同步文件夹的命令：(Rclone远程配置名称：$rclone_remote_name, Rclone线程数:$rclone_thread_count)" >> $logfile
			;;
		20)
			# 执行Sync-仅删除视频文件的命令
			echo "执行Sync-仅删除视频文件的命令"
			screen -dmS Sync-del-video find $SyncFolder -type f \( -name "*.mp4" -o -name "*.avi" -o -name "*.mkv" \) -delete
			echo "$time ---- 用户操作：执行Sync-仅删除视频文件的命令" >> $logfile
			;;
		21)
			# 执行Sync-生成略缩图的命令
			echo "执行Sync-生成略缩图的命令"
			screen -dmS Sync-thumb python3 $MainFolder/get_video_thumb_pic.py $SyncFolder 0
			echo "$time ---- 用户操作：执行Sync-生成略缩图的命令" >> $logfile
			;;		
		22)
			# 执行Sync-清理文件夹的命令
			echo "执行Sync-清理文件夹的命令"
			# 删除 sync 文件夹
			rm -rf $SyncFolder
			mkdir $SyncFolder
			echo "$time ---- 用户操作：执行Sync-清理文件夹的命令" >> $logfile
			;;
		23)
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
			echo "$time ---- 用户操作：执行Cancel-Downloads-取消同步视频任务的命令" >> $logfile
			;;
		24)
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
			echo "$time ---- 用户操作：执行Cancel-Sync-取消同步视频任务的命令" >> $logfile
			;;
		25)
			# 执行Clear-Downloads-删除空白略缩图的命令
			screen -dmS Clear-Downloads python3 $MainFolder/check_0000jpg.py $DownloadFolder
			echo "$time ---- 用户操作：执行Clear-Downloads-删除空白略缩图的命令" >> $logfile
			;;
		26)
			# 执行Clear-Sync-删除空白略缩图的命令
			screen -dmS Clear-Sync python3 $MainFolder/check_0000jpg.py $SyncFolder
			echo "$time ---- 用户操作：执行Clear-Sync-删除空白略缩图的命令" >> $logfile
			;;
		27)
			# 执行Query-Size-查询文件夹大小的命令
			du -sh $DownloadFolder ; du -sh $SyncFolder
			echo "$time ---- 用户操作：执行Query-Size-查询文件夹大小的命令" >> $logfile
			;;
		0)
			# 退出脚本
			exit 0
			;;
		*)
			echo "无效的选项"
			show_menu
			;;
	esac
}

show_menu
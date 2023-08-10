#!/bin/bash
MainFolder="/root/StreaMonitor"
logfile="$MainFolder/log-RunOperation.log"

while read -r event
do
	time=$(date +"%Y-%m-%d %H:%M:%S")
	container_name=$(echo "$event" | awk '{print $2}')

	case $event in
		*attach*)
			echo "$time----容器操作：$container_name Container attached" >> "$logfile"
			;;
		*commit*)
			echo "$time----容器操作：$container_name New image committed" >> "$logfile"
			;;
		*create*)
			echo "$time----容器操作：$container_name Container created" >> "$logfile"
			;;
		*die*)
			echo "$time----容器操作：$container_name Container died" >> "$logfile"
			;;
		*kill*)
			echo "$time----容器操作：$container_name Container killed" >> "$logfile"
			;;
		*oom*)
			echo "$time----容器操作：$container_name Out of memory" >> "$logfile"
			;;
		*pause*)
			echo "$time----容器操作：$container_name Container paused" >> "$logfile"
			;;
		*start*)
			echo "$time----容器操作：$container_name Container started" >> "$logfile"
			;;
		*restart*)
			echo "$time----容器操作：$container_name Container restarted" >> "$logfile"
			;;
		*stop*)
			echo "$time----容器操作：$container_name Container stopped" >> "$logfile"
			;;
		*unpause*)
			echo "$time----容器操作：$container_name Container unpaused" >> "$logfile"
			;;
		*update*)
			echo "$time----容器操作：$container_name Container updated" >> "$logfile"
			;;
	esac
done < <(docker events --filter 'event=attach' --filter 'event=commit' --filter 'event=create' --filter 'event=die' --filter 'event=kill' --filter 'event=oom' --filter 'event=pause' --filter 'event=start' --filter 'event=restart' --filter 'event=stop' --filter 'event=unpause' --filter 'event=update' --format '{{.Time}} {{.ID}}') &

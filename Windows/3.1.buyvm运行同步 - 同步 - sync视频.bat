echo sync video
rclone copy "./sync" sc:SC --progress --transfers 10
echo snync complete
pause
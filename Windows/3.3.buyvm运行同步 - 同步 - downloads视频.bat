echo sync video
rclone copy "./downloads" sc:SC --progress --transfers 10
echo snync complete
pause
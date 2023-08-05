@echo off
setlocal enabledelayedexpansion

rem 设置文件夹路径
set "folder=./downloads"

rem 遍历文件夹中的所有文件
for /r "%folder%" %%a in (*.mp4 *.avi *.mkv) do (
    rem 获取文件的路径和名称
    set "filepath=%%~fa"
    set "filename=%%~nxa"

    rem 输出删除的文件名和路径
    echo 删除文件: !filepath!

    rem 删除文件
    del "!filepath!"
)

endlocal
pause
@echo off
setlocal enabledelayedexpansion

rem �����ļ���·��
set "folder=./downloads"

rem �����ļ����е������ļ�
for /r "%folder%" %%a in (*.mp4 *.avi *.mkv) do (
    rem ��ȡ�ļ���·��������
    set "filepath=%%~fa"
    set "filename=%%~nxa"

    rem ���ɾ�����ļ�����·��
    echo ɾ���ļ�: !filepath!

    rem ɾ���ļ�
    del "!filepath!"
)

endlocal
pause
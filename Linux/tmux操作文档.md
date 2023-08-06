## 安装

要在 CentOS 上安装 tmux，您可以按照以下步骤进行操作：

1. 打开终端并以 root 用户身份登录。

2. 使用以下命令安装 EPEL 存储库（如果尚未安装）：
   
   ```bash
   yum install epel-release
   ```

3. 运行以下命令来安装 tmux：
   
   ```bash
   yum install tmux
   ```

4. 安装完成后，您可以通过运行以下命令来验证 tmux 是否成功安装：
   
   ```bash
   tmux -V
   ```
   
   如果成功安装，将显示 tmux 的版本信息。

现在，您已成功在 CentOS 上安装了 tmux。您可以使用 `tmux` 命令启动 tmux，并开始创建和管理终端会话。

## 基本操作

使用 tmux 可以创建和管理终端会话。以下是 tmux 的一些基本用法：

1. 启动 tmux：在终端中输入 `tmux` 命令，按下回车键即可启动 tmux。

2. 创建新会话：启动 tmux 后，将创建一个新的会话。会话将在后台运行，并且您可以在其中执行命令。您可以使用以下命令创建新会话：
   
   ```
   tmux new-session -s session-name
   ```
   
   其中 `session-name` 是您为会话指定的名称。如果不指定名称，会话将自动分配一个默认名称。

3. 进入会话：如果您启动了多个会话，可以使用以下命令进入特定会话：
   
   ```
   tmux attach-session -t session-name
   ```
   
   其中 `session-name` 是要进入的会话的名称。

4. 分离会话：如果您想在保持会话运行的同时断开终端连接，可以使用以下命令分离会话：
   
   ```
   tmux detach-client
   ```
   
   这将使会话继续在后台运行，即使您断开了终端连接。

5. 列出会话：使用以下命令列出当前存在的会话：
   
   ```
   tmux list-sessions
   ```

6. 在会话中切换窗格：在 tmux 中，会话可以分为多个窗格，您可以在窗格之间切换。以下是一些常用的窗格切换命令：
   
   - 切换到下一个窗格：`Ctrl+b`，然后按下 `o`。
   - 切换到上一个窗格：`Ctrl+b`，然后按下 `;`。
   - 切换到指定编号的窗格：`Ctrl+b`，然后按下窗格编号（从 0 开始）。

这只是 tmux 的一些基本用法。tmux 还有更多功能和选项，您可以查阅 tmux 的文档或参考资料以深入了解更多用法和配置选项。

## 删除操作

要删除 tmux 中的会话，您可以使用以下命令：

1. 列出当前存在的会话：使用以下命令列出当前存在的会话及其编号：
   
   ```
   tmux list-sessions
   ```

2. 选择要删除的会话：根据列出的会话列表，确定要删除的会话的编号或名称。

3. 删除会话：使用以下命令删除指定的会话：
   
   ```
   tmux kill-session -t session-id
   ```
   
   或
   
   ```
   tmux kill-session -t session-name
   ```
   
   其中 `session-id` 是会话的编号，`session-name` 是会话的名称。

请注意，删除会话将永久删除会话及其所有窗口和窗格，无法恢复。在删除会话之前，请确保您不再需要其中的任何数据或进程。

如果您只是想分离会话而不是删除它，可以使用 `detach-client` 命令将会话分离，而不会删除会话本身。

## 仅创建会话，并执行命令

如果您只想创建一个名为 "StreaMonitor-Downloader" 的 tmux 会话，并在其中执行命令 `python3 /root/StreaMonitor/Linux/Downloader.py`，而不进入会话，可以使用以下 shell 脚本：

```bash
#!/bin/bash

# 创建会话并执行命令
tmux new-session -d -s StreaMonitor-Downloader "python3 /root/StreaMonitor/Linux/Downloader.py"
```

将上述脚本保存为一个文件（例如 `start_session.sh`），然后在终端中运行以下命令来执行该脚本：

```bash
chmod +x start_session.sh  # 添加执行权限
./start_session.sh  # 执行脚本
```

这将创建一个名为 "StreaMonitor-Downloader" 的 tmux 会话，并在其中执行指定的 Python 脚本，但不会进入会话。您可以使用 `tmux list-sessions` 命令来列出当前的 tmux 会话，以验证会话是否成功创建。

请确保在执行脚本之前，路径 `/root/StreaMonitor/Linux/Downloader.py` 中的文件存在，并且您具有执行该文件的权限。

## 仅执行命令：

    tmux send-keys -t StreaMonitor-Downloader:0 "stop *" Enter

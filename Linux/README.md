# StreaMonitor
A Python3 application for monitoring and saving (mostly adult) live streams from various websites.

Inspired by [Recordurbate](https://github.com/oliverjrose99/Recordurbate)

## Supported sites
| Site name      | Abbreviation | Aliases                     | Quirks                 | Selectable resolution |
|----------------|--------------|-----------------------------|------------------------|-----------------------|
| Amateur.TV     | `ATV`        |                             |                        | Yes                   |
| Bongacams      | `BC`         |                             |                        | Yes                   |
| Cam4           | `C4`         |                             |                        | Yes                   |
| Cams.com       | `CC`         |                             |                        | Currently only 360p   |
| CamSoda        | `CS`         |                             |                        | Yes                   |
| Chaturbate     | `CB`         |                             |                        | Yes                   |
| Cherry.TV      | `CHTV`       |                             |                        | Yes                   |
| Dreamcam VR    | `DCVR`       |                             |                        | No                    |
| Flirt4Free     | `F4F`        |                             |                        | Yes                   |
| ManyVids Live  | `MV`         |                             |                        | Yes                   |
| MyFreeCams     | `MFC`        |                             |                        | Yes                   |
| SexChat.hu     | `SCHU`       |                             | use the id as username | No                    |
| StreaMate      | `SM`         | PornHubLive, PepperCams,... |                        | Yes                   |
| StripChat      | `SC`         | XHamsterLive,...            |                        | Yes                   |
| StripChat VR   | `SCVR`       |                             | for VR videos          | No                    |

Currently not supported:
* ImLive (Too strict captcha protection for scraping)
* LiveJasmin (No nudity in free streams)

There are hundreds of clones of the sites above, you can read about them on [this site](https://adultwebcam.site/clone-sites-by-platform/).

## Requirements
* Python 3
  * Install packages listed in requirements.txt with pip.
* FFmpeg

## Usage

The application has the following interfaces:
* Console
* External console via ZeroMQ (sort of working)
* Web interface (only status)

### Linux前置条件

#### （未成功部署，使用docker吧）

- 打开终端并以 root 用户身份登录。

- 使用以下命令安装 EPEL 存储库（如果尚未安装）：

  ```bash
  yum install epel-release
  ```

- 运行以下命令来安装 tmux、screen、rclone：

  ```bash
  yum install tmux screen && curl -k https://rclone.org/install.sh | sudo bash
  ```

- 安装完成后，您可以通过运行以下命令来验证 tmux 是否成功安装：

  ```bash
  tmux -V
  ```

  如果成功安装，将显示 tmux 的版本信息。

- 安装python

  ```
  3.10.12
  ```

- pip包

  ```
  pip3 install -r requirements.txt
  ```

- 安装ffmpeg，先下载源码包：

  ```bash
  git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
  ```

  然后进入ffmpeg文件夹，依次执行下列语句，当然连起来也可以：

  ```bash
  cd ffmpeg && ./configure
  make
  make install
  ```

  时间较长，不出意外会正常安装好。

  但是因为configure时候没有指定路径，所以直接ffmpeg会提示找不到。

  所以要将编译好的ffmpeg复制到bin目录即可：

  ```bash
  cp ffmpeg /usr/bin/ffmpeg
  ```

  然后检查版本。

  ```bash
  ffmpeg -version
  ```

- 使用run.sh

  ```
  bash run.sh
  ```

  

#### Starting and console

Start the downloader (it does not fork yet)\
Automatically imports all streamers from the config file.

```
python Downloader.py
```

On the console you can use the following commands:
```
add <username> <site> - Add streamer to the list (also starts monitoring)
remove <username> [<site>] - Remove streamer from the list
start <username> [<site>] - Start monitoring streamer
start * - Start all
stop <username> [<site>] - Stop monitoring
stop * - stop all
status - Status display 
status2 - A slightly more readable status table
quit - Clean exit (Pressing CTRL-C also behaves like this)
```
For the `username` input, you usually have to enter the username as represented in the original URL of the room. 
Some sites are case-sensitive.

For the `site` input, you can use either the full or the short format of the site name. (And it is case-insensitive)

#### "Remote" controller
Add or remove a streamer to record (Also saves config file)
```
python3 Controller.py add <username> <website>
python3 Controller.py remove <username>
```

Start/stop recording streamers
```
python3 Controller.py <start|stop> <username>
```

List the streamers in the config
```
python3 Controller.py status
```

#### Web interface

You can access the web interface on port 5000. 
It just prints the same information as the status command. 
You can also get a list of the recorded streams.

Further improvements can be expected.

## Docker support

You can run this application in docker. I prefer docker-compose so I included an example docker-compose.yml file that you can use.
Simply start it in the folder with `docker-compose up`.

## Configuration

You can set some parameters in the parameters.py.

## Disclaimer

This program is only a proof of concept and education project, I don't encourage anybody to use it. \
Most (if not every) streamers disallow recording their shows. Please respect their wish. \
If you don't, and you record them despite this request, please don't ever publish or share any recordings. \
If you either record or share the recorded shows, you might be legally punished. \
Also, please don't use this tool for monetization in any way.



## 常见错误

### 找不到或者版本过旧的 nasm/yasm

```
[root@localhost ~]# cd ffmpeg && ./configure
nasm/yasm not found or too old. Use --disable-x86asm for a crippled build.

If you think configure made a mistake, make sure you are using the latest
version from Git.  If the latest version fails, report the problem to the
ffmpeg-user@ffmpeg.org mailing list or IRC #ffmpeg on irc.libera.chat.
Include the log file "ffbuild/config.log" produced by configure as this will help
solve the problem.

```

要解决这个问题，您可以尝试以下几个步骤：

1. 检查 nasm 或 yasm 是否已经安装在您的系统上。您可以运行以下命令来检查它们的安装情况：

   ```bash
   nasm -v
   yasm --version
   ```

   如果它们已经安装，您将看到相应的版本信息。如果它们未安装，您可以使用包管理器（如apt、yum等）来安装它们。

   ```bash
   sudo yum install nasm yasm
   ```

2. 如果您已经安装了 nasm 或 yasm，但仍然遇到问题，可能是因为版本过旧。您可以尝试升级 nasm 或 yasm 到最新版本。具体的升级方法取决于您的操作系统和包管理器。

3. 如果您无法安装或升级 nasm/yasm，您可以尝试使用 `--disable-x86asm` 参数来禁用 x86 汇编优化。这将导致编译过程中缺少一些优化功能，但可以让您继续进行编译。您可以运行以下命令来执行配置并禁用 x86 汇编优化：

   ```bash
   ./configure --disable-x86asm
   ```

   请注意，禁用 x86 汇编优化可能会影响 FFmpeg 的性能。
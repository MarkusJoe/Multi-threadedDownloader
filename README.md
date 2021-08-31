# Multi-threadedDownloader
# 使用前准备(Windows)

### 本程序基于[和风天气API](https://dev.qweather.com/)
下载完文件请将文件夹内`weather-icon.zip`里的`weather-icon`文件夹解压到和`Weather.py`同目录下

请现在电脑上安装python 3.x版

首先在路径栏中输入 `pip -r requirements.txt` 等待安装完成后打开Config.yaml 修改内容

以下是各个参数代表的意义

Config.yaml
 - `mode`:  --> free > dev
    - free: 免费 使用只需注册实名后即可使用 -> 只能获取3天的天气(包括今天在内)
    - dev: 个人开发者 注册实名后提交认证信息即可使用 -> 可以获取7天天气&1天生活建议&未来24小时天气预报...其他功能
 - `key`:  API的密钥
 - `location`:  获取数据的城市 内容可在location.txt文件中查找
 - `sender`:  发送邮件的账号
 - `password`:  发送邮件账号的登录密钥
 - `receiver`:  接收邮件的账号
 - `server`:  发送邮件的中转服务器
 - `port`:  服务器端口
 - `time`:  发送时间

 # 运行程序

程序没有图形界面因此使用Windows的cmd作为终端
双击文件夹内`Weather.exe`即可运行(将使用前准备完成)



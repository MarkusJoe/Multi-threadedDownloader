# Multi-threadedDownloader
# 使用前准备

- 程序基于Python3编程， 请提前安装
- 下载所有文件
- 打开文件夹在路径栏输入`pip -r requirements.txt` 等待安装成功后即可

# 如何使用
- 1.双击打开py文件(如果可以)
- 2.打开.exe文件 no-console.exe 为无终端版本

## 原理
通过requests获取文件大小(bytes)并分配给每个线程固定大小的数据块，再使用多线程并发下载





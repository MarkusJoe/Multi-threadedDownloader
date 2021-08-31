import os
import random
import re
import time
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from tkinter import filedialog, messagebox

import requests
import yaml

# 窗口居中
root_master = tk.Tk()
root_master.title('文件下载')
root_master.resizable(False, False) # 不可编辑窗口
screen_width = root_master.winfo_screenwidth()
screen_height = root_master.winfo_screenheight()
cus_width = 400
cus_height = 240
cus_x = (screen_width - cus_width) / 2
cus_y = (screen_height - cus_height) / 2
root_master.geometry('%dx%d+%d+%d' %(cus_width, cus_height, cus_x, cus_y))

var_e1 = tk.StringVar()
e1 = tk.Entry(show=None, textvariable=var_e1, justify='center', width=45)

executor_public = ThreadPoolExecutor(3) # 公用

# UA列表
UA_list = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36"
]

def validateName(file_name): # 将无法作为文件名的字符替换
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_name = re.sub(rstr, "_", file_name)
    return new_name

def singleThread(url): # 单线程
    start_time = time.time()
    r = requests.get(url, headers={"User-Agent":random.choice(UA_list)}, stream=True)
    file_name = url.split('/')[-1]
    validatedname = validateName(file_name)
    with open('config/configuration.yaml', 'r') as f_p:
        configuration = yaml.load(f_p.read(), Loader=yaml.Loader)
        path = configuration['Configuration']['Path']
    if len(validatedname) > 127:  # 文件名大于127字符自动替换文件名为"UNNAMED"
        validatedname = 'UNNAMED'
    with open(f'{path}/{validatedname}', 'wb') as f:
        f.write(r.content)
    end_time = time.time()
    l_s_down = tk.Label(text=f'下载完成 用时{round(end_time - start_time, 2)}秒')
    l_s_down.place(x=100, y=120, width=200)
    var_e1.set('')
    return 'downloaded'

def display_path(): # 在界面上显示存储路径
    with open('config/configuration.yaml', 'r') as f_p:
        configuration = yaml.load(f_p.read(), Loader=yaml.Loader)
        path = configuration['Configuration']['Path']
        l_path = tk.Label(text = f'下载文件保存路径: {path}')
        l_path.place(x=0, y=160, width=400)

def openfolder(): # 打开选择的文件路径
    with open('config/configuration.yaml', 'r') as f_p:
        configuration = yaml.load(f_p.read(), Loader=yaml.Loader)
        path = configuration['Configuration']['Path']
    os.system('explorer.exe %s' %(path))

def select_path(): # 选择保存路径
    root_path = tk.Tk()
    root_path.withdraw()
    path = filedialog.askdirectory()
    if path != '':
        config = {'Configuration': {'Path': f'{path}', 'Thread':16}}
        print('Selected file path: ', path)
        with open('config/configuration.yaml', 'w') as f:
            yaml.dump(config, f)
    display_path()

def init():
    config = {'Configuration': {'Path': f'{os.getcwd()}', 'Thread': 16}}
    print('File Save path:', os.getcwd())
    with open('config/configuration.yaml', 'w') as f:
        yaml.dump(config, f)


def thread_down(url, start, end, name, path, start_time, length, max_worker, ThreadID): # 文件分块下载
    headers = {'User-Agent':random.choice(UA_list), 'Range':f'bytes={start}-{end}'}
    r = requests.get(url, headers=headers, stream=True)
    with open(f'{path}/{name}', 'r+b') as f:
        f.seek(start)
        for data in r.iter_content(1024*1024*5):
            f.write(data)
    print(f'{ThreadID} / {max_worker} threads done.')
    end_time = time.time()
    file_size = os.path.getsize(f'{path}/{name}')
    if length == file_size:
        l_down = tk.Label(text=f'已完成 用时{round(end_time-start_time, 1)}秒')
        l_down.place(x=100, y=120, width=200)
        var_e1.set('')

def run(url): # 并发多线程 启动thread_down
    start_time = time.time()
    with open('./config/configuration.yaml', 'r') as f_p:
        configuration = yaml.load(f_p.read(), Loader=yaml.Loader)
        path = configuration['Configuration']['Path']
        max_worker = configuration['Configuration']['Thread']
    try:
        r_i = requests.head(url, headers={'User-Agent':random.choice(UA_list)})
        length = int(r_i.headers['Content-Length'])
        l_m_connect = tk.Label(text='文件正在下载中')
        l_m_connect.place(x=100, y=120, width=200)
        part = length // max_worker
        file_name = url.split('/')[-1]
        validatedname = validateName(file_name)
        executor = ThreadPoolExecutor(max_workers=max_worker)
        if len(validatedname) > 127: # 文件名大于127字符自动替换文件名为"UNNAMED"
            validatedname = 'FileNameTooLong'
        open(f'{path}/{validatedname}', 'w').close() # 创建同名文件
        for i in range(max_worker): # 处理每个线程下载的数据块大小
            start = part * i
            if i == max_worker - 1:
                end = length
                print(f'Thread-{i} download range: {end - start} Bytes')
            else:
                end = start + part
                print(f'Thread-{i} download range: {end - start} Bytes')
            executor.submit(thread_down, url, start, end, file_name, path, start_time, length, max_worker, i)
    except Exception as e:
        print(e)
        messagebox.showerror(title='连接错误', message='          连接错误          ')
        var_e1.set('')

def MultiOrSingle(): # 判断文件大小 文件大于50Mb选择使用多线程 小于50Mb使用单线程
    url = e1.get()
    if url != '':
        try:
            r_c = requests.head(url, headers={'User-Agent':random.choice(UA_list)})
            len_file = r_c.headers['Content-Length']
            print(f'文件大小:{round(int(len_file) / 1024 / 1024, 2)} MB')
            if int(len_file) < 52428800:
                print('本次下载使用单线程')
                executor_public.submit(singleThread, url)
                l_s_connect = tk.Label(text='文件正在下载中')
                l_s_connect.place(x=100, y=120, width=200)
            else:
                print('本次下载使用多线程')
                executor_public.submit(run, url)
        except:
            messagebox.showerror(title='连接错误', message='     连接错误请, 输入正确的地址     ')
            var_e1.set('')
    else:
        messagebox.showerror(title='输入错误', message='               请输入文件地址              ')

# 各部件实例化
b1 = tk.Button(text='开始下载', command=MultiOrSingle)
b2 = tk.Button(text='选择下载路径', command=select_path)
b3 = tk.Button(text='打开文件夹', command=openfolder)
b4 = tk.Button(text='初始化', command=init)

l1 = tk.Label(text='输入资源链接:')
l2 = tk.Label(text='在同目录下的config文件夹内找到名为configuration.yaml\nThread为线程数 默认线程数是16')

l1.place(x=160, y=5)
l2.place(x=40, y=190)
e1.place(x=45, y=35)
b1.place(x=80, y=80, width=100)
b2.place(x=220, y=80, width=100)
b3.place(x=80, y=115, width=100)
b4.place(x=220, y=115, width=100)

if __name__ == '__main__':
    display_path()
    root_master.mainloop()

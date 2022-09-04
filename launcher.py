import tkinter
from tkinter import ttk
from tkinter import messagebox
from himawari8 import Himawari8
from concurrent.futures import ThreadPoolExecutor

class Data(object):
    def __init__(self):
        self.properties = {'enabled':False }
        self.service = Himawari8()


def switch(button, data):
    properties = data.properties
    button['state'] = 'disabled'
    button['text'] = '处理中...'
    if properties['enabled']:
        stop(data)
        properties['enabled'] = False
        button['text'] = '开启'
    else:
        start(data)
        properties['enabled'] = True
        button['text'] = '关闭'
    button['state'] = 'normal'

def start(data):
    data.service.start()

def stop(data):
    data.service.stop()

# 另开一个线程防止主线程太长
class ResultHandler:

    def __init__(self, button):
        self.btn = button

    def handler(self, result):
        self.btn['text'] = '更新桌面'
        self.btn['state'] = 'normal'
        messagebox.showinfo("成功！", "桌面更新完成！")

def work(data):
    print('start flush desktop')
    data.service.work()

def flush(button, data):
    button['text'] = '处理中...'
    button['state'] = 'disabled'
    handler = ResultHandler(button)
    pool = ThreadPoolExecutor(max_workers=1)
    future1 = pool.submit(work, data)
    future1.add_done_callback(ResultHandler(button).handler)

def main():
    root = tkinter.Tk()
    root.geometry('130x100')
    root.resizable(width=0, height=0)
    frame = ttk.Frame(root, padding=20)
    frame.grid()
    data = Data()

    enable_button = ttk.Button(frame, text="开启")
    enable_button.grid()
    enable_button['command'] = lambda: switch(enable_button, data)

    reflush_button = ttk.Button(root, text="更新桌面", padding=5)
    reflush_button.grid()
    reflush_button['command'] = lambda: flush(reflush_button, data)

    root.mainloop()

if __name__ == '__main__':
    main()

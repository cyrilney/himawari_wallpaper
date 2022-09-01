import tkinter
from tkinter import ttk
from tkinter import messagebox
from himawari8 import Himawari8

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

def flush(button,data):
    button['text'] = '处理中...'
    button['state'] = 'disabled'
    data.service.work()
    button['text'] = '更新桌面'
    button['state'] = 'normal'







def main():

    # 重定向输出流  日志文件化
    fp = open("print.log", "w+")
    sys.stdout = fp

    root = tkinter.Tk()
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


def message(title, info):
    messagebox.showinfo(title, info)

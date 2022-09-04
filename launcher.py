import tkinter
from tkinter import ttk
from tkinter import messagebox
from himawari8 import Himawari8
import threading
from concurrent.futures import ThreadPoolExecutor
import pystray
from PIL import Image
from pystray import MenuItem, Menu

class Data(object):
    def __init__(self):
        self.properties = {'enabled':False }
        self.service = Himawari8()

# 开关himawari事件方法
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

# 异步回调方法处理长时间更新桌面
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

# 刷新事件方法
def flush(button, data):
    button['text'] = '处理中...'
    button['state'] = 'disabled'
    handler = ResultHandler(button)
    pool = ThreadPoolExecutor(max_workers=1)
    future1 = pool.submit(work, data)
    future1.add_done_callback(ResultHandler(button).handler)

def main():
    root = tkinter.Tk()
    root.iconbitmap("static/earth.png")
    root.resizable(width=0, height=0)
    frame = ttk.Frame(root, padding=50)
    frame.grid()
    data = Data()

    enable_button = ttk.Button(frame, text="开启")
    enable_button.grid()
    enable_button['command'] = lambda: switch(enable_button, data)

    reflush_button = ttk.Button(root, text="更新桌面", padding=5)
    reflush_button.grid()
    reflush_button['command'] = lambda: flush(reflush_button, data)

    def quit_window(icon: pystray.Icon):
        icon.stop()
        root.destroy()

    def show_window():
        root.deiconify()

    def on_exit():
        root.withdraw()

    window.protocol('WM_DELETE_WINDOW',on_exit)
    menu = (MenuItem('显示', show_window, default=True), Menu.SEPARATOR, MenuItem('退出', quit_window))
    image = Image.open("static/earth.png")
    icon = pystray.Icon("icon", image, "图标名称", menu)
    threading.Thread(target=icon.run, daemon=True).start()
    root.mainloop()

if __name__ == '__main__':
    main()

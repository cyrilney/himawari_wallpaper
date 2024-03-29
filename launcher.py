import tkinter
from tkinter import ttk
from tkinter import messagebox
from himawari8 import Himawari8
import threading
from concurrent.futures import ThreadPoolExecutor
from consts import LaucherConsts
import pystray
from PIL import Image
from pystray import MenuItem, Menu
import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


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
        button['text'] = LaucherConsts.LAUCHER_OPEN_BUTTON_TEXT
    else:
        start(data)
        properties['enabled'] = True
        button['text'] = LaucherConsts.LAUCHER_CLOSE_BUTTON_TEXT
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
        self.btn['text'] = LaucherConsts.LAUCHER_REFLUSH_BUTTON_TEXT
        self.btn['state'] = 'normal'
        messagebox.showinfo("成功！", LaucherConsts.LAUCHER_REFLUSH_SUCCESS_MESSAGE)

def work(data):
    logging.info('start flush desktop')
    data.service.work()

# 刷新事件方法
def flush(button, data):
    button['text'] = LaucherConsts.LAUCHER_WORKING_BUTTON_TEXT
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

    enable_button = ttk.Button(frame, text=LaucherConsts.LAUCHER_OPEN_BUTTON_TEXT)
    enable_button.grid()
    enable_button['command'] = lambda: switch(enable_button, data)

    reflush_button = ttk.Button(root, text=LaucherConsts.LAUCHER_REFLUSH_BUTTON_TEXT, padding=5)
    reflush_button.grid()
    reflush_button['command'] = lambda: flush(reflush_button, data)

    def quit_window(icon: pystray.Icon):
        icon.stop()
        root.destroy()

    def show_window():
        root.deiconify()

    def on_exit():
        root.withdraw()

    root.protocol('WM_DELETE_WINDOW',on_exit)
    menu = (MenuItem('显示', show_window, default=True), Menu.SEPARATOR, MenuItem('退出', quit_window))
    image = Image.open("static/earth.png")
    icon = pystray.Icon("icon", image, "向日葵8号动态桌面", menu)
    threading.Thread(target=icon.run, daemon=True).start()
    root.mainloop()

if __name__ == '__main__':
    main()

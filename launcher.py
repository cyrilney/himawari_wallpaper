import tkinter as tk
from himawari8 import Himawari8

def flashDestTop():
    hima = Himawari8()
    hima.work()

if __name__ == '__main__':
    window = tk.Tk()
    window.title('Himawari8 dasktop.')
    window.geometry('500x300')
    # 壁纸设置按钮
    b = tk.Button(window, text="hit me", command=flashDestTop)
    b.pack()

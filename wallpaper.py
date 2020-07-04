from PIL import Image
import win32gui
import win32con
import win32api
import re
import sys
import os


class IWallPaperSetter():
    def setWallPaper(self, filePath):
        pass

class Win32WallPaperSetter(IWallPaperSetter):
    """docstring for Win32WallPaperSetter."""

    def setWallpaper(self, imagepath):
        k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2") 
        win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,imagepath, 1+2)

    def setWallPaperBMP(self, imagePath):
        bmpImage = Image.open(imagePath)
        newPath = imagePath.replace('.png', '.bmp')
        bmpImage.save(newPath, "BMP")
        self.setWallpaper(newPath)

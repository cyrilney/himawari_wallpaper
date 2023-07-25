import os


class IWallPaperSetter():
    def setWallPaper(self, filePath):
        pass


class Win32WallPaperSetter(IWallPaperSetter):

    def __setWallpaper(self, imagepath):
        import win32gui
        import win32con
        import win32api
        k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "4")
        win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, imagepath, 1 + 2)

    def setWallPaper(self, imagePath):
        from PIL import Image
        bmpImage = Image.open(imagePath)
        newPath = imagePath.replace('.png', '.bmp')
        bmpImage.save(newPath, "BMP")
        self.__setWallpaper(newPath)


class MacOsWallPaperSetter(IWallPaperSetter):
    def setWallPaper(self, imagePath):
        cmdstr = "osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"%s\"'" % imagePath
        f = os.popen(cmdstr)
        print(f.read())

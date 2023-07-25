import sys
import urllib
import urllib.request
import ssl
import datetime
import time
import os
from wallpaper import Win32WallPaperSetter
import PIL.Image as Image
from apscheduler.schedulers.background import BackgroundScheduler
from consts import HimawariPreference as Preference


class Himawari8(object):

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.work, 'interval', minutes=Preference.HIMA_REFLUSH_INTERVAL_MINUTES)
        # 启动后暂停 方便之后开启
        self.scheduler.start()
        self.scheduler.pause()

    def start(self):
        self.scheduler.resume()

    def stop(self):
        self.scheduler.pause()

    def _getImg(self, url, filename):
        fp = open(filename, 'wb')
        try:
            print("begin to download url: %s, filename: %s" %(url, filename))
            context = ssl._create_unverified_context()
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request, timeout=20, context=context)
            img = response.read()
            fp.write(img)
            print("download file %s" %filename)
        except:
            print('download filename %s error!' %filename)
            raise
        finally:
            fp.close()

    def _mergeImg(self, imagefiles, saveName):
        IMAGE_SIZE = 550
        print('save image begin...')
        if len(imagefiles) != 4 or len(imagefiles[0]) != 4 or len(imagefiles[1]) != 4 or len(imagefiles[2]) != 4 or len(imagefiles[3]) != 4:
            print('error save error. image not enough.')
            return 0

        to_image = Image.new('RGB', (4 * IMAGE_SIZE, 4 * IMAGE_SIZE)) #创建一个新图

        for row in range(0, 4):
            for col in range(0, 4):
                from_image = Image.open(imagefiles[row][col])
                to_image.paste(from_image, (row * IMAGE_SIZE, col * IMAGE_SIZE))
        # 保存图片
        to_image.save(saveName)
        print('save image end.')
        return 1

    def work(self):

        PATH = os.getcwd()
        querytime = datetime.datetime.now() - datetime.timedelta(hours=8,minutes=20)
        querytime = datetime.datetime(year=querytime.year, month=querytime.month, day=querytime.day, hour=querytime.hour, minute=int(querytime.minute/10)*10, second=0)
        querystr = querytime.strftime('%Y/%m/%d/%H%M%S')

        # 下载文件
        imagefiles = [[],[],[],[]]
        for row in range(0, 4):
            for col in range(0, 4):
                url = (Preference.URL_PREFIX %(str(querystr), row, col))
                filename = os.path.join(PATH ,(Preference.DOWNLOAD_FILE_PREFIX %(querystr[-6:], row, col)))

                try_cnt = 0
                while try_cnt < Preference.WGET_IMAGE_RETRY:
                    try:
                        self._getImg(url,filename)
                        imagefiles[row].append(filename)
                    except Exception as err:
                        print("download " + filename + " error:")
                        print(err)
                        try_cnt += 1
                        continue
                    break

        # 合并图像
        savename = os.path.join(PATH, (Preference.SAVE_NAME_PREFIX % querystr[-6:]))
        if self._mergeImg(imagefiles, savename):
            wallPaserSetter = self.getWallPaperSetterByOs()
            wallPaserSetter.setWallPaper(savename)

        time.sleep(10)  # 等待10s保证 文件存在

        for filename in os.listdir():
           l = os.path.splitext(filename)
           if 'hima' in l[0] and l[1] in ('.jpg','.png','.JPG','.PNG','.bmp'):
               os.remove(filename)


    def getWallPaperSetterByOs(self):  # 目前只支持 MacOs 和 Windows系统
        if sys.platform == 'darwin':
            from wallpaper import MacOsWallPaperSetter
            return MacOsWallPaperSetter()
        else:
            from wallpaper import Win32WallPaperSetter
            return Win32WallPaperSetter()

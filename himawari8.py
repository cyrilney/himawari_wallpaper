import urllib
import urllib.request
import ssl
import datetime
import os
from wallpaper import Win32WallPaperSetter
import PIL.Image as Image
from threading import Timer


class Himawari8(object):

    def __init__(self):
        self.scheduler = Timer(600, self.work)

    def start(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.cancel()

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

        RETRY = 3

        # 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/4d/550/2020/10/14/065000_3_0.png'
        #  http://himawari8-dl.nict.go.jp/himawari8/img/D531106/4d/550/2020/10/14/070000_2_0.png
        # 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/4d/550/2020/10/14/070000_0_0.png'
        URL_PREFIX = 'https://himawari8-dl.nict.go.jp/himawari8/img/D531106/4d/550/%s_%d_%d.png'
        DOWNLOAD_FILE_PREFIX = 'himawari8_earch_%s_%d_%d.png'
        PATH = os.getcwd()
        querytime = datetime.datetime.now() - datetime.timedelta(hours=8,minutes=20)
        querytime = datetime.datetime(year=querytime.year, month=querytime.month, day=querytime.day, hour=querytime.hour, minute=int(querytime.minute/10)*10, second=0)
        querystr = querytime.strftime('%Y/%m/%d/%H%M%S')

        # 下载文件
        imagefiles = [[],[],[],[]]
        for row in range(0, 4):
            for col in range(0, 4):
                url = (URL_PREFIX %(str(querystr), row, col))
                filename = os.path.join(PATH ,(DOWNLOAD_FILE_PREFIX %(querystr[-6:], row, col)))

                try_cnt = 0
                while try_cnt < RETRY:
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
        savename = os.path.join(PATH, ('himawari8_earch_big_%s.png' % querystr[-6:]))
        if self._mergeImg(imagefiles, savename):
            # pass
            wallPaserSetter = Win32WallPaperSetter()
            wallPaserSetter.setWallPaperBMP(savename)

        for filename in os.listdir():
           l = os.path.splitext(filename)
           if 'hima' in l[0] and l[1] in ('.jpg','.png','.JPG','.PNG','.bmp'):
               os.remove(filename)

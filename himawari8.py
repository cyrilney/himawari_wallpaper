import urllib
import urllib.request
import datetime
from wallpaper import Win32WallPaperSetter
import PIL.Image as Image


class Himawari8:

    def getImg(self, url, filename):
        fp = open(filename, 'wb')
        try:
            print("begin to download url: %s, filename: %s" %(url, filename))
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request, timeout=60)
            img = response.read()
            fp.write(img)
            print("download file %s" %filename)
        except:
            print('download filename %s error!' %filename)
            raise
        finally:
            fp.close()

    def mergeImg(self, imagefiles, saveName):
        IMAGE_SIZE = 550
        print('save image begin...')
        if len(imagefiles) != 4 or len(imagefiles[0]) != 4 or len(imagefiles[1]) != 4 or len(imagefiles[2]) != 4 or len(imagefiles[3]) != 4:
            print('error save error. image not enough.')
            return

        to_image = Image.new('RGB', (4 * IMAGE_SIZE, 4 * IMAGE_SIZE)) #创建一个新图

        for row in range(0, 4):
            for col in range(0, 4):
                from_image = Image.open(imagefiles[row][col])
                to_image.paste(from_image, (row * IMAGE_SIZE, col * IMAGE_SIZE))
        # 保存图片
        to_image.save(saveName)
        print('save image end.')

    def work(self):

        # http://himawari8-dl.nict.go.jp/himawari8/img/D531106/4d/550/2020/06/18/085000_0_0.png
        URL_PREFIX = 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/4d/550/%s_%d_%d.png'
        DOWNLOAD_FILE_PREFIX = 'himawari8_earch_%s_%d_%d.png'
        querytime = datetime.datetime.now() - datetime.timedelta(hours=8,minutes=30)
        querytime = datetime.datetime(year=querytime.year, month=querytime.month, day=querytime.day, hour=querytime.hour, minute=int(querytime.minute/10)*10, second=0)
        querystr = querytime.strftime('%Y/%m/%d/%H%M%S')

        # 下载文件
        imagefiles = [[],[],[],[]]
        for row in range(0, 4):
            for col in range(0, 4):
                url = (URL_PREFIX %(str(querystr), row, col))
                filename = (DOWNLOAD_FILE_PREFIX %(querystr[-6:], row, col))
                try:
                    self.getImg(url,filename)
                    imagefiles[row].append(filename)
                except Exception as err:
                    print("download " + filename + " error:")
                    print(err)

        # 合并图像

        savename = ('himawari8_earch_big_%s.png' % querystr[-6:])
        self.mergeImg(imagefiles, savename)

        wallPaserSetter = Win32WallPaperSetter()
        wallPaserSetter.setWallpaper(savename)


if __name__ == '__main__':
    hima = Himawari8()
    hima.work()

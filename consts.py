
class LaucherConsts: # laucher.py 相关文案
    LAUCHER_OPEN_BUTTON_TEXT = '开启'
    LAUCHER_CLOSE_BUTTON_TEXT = '关闭'
    LAUCHER_WORKING_BUTTON_TEXT = '处理中...'
    LAUCHER_REFLUSH_BUTTON_TEXT = '更新桌面'
    LAUCHER_REFLUSH_SUCCESS_MESSAGE = '桌面更新成功！'


class HimawariPreference: # 向日葵八号相关配置
    HIMA_REFLUSH_INTERVAL_MINUTES = 10
    WGET_IMAGE_RETRY = 3  # 图片重试次数
    # 文件目录， url格式 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/4d/550/2020/10/14/065000_3_0.png'
    URL_PREFIX = 'https://himawari8-dl.nict.go.jp/himawari8/img/D531106/4d/550/%s_%d_%d.png'
    DOWNLOAD_FILE_PREFIX = 'himawari8_earch_%s_%d_%d.png'
    SAVE_NAME_PREFIX 'himawari8_earch_big_%s.png'

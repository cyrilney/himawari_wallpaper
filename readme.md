## Himawari 壁纸脚本
气象卫星更新脚本：定期将气象卫星设置为壁纸

### 环境（运行源码需要 Python3）

#### 导包
* pillow 用于图像处理， 定时任务apscheduler，win操作库pywin32

        pip3 install pillow==9.5.0 apscheduler pystray

* **Windows 操作系统, 需通过注册表修改壁纸**
  
        pip3 install pywin32

#### 修改历史

* 支持MacOS操作系统


* 版本0.0.1 设置初始壁纸。 没有定时设置功能。

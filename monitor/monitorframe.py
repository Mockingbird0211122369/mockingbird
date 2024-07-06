from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog
from monitor.page2 import Ui_Dialog
from monitor.Video import Video


class MonitorDialog(QDialog):
    fileSelected = QtCore.pyqtSignal(str)  # 用于处理文件选择的信号

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.fileSelected.connect(self.onFileSelected)
        self.th1 = None

        # 连接按钮点击事件到openFileDialog方法
        self.ui.pushButton.clicked.connect(self.openFileDialog)

    def startVideo(self, video_path):
        if self.th1:
            self.th1.stop()
        self.th1 = Video(video_path)
        self.th1.send.connect(self.showimg)
        self.th1.start()
        print("视频线程已启动")

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "选择视频文件", "",
                                                  "视频文件 (*.mp4 *.avi *.mov);;所有文件 (*)", options=options)
        if fileName:
            self.fileSelected.emit(fileName)

    def onFileSelected(self, filePath):
        self.startVideo(filePath)

    def showimg(self, h, w, c, b, th_id, num):
        try:
            print(f"收到帧：{h}x{w}x{c}, 线程ID：{th_id}, 车辆数量：{num}")

            # 从字节创建QImage
            image = QImage(b, w, h, w * c, QImage.Format_BGR888)

            if image.isNull():
                print("从字节创建QImage失败")
                return

            pix = QPixmap.fromImage(image)

            if pix.isNull():
                print("从QImage创建QPixmap失败")
                return

            # 更新UI
            width = self.ui.label.width()
            height = self.ui.label.height()
            scale_pix = pix.scaled(width, height, Qt.KeepAspectRatio)
            self.ui.label.setPixmap(scale_pix)
            self.ui.label_2.setText(str(num))
        except Exception as e:
            print(f"显示图像时出错: {e}")

    def closeEvent(self, event):
        if self.th1:
            self.th1.stop()
            print("视频线程已停止")
        event.accept()

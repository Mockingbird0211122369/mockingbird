import cv2 as cv
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from monitor.page3 import Ui_Dialog  # 导入生成的 UI 文件
from AI.car2 import car_recognition

# 新的对话框类，用于显示处理后的图像
class CarRecognitionDialog(QDialog):
    def __init__(self):
        super().__init__()

        # 设置 UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # 连接按钮点击事件到槽函数
        self.ui.pushButton.clicked.connect(self.load_image)

    def load_image(self):
        # 打开文件资源管理器选择文件
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图片文件", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            # 读取图像并调用车流识别函数
            img = cv.imread(file_name)
            if img is None:
                print("Error: Unable to load image.")
                return

            # 调用car_recognition函数，并获取返回的品牌、分数和年份
            processed_img, brand, score, year = car_recognition(img)

            # 将处理后的图像转换为 QImage，并在标签上显示
            height, width, channel = processed_img.shape
            bytes_per_line = 3 * width
            q_img = QImage(processed_img.data, width, height, bytes_per_line, QImage.Format_BGR888)
            self.ui.label.setPixmap(QPixmap.fromImage(q_img))

            # 将品牌、分数和年份设置到对应的标签中
            self.ui.label_2.setText(f"品牌: {brand}")
            self.ui.label_3.setText(f"分数: {score}")
            self.ui.label_4.setText(f"年份: {year}")

# 创建并显示对话框
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    dialog = CarRecognitionDialog()
    dialog.show()
    sys.exit(app.exec_())

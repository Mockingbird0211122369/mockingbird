import cv2 as cv
from PyQt5.QtCore import QThread, pyqtSignal
from AI.car import vehicle_detect

class Video(QThread):
    send = pyqtSignal(int, int, int, bytes, int, int)  # emit

    def __init__(self, video_id):
        super().__init__()
        self.th_id = 0
        if video_id == 'data/vd1.mp4':
            self.th_id = 1
        elif video_id == 'data/vd2.mp4':
            self.th_id = 2
        else:
            self.th_id = 3  # Add more cases if you have more videos
        self.dev = cv.VideoCapture(video_id)
        if not self.dev.isOpened():
            print(f"Failed to open video file: {video_id}")
        else:
            print(f"Video file {video_id} opened successfully")

    def run(self):
        while self.dev.isOpened():
            try:
                ret, frame = self.dev.read()
                if not ret:
                    print('未接收到帧或视频已结束。')
                    break  # 如果未接收到帧则退出循环
                frame, num = vehicle_detect(frame)
                h, w, c = frame.shape
                img_bytes = frame.tobytes()
                self.send.emit(h, w, c, img_bytes, self.th_id, num)
                QThread.msleep(30)  # 睡眠以控制帧率
                print('输出一帧')
            except Exception as e:
                print(f"读取帧时出错: {e}")
                break

    def stop(self):
        print("停止视频线程")
        self.dev.release()
        self.quit()
        self.wait()

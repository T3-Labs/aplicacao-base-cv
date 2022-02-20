import cv2

from PyQt5.QtCore import QThread
from time import sleep
from PyQt5 import QtCore


class Camera(QThread):
    sendFrame = QtCore.pyqtSignal(object)

    def __init__(self, video_path) -> None:
        super().__init__()
        self.video_path = video_path

    def video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        return cap

    def run(self) -> None:
        """
        Parameters
        ----------
        video: None for read cam
        Video: video file path for read video file
        """
        if self.video_path:
            cap = self.video(self.video_path)
        else:
            cap = self.video(0)

        fps = cap.get(cv2.CAP_PROP_FPS)
        while(cap.isOpened() and self.isInterruptionRequested() is not True):
            ret, frame = cap.read()
            if frame is not None:
                self.sendFrame.emit(frame)
            sleep(1/fps)
        cap.release()

    def set_camera_configs(self, width, height):
        self.camera.Width.SetValue(width)
        self.camera.Width.SetValue(height)
    
    def __del__(self):
        self.requestInterruption()
        self.wait()

#Interface de Comunicação com a Camera

#Calibração


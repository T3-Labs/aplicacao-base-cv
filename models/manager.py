
from typing import NoReturn
from models.qmqt import QMQT
from models.detector import Detector
from models.camera import Camera
from models.postprocess import PostProcess
from PyQt5.QtCore import QObject

class Manager(QObject):

    def __init__(self, video_path) -> NoReturn:
        super().__init__()
        self.cam = Camera(video_path)
        self.inference = Detector()
        self.postprocess = PostProcess()

        self.cam.sendFrame.connect(self.inference.receiveFrame)
        self.inference.sendInferences.connect(self.postprocess.receiveInferences)
        


    def start(self) -> NoReturn:
        self.postprocess.start()
        self.inference.start()
        self.cam.start()
        

    

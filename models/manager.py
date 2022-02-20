
from typing import NoReturn
from models.qmqt import QMQT
from models.detector import Detector
from models.camera import Camera
from models.postprocess import PostProcess

class Manager():

    def __init__(self, video_path) -> NoReturn:
        self.frameQueue = QMQT(buffer = 1)
        self.inferenceQueue = QMQT(buffer = 1)
        self.resultsQueue = QMQT(buffer = 1)
        self.cam = Camera(video_path, self.frameQueue)
        self.inference = Detector(self.frameQueue, self.inferenceQueue)
        self.postprocess = PostProcess(self.inferenceQueue, self.resultsQueue)
        


    def run(self) -> NoReturn:
        self.inference.start()
        self.cam.start()
        self.postprocess.start()

    

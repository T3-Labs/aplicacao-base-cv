
from typing import NoReturn
from models.qmqt import QMQT
from models.detector import Detector
from models.camera import Camera
from models.postprocess import PostProcess

class Manager():

    def __init__(self, video_path) -> NoReturn:
        self.frameQueue = QMQT(buffer = 5)
        self.inferenceQueue = QMQT(buffer = 5)
        self.videoQueue = QMQT(buffer = 5)
        self.resultsQueue = QMQT(buffer = 5)
        self.inference = Detector(self.frameQueue, self.inferenceQueue)
        self.postprocess = PostProcess(self.videoQueue, self.inferenceQueue, self.resultsQueue)
        self.cam = Camera(video_path, self.frameQueue, self.videoQueue)


    def run(self) -> NoReturn:
        self.inference.start()
        self.cam.start()
        self.postprocess.start()

    

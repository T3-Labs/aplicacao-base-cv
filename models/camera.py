import cv2

from PyQt5.QtCore import QThread
from models.calibrate import Calibrate
from time import sleep
#from pypylon import pylon


class Camera(QThread):

    def __init__(self, video_path, frameQueue, videoQueue) -> None:
        super().__init__()
        self.video_path = video_path
        self.frameQueue = frameQueue
        self.videoQueue = videoQueue

    
    def capture(self):
        cap = cv2.VideoCapture(0)
        return cap
    
    def video(self, video_path: str):
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
            cap = self.capture()
        while(cap.isOpened() and self.isInterruptionRequested() is not True):
            ret, frame = cap.read()
            if frame is not None:
                self.frameQueue.collect(frame)
                self.videoQueue.collect(frame)
            else:
                pass

            sleep(1/17)
        cap.release()

    def init_camera(self):
        #self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        #return self.camera
        ...

    def set_camera_configs(self, width, height):
        self.camera.Width.SetValue(width)
        self.camera.Width.SetValue(height)
    
    def converter_to_bgr(self):
        #converter = pylon.ImageFormatConverter()
        #converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        #converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        #return converter
        ...

    def dummy(self, width: int, height: int) -> None: #NOTE Função run para a camera Basler, ainda não testada!
        camera = self.init_camera()
        self.set_camera_configs(width, height)
        converter = self.converter_to_bgr()
        while camera.IsGrabbing():
            #grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            #if grabResult.GrabSucceeded():
                #image = converter.Convert(grabResult)
                #img = image.GetArray()
                cv2.namedWindow('Basler', cv2.WINDOW_NORMAL)
                #cv2.imshow('Frame', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            #grabResult.Release()
        camera.StopGrabbing()

        cv2.destroyAllWindows()

    def __del__(self):
        self.requestInterruption()
        self.wait()

#Interface de Comunicação com a Camera

#Calibração


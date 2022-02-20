from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore
import sys
import numpy as np
import cv2
from models.drawner import Drawner
from models.tracker import Tracker
from shapely.geometry import LineString
from queue import Queue

class PostProcess(QThread):

    sendFrame = pyqtSignal(object)
    sendCount = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self.tracker = Tracker(3, 1, 30)
        self.count_objs = 0
        self.colors = [
                        (255, 0, 0), (0, 255, 0), (10, 240, 120),
                        (255, 255, 0),(0, 255, 255), (255, 0, 255),
                        (255, 127, 255),(127, 0, 255), (127, 0, 127)
                        ]
        self.inferenceQueue = Queue(1)

    @staticmethod
    def _extract_roi_coords(bbox: tuple)-> np.array:
        x, y, w, h = bbox
        x, y, w, h = int(abs(x)), int(abs(y)), int(abs(w)), int(abs(h))
        roi_coords = x, y, x+w, y+h
        return roi_coords
        
    @staticmethod
    def _binarizer(image: np.array, roi_coords: tuple)-> np.array:
        if image.size != 0:
            x_min, y_min, x_max, y_max = roi_coords
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = gray[x_min: x_max, y_min: y_max]
            ret, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_OTSU)
            return thresh
        else:
            return image
    
    @staticmethod
    def _edges(image: np.array)-> np.array:
        if image.size != 0 or image is not None:
            blurred = cv2.GaussianBlur(image, (3, 3), cv2.BORDER_DEFAULT)
            grad = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            gradient = cv2.morphologyEx(blurred, cv2.MORPH_GRADIENT, grad)
            edges = cv2.Canny(image=image, threshold1=50, threshold2=200)
            return gradient
        else:
            return image

    @staticmethod
    def _hull(thresh_img: np.array, roi_coords: tuple)-> np.array:
        if thresh_img.size != 0 :
            contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            if contours:
                c = max(contours, key = cv2.contourArea)
                hull = cv2.convexHull(c)
                return hull, contours
            else:
                return []
        else:
            return ()

    @staticmethod    
    def centroid(results: list)-> tuple:
        centers = []        
        for result in results:
            bbox = result[0]
            centerCoord = (int(bbox[0]+(bbox[2]/2)), int(bbox[1]+(bbox[3]/2)))
            centers.append(centerCoord)
        return centers


    @staticmethod
    def extract_bbox(results: list)->tuple:
        if results[-1] != "Unknown":
            bboxes = list(map(lambda x: x[0], results))
        else:
            bboxes = None
        return bboxes

    
    def postprocess(self, image: np.array, results: list, method: str = "bbox")-> np.array:
        hull = 0
        contours = 0
        threah_roi = 0
        for result in results:
            bbox = result[0]
            label = result[-1]
            image = Drawner.draw_bbox(image, bbox, label)
        return image

    @staticmethod
    def extract_points(tracker):
        points = []
        for i in range(len(tracker.tracks)):
            if (len(tracker.tracks[i].trace) > 1):
                for j in range(len(tracker.tracks[i].trace) - 1):
                    x_max_y_max = tracker.tracks[i].trace[j + 1][0][0].tolist()
                    x2, y2 = x_max_y_max[0]
                    points.append((x2, y2))
        return points

    def get_trace_from_object(self):
        ...

    def tracker_obj(self, frame: np.array, tracker: list, colors: list):
        H, W = frame.shape[:2]
        cv2.line(frame, (W//2, 0), (W //2, H), (0, 255, 0), 2)
        for i in range(len(tracker.tracks)):
            if (len(tracker.tracks[i].trace) > 1):
                clr = tracker.tracks[i].track_id % 9
                for j in range(len(tracker.tracks[i].trace) - 1):
                    x_min_y_min = tracker.tracks[i].trace[j][0][0].tolist()
                    x_max_y_max = tracker.tracks[i].trace[j + 1][0][0].tolist()
                    x1, y1 = x_min_y_min[0]
                    x2, y2 = x_max_y_max[0]
                    cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), colors[clr], 2)
                
                if tracker.tracks[i].counted == False:
                    matrix_1 = tracker.tracks[i].trace[0][0].tolist()
                    matrix_2 = tracker.tracks[i].trace[-1][-1].tolist()
                    p1 = tuple(matrix_1[0])
                    p2 = tuple(matrix_2[0])
                    line1 = LineString([p1, p2])
                    line2 = LineString([(W//2, 0), (W //2, H)])
                    if line1.intersects(line2):
                        self.count_objs+=1
                        tracker.tracks[i].counted = True
                        cv2.line(frame, (W//2, 0), (W //2, H), (0, 0, 255), 2)
                    else:
                        continue

                    
        return frame


    def receiveInferences(self, inferences):
        if inferences is not None:
            self.inferenceQueue.put(inferences)

    def run(self):
        frameCounter = 0
        while not self.isInterruptionRequested():
            if self.inferenceQueue.qsize()>0:
                results, frame = self.inferenceQueue.get()
                centroIDS = self.centroid(results)
                img = frame.copy()
                #if centroIDS:
                #    if frameCounter % 2 == 0:
                #        self.tracker.Update(centroIDS)
                #img = self.tracker_obj(frame, self.tracker, self.colors)

                img = self.postprocess(img, results)

                self.sendFrame.emit(img)
                self.sendCount.emit(self.count_objs)
            else:
                self.yieldCurrentThread()



    def __del__(self):
        self.requestInterruption()
        self.wait()

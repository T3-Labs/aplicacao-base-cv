from PyQt5.QtCore import QThread
from PyQt5 import QtCore
import sys
import numpy as np
import cv2
from models.drawner import Drawner
from models.tracker import Tracker
from shapely.geometry import LineString


class PostProcess(QThread):

    def __init__(self, videoQueue, inferenceQueue, resultsQueue) -> None:
        super().__init__()
        self.videoQueue = videoQueue
        self.inferenceQueue = inferenceQueue
        self.resultsQueue = resultsQueue
        self.tracker = Tracker(3, 1, 30)
        self.count_objs = 0
        self.allMeasurement = 0
        self.colors = [
                        (255, 0, 0), (0, 255, 0), (10, 240, 120),
                        (255, 255, 0),(0, 255, 255), (255, 0, 255),
                        (255, 127, 255),(127, 0, 255), (127, 0, 127)
                        ]


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
        measurements = []
        if results[-1]!="Unknown":
            for result in results:
                bbox = result[0]
                measurement = result[-1][0]
                centerCoord = (int(bbox[0]+(bbox[2]/2)), int(bbox[1]+(bbox[3]/2)))
                centers.append(centerCoord)
                measurements.append(measurement)
            return centers, measurements
        else:
            return []


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
        if results[-1] != "Unknown":
            for result in results:
                bbox = result[0]
                label = result[-1]
                image = Drawner.draw_bbox(image, bbox, label)
            return image
        else:
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
                plateWidth = tracker.tracks[i].measurement[0]/10
                plateHeight = tracker.tracks[i].measurement[1]/10
                plateWidth = float("{:.2f}".format(plateWidth))
                plateHeight = float("{:.2f}".format(plateHeight))
                cv2.putText(frame, f"{plateWidth}cm X {plateHeight}cm", (int(x1), int(y1)), 0, 1 / 2.5, [110, 255, 10], thickness=1, lineType=cv2.LINE_AA)
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
                        self.allMeasurement+= (tracker.tracks[i].measurement[0]/10)*(tracker.tracks[i].measurement[1]/10)
                        cv2.line(frame, (W//2, 0), (W //2, H), (0, 0, 255), 2)
                    else:
                        continue

                    
        return frame


    def run(self):
        frameCounter = 0
        while not self.isInterruptionRequested():
            if self.videoQueue.get_size()>0:
                frame = self.videoQueue.cat()
                results = self.inferenceQueue.cat()
                centroIDS, measurements = self.centroid(results)
                img = frame.copy()
                H, W = img.shape[:2]
                if centroIDS:
                    if frameCounter % 2 == 0:
                        self.tracker.Update(centroIDS, measurements)
                img = self.tracker_obj(frame, self.tracker, self.colors)
                cv2.putText(img, f"{self.count_objs}", (W-40, H - H +40), 0, 2 / 3, [0, 255, 10], thickness=1, lineType=cv2.LINE_AA)
                self.resultsQueue.collect([img, self.count_objs, self.allMeasurement])
            

    def __del__(self):
        self.requestInterruption()
        self.wait()

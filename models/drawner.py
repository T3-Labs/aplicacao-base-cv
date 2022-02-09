import cv2
import numpy as np
import random

class Drawner:

    def __init__(self) -> None:
        ...

    @staticmethod
    def plot_one_box(x, image, line_thickness=None):
        color = (255, 110, 50)
        tl = line_thickness or round(0.002 * (image.shape[0] + image.shape[1]) / 2) + 1
        top_left = int(x[0]), int(x[1])
        bottom_right = int(x[0]+x[2]), int(x[1]+x[3])
        centerCoord = (int(x[0]+(x[2]/2)), int(x[1]+(x[3]/2)))
        cv2.circle(image, centerCoord, 2, (0, 0, 255), -1)
        cv2.rectangle(image, top_left, bottom_right, color, thickness=tl, lineType=cv2.LINE_AA)
        return image
    
    @staticmethod
    def draw_label(frame: np.array, bbox: tuple, label: str)-> np.array:
        x1, y1, _, _ = bbox
        x1 = int(x1)
        y1 = int(y1)
        tl = 2
        tf = max(tl - 1, 1)  
        cv2.putText(frame, label, (x1, y1 - 2), 0, tl / 3, [0, 255, 10], thickness=tf, lineType=cv2.LINE_AA)
        return frame

    @classmethod
    def draw_bbox(self, frame: np.array, bbox: tuple, label: str = None)-> np.array:
        x1, y1, x2, y2 = bbox
        frame = self.plot_one_box([x1,y1,x2,y2], frame, line_thickness=2)
        if label:
            frame = self.draw_label(frame, bbox, label)
            return frame
        else:
            return frame        

    @classmethod
    def draw_contour(self, frame: np.array, contours: np.array)-> np.array:
        if type(contours) is not list:
            cv2.polylines(frame, [contours], color=(255, 110, 50), isClosed=True, thickness=2)
            return frame
        else:
            return frame
    
    @classmethod
    def make_line(self, frame):
        H, W = frame.shape[:2]
        cv2.line(frame, (0, H // 2), (W, H // 2), (0, 0, 255), 2)
        return frame

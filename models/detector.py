#External
from PyQt5.QtCore import QThread
import cv2
import numpy as np
from dotenv import load_dotenv, find_dotenv
#Built-In
import os
from pathlib import Path
from time import time


class Detector(QThread):

    def __init__(self, frameQueue, resultQueue) -> None:
        super().__init__()
        load_dotenv(find_dotenv())
        weights = os.getenv("WEIGHTS_PATH")
        cfg = os.getenv("CFG_PATH")
        self.labels = self._load_labels(os.getenv("LABELS_PATH"))
        self.model = cv2.dnn.readNetFromDarknet(str(cfg), str(weights))
        self.model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        self.layers_names = self._get_layers_names()
        self.conf_threshold = 0.5
        self.nms_threshold = 0.4
        self.frameQueue = frameQueue
        self.resultQueue = resultQueue

    @staticmethod
    def _load_labels(labels_path: str):

        with open(labels_path,'r') as labels_file:
            labels = labels_file.read()
        labels = labels.split("\n")
        labels = list(map(lambda x: x.strip(), labels))
        labels = dict({k: v for k, v in enumerate(labels)})
        labels.update({-1: 'Unknown'})
        return labels

    def _get_layers_names(self):
        layers_names = self.model.getLayerNames()
        layers_names = [layers_names[i-1] for i in self.model.getUnconnectedOutLayers()]
        return layers_names

    def inference(self, inputs)-> np.array:
        if not isinstance(inputs, np.ndarray) and len(inputs) == 1:
            inputs = inputs.pop()

        blob = cv2.dnn.blobFromImage(inputs, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)
        self.model.setInput(blob)
        layerOutputs = self.model.forward(self.layers_names)
        Width = inputs.shape[1]
        Height = inputs.shape[0]

        class_ids = []
        confidences = []
        boxes = []
        detections = []
        for out in layerOutputs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.conf_threshold,
                                   self.nms_threshold)
                                   
        if len(indices) > 0:
            for i in indices:
                box = boxes[i]
                detections.append((box, confidences[i], self.labels[0]))
        return detections, inputs


    def run(self):
        while not self.isInterruptionRequested():
            if self.frameQueue.get_size()>0:
                item = self.frameQueue.cat()
                results = self.inference(item)
                self.resultQueue.collect(results)    
            else:
                pass
    
    def __del__(self):
        self.requestInterruption()
        self.wait()
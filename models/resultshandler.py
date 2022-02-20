from PyQt5.QtCore import QThread
from PyQt5 import QtCore
from queue import Queue


class ResultsHandler(QThread):
    
    sendFrame = QtCore.pyqtSignal(object)
    sendValuesToView = QtCore.pyqtSignal(object)
    sendValuesToDataIter = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.resultsQueue = Queue(5)
    
    def run(self):
        while not self.isInterruptionRequested():
            frame, obj_count = self.resultsQueue.cat()
            self.sendFrame.emit(frame)
            self.sendValuesToView.emit(obj_count)
            data = self.make_payload(obj_count)
            self.sendValuesToDataIter.emit(data)

    @staticmethod
    def make_payload(objects: int):
        data = dict()
        data["line"] = 1
        data["obj_quantity"] = objects
        return data


    def __del__(self):
        try: 
            self.sendFrame.disconnect()
            self.sendValuesToView.disconnect()
        except Exception as e:
            print(f"Warning: {e}")
            pass

        self.requestInterruption()
        self.wait()

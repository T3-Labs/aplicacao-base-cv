from models.manager import Manager
from views.view import MainWindow
from models.resultshandler import ResultsHandler
from PyQt5.QtCore import QObject


class MainController(QObject):

    def __init__(self) -> None:
        super().__init__()
        self.manager = Manager()
        #self.resultshandler = ResultsHandler()
        self.window = MainWindow()
        self.manager.postprocess.sendFrame.connect(self.window.show_frame)
        self.manager.postprocess.sendCount.connect(self.window.refresh_text)

    def run(self) -> None:
        #self.resultshandler.sendFrame.connect(self.window.show_frame)
        #self.resultshandler.sendValuesToView.connect(self.window.refresh_text)
        



        self.window.showFullScreen()
        #self.resultshandler.start()
        self.manager.start()

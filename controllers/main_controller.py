from PyQt5.QtCore import QObject

from models.manager import Manager
from models.resultshandler import ResultsHandler
from views.view import MainWindow


class MainController(QObject):

    def __init__(self) -> None:
        super().__init__()
        self.manager = Manager()
        self.window = MainWindow()
        self.manager.postprocess.sendFrame.connect(self.window.show_frame)
        self.manager.postprocess.sendCount.connect(self.window.refresh_text)

    def run(self) -> None:
        self.window.showMaximized()
        self.manager.start()

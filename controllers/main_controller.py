from models.manager import Manager
from views.view import MainWindow
from models.resultshandler import ResultsHandler
from controllers.dataiter import DataIter


class MainController():

    def __init__(self, video_path) -> None:
        self.menager = Manager(video_path)
        self.resultshandler = ResultsHandler(self.menager.resultsQueue)
        self.window = MainWindow()

    def run(self) -> None:
        self.resultshandler.sendFrame.connect(self.window.show_frame)
        self.resultshandler.sendValuesToView.connect(self.window.refresh_text)
        self.window.showFullScreen()
        self.resultshandler.start()
        self.menager.run()

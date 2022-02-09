from controllers.main_controller import MainController
import PyQt5
import sys
from PyQt5.QtCore import QLibraryInfo
import os

    
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)


if __name__=='__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    controller =  MainController(video_path="data/videos/placa_3.mp4")
    controller.run()
    sys.exit(app.exec_())


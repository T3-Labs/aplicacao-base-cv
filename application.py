import os
import sys

import PyQt5
from PyQt5.QtCore import QLibraryInfo

from controllers.main_controller import MainController

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)


if __name__=='__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    controller =  MainController()
    controller.run()
    sys.exit(app.exec_())


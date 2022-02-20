#external libraries
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFontDatabase
import sys

from scipy.optimize.optimize import main


class MainWindow(QtWidgets.QMainWindow):
    
    receiveValue = QtCore.pyqtSignal(object)
    
    def __init__(self) -> None:
        super().__init__()
        QFontDatabase.addApplicationFont("./settings/font/Aldrich-Regular.ttf")
        title = "Detector de objetos - DEMO"
        self.setStyleSheet("QMainWindow{background-color:#31363b} QWidget{background-color:#31363b;font-family: \"Aldrich\"; font-size: 18pt; color:#FFFFFF} QGraphicsView{background-color:#232629}")
        self.setWindowTitle(title)
        mainLayout = QtWidgets.QVBoxLayout()
    
        self.headerLayout = QtWidgets.QHBoxLayout()
        self.bodyLayout = QtWidgets.QGridLayout()
        
        headerWidget = QtWidgets.QWidget()
        headerWidget.setLayout(self.headerLayout)

        bodyWidget = QtWidgets.QWidget()
        bodyWidget.setLayout(self.bodyLayout)

        mainLayout.addWidget(headerWidget)
        mainLayout.addWidget(bodyWidget)
        
        qiconImage = QtGui.QImage("./views/logo.png")
        iconWidget = QtWidgets.QLabel()
        iconWidget.setPixmap(QtGui.QPixmap.fromImage(qiconImage))

        titleWidget = QtWidgets.QLabel(title)
        titleWidget.setStyleSheet('font-size: 24pt')

        self.headerLayout.addWidget(iconWidget, alignment=Qt.AlignmentFlag.AlignLeft)
        self.headerLayout.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum))
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.headerLayout.addWidget(line)
        self.headerLayout.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum))
        self.headerLayout.addWidget(titleWidget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.headerLayout.addItem(QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.headerLayout.addWidget(line)
        self.headerLayout.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum))

        

        self.graphicsView = QtWidgets.QGraphicsView()
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        self.bodyLayout.addWidget(self.graphicsView)
        
        self.textLayout = QtWidgets.QVBoxLayout()
        self.textWidget = QtWidgets.QWidget()
        self.textWidget.setLayout(self.textLayout)

        self.countWidget = QtWidgets.QLabel(f"Contagem\n\n 0")
        self.countWidget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.textLayout.addWidget(self.countWidget)

        self.headerLayout.addWidget(self.textWidget)
    
        widget = QtWidgets.QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)


    def show_frame(self, frame):
        self.scene.clear()
        qimage = QtGui.QImage(frame.data, 
                               frame.shape[1], 
                               frame.shape[0],  
                               QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qimage.rgbSwapped())
        pixmapItem = self.scene.addPixmap(pixmap)
        self.graphicsView.fitInView(pixmapItem, Qt.KeepAspectRatio)
    
    def refresh_text(self, value: list):
        self.countWidget.setText(f"Contagem\n\n {value}")

if __name__ == "__main__":

    app=QtWidgets.QApplication(sys.argv)
    window=MainWindow()
    window.showFullScreen()
    sys.exit(app.exec_())



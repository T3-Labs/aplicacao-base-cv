#external libraries
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, Qt
#import cv2 NOTE problemas com QT
#built-in libraries
import sys

from scipy.optimize.optimize import main


class MainWindow(QtWidgets.QMainWindow):
    
    receiveValue = QtCore.pyqtSignal(object)
    
    def __init__(self) -> None:
        super().__init__()
        title = "T3 Labs - Métricas de Produtividade"
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

        qiconImage = QtGui.QImage("./views/resized_logo.png")
        iconWidget = QtWidgets.QLabel()
        iconWidget.setPixmap(QtGui.QPixmap.fromImage(qiconImage))
        
        qiconImage2 = QtGui.QImage("./views/logo_fonte_preta.png")
        iconWidget2 = QtWidgets.QLabel()
        iconWidget2.setPixmap(QtGui.QPixmap.fromImage(qiconImage2))

        titleWidget = QtWidgets.QLabel(title)
        titleWidget.setStyleSheet('font-family: \"DejaVu Sans\"; font-size: 24pt')

        self.headerLayout.addWidget(iconWidget, alignment=Qt.AlignmentFlag.AlignLeft)
        self.headerLayout.addWidget(titleWidget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.headerLayout.addWidget(iconWidget2, alignment=Qt.AlignmentFlag.AlignRight)

        self.graphicsView = QtWidgets.QGraphicsView()
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        self.bodyLayout.addWidget(self.graphicsView)
        
        self.textLayout = QtWidgets.QVBoxLayout()
        self.textWidget = QtWidgets.QWidget()
        self.textWidget.setLayout(self.textLayout)

        self.countWidget = QtWidgets.QLabel(f"Contagem:\n\n 0")
        self.countWidget.setStyleSheet('font-family: \"DejaVu Sans\"; font-size: 18pt')
        self.countWidget.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.areaWidget = QtWidgets.QLabel("Área Total Produzida:")
        self.areaWidget.setStyleSheet('font-family: \"DejaVu Sans\"; font-size: 18pt')
        self.areaWidget.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.produtivityWidget = QtWidgets.QLabel("Area Útil:\n\n 30m²")
        self.produtivityWidget.setStyleSheet('font-family: \"DejaVu Sans\"; font-size: 18pt')
        self.produtivityWidget.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.textLayout.addWidget(self.countWidget)
        self.textLayout.addWidget(self.areaWidget)
        self.textLayout.addWidget(self.produtivityWidget)

        self.bodyLayout.addWidget(self.textWidget, 0, 1)
    
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
        self.countWidget.setText(f"Contagem:\n\n {value}")

if __name__ == "__main__":

    app=QtWidgets.QApplication(sys.argv)
    window=MainWindow()
    window.showFullScreen()
    sys.exit(app.exec_())



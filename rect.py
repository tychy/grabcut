import sys
from PyQt5 import QtWidgets, QtCore, QtGui, Qt
import cv2
import numpy as np
import matplotlib.pyplot as plt
class MainWindow:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()

        # The path to our image
        self.imagePath = "images/gcn.jpg"

        # we call our function initGui()
        self.initGui()
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()


        self.window.setGeometry(400, 100, 300, 500)
        self.window.setWindowTitle("QLabel and Image")
        self.window.setStyleSheet("border: 3px solid #4e4e4e; background-color:#6e6e6e")
        self.window.show()
        sys.exit(self.app.exec_())

    # create a function to initialize the GUI
    def initGui(self):
        # The two buttons apply and cancel
        self.applyBtn = QtWidgets.QPushButton("Apply", self.window)
        self.applyBtn.setGeometry(170, 420, 120, 30)
        self.applyBtn.setStyleSheet("background-color:#4e4e4e; color:#f7f7f7;")
        self.applyBtn.clicked.connect(self.calc)
        """
        self.cancelBtn = QtWidgets.QPushButton("Cancel", self.window)
        self.cancelBtn.setGeometry(10, 420, 120, 30)
        self.cancelBtn.setStyleSheet("background-color:#4e4e4e; color:#f7f7f7")
        """
        # The QLabel where we can display an Image
        self.label = QtWidgets.QLabel(self.window)
        self.label.setGeometry(0, 0, 300, 400)
        self.label.setStyleSheet("background-color:#ffffff")

        # The image
        self.image = QtGui.QImage(self.imagePath)
        self.pixmapImage = QtGui.QPixmap.fromImage(self.image)

        # display our image on the label
        self.label.setPixmap(self.pixmapImage)

        # frame our image on the label
        self.label.setScaledContents(True)

    def calc(self):
        print("culc")
        """
        image = Image.open(self.img)
        image = ImageOps.grayscale(image)
        image = image.filter(ImageFilter.GaussianBlur(3))
        data = np.asarray(image)
        fig = plt.figure()
        plt.contour(data)
        fig.savefig("result.png")
        self.button2.setIcon(QIcon("result.png"))
        """

        image = cv2.imread(self.imagePath)
        mask = np.zeros(image.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        rect = (50, 50, 250, 300)
        cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        image = image * mask2[:, :, np.newaxis]
        cv2.imwrite("result.png", image)
        self.image = QtGui.QImage("result.png")
        self.pixmapImage = QtGui.QPixmap.fromImage(self.image)
        self.label.setPixmap(self.pixmapImage)
        self.window.show()
        print("show")

main = MainWindow()
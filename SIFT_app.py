#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from python_qt_binding import loadUi

import cv2
import sys
import numpy as np

# Constructor for the My_App class.
# Initializes the application and sets up the user interface.
class My_App(QtWidgets.QMainWindow):
    def __init__(self):
        super(My_App, self).__init__()
        loadUi("./SIFT_app.ui", self)

        self._cam_id = 0
        self._cam_fps = 10
        self._is_cam_enabled = False
        self._is_template_loaded = False

        self.browse_button.clicked.connect(self.SLOT_browse_button)
        self.toggle_cam_button.clicked.connect(self.SLOT_toggle_camera)

        self._camera_device = cv2.VideoCapture(self._cam_id)
        self._camera_device.set(3, 320)
        self._camera_device.set(4, 240)

        # Timer used to trigger the camera
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.SLOT_query_camera)
        self._timer.setInterval(1000 / self._cam_fps)

    # Slot function triggered when the user clicks the browse button.
    # Opens a file dialog for selecting a template image file.
    def SLOT_browse_button(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if dlg.exec_():
            self.template_path = dlg.selectedFiles()[0]

        pixmap = QtGui.QPixmap(self.template_path)
        self.template_label.setPixmap(pixmap)
        print("Loaded template image file: " + self.template_path)

    # Slot function triggered when the user clicks the toggle camera button.
    # Starts or stops the camera stream.
    def SLOT_toggle_camera(self):
        if not self._is_cam_enabled:
            self._camera_device.open(self._cam_id)
            self._is_cam_enabled = True
            self.toggle_cam_button.setText("Stop Camera")
            self._timer.start()
        else:
            self._timer.stop()
            self._camera_device.release()
            self._is_cam_enabled = False
            self.toggle_cam_button.setText("Start Camera")

    # Slot function triggered by the timer to query camera frames.
    # Processes and displays camera frames as needed.
    def SLOT_query_camera(self):
        ret, frame = self._camera_device.read()
        if ret:
            # Process the camera frame here as needed
            # For example, you can display it in a QLabel widget
            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            qImg = QtGui.QImage(frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            self.camera_label.setPixmap(pixmap)

    # Converts an OpenCV image to a QPixmap.
    # @param cv_img: OpenCV image.
    # @return: QPixmap representation of the input image.
    def convert_cv_to_pixmap(self, cv_img):
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        height, width, channel = cv_img.shape
        bytesPerLine = channel * width
        q_img = QtGui.QImage(cv_img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        return QtGui.QPixmap.fromImage(q_img)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myApp = My_App()
    myApp.show()
    sys.exit(app.exec_())


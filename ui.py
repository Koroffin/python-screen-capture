from PyQt6 import QtWidgets, QtGui, QtCore
from PIL import ImageQt
import pygetwindow as gw
import sys
from lib import capture  # Import the capture function

class Window(QtWidgets.QWidget):
    screenshot_captured = QtCore.pyqtSignal(QtGui.QPixmap)
    def __init__(self):
        super().__init__()

        self.initUI()

        self.screenshot_captured.connect(self.set_screenshot)

    def initUI(self):
        self.setWindowTitle('Window Capture')

        # Create a dropdown for active windows
        self.dropdown = QtWidgets.QComboBox(self)
        self.dropdown.addItems([win.title for win in gw.getAllWindows() if win.title])

        # Create a button to capture the screenshot
        self.button = QtWidgets.QPushButton('Screenshot', self)
        self.button.clicked.connect(self.capture_screenshot)

        # Create a QLabel to display the screenshot
        self.image_label = QtWidgets.QLabel(self)

        # Create a layout and add the dropdown, button, and QLabel to it
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.dropdown)
        layout.addWidget(self.button)
        layout.addWidget(self.image_label)
    
    def PIL_to_qimage(self, pil_img):
        temp = pil_img.convert('RGBA')
        return QtGui.QImage(
            temp.tobytes('raw', "RGBA"),
            temp.size[0],
            temp.size[1],
            QtGui.QImage.Format.Format_RGBA8888
        )

    def capture_screenshot(self):
        try:
            # Call the capture function with the selected window title
            screenshot = capture(self.dropdown.currentText())

            # Convert the screenshot to a QPixmap
            qimage = self.PIL_to_qimage(screenshot)
            pixmap = QtGui.QPixmap.fromImage(qimage)

            if pixmap.isNull():
                print("Failed to convert screenshot to QPixmap")
                return

            # Emit the screenshot_captured signal with the pixmap
            self.screenshot_captured.emit(pixmap)
        except Exception as e:
            print(f"An error occurred: {e}")

    @QtCore.pyqtSlot(QtGui.QPixmap)
    def set_screenshot(self, pixmap):
        # Set the pixmap of the QLabel
        self.image_label.setPixmap(pixmap)

def main():
    app = QtWidgets.QApplication(sys.argv)

    win = Window()
    win.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
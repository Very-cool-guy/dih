from gui import editor
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.editor = editor.DihEditor()
        self.setCentralWidget(self.editor)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

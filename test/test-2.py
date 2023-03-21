from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

class SimpleBrowser:
    def __init__(self, file_path):
        self.app = QApplication([])
        self.view = QWebEngineView()
        self.view.load(QUrl.fromLocalFile(file_path))
        self.view.show()

    def run(self):
        self.app.exec_()

b = SimpleBrowser(r'C:\Users\User\Documents\GitHub\md-preview.py\README.md')
b.run()
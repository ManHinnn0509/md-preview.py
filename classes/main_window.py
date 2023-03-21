import os

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

from util.file_utils import read_file, send_request

class MainWindow:
    def __init__(self) -> None:
        self.app = QApplication([])
        self.browser = QWebEngineView()

        self.browser.setAcceptDrops(True)
        self.browser.dragEnterEvent = self.__drag_enter_event
        self.browser.dropEvent = self.__drop_event

        self.browser.setWindowTitle("GitHub README Renderer")
        self.browser.setHtml(self.__get_default_html())
    
    def start(self):
        self.browser.show()
        self.app.exec_()
    
    def __drag_enter_event(self, event):
        if (event.mimeData().hasUrls()):
            event.acceptProposedAction()

    def __drop_event(self, event):
        for url in event.mimeData().urls():
            if url.isLocalFile():
                filepath = url.toLocalFile()
                abs_filepath = os.path.abspath(filepath)
                if abs_filepath.endswith('.md'):
                    self.browser.setUrl(QUrl.fromLocalFile(abs_filepath))
                    event.acceptProposedAction()
                    self.__render(abs_filepath)
                    return
        
        event.ignore()

    def __render(self, abs_filepath: str):
        s = read_file(abs_filepath)
        if (s == None):
            print(f"[ERROR] Unable to read .md file from: [{abs_filepath}]")
            return

        token = os.getenv("GITHUB_TOKEN")
        html = send_request(s, token)

        if (html == None):
            print(f"[ERROR] Unable to render .md file from GitHub API")
            return

        self.browser.setHtml(html)

        

    def __get_default_html(self):
        html = f"""
        <h1>Drag and drop any .md file to here</h1>
        """

        return html

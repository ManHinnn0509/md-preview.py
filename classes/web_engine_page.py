import webbrowser

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage

class WebEnginePage(QWebEnginePage):
    def acceptNavigationRequest(self, url: QUrl, type: 'QWebEnginePage.NavigationType', isMainFrame: bool) -> bool:
        # return super().acceptNavigationRequest(url, type, isMainFrame)

        # If the scheme is data, which means it's a .md file
        # Should be from drag & drop
        if (url.scheme() == "data"):
            return True

        else:
            webbrowser.open(url.toString())
            return False
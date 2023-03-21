import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

app = QApplication(sys.argv)
view = QWebEngineView()

# view.load(QUrl.fromLocalFile("./README.md"))
view.setUrl(QUrl("https://codepen.io/jonneal/pen/vzPwWo"))

view.show()
sys.exit(app.exec_())

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView

app = QApplication([])
window = QMainWindow()
view = QWebEngineView()

html = """
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Example</title>
	<style>
		body {
			background-color: white;
			color: black;
		}
		
		.dark-mode body {
			background-color: black;
			color: white;
		}
	</style>
	<script>
		if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
			document.documentElement.classList.add('dark-mode');
		}
	</script>
</head>
<body>
	<h1>Hello world!</h1>
</body>
</html>
"""

view.setHtml(html, QUrl(''))
window.setCentralWidget(view)
window.show()
app.exec_()

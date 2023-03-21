import os

import requests as req

from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineScript

from util.file_utils import read_file

class MainWindow:
    def __init__(self, token: str, css_path: str) -> None:
        self.app = QApplication([])
        self.browser = QWebEngineView()

        self.token = token
        self.css_path = css_path
        self.css_content = read_file(css_path)
        print(self.css_content == None)

        self.browser.setAcceptDrops(True)
        self.browser.dragEnterEvent = self.__drag_enter_event
        self.browser.dropEvent = self.__drop_event

        self.browser.setWindowTitle("GitHub README Renderer")
        self.browser.setHtml(self.__get_default_html())
    
    def start(self):
        self.browser.show()
        self.app.exec_()

    def __render(self, abs_filepath: str):
        content = read_file(abs_filepath)
        if (content == None):
            print(f"[ERROR] Unable to read .md file from: [{abs_filepath}]")
            return

        r = req.post(
            url="https://api.github.com/markdown",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28"
            },
            json={
                "text": content
            }
        )
        if (r.status_code != 200):
            print(f"[ERROR] Unable to render markdown with GitHub API, reason: {r.reason}")
            return

        html = self.__format_html(r.text)
        self.browser.setHtml(
            # Load the rendered HTML
            html,
            # Kinda like set the current directory to where the dropped .md file is
            QUrl.fromLocalFile(abs_filepath)
        )
        
        # css files & load

        md_body_style = '''
            .markdown-body {
                box-sizing: border-box;
                min-width: 200px;
                max-width: 980px;
                margin: 0 auto;
                padding: 45px;
            }

            @media (max-width: 767px) {
                .markdown-body {
                    padding: 15px;
                }
            }

            /* This fix the weird image stretching */
            .markdown-body img {
                height: auto;
            }
        '''
        self.__load_css("github_css", self.css_content)
        self.__load_css("md_body", md_body_style)
        

    def __format_html(self, content: str):
        html = f'''
            <meta name="viewport" content="width=device-width, initial-scale=1">
            
            <article class="markdown-body">
                {content}
            </article>
        '''

        return html

    def __load_css(self, javascript_name, css_content):
        # Modified from: https://stackoverflow.com/a/51389886
        javascript = """
            (function() {
                css = document.createElement('style');
                css.type = 'text/css';
                css.id = "%s";
                document.head.appendChild(css);
                css.innerText = `%s`;
            }) ()
        """ % (javascript_name, css_content)

        script = QWebEngineScript()
        self.browser.page().runJavaScript(javascript, QWebEngineScript.ApplicationWorld)
        script.setName(javascript_name)
        script.setSourceCode(javascript)
        script.setInjectionPoint(QWebEngineScript.DocumentReady)
        script.setRunsOnSubFrames(True)
        script.setWorldId(QWebEngineScript.ApplicationWorld)
        self.browser.page().scripts().insert(script)

    def __get_default_html(self):
        html = f"""
        <h1>Drag and drop any .md file to here</h1>
        """

        return html

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
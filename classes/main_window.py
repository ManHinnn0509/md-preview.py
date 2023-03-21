import os

import requests as req

from PyQt5.QtCore import Qt, QUrl, QFileSystemWatcher
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineScript, QWebEnginePage

from util.file_utils import read_file
from config import WINDOW_TITLE

class WebEnginePage(QWebEnginePage):
    
    def acceptNavigationRequest(self, url: QUrl, type: 'QWebEnginePage.NavigationType', isMainFrame: bool) -> bool:
        # return super().acceptNavigationRequest(url, type, isMainFrame)
        # print(url.scheme())
        # print(url.path())
        # print(url.url())
        if (url.scheme().startswith("http")):
            return False

        return True

class MainWindow:
    def __init__(self, token: str, css_path: str, css_content: str) -> None:
        self.app = QApplication([])
        self.browser = QWebEngineView()
        self.fs_watcher = QFileSystemWatcher([])
        self.fs_watcher.fileChanged.connect(self.__file_changed)

        self.token = token
        self.css_path = css_path
        self.css_content = css_content

        # self.page = WebEnginePage(self.browser)
        # self.browser.setPage(self.page)
        self.browser.setContextMenuPolicy(Qt.NoContextMenu)

        self.browser.setAcceptDrops(True)
        self.browser.dragEnterEvent = self.__drag_enter_event
        self.browser.dropEvent = self.__drop_event

        self.browser.setWindowTitle(WINDOW_TITLE)
        self.browser.setHtml(self.__get_default_html())
    
    def start(self):
        self.browser.show()
        self.app.exec_()

    def __render(self, md_abspath: str):
        content = read_file(md_abspath)
        if (content == None):
            print(f"[ERROR] Unable to read .md file from: [{md_abspath}]")
            return

        # Send request to GitHub API
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
            QUrl.fromLocalFile(md_abspath)
        )
        
        # css files & load

        # From: https://github.com/sindresorhus/github-markdown-css#usage
        md_body_style = '''
            .markdown-body {
                box-sizing: border-box;
                min-width: 200px;
                max-width: 980px;
                margin: 0 auto;
                padding: 45px;
            }

            /* I don't think this works but I'm just gonna keep it here */
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

    def __load_css(self, javascript_name: str, css_content: str):
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

    # --- Events ---

    def __file_changed(self, path):
        # Solution from: https://ymt-lab.com/en/post/2021/pyqt5-qfilesystemwatcher-test/
        self.browser.setWindowTitle(WINDOW_TITLE + " " + "(Reloading...)")
        self.__render(path)
        self.browser.setWindowTitle(WINDOW_TITLE)

    def __drag_enter_event(self, event):
        if (event.mimeData().hasUrls()):
            event.acceptProposedAction()

    def __drop_event(self, event):
        for url in event.mimeData().urls():
            if url.isLocalFile():
                filepath = url.toLocalFile()
                abs_filepath = os.path.abspath(filepath)
                if abs_filepath.endswith('.md'):

                    url = QUrl.fromLocalFile(abs_filepath)

                    self.browser.setUrl(url)
                    self.__render(abs_filepath)
                    
                    # Clear all the paths, empty the list
                    fs_files = self.fs_watcher.files()
                    if (len(fs_files) != 0):
                        self.fs_watcher.removePaths(fs_files)
                    
                    # Add the current file to monitor
                    self.fs_watcher.addPath(abs_filepath)

                    event.acceptProposedAction()
                    
                    return
        
        event.ignore()
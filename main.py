import os

from dotenv import load_dotenv

from classes import MainWindow
from config import DEFAULT_CSS_FILE_PATH

def main():
    load_dotenv()

    token = os.getenv("GITHUB_TOKEN")
    if (token == None):
        print("[ERROR] GitHub token not found in .env file")
        return
    
    token = token.strip()
    css_path = os.path.abspath(DEFAULT_CSS_FILE_PATH)
    # css_path = css_path.replace("\\", "/")
    # css_path = "file:///" + css_path
    # print(css_path)

    w = MainWindow(token, css_path)
    w.start()

if (__name__ == "__main__"):
    main()

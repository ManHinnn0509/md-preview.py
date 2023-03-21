import os

from dotenv import load_dotenv

from classes import MainWindow
from util.file_utils import read_file
from config import DEFAULT_CSS_FILE_PATH

def main():
    
    token = os.getenv("GITHUB_TOKEN")
    if (token == None):
        print("[ERROR] GitHub token not found in .env file")
        return
    
    token = token.strip()
    css_path = os.path.abspath(DEFAULT_CSS_FILE_PATH)
    css_content = read_file(css_path)

    if (css_content == None):
        print("[ERROR] Unable to read css content")
        return

    w = MainWindow(token, css_path, css_content)
    w.start()

if (__name__ == "__main__"):
    load_dotenv()
    main()

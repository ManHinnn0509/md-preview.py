import os

from dotenv import load_dotenv

from classes import MainWindow

def main():
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if (token == None):
        print("[ERROR] GitHub token not found in .env file")
        return
    w = MainWindow()
    w.start()

if (__name__ == "__main__"):
    main()

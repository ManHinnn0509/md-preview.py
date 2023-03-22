# App attributes etc
WINDOW_TITLE = "GitHub README Preview"
WINDOW_ICON_PATH = './imgs/icon/icon.ico'

# Path to the .css file to be used
# ! PyQt5 web view doesn't support css @media query !
DEFAULT_CSS_FILE_PATH = "./css/github-markdown-dark.min.css"

# Decide if the rendered content's height should be adjusted based on the content
# If False, the height of the rendered content will NOT be adjusted based on the content
# I suggest leaving this to True
LIMIT_HEIGHT = True
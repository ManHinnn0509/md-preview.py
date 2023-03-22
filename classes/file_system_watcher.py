from PyQt5.QtCore import QFileSystemWatcher

class FileSystemWatcher(QFileSystemWatcher):
    def __init__(self, *args, **kwargs):
        super(FileSystemWatcher, self).__init__(*args, **kwargs)

    def clear(self):
        fs_files = self.files()
        if (len(fs_files) != 0):
            self.removePaths(fs_files)
    
    
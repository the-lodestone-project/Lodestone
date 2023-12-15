"""
Lodestone File Stream Service (TM)
Shortened to LStream
"""
from io import StringIO

class LSFile:
    def __init__(self, filename: str):
        """
        Opens a file for I/O
        """
        self.filename = filename

        try:
            with open(filename, "r") as f:
                self.io = StringIO(f.read())
        except FileNotFoundError:
            self.io = StringIO()

        self.open = open(filename, "w+")

        self.read = self.io.read
        self.readlines = self.io.readlines
        self.readline = self.io.readline
        self.write = self.io.write
        self.flush = self.io.flush
        self.close = self.io.close

    def __del__(self):
        self.open.write(self.read())
        self.open.close()

class LStream:
    CHAT = 1
    LOGGER = 2
    FILE = LSFile

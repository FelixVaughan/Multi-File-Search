from PyPDF2 import PdfFileReader
import slate3k as PDFReader
from os.path import splitext
import random

class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

    def __init__(self):
        self.available = {}
        self.initializeColors()

    def initializeColors(self):
        for i in color.__dict__:
            if(i.find("__") == -1 and i != 'END' and i != 'BOLD' and i.isupper()):
                self.available[i] = color.__dict__[i]

    def selectRandomColor(self):
        key, value = random.choice(list(self.available.items()))
        del self.available[key]
        if not self.available:
            self.initializeColors()
        return value


class WordManager:
    def __init__(self, word):
        self.word = word
        self.occurences = []
        self.color = None #each File will have a color object. choose color from this object then use it to highlight below variable.
        self.highlightedWord = None

    def frequency():
        return len(occurences)

    def addOccurrence(self,page,row):
        self.occurences.append((page,row))

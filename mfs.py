import slate3k as PDFReader
from os.path import splitext
import random

ACCEPTABLE_SUFFIXES = ["pdf","txt","c","cpp","py","pyx","java"] #this list can be extended to include any type of code file. These are not all included for obvious reasons
def checkSuffix(suffix):
    if suffix not in ACCEPTABLE_SUFFIXES:
        return False
    else:
        return True

def findOccurences(key,word,wordStore,cycle):
    index = 0
    while index < len(word):
            index = word.find(key, index)
            if index == -1:
                break
            if cycle < 2:
                wordStore.append(cycle + index)
            else:
                wordStore.append(cycle + index - 3)
            index += len(key)

def readPDF(stream, keyword):
    with open(stream,"rb") as file:
        pdf = PDFReader.PDF(file)
        occurences = []
        for content in pdf:
            print(content)
            findOccurences(keyword,content,occurences,0)
        print(len(occurences))

def readText(file, keyword):
    absKeyLength = len(keyword) - 1
    file = input("File to search: ")
    with open(file, encoding='utf8') as f:
        carryOver = ""
        cycle = 0
        occurences = []
        while True:
            data = f.read(1024)
            if not data:
                break

            data = carryOver + data
            findOccurences(keyword,data,occurences,cycle)
            suffix = data[len(data)-absKeyLength - 1 : len(data)]
            carryOver = cycle + 1024
        print(occurences)

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

class File:
    def __init__(self,path):
        self.path = path
        try:
            if checkSuffix(self.getSuffix()) == False:
                raise ValueError
            self.file = open(path,"r")
        except ValueError:
            print(f"'{path}' does not contain a valid suffix, skipping...") #make sure to add skip clause in main loop
        except FileNotFoundError:
            print(f"No file found at '{path}', skipping...")   #make sure to add skip clause in main loop

    def getSuffix(self):
        reverse_path = self.path[::-1]
        suffix_index = reverse_path.index(".")
        reverse_suffix = reverse_path[0:suffix_index]
        return reverse_suffix[::-1]

file = File("/Users/Felix Vaughan/Desktop/toAlex.txt")

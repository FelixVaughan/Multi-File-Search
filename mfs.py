import slate3k as PDFReader
import random
import sys
import shutil
import os

ACCEPTABLE_SUFFIXES = ["pdf","txt","c","cpp","py","pyx","java"] #can be extended to all code types. Limited here for obvious reasons
def allowedSuffix(suffix):
    if suffix not in ACCEPTABLE_SUFFIXES: return False
    else: return True

def findOccurences(key,word,wordStore,cycle): #slow but easy. Use for testing
    index = 0
    while index < len(word):
            index = word.find(key, index)
            if index == -1: break
            if cycle < 2:
                wordStore.append(cycle + index)
            else:
                wordStore.append(cycle + index - 3)
            index += len(key)

def extractPageContents(fileObject):
    fileContent = []
    if(fileObject.getSuffix() == "pdf"):
        file = open(fileObject.path, "rb")
        fileContent = PDFReader.PDF(file)
    else:
        file = open(fileObject.path, encoding="utf8")
        content = file.read()
        fileContent.append(content)
    return fileContent




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
        for i in Color.__dict__:
            if(i.find("__") == -1 and i != 'END' and i != 'BOLD' and i.isupper()):
                self.available[i] = Color.__dict__[i]

    def selectRandomColor(self):
        key, value = random.choice(list(self.available.items()))
        del self.available[key]
        if not self.available:
            self.initializeColors()
        return value


class WordManager:
    def __init__(self, word, color=None):
        self.word = word
        self.frequency = 0
        if color is None:
            self.color = None
            self.highlightedWord = self.word
        else:
            self.color = color
            self.highlightedWord = Color.BOLD + self.color + self.word + Color.END


class File:
    def __init__(self,path,listOfWords):
        self.colors = Color()
        self.wordsToManage = {}
        self.path = path
        self.pages = []
        self.info = {}
        try:
            if not allowedSuffix(self.getSuffix()):
                raise ValueError
            if self.getSuffix() == "pdf":
                self.file = open(path, "rb")
            else:
                self.file = open(path, encoding="utf8")

            if listOfWords:
                for word in listOfWords:
                    wordObject = WordManager(word, self.colors.selectRandomColor())
                    self.wordsToManage[word] = wordObject
            else:
                sys.exit("No words to search, goodbye!")

        except ValueError:
            print(f"'{path}' does not contain a valid suffix, skipping...")
            raise ValueError #allows for file to be skipped in main loop
        except FileNotFoundError:
            print(f"No file found at '{path}', skipping...")
            raise FileNotFoundError #allows for file to be skipped in main loop


    def getSuffix(self):
        reverse_path = self.path[::-1]
        suffix_index = reverse_path.index(".")
        reverse_suffix = reverse_path[0:suffix_index]
        return reverse_suffix[::-1]

    def printPage(self,pageNumber):
        os.system('clear')
        print(f"{[p.number for p in self.pages]}\nCurrently on page {self.pages[pageNumber].number}")
        page = self.pages[pageNumber]
        print(f"{page.content}\n{page.hits} hits")
        for word in page.info:
            print(f"word: '{word}' found at index(es): ", [i[0] for i in page.info[word]])

    def display(self):
        print(f"{len(self.pages)} page(s) match in file. Naviagte with a or d to or type a number to goto page. q to go back and q! to exit")
        pageNumber = 0
        while True:
            do = input("")
            if do == 'q': break
            elif do == "q!": return "quit"
            elif do == 'd' and len(self.pages) > 1 and pageNumber is not len(self.pages)-1: pageNumber += 1
            elif do == 'a' and len(self.pages) > 1 and pageNumber is not 0: pageNumber -= 1
            else:
                try:
                    isinstance(eval(do),int)
                    pageNumber = eval(do)
                except NameError:
                    print("Input not valid. Try again")
                    continue
            self.printPage(pageNumber)


class Page:
    def __init__(self, content, info, hits, num = None):
        if num is None: self.number = 1
        self.info = info
        self.number = num
        self.hits = hits
        self.raw_content = content
        self.content = self.pagify(content)

    def pagify(self, string):
        lines = string.splitlines()
        width = max(len(s) for s in lines)
        res = ['┌' + '─' * width + '┐']
        for line in lines:
            res.append('│' + (line + ' ' * width)[:width] + '│')
        res.append('└' + '─' * width + '┘')
        return '\n'.join(res)


class TreeNode:
    def __init__(self):
        self.children = {}
        self.isEndOfWord = False

class TrieTree:
    def __init__(self,root):
        self.root = root

    def insert(self,word):
        current = self.root
        for w in word:
            if w not in current.children.keys():
                node = TreeNode()
                current.children[w] = node
                current = node
            else:
                current = current.children[w]
        current.isEndOfWord = True

    def search(self,word,storage):
        for index in range(len(word)):
            depth = 0
            current = self.root
            current_word = []
            for w in word[index:]:
                if current.children:
                    if w not in current.children.keys():
                        break
                    else:
                        current = current.children[w]
                        depth += 1
                        current_word.append(w)
                        if current.isEndOfWord:
                            current_word_string = "".join(current_word)
                            if current_word_string not in storage.keys():
                                storage[current_word_string] = []
                            storage[current_word_string].append((index,depth))
        return storage

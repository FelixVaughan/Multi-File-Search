import slate3k as PDFReader
import random
import sys
import shutil

ACCEPTABLE_SUFFIXES = ["pdf","txt","c","cpp","py","pyx","java"] #can be extended to all code types. Limited here for obvious reasons
def allowedSuffix(suffix):
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
        self.occurences = []
        if color is None:
            self.color = None
            self.highlightedWord = self.word
        else:
            self.color = color
            self.highlightedWord = Color.BOLD + self.color + self.word + Color.END

    def frequency():
        return len(occurences)

    def addOccurrence(self,page,row):
        self.occurences.append((page,row))

class File:
    def __init__(self,path,listOfWords):
        self.colors = Color()
        self.wordsToManage = [] #make sure list is of type word managers. loop through these and set colors
        self.path = path
        self.pages = []
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
                    self.wordsToManage.append(wordObject)
            else:
                print("No words to search, goodbye!")
                sys.exit()

        except ValueError:
            print(f"'{path}' does not contain a valid suffix, skipping...") #make sure to add skip clause in main loop
        except FileNotFoundError:
            print(f"No file found at '{path}', skipping...")   #make sure to add skip clause in main loop


    def getSuffix(self):
        reverse_path = self.path[::-1]
        suffix_index = reverse_path.index(".")
        reverse_suffix = reverse_path[0:suffix_index]
        return reverse_suffix[::-1]


class Page:
    def __init__(self,content, width, hits, num = None):
        if num is None:
            self.number = 1
        self.number = num
        self.hits = hits #word number pairs
        self.raw_content = content
        self.content = self.pagify(content, width)

    def pagify(self, string, width):
        lines = string.splitlines()
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
                            storage["".join(current_word)].append((index,depth))
        return storage

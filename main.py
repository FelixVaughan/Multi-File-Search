from mfs import *
import sys
import threading
import os

#windows does not allow ANSI colors by default.
if sys.platform.find("win") is not -1:
    os.system("color")

def splitArgs(lst):
    try:
        index = lst.index(":")
        files = lst[1:index]
        words = lst[index + 1:len(lst)]
        return [files, words]
    except ValueError:
        sys.exit("Inputs not entered properly (remember, format is files : words). Exiting...")

def initializedFiles(fileList,wordList):
    fileObjects = []
    for f in fileList:
        try:
            file = File(f,wordList)
            fileObjects.append(file)
        except (ValueError, FileNotFoundError):
            continue
    if len(fileObjects):
        return fileObjects
    else:
        sys.exit("No files to search. Exiting...")

def initializedTree(listOfWords):
    trieTree = TrieTree(TreeNode())
    for word in listOfWords:
        trieTree.insert(word)
    return trieTree

def processFile(fileObject,wordTree,destination):
    pages = extractPageContents(fileObject)
    for p in range(len(pages)):
        result = {}
        hits = 0
        wordTree.search(pages[p],result)
        if result:
            page_content = pages[p]
            for r in result:
                amountOfOccurences = len(result[r])
                page_content = page_content.replace(r,fileObject.wordsToManage[r].highlightedWord)
                fileObject.wordsToManage[r].frequency += amountOfOccurences
                hits += amountOfOccurences
            page = Page(page_content,result,hits,p)
            fileObject.pages.append(page)
    destination.append(fileObject)

def displayLoop(completedFiles):
    numberOfFiles = len(completedFiles)
    os.system('clear')
    fileSelectMessage =  f"you have {len(completedFiles)} files to view.\n"
    for i in range(numberOfFiles):
        option = f"  Press {i} to view '{completedFiles[i].path}' Press q to exit\n"
        fileSelectMessage += option
    while True:
        try:
            userInput = input(fileSelectMessage)
            if userInput == 'q': break
            isinstance(userInput,int)
            fileSelect = eval(userInput)
            file = completedFiles[fileSelect]
            status = file.display()
            if status == "quit": break
        except (NameError, IndexError):
            print("Input is not valid. Try again.")
            continue
        finally:
            os.system('clear')



def main():
    args = splitArgs(sys.argv)
    files = args[0]
    words = args[1]
    fileObjects = initializedFiles(files,words)
    wordTree = initializedTree(words)
    completedFiles = []
    threads = []
    for file in fileObjects:
        thread = threading.Thread(target=processFile,args=[file,wordTree,completedFiles])
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    displayLoop(completedFiles)

if __name__ == "__main__":
    main()

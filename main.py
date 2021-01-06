from mfs import *
import sys
import threading

#windows does not allow ANSI colors by default.
if sys.platform.find("win") is not -1:
    from colorama import init
    init()

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
    # TODO: add some info to file hits field var

def main():
    args = splitArgs(sys.argv)
    files = args[0]
    words = args[1]
    fileObjects = initializedFiles(files,words)
    wordTree = initializedTree(words)
    completedFiles = [] #make thread safe
    threads = []
    for file in fileObjects:
        thread = threading.Thread(target=processFile,args=[file,wordTree,completedFiles])
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print(completedFiles)
    
if __name__ == "__main__":
    main()

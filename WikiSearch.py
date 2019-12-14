import sys #argvs
from bs4 import BeautifulSoup #parsing html
import requests #get site html
import re #regex
#import os #current working directory

def getArgs():
    args = []
    for i in range (1,len(sys.argv)):
        args.append(sys.argv[i])
    return args
def readFile(filePath):
    with open(filePath,"r") as file:
        return file.readlines()
def saveToFile(filePath,lines):
    with open(filePath,"r+") as file:
        file.writelines(lines)
def getFilePath(args):
    for arg in args:
        arg = re.findall("\.*.txt",arg)
    if len(args)>1 or len(args)==0:
        return None
    else:
        return args[0]
def getData(site):
    description = []
    source = requests.get(site).text
    soup = BeautifulSoup(source, 'lxml')
    if soup.find('button',class_="oo-ui-inputWidget-input oo-ui-buttonElement-button"):
        #TODO get results or show not found
        description.append("not found")
    else:
        article = soup.find('div', class_="mw-parser-output")
        for txt in article.find_all('p'): 
            string = txt.text
            if string!="" and string!="\n":
                string = re.sub("\[[0-9]*]","",string) #get rid of [1],[2] etc
                string = re.sub("\\xa0"," ",string) #get rid of \xa0
                description.append(string)
    return description, site
def getEnglishWikipedia(item):
    item = re.sub("\ +","_",item) #replace spaces with '_' (for www address)
    site = "https://en.wikipedia.org/w/index.php?search=" + item
    return getData(site)
def getPolishWikipedia(item):
    item = re.sub("\ +","_",item) #replace spaces with '_' (for www address)
    site = "https://pl.wikipedia.org/w/index.php?search=" + item
    return getData(site)
def start(args):
    if len(args)==0:
        print("Please specify txt file path. ex: WikiSearch myTextFile.txt")
    else:
        filePath = getFilePath(args)
        toWrite=[]
        for line in readFile(filePath):
            line.replace("\n","")
            line.replace(" ","")
            description , site = getPolishWikipedia(line)
            toWrite.append(line + " - " + description[0]+site)
        saveToFile(filePath,toWrite)
if __name__ == "__main__":
    start(getArgs())
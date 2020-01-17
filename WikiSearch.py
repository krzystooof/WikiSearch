import sys #argvs
from bs4 import BeautifulSoup #parsing html
import requests #get site html
import re #regex
#import os #current working directory

notFound = 0

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
    args2 =[]
    for arg in args:
        arg = re.findall(".+.txt",arg)
        if len(arg) is not 0:
            args2.append(arg)
    if len(args2)>1 or len(args2)==0:
        return None
    else:
        return args2[0][0]
def getCountryCodes(args):
    args2 =[]
    for arg in args:
        args2.append(re.findall("\.[a-zA-Z]{2,3}",arg))
    args3 = [x for x in args2 if x] #get rid of empty elements
    args2.clear()
    args2 = [word for arg in args3 for word in arg if word != ".txt"]
    if len(args2)==0:
        return None
    return args2
def getOptions(args):
    args2 =[]
    for arg in args:
        args2.append(re.findall("-.{1,}",arg))
    args3 = [letter for arg in args2 for word in arg for letter in word if letter != '-']
    if len(args3)==0:
        return None
    else:
        return args3
def specifyOption(item,options):
    item.replace("\n","") #get rid of newlines
    print("More than one match found for "+item)
    number=1
    for t in options:
        print(str(number)+". "+t, sep='')
        number+=1
    userInput = input("Please specify one: ")
    if int(userInput):
        return int(userInput)-1
    else:
        print(userInput+" is not a number")
        return specifyOption(item,options)                
def getFromWikipedia(countryCode ,item):
    site = "https://"+countryCode+".wikipedia.org/w/index.php?search=" + item
    description = []
    try:
        source = requests.get(site).text
        soup = BeautifulSoup(source, 'lxml')
        #no results
        if soup.find('div',class_="mw-search-form-wrapper"):
            description.append("")
            site = ""
            print("No results for "+item)
            global notFound
            notFound+=1
        else:
            article = soup.find('div', class_="mw-parser-output")
            pList = article.find_all('p',recursive=False)
            #one result
            if len(pList) > 1:
                for p in pList: 
                    string = p.text
                    if string!="" and string!="\n":
                        string = re.sub("\[[0-9]*]","",string) #get rid of [1],[2] etc
                        string = re.sub("\\xa0"," ",string) #get rid of \xa0
                        description.append(string)
            #more than one result
            else:
                titles = []
                descriptions = []
                for li in article.find_all('li'):
                    part = li.find('a', href=True)
                    titles.append(part['title'])
                    descriptions.append(li.text)
                selectedItem = titles[specifyOption(item,descriptions)]
                return getFromWikipedia(countryCode, selectedItem)            
    except ConnectionError:
        print("Connection error at " + item)
        description.append("")
        site = ""
    return item, description, site
def refactorString(item):
    item.replace("\n","") #get rid of newlines
    item.replace(" ","") #get rid of spaces
    item = re.sub("\ +","_",item) #replace spaces with '_' (for www address)
    return item
def start(args):
    filePath = getFilePath(args)
    if filePath is None:
        print("Please specify txt file path. ex: WikiSearch myTextFile.txt")
    else:
        options = getOptions(args)
        countryCodes = getCountryCodes(args)
        toWrite=[]
        #TODO options and countrycodes
        for line in readFile(filePath):
            if line is not "" or " ":
                item, description , itemUrl = getFromWikipedia("en", refactorString(line)) #en for english, pl for polish etc
                toWrite.append(line + description[0]+itemUrl) #description [0] - only first paragraph
        saveToFile(filePath,toWrite)
        print("Results saved to "+filePath if notFound is 0 else "Results saved to "+filePath+". Not found "+str(notFound)+" items")
def checkInternetConnection(host='https://en.wikipedia.org/'):
    try:
        requests.get(host) 
        return True
    except:
        return False

if __name__ == "__main__":
    start(getArgs())
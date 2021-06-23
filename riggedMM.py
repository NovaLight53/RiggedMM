#RiggedMM.py
#Goal: Find if matchmaking is rigged. 
#Note: CVC dict = python dictionary of Card Vs Card rates. 

import urllib.request
import json
import pandas as pd

 
def apikey(playertag):
    """ Takes in a player tag and outputs all their battle log data.""" 
    key = #You'll need to make your own api key on developer.clashroyale.com
    base_url = "https://api.clashroyale.com/v1"
    endpoint = "/players/%23" + playertag + "/battlelog/" 
    request = urllib.request.Request(base_url+endpoint, None, {"Authorization": "Bearer %s" % key})
    response = urllib.request.urlopen(request).read().decode("utf-8")
    data = json.loads(response)           
    return data

def createDictionary():
    with open("emptyDict.txt") as f:
        data = f.read().rstrip("/n")
        dictionary = eval(data)
        
        return dictionary

def apikeyPlayer(playertag):
    """ Takes in a player tag and outputs all their playertag data."""
    key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjE5NDA1MDllLTNiNmEtNDdhZC04NjczLTQ0YWZkY2NjZmFhNSIsImlhdCI6MTYwOTk5MTIxNiwic3ViIjoiZGV2ZWxvcGVyLzQ3YTk0NDRkLWE2MzQtMzFkMy00NjY0LTMwOGIyNWQyNjg1NCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI3My4yMjUuMC4zMyIsIjczLjQyLjEzMC4xODMiXSwidHlwZSI6ImNsaWVudCJ9XX0.yvymjLs6yJ__N8nZfSKWvB36-f15Vtn1Fw6fJ7Exn6t0sd8Ca20fwqyuza0QzQP80JDirLu_aihopCMZ3jOH-g'
    base_url = "https://api.clashroyale.com/v1"

    endpoint = "/players/%23" + playertag + "/" 
    request = urllib.request.Request(base_url+endpoint, None, {"Authorization": "Bearer %s" % key})
    response = urllib.request.urlopen(request).read().decode("utf-8")
    data = json.loads(response) 
    json_object = json.dumps(data)  
    with open("player.json", "w") as f: #This is a json file I use to see the data from the API easier
         f.write(json_object)        
    return data     

def updateDicts(dict1, dict2):
    """updates the two dictionaries and returns one with the sum off all the key entries"""
    finalDict = {}
    for key in dict1:
        finalDict[key] = dict1[key] + dict2[key]
    return finalDict
def CreateCVCdict():
    """gets the card vs card dictionary faster"""
    with open("CVCdict.txt") as f:
       data = f.read().rstrip("/n")
       dictionary = eval(data)
       return dictionary

def UsageRate(dict):
    """takes in a dictionary of uses, outputs the usage rates of all the cards"""
    gamesPlayed = sumDict(dict)/8
    newDict = {}
    for i in dict:
        newDict[i] = dict[i]/gamesPlayed
    return newDict

def sumDict(dictionary):
    sum = 0
    for i in dictionary:
        sum += dictionary[i] 
    return sum

def updateNestedDicts(d1, d2):
    """Updates two dictionaries, assuming they have the same entries"""
    finalDict = createDictionary()
    for key in d1:
        #print(key)
        newDict = updateDicts(d1[key], d2[key])
        finalDict[key] = newDict
    return finalDict

def toFileCVC(data):
    """takes in a massive dictionary and throws it into a JSON file"""
    with open("cardVsCardRates.json", "w") as f: #not really needed file, used to quickly look at my data early on
        json_object = json.dumps(data)
        f.write(json_object)
        return

def toFileUses(data):
    with open("usageRates.json", "w") as f:
        json_object = json.dumps(data)
        f.write(json_object)


def readFile(filename):
    try:
        with open(filename, 'r') as f:
            rawdata = f.read()
            data = eval(rawdata)
            return data
    except PermissionError as error: #1/25000 times opening a file would cause a permission error.  Error fix. 
        return 0

def dictToList(dict):
    L = []
    for key in dict:
        L += [dict[key]]
    return L

def chiSquare(observed, expected):
    """takes in a list of numbers, the observed and expected values and outputs the chi-square value"""
    total = 0
    for i  in range(len(observed)):
        total += (((observed[i] - expected[i])**2)/expected[i])
    return total

def expectedValues(dictionary, usage):
    """takes in a dictionary of values and multiplies them by a constant.  That number is the sum of the dictionary"""
    newDictionary = createDictionary()
    constant = sumDict(dictionary)/8
    for key in newDictionary:

        newDictionary[key] = usage[key] * constant
    return newDictionary

def allChiSquares(data, scaledUsage):
    """takes in all the data, nested dicts, and scaled usage rates.  Gets expected values for each and then gets a chi squared for each value"""
    XsqDict = createDictionary()
    for key in data:
        #need to get a chi squared value from it. Observed is just data[key].  Need to listify it.
        observed = dictToList(data[key])
        expected = dictToList(expectedValues(data[key], scaledUsage))
        chisq = chiSquare(observed, expected)
        XsqDict[key] = chisq
    return XsqDict

def writeToFile(data):
    with open("battletags.txt", "w") as f:
        f.write(str(data))


def riggedMM(starter, n, CVCdict, lower, upper): 
    """inputs: Starter, n , CVC dictionary, lower, upper
    starter: root of recursive tree
    n: depth of the recursive tree
    CVC dict: Card Vs Card dictionary
    lower and upper: Lower and upper bounds for trophies to check
    returns a CVC type dictionary all filled out with battle data. Updates the battle tags list"""

    data = apikey(starter)
    ladderTags = []
    battleTags = readFile("battletags.txt")
    if battleTags == 0:
        print("error")
        print(n, starter)
        return CVCdict
    newBattleTags = []
    for i in data:
        if i["type"]  in ["PvP", "Ladder_CrownRush"]:
            if (lower < i["team"][0]["startingTrophies"]< upper) == True:    
                oppTag =i["opponent"][0]["tag"][1:]
                tag = str(min(oppTag, starter)[:5]) + str(max(oppTag, starter)[:5]) + i["battleTime"][9:15] #unique battle tag for each battle.  
                if tag not in battleTags:
                    ladderTags += [i["opponent"][0]["tag"][1:]]
                    newBattleTags += [tag]
                    for playerCard in i["team"][0]["cards"]:
                        for oppCard in i["opponent"][0]["cards"]:
                            CVCdict[playerCard["name"]][oppCard["name"]] += 1
                            CVCdict[oppCard["name"]][playerCard["name"]] += 1               
    battleTags += newBattleTags
    try:
        writeToFile(battleTags) 
    except PermissionError as error: 
        print("error")
        CVCdict = CreateCVCdict()
    if n == 0: 
        return CVCdict
    masterDict = CreateCVCdict() # makes CardVsCard (CVC) nested dictionary
    if n > 1:
        print(len(ladderTags), n)
    for opponent in ladderTags:
        newDict = riggedMM(opponent, n-1, CreateCVCdict(), lower, upper) 
        masterDict = updateNestedDicts(masterDict, newDict)  
    return masterDict

def clearTags():
    """This function was used to clear the file that had all the unique 'battle tags' to prevent duplicates from being counted"""
    with open('battleTags.txt', "w") as f:
        f.write('[]')    
        
me = '2CL8J90GC' # my tag.  Used for testing purposes

def getData(lower, upper, starter, data):
    """function that gets data.  Takes in lower and upper trophy bounds, a starting tag and data.  The data input is old data that gets updated with the new data"""
    newData = riggedMM(starter, 4, CreateCVCdict(), lower, upper)
    rawData = updateNestedDicts(data, newData)
    analyzedData =  analyzeData(rawData)
    toExcel(rawData, analyzedData, 'excel.xlsx', lower, upper) #excel spreadsheet for exporting the data
    print(len(readFile("battletags.txt"))) #how many battles were analyzed
    return rawData

def toExcel(data, analyzedData, filename, lower, upper):
    """takes the data and exports it to excel"""
    df1 = pd.DataFrame(data)
    df2 = pd.DataFrame(analyzedData)
    writer = pd.ExcelWriter(filename)
    df1.to_excel(writer, sheet_name = 'Raw Data ' + str(lower) + '-' + str(upper)) #writes the data to excel
    df2.to_excel(writer, sheet_name = 'Analyzed Data ' + str(lower) + '-' + str(upper))
    writer.save()
    
def analyzeData(CVCdict):
    """takes in a CVC dict and outputs fully normalized data and chi squared values."""
    battlesPlayed = len(readFile("battletags.txt")) 
    usages = createDictionary()
    newDict = CreateCVCdict()
    chisq = createDictionary()
    for card in newDict:
        s = sumDict(CVCdict[card])
        usages[card] = s/(8*battlesPlayed)
        for oppCard in newDict[card]:
            newDict[card][oppCard] = CVCdict[card][oppCard]/s
    nFactor = sumDict(usages)
    for card in newDict:
        newDict[card][''] = ''
        newDict[card]["Usage"] = usages[card]/nFactor
    observed = []
    for card in newDict:
        for oppCard in newDict:
            observed += [newDict[oppCard][card]] #observed values were the values found in data
        expected = 102*[newDict[card]['Usage']] #if there was no bias in MM, the values should converge to the expected value. 
        chisq[card] = chiSquare(observed, expected) #gets the chi-squared P values
        observed = []
    newDict[''] = ''
    newDict['Chi-Square P-values'] = chisq
    return newDict


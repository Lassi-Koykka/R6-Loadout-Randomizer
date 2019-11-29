import requests
import json
import random
from bs4 import BeautifulSoup

def newSoup(url):
    """Create a new soup object"""
    response = requests.get(url)
    new_soup = BeautifulSoup(response.text, 'html.parser')
    return new_soup

def parseLists(item):
    """Loads the wikipage of the operator or item and parses necessary infomation such as a name, and a list of weapons or attachments"""
    if item != 'Sentry' and item != 'Trapper':
        response = requests.get('https://rainbowsix.fandom.com/wiki/' + item)
        soup = BeautifulSoup(response.text, 'html.parser')
        thingsList = []
        try:
            things_html = soup.find(class_='article-table').find_all('td')
        except:
                print("couldn't find the page, retrying with:")
                print('https://rainbowsix.fandom.com/wiki/' + item + '/Siege' + '\n')
                response = requests.get('https://rainbowsix.fandom.com/wiki/' + item +
                                        '/Siege')
                soup = BeautifulSoup(response.text, 'html.parser')
                things_html = soup.find(class_='article-table').find_all('td')
                #all cells of the table
        try:
            for i in things_html:
                #print(i)
                #print('\n')
                i = str(i)
                tempSoup = BeautifulSoup(i, 'html.parser')
                el = tempSoup.find_all('a')
                #parsing all <a href='link'>text</a> items to a list
                tempList = []
                if el != []:
                    #if the list doesn't contain links it creates an empty list. ignore them.
                    for j in el:
                        tempList.append({
                            "name": j.get_text(),
                            "link": j['href']
                        })  # key is name of thing, val is link
                    thingsList.append(tempList)
        except:
            print(things_html)
        #print(thingsList)
        return thingsList

def listNames(url):
    """Parses a list of names from the teams wikipage"""
    namelist = []
    soup = newSoup(url)
    el = soup.find_all(class_='category-page__member-link')
    for item in el:
        if item.get_text() == 'Pointman' or item.get_text() == 'Breacher':
            continue
        else:
            namelist.append(item.get_text())
    print('\n')
    print(namelist)
    print('\n')
    return namelist

def parseAttachments(weaponsList):
    """Parses attachments for weapons if they have any listed"""
    weapons = []
    for i in weaponsList:  # add weapons with attachments
        #print(i)
        #if i["name"] == "SAS":
            #continue
        if i["link"] == '/wiki/SASG-12':
            i["link"] = '/wiki/SASG-12/Siege'
        attachments = []
        link = i["link"].replace(' ', '_')
        #print(link)
        response = requests.get('https://rainbowsix.fandom.com' + link)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            attachments_html = soup.find(class_='article-table').find_all('td')
            for j in attachments_html:
                j = str(j)
                tempSoup = BeautifulSoup(j, 'html.parser')
                el = tempSoup.find_all('a')
                #parsing all <a href='link'>text</a> items to a list
                tempList = ["-"]
                if el != []:
                    #if the list doesn't contain links it creates an empty list. ignore them
                    for k in el:
                        tempList.append(k.get_text())
                    attachments.append(tempList)
        except:
            attachments = ["-"]
            print("No attachments found for :" + i["name"])
        weapons.append({'name': i["name"],'attachments': attachments})

    return weapons

def createOpList(nameList):
    """Creates and returns a list of operator objects by using parseLists and parseAttachments"""
    operators = []
    for i in nameList:
        if i != 'Recruit' and i != 'Sentry' and i != 'Trapper':
            loadout = parseLists(i)
            primaries = parseAttachments(loadout[0])
            secondaries = parseAttachments(loadout[1])
            gadgets = loadout[2]
            
            operators.append({'name': i,'primaries': primaries,'secondaries': secondaries,'gadgets': gadgets})
    return operators

def saveOperators(operators, filepath):
    """Saves the operators to a JSON file as alist of dictionaries"""
    with open(filepath, 'w') as opSaveFile:
        json.dump(operators, opSaveFile, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def readOperators(filename):
    """Reads the operators from the JSON file as a list of dictionaries"""
    with open(filename, 'r') as filehandler:
        return json.loads(filehandler.read())

def operatorFilesExist():
    """Checks if both operator files exist, parses and creates new ones if they don't"""
    try:
        f1 = open('attackers.json')
        f1.close()
        f2 = open('defenders.json')
        f2.close()
    except:
        print("Both operator files do not exist. Parsing and creating new ones\n")

        attackers = listNames(
            'https://rainbowsix.fandom.com/wiki/Category:Attacker')

        atk_operators = createOpList(attackers)
        saveOperators(atk_operators, 'attackers.json')

        #create a list of defenders
        defenders = listNames(
            'https://rainbowsix.fandom.com/wiki/Category:Defender')

        def_operators = createOpList(defenders)
        saveOperators(def_operators, 'defenders.json')
    print("Operator files found.\n")

def rndFromList(list):
    """Generates a random index number for a list and returns the object from that index"""
    return list[random.randrange(0, len(list))]

def randomizeOperator(operatorList):
    """returns a random operator with a randomly generated loadout from a specified teams' .json file"""
    operator = rndFromList(operatorList)
    print("\nOperator: " + operator['name'])
    primary = rndFromList(operator['primaries'])
    print("\nPrimary: " + primary['name'] + "\n")
    for attachType in primary['attachments']:
        print("\t" + rndFromList(attachType))
    secondary = rndFromList(operator['secondaries'])
    print("\nSecondary: " + secondary['name'] + "\n")
    for attachType in secondary['attachments']:
        print("\t" + rndFromList(attachType))
    gadget = rndFromList(operator['gadgets'])
    print("\nGadget: " + gadget['name'] + "\n")

def updateOperatorFiles():
    """Parses operator info again and rewrites the .json files"""
    #Create a list of attackers
    attackers = listNames('https://rainbowsix.fandom.com/wiki/Category:Attacker')

    atk_operators = createOpList(attackers)
    saveOperators(atk_operators, 'attackers.json')

    #create a list of defenders
    defenders = listNames('https://rainbowsix.fandom.com/wiki/Category:Defender')

    def_operators = createOpList(defenders)
    saveOperators(def_operators, 'defenders.json')

def deliverOperators():
    """Checks if operator files exist and returns a random loadout"""
    operatorFilesExist()
    print("[A]ttackers\n[D]efenders")
    teamchoice = input()
    if teamchoice == 'A' or teamchoice == 'a':
        atk_operators = readOperators('attackers.json')
        randomizeOperator(atk_operators)

    elif teamchoice == 'D' or teamchoice == 'd':
        def_operators = readOperators('defenders.json')
        randomizeOperator(def_operators)

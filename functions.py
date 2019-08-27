import requests
from objects import *
from bs4 import BeautifulSoup


def newSoup(url):
    response = requests.get(url)
    new_soup = BeautifulSoup(response.text, 'html.parser')
    return new_soup

def parseLists(item):
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
                })  #key is name of thing, val is link
            thingsList.append(tempList)

    #print(thingsList)
    return thingsList


def parseAttachments(weaponsList):
    weapons = []
    for i in weaponsList:  #add weapons with attachments
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
                tempList = ["No attachment"]
                if el != []:
                    #if the list doesn't contain links it creates an empty list. ignore them
                    for k in el:
                        tempList.append(k.get_text())
                    attachments.append(tempList)
        except:
            attachments = ["-"]
            print("No attachments found for :" + i["name"])
        weapons.append(weapon(i["name"], attachments))

    return weapons

def createOpList(nameList):
    operators = []
    for i in nameList:
        if i == 'Recruit':
            continue
        loadout = parseLists(i)
        primaries = parseAttachments(loadout[0])
        secondaries = parseAttachments(loadout[1])
        gadgets = loadout[2]

        operators.append(Operator(i, primaries, secondaries, gadgets))
    return operators
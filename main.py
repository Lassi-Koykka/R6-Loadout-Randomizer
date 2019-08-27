import requests
import random
from functions import *

from bs4 import BeautifulSoup
import objects


attackers = []
defenders = []
atk_operators = []
def_operators = []


#Create a list of attackers
soup = newSoup('https://rainbowsix.fandom.com/wiki/Category:Attacker')
el = soup.find_all(class_='category-page__member-link')
for item in el:
    attackers.append(item.get_text())
print(attackers)

atk_operators = createOpList(attackers)

#create a list of defenders
soup = newSoup('https://rainbowsix.fandom.com/wiki/Category:Defender')
el = soup.find_all(class_='category-page__member-link')
for item in el:
    defenders.append(item.get_text())
print(defenders)

def_operators = createOpList(defenders)



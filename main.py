import requests
import random
from functions import *

from bs4 import BeautifulSoup
import objects


attackers = []
defenders = []
atk_operators = []
def_operators = []


#Ask user what they want to do
print("[1] Refresh operator loadout information in memory \n[2] Randomize a loadout\n")
userInput = input()
if userInput == '1':
    #Create a list of attackers
    attackers = listNames('https://rainbowsix.fandom.com/wiki/Category:Attacker')

    atk_operators = createOpList(attackers)
    saveOperators(atk_operators, 'attackers')


    #create a list of defenders
    defenders = listNames('https://rainbowsix.fandom.com/wiki/Category:Defender')

    def_operators = createOpList(defenders)
    saveOperators(def_operators, 'defenders')
#elif userInput == '2':
    #print("[A]ttackers\n[D]efenders")
    #teamchoice = input()
    #if userInput == 'A'


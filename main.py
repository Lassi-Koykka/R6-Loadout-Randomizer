import requests
import random
from functions import (
    listNames, saveOperators, 
    readOperators, operatorFilesExist, 
    createOpList, updateOperatorFiles, deliverOperators
)

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
    updateOperatorFiles()
elif userInput == '2':
    deliverOperators()

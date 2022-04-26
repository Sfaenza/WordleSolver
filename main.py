from ast import While
from turtle import pos
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

driver = None
game = None
keyboard = None
keys = {'q':'11','w':'12','e':'13','r':'14','t':'15','y':'16','u':'17','i':'18','o':'19','p':'110','a':'22',
's':'23','d':'24','f':'25','g':'26','h':'27','j':'28','k':'29','l':'210',
'enter':'31','z':'32','x':'33','c':'34','v':'35','b':'36','n':'37','m':'38'
}
#### Gets the next words based upon current frequencies of the current list and letters previously guessed
def getNextGuess(guesses,possiblewords,allwords):
    dict= {}

    for i in possiblewords:
        q = list(set(i))
        for j in q:
            if j in dict:
                dict[j] = dict[j] +1
            else:
                dict[j] = 1

    sorted_keys = sorted(dict, key=dict.get,reverse=True) 
    dict1={}
    for w in sorted_keys:
        dict1[w] = dict[w]
    
    sum = 0
    maxSum = 0
    nextGuess =''
    letters = []
    dict2 = dict1
    for word in guesses:
        letters = letters + list(set(word))
        for letter in letters:
            if letter in dict1:
                dict1.pop(letter)
    if len(dict1.keys()) > 0:
        for word in allwords:
            sum = 0
            for letter in list(set(word)):
                if(letter in dict1):
                    sum = sum + dict1[letter]
            if(sum>maxSum):
                maxSum = sum
                nextGuess = word
    else:
        for word in allwords:
            sum = 0
            for letter in list(set(word)):
                if(letter in dict2):
                    sum = sum + dict1[letter]
            if(sum>maxSum):
                maxSum = sum
                nextGuess = word    

    if(nextGuess == ''):
        nextGuess = possiblewords[0]

        
    return nextGuess

def loadWords():
    words = []
    with open('words.txt','r') as f:
        data = f.readlines()
        for i in data:
            words.append(i[0:5].lower())
    return words

def updateList(list,letter, pos):
    newlist =[]
    for i in list:
        if letter in i and letter != i[pos]:
            newlist.append(i)
    return newlist

def updateList2(list,letter,pos):
    newlist =[]
    for i in list:
        if letter == i[pos]:
            newlist.append(i)
    return newlist

def updateList3(list,letter):
    newlist = []
    for i in list:
        if letter not in i:
            newlist.append(i)
    return newlist

def updatePossibleWords(hints,currentlist,word):
    doubles = []
    single =[]
    for i in word:
        if i in single and i not in doubles:
            doubles.append(i)
        single.append(i)

    dict = {}
    for i in doubles:
        for j in range(len(word)):
            if(i == word[j]):
                if(hints[j]=='correct'):
                    dict[i]= 'correct'

    for i in doubles:
        if i in dict:
            for j in range(len(word)):
                if(i == word[j]):
                    if(hints[j]=='absent'):
                        hints[j] ='present'
    

    for index,i in enumerate(hints):
        if i == 'present':
            currentlist=updateList(currentlist,word[index],index) 
        if i == 'correct':
            currentlist=updateList2(currentlist,word[index],index) 
        if i == 'absent':
            currentlist=updateList3(currentlist,word[index]) 
    return currentlist

def startgame():
    PATH = './chromedriver'
    global driver
    global game
    global keyboard
    driver = webdriver.Chrome(PATH)
    driver.get("https://wordleunlimited.org")
    game = driver.find_element(by=By.CSS_SELECTOR, value='body > game-app').shadow_root.find_element(by=By.CSS_SELECTOR, value='game-theme-manager').find_element(by=By.CSS_SELECTOR, value='#game')
    close= game.find_element(by=By.CSS_SELECTOR, value='#game > game-modal').shadow_root.find_element(by=By.CSS_SELECTOR, value='div').find_element(by=By.CSS_SELECTOR, value='div > div > div')
    close.click()
    keyboard = game.find_element(by=By.CSS_SELECTOR, value='#game > game-keyboard').shadow_root.find_element(by=By.CSS_SELECTOR, value='#keyboard')

def guessword(word):
    for i in word:
        global keys
        global keyboard
        global driver
        key = keyboard.find_element(by=By.CSS_SELECTOR, value='#keyboard > div:nth-child(' + keys[i][0] +')').find_element(by=By.CSS_SELECTOR, value='#keyboard > div:nth-child(' + keys[i][0] +') > button:nth-child(' + keys[i][1:] +')')
        driver.execute_script("arguments[0].click();", key)
    key = keyboard.find_element(by=By.CSS_SELECTOR, value='#keyboard > div:nth-child(' + keys['enter'][0] +')').find_element(by=By.CSS_SELECTOR, value='#keyboard > div:nth-child(' + keys['enter'][0] +') > button:nth-child(' + keys['enter'][1:] +')')
    driver.execute_script("arguments[0].click();", key)

def gethints(row):
    global game
    hints = []
    count = 0
    for i in range(1,6):
        word = game.find_element(by=By.CSS_SELECTOR, value='#board-container').find_element(by=By.CSS_SELECTOR, value='#board').find_element(by=By.CSS_SELECTOR, value='#board > game-row:nth-child('+str(row)+')').shadow_root.find_element(by=By.CSS_SELECTOR, value='div').find_element(by=By.CSS_SELECTOR, value='div > game-tile:nth-child('+str(i)+')')
        hints.append(word.get_attribute('evaluation'))
        if(word.get_attribute('evaluation') == 'correct'):
            count+=1
    if(count==5):
        return 'DONE'
    return hints

def restart():
    time.sleep(6)
    global game
    restart = game.find_element(by=By.CSS_SELECTOR, value='#game > game-modal > game-stats').shadow_root.find_element(by=By.CSS_SELECTOR, value='div > div.footer > div.countdown').find_element(by=By.CSS_SELECTOR, value='#timer > div')
    restart.click()
    time.sleep(.5)
    global keyboard
    global driver
    driver.get("https://wordleunlimited.org")
    game = driver.find_element(by=By.CSS_SELECTOR, value='body > game-app').shadow_root.find_element(by=By.CSS_SELECTOR, value='game-theme-manager').find_element(by=By.CSS_SELECTOR, value='#game')
    keyboard = game.find_element(by=By.CSS_SELECTOR, value='#game > game-keyboard').shadow_root.find_element(by=By.CSS_SELECTOR, value='#keyboard')

def play():
    allWords = loadWords()
    possiblewords = allWords
    guesses = []
    for i in range(6):
        if(len(possiblewords)> 1):
            guess = getNextGuess(guesses,possiblewords,allWords)
        elif(len(possiblewords)==1):
            guess = possiblewords[0]
        else:
            guess = 'means'
        guesses.append(guess)
        print(guess)
        guessword(guess)
        hints = gethints(i+1)
        if(hints == 'DONE'):
            restart()
            break
        possiblewords= updatePossibleWords(hints,possiblewords,guess)
        print(possiblewords)
        time.sleep(4)
        if(guess == 'means'):
            restart()


def main():
    startgame()
    for j in range(15):
        play()



main()
driver.quit()
# row = game.find_element(by=By.CSS_SELECTOR, value='#board-container').find_element(by=By.CSS_SELECTOR, value='#board').find_element(by=By.CSS_SELECTOR, value='#board > game-row:nth-child('+str(i)+')')#.shadow_root.find_element(by=By.CSS_SELECTOR, value='div')#.find_element('div > game-tile:nth-child('+str(j)+')')
# #tile = row.find_element(by=By.CSS_SELECTOR, value='div > game-tile:nth-child(1)')

# driver.execute_script("""document.querySelector('body > game-app').shadowRoot.querySelector('game-theme-manager').querySelector('#game').querySelector('#board-container').querySelector('#board').querySelector('#board > game-row:nth-child(1)')._letters="fjord";""")




#driver.document.querySelector().shadowRoot.querySelector('game-theme-manager').querySelector('#game').querySelector('#game > game-modal').shadowRoot.querySelector('div').querySelector('div').querySelector('div > div > div').click()

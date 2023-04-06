import asyncio
import pygame
import numpy

# Constants
NUMBERS     = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
X = 800
Y = 768
LEFT_MARGIN = X * 0.1875

# Colors
PINK            = (215, 65, 167)
BACKGROUND      = (58, 23, 114)
WHITE           = (205, 205, 205)
GREEN           = (33, 78, 52)

# Fonts
QAZ = "fonts/Qaz.ttf"
SUNNYSPELLS = "fonts/SunnySpellsBasicRegular.ttf"

pygame.init()

screen = pygame.display.set_mode((X, Y))

pygame.display.set_caption("Crack the Code")

# Fonts
title_font = pygame.font.Font(QAZ, 48)
number_font = pygame.font.Font(SUNNYSPELLS, 48)
scoreTitle_font = pygame.font.Font(QAZ, 25)

# UI Elements
title = title_font.render("Crack the Code", True, PINK)
restart_text = title_font.render("Press R to restart", True, WHITE)
scoreExcelent = scoreTitle_font.render("Excellent", True, WHITE)
scoreGood = scoreTitle_font.render("Good", True, WHITE)

# Text Positioning
def getWinString(number):
    return "You Won! The number was " + listToNumber(number)

def getLoseString(number):
    return "You Lost :( The number was " + listToNumber(number)

def getStringWidth(text, font):
    text_width, text_height = font.size(text)
    return text_width

def getStringHeight(text, font):
    text_width, text_height = font.size(text)
    return text_height

# UI
def createRow(y):
    x = LEFT_MARGIN - 15
    for i in range(0,4):
        pygame.draw.rect(screen, PINK, pygame.Rect(x, y, 55, 55),  2, 3)
        x += 60

def createMatrix(height):
    count = 1
    while count <= height:
        createRow(70 * count)
        count += 1

# Generates a number with 4 random non-zero non-repeating digits
def generateRandomNumber():
    randomNumber = []
    while len(randomNumber) < 4:
        newNumber = str(numpy.random.randint(1,9))
        if newNumber not in randomNumber:
            randomNumber.append(newNumber)
    return randomNumber

def listToNumber(list):
    return str(''.join(map(str,list)))

def compareNumbers(randomNumber, input):
    counter = 0
    inTheSamePosition = 0
    inTheNumber = 0
    for i in input:
        if i in randomNumber:
            if randomNumber[counter] == i:
                inTheSamePosition += 1
            else:
                inTheNumber += 1
        counter += 1
    return (str(inTheNumber), str(inTheSamePosition))


async def main():

    run = True
    restart = True
    endGame = False
    win = False
    lose = False
    showText = True
    showScoreTitle = False

    while run:
        screen.fill(BACKGROUND)

        if restart == True:
            endGame = False
            showText = True
            showScoreTitle = False
            numberToGuess = generateRandomNumber()
            winText = title_font.render(getWinString(numberToGuess), True, WHITE)
            loseText = title_font.render(getLoseString(numberToGuess), True, WHITE)
            print(listToNumber(numberToGuess))
            actualNumbers = []
            permanentNumbers = []
            scores = []
            matrixHeight = 1
            restart = False

        if endGame == True:
            showText = False
            actualNumbers = []
            permanentNumbers = []
            scores = []
            matrixHeight = 0
            if win:
                string = getWinString(numberToGuess)
                screen.blit(winText, (X/2 - (getStringWidth(string, title_font) / 2), Y/2 - 2* (getStringHeight(string, title_font))))
                screen.blit(restart_text, (X/2 - (getStringWidth(string, title_font) / 2), Y/2 + (getStringHeight(string, title_font))))
            elif lose:
                string = getLoseString(numberToGuess)
                screen.blit(loseText, (X/2 - (getStringWidth(string, title_font) / 2), Y/2 - 2 * (getStringHeight(string, title_font))))
                screen.blit(restart_text, (X/2 - (getStringWidth(string, title_font) / 2), Y/2 + (getStringHeight(string, title_font))))

        if showText == True:
                screen.blit(title, (10, 10))
                if showScoreTitle == True:
                    screen.blit(scoreGood, (450, 40))
                    screen.blit(scoreExcelent, (535, 40))
                    
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # The game is ongoing
                if endGame == False:
                    if event.unicode in NUMBERS and len(actualNumbers) < 4:
                        if event.unicode not in actualNumbers:
                            actualNumbers.append(event.unicode)
                    elif event.key == pygame.K_BACKSPACE:
                        actualNumbers = actualNumbers[:-1]
                    elif event.key == pygame.K_r:
                        restart = True
                    elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and len(actualNumbers) == 4:
                        permanentNumbers.append(actualNumbers)
                        score = compareNumbers(numberToGuess, actualNumbers)
                        scores.append(score)
                        matrixHeight += 1
                        showScoreTitle = True
                        actualNumbers = []
                        if score[1] == '4':
                            endGame = True
                            win = True
                        elif matrixHeight == 10:
                            endGame = True
                            lose = True
                # The game is over
                if event.key == pygame.K_r:
                    restart = True

        createMatrix(matrixHeight)

        ### Number Printing ###
        y = Y * 0.104
        for list in permanentNumbers:
            x = LEFT_MARGIN
            for number in list:
                numberText = number_font.render(number, True, WHITE)
                screen.blit(numberText, (x, y))
                x += 60
            y += 70
        
        x = LEFT_MARGIN
        for number in actualNumbers:
            numberText = number_font.render(number, True, WHITE)
            screen.blit(numberText, (x, y))
            x += 60
        
        # Scores
        y = Y * 0.104
        for score in scores:
            x = LEFT_MARGIN + 325
            inTheNumber = number_font.render(score[0], True, WHITE)
            screen.blit(inTheNumber, (x, y))
            x += 100
            inTheSamePosition = number_font.render(score[1], True, WHITE)
            screen.blit(inTheSamePosition, (x, y))
            y += 70

        pygame.display.flip()

        await asyncio.sleep(0)


asyncio.run(main())

pygame.quit()
import numpy
import pygame

# Constants
NUMBEROFTRIES = 10
MINIMUM_WIDTH = 800
MINIMUM_HEIGHT = 950

#### Text Positioning ####

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
##########################

###### List Handling ######

# Returns a "cleanList" a list [' ', ..., ' '] with as many ' ' as the code to crack
def cleanList(codeLength):
	actualNumbers = []
	for i in range(0, codeLength):
		actualNumbers.append(' ')
	return actualNumbers

# We specify the number we want to add to the list, the current value of selectedSquare and the list of the actualNumbers
def addNumber(number, selectedSquare, actualNumbers):
	if number not in actualNumbers:
		if (not isListComplete(actualNumbers)) and (selectedSquare == -1):
			index = actualNumbers.index(' ')
			actualNumbers[index] = number
		# If the list is complete or incomplete but there is a square selected we have to replace that number with a new one
		elif selectedSquare != -1:
			actualNumbers[selectedSquare] = number
		
		# We deselect any square that was selected
		return -1
		
	# If we selected a square and input a number that is already on the list we simply return the previous value
	# To the user it seems like it does nothing
	return selectedSquare

# If no square is selected it looks for the first number it finds and replaces it with ' '
def deleteNumber(list, selectedSquare):
	if selectedSquare == -1:
		for i in range(1, len(list) + 1):
			if list[-i] != ' ':
				list[-i] = ' '
				return list
	else:
		list[selectedSquare] = ' '
		return list
	return list

# Just checks if the list is not filled with ' '
def hasElementToDelete(list):
	for i in range(0, len(list)):
		if list[i] != ' ':
			return True
	return False

# ["1", "2", "3", "4"] -> 1234
def listToNumber(list):
	return str(''.join(map(str,list)))

# Returns true if the list has no ' ' in it 
def isListComplete(list):
	return (not ' ' in list)
############################

# Generates a number with 4 random non-zero non-repeating digits
def generateRandomNumber(codeLength):
	randomNumber = []
	while len(randomNumber) < codeLength:
		newNumber = str(numpy.random.randint(1,9))
		if newNumber not in randomNumber:
			randomNumber.append(newNumber)
	return randomNumber

# Compares the random number with the user's input, return a tuple of strings (goodNumbers, excellentNumbers)
def compareNumbers(randomNumber, input):
	counter = 0
	goodNumbers = 0
	excellentNumbers = 0
	for i in input:
		if i in randomNumber:
			if randomNumber[counter] == i:
				excellentNumbers += 1
			else:
				goodNumbers += 1
		counter += 1
	return (str(goodNumbers), str(excellentNumbers))

# Appends the number we submit to the permanentNumbers and the score to the scores list, also checks if the conditions to win are met
def submitNumber(permanentNumbers, actualNumbers, matrixHeight, numberToGuess, scores, codeLength):
	permanentNumbers_return = permanentNumbers.copy()
	permanentNumbers_return.append(actualNumbers.copy())
	score = compareNumbers(numberToGuess, actualNumbers.copy())
	scores_return = scores.copy()
	scores_return.append(score)
	matrixHeight += 1
	selectedSquare = -1
	showScoreTitle = True
	actualNumbers_return = actualNumbers.copy()
	actualNumbers_return = cleanList(codeLength)
	endGame = False
	win = False
	lose = False
	if score[1] == str(codeLength):
		endGame = True
		win = True
	elif matrixHeight == NUMBEROFTRIES + 1:
		endGame = True
		lose = True

	return permanentNumbers_return, scores_return, actualNumbers_return, matrixHeight, selectedSquare, showScoreTitle, endGame, win, lose

# Handles the resizing of the window
def resize(width, height, screen):
	# The window cannot be resized less than the minimum
	if (width >= MINIMUM_WIDTH) and (height >= MINIMUM_HEIGHT):
		window_X = width
		window_Y = height
		screen = pygame.display.set_mode((window_X, window_Y), pygame.RESIZABLE)
	else:
		window_X = MINIMUM_WIDTH
		window_Y = MINIMUM_HEIGHT
		screen = pygame.display.set_mode((window_X, window_Y), pygame.RESIZABLE)
	
	return window_X, window_Y, screen

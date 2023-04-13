import asyncio
import pygame
import numpy

# Constants
MINIMUM_WIDTH = 800
MINIMUM_HEIGHT = 950
NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
NUMBEROFTRIES = 10
CODELENGTH = 4
MATRIXSQUARESIZE = 55	# The size of the numbers should be defined according to this value
KEYBOARD_SQUARESIZE = 70
SUBMIT_BUTTON_WIDTH = 250
SUBMIT_BUTTON_HEIGHT = 50

pygame.init()

# Initial values
window_X = 800
window_Y = 950

print(window_X)
print(window_Y)
left_margin = 200 	# Used to move the numbers, squares and scores horizontally

# Colors
PINK			= (215, 65, 167)
PURPLE			= (58, 23, 114)
WHITE			= (205, 205, 205)
BLACK			= (0, 0, 0)
GREY 			= (172, 165, 185)
GREY2			= (205, 205, 205)

# Fonts
QAZ 			= "assets/fonts/Qaz.ttf"
SUNNYSPELLS 	= "assets/fonts/SunnySpellsBasicRegular.ttf"

screen = pygame.display.set_mode((window_X, window_Y), pygame.RESIZABLE)

pygame.display.set_caption("Crack the Code")

# Fonts
title_font      = pygame.font.Font(QAZ, 48)
subtitle_font   = pygame.font.Font(QAZ, 35)
scoreTitle_font = pygame.font.Font(QAZ, 25)
number_font     = pygame.font.Font(SUNNYSPELLS, 48)
keyboard_font   = pygame.font.Font(SUNNYSPELLS, 80)

# UI Elements
title			= title_font.render("Crack the Code", True, PINK)
submitWhite		= subtitle_font.render("Submit", True, GREY2)
submitPurple	= subtitle_font.render("Submit", True, PURPLE)
restart_text 	= subtitle_font.render("To restart press R or click the screen", True, WHITE)
scoreExcelent 	= scoreTitle_font.render("Excellent", True, WHITE)
scoreGood		= scoreTitle_font.render("Good", True, WHITE)

# Images
backspace = pygame.image.load("assets/img/backspace.png").convert_alpha() #convert.alpha is to keep transparency

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

#### UI ####
def createRow(y, selectedSquare, leftMargin):
	x = leftMargin
	for i in range(0, CODELENGTH):
		if selectedSquare == i:
			pygame.draw.rect(screen, WHITE, pygame.Rect(x, y, MATRIXSQUARESIZE, MATRIXSQUARESIZE),  2, 3)
		else:
			pygame.draw.rect(screen, PINK, pygame.Rect(x, y, MATRIXSQUARESIZE, MATRIXSQUARESIZE),  2, 3)
		x += MATRIXSQUARESIZE + 5

def createMatrix(height, selectedSquare, left_margin):
	count = 1
	while count < height:
		createRow(70 * count, -1, left_margin)
		count += 1
	if height != 0:
		createRow(70 * count, selectedSquare, left_margin)

def drawKeyboard(actualNumbers, keyboard_X, keyboard_Y):
	# Squares
	x = keyboard_X
	
	# Squares for the numbers
	for i in range(1,10):
		# If a number is introduced the color of its key changes
		if str(i) in actualNumbers:
			pygame.draw.rect(screen, BLACK, pygame.Rect(x, keyboard_Y, KEYBOARD_SQUARESIZE, KEYBOARD_SQUARESIZE),  0, 3)
		else:
			pygame.draw.rect(screen, PINK, pygame.Rect(x, keyboard_Y, KEYBOARD_SQUARESIZE, KEYBOARD_SQUARESIZE),  0, 3)
		x += KEYBOARD_SQUARESIZE + 5
	
	# Square for the backspace
	pygame.draw.rect(screen, PINK, pygame.Rect(x, keyboard_Y, KEYBOARD_SQUARESIZE, KEYBOARD_SQUARESIZE),  0, 3)
	
	# Numbers / Backspace
	x = keyboard_X + 20
	y = keyboard_Y + 5
	for i in range(1, 10):
		# Same logic that with the squares, if its on the list the color changes
		if str(i) in actualNumbers:
			numberText = keyboard_font.render(str(i), True, PINK)
		else:
			numberText = keyboard_font.render(str(i), True, PURPLE)
		screen.blit(numberText, (x, y))
		x += KEYBOARD_SQUARESIZE + 5
	
	# Backspace Image
	screen.blit(backspace, (keyboard_X + (KEYBOARD_SQUARESIZE + 5) * 9, keyboard_Y))

	# Submit Button
	x = keyboard_X + (KEYBOARD_SQUARESIZE + 5) * (5 - (SUBMIT_BUTTON_WIDTH / 75) / 2) - 5
	y = keyboard_Y + KEYBOARD_SQUARESIZE + 10
	x_string = (x + (SUBMIT_BUTTON_WIDTH / 2)) - (getStringWidth("submit", subtitle_font) / 2) - 3
	y_string = (y + (SUBMIT_BUTTON_HEIGHT / 2)) - (getStringHeight("submit", subtitle_font) / 2)
	if isListComplete(actualNumbers):
		pygame.draw.rect(screen, PINK, pygame.Rect(x, y, SUBMIT_BUTTON_WIDTH, SUBMIT_BUTTON_HEIGHT),  0, 3)
		screen.blit(submitPurple, (x_string, y_string))
	else:
		pygame.draw.rect(screen, GREY, pygame.Rect(x, y, SUBMIT_BUTTON_WIDTH, SUBMIT_BUTTON_HEIGHT),  0, 3)
		screen.blit(submitWhite, (x_string, y_string))


#### Auxiliary Functions ####

# Generates a number with 4 random non-zero non-repeating digits
def generateRandomNumber():
	randomNumber = []
	while len(randomNumber) < CODELENGTH:
		newNumber = str(numpy.random.randint(1,9))
		if newNumber not in randomNumber:
			randomNumber.append(newNumber)
	return randomNumber

# ["1", "2", "3", "4"] -> 1234
def listToNumber(list):
	return str(''.join(map(str,list)))

def isListComplete(list):
	return (not (' ' in list)) and (len(list) == CODELENGTH)

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

# We specify the number we want to add, the current value of selectedSquare and the list of the actualNumbers
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

def submitNumber(permanentNumbers, actualNumbers, matrixHeight, numberToGuess, scores):
	permanentNumbers_return = permanentNumbers.copy()
	permanentNumbers_return.append(actualNumbers.copy())
	score = compareNumbers(numberToGuess, actualNumbers.copy())
	scores_return = scores.copy()
	scores_return.append(score)
	matrixHeight += 1
	selectedSquare = -1
	showScoreTitle = True
	actualNumbers_return = actualNumbers.copy()
	actualNumbers_return = [' ', ' ', ' ', ' ']
	endGame = False
	win = False
	lose = False
	if score[1] == str(CODELENGTH):
		endGame = True
		win = True
	elif matrixHeight == NUMBEROFTRIES + 1:
		endGame = True
		lose = True

	return permanentNumbers_return, scores_return, actualNumbers_return, matrixHeight, selectedSquare, showScoreTitle, endGame, win, lose
	
# Function that happens every frame
async def main(screen, window_X, window_Y):
	run = True
	restart = True
	endGame = False
	win = False
	lose = False
	showText = True
	showScoreTitle = False
	matrixHeight = 1
	selectedSquare = -1

	while run:
		# UI Related
		left_margin = window_X / 2 - 510/2	# 510 pixels is the aproximate width of the matrix and the scores combined
		keyboard_X = int((window_X / 2) - ((((KEYBOARD_SQUARESIZE + 5) * 10) - 5) / 2))
		keyboard_Y = window_Y - 150

		screen.fill(PURPLE)
		createMatrix(matrixHeight, selectedSquare, left_margin)

		if restart == True:
			endGame = False
			lose = False
			win = False
			showText = True
			showScoreTitle = False
			numberToGuess = generateRandomNumber()
			winText = title_font.render(getWinString(numberToGuess), True, WHITE)
			loseText = title_font.render(getLoseString(numberToGuess), True, WHITE)
			print(listToNumber(numberToGuess))
			actualNumbers = [' ', ' ', ' ', ' ']
			permanentNumbers = []
			scores = []
			matrixHeight = 1
			restart = False

		if endGame == True:
			showText = False
			actualNumbers = [' ', ' ', ' ', ' ']
			permanentNumbers = []
			scores = []
			matrixHeight = 0
			if win:
				string = getWinString(numberToGuess)
				screen.blit(winText, (window_X/2 - (getStringWidth(string, title_font) / 2), window_Y/2 - 2* (getStringHeight(string, title_font))))
				screen.blit(restart_text, (window_X/2 - (getStringWidth(string, title_font) / 2), window_Y/2 + (getStringHeight(string, title_font))))
			elif lose:
				string = getLoseString(numberToGuess)
				screen.blit(loseText, (window_X/2 - (getStringWidth(string, title_font) / 2), window_Y/2 - 2 * (getStringHeight(string, title_font))))
				screen.blit(restart_text, (window_X/2 - (getStringWidth(string, title_font) / 2), window_Y/2 + (getStringHeight(string, title_font))))

		if showText == True:
				screen.blit(title, (10, 10))
				# On-Screen Keyboard
				drawKeyboard(actualNumbers, keyboard_X, keyboard_Y)
				if showScoreTitle == True:
					screen.blit(scoreGood, (left_margin + 300, 40))
					screen.blit(scoreExcelent, (left_margin + 385, 40))
					
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				# The game is ongoing
				if endGame == False:
					if (event.unicode in NUMBERS):
						selectedSquare = addNumber(event.unicode, selectedSquare, actualNumbers)
					elif event.key == pygame.K_BACKSPACE:
						actualNumbers = deleteNumber(actualNumbers, selectedSquare)
						selectedSquare = -1
					elif event.key == pygame.K_r:
						restart = True
					elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and isListComplete(actualNumbers):
						permanentNumbers, scores, actualNumbers, matrixHeight, selectedSquare, showScoreTitle, endGame, win, lose = submitNumber(permanentNumbers, actualNumbers, matrixHeight, numberToGuess, scores)
					elif event.key == pygame.K_ESCAPE:
						run = False
				# The game is over
				elif event.key == pygame.K_r:
					restart = True
				
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				if endGame == False:
					mouse = pygame.mouse.get_pos()
					#### On-screen Keyboard Actions ####
					# We check if we are on the rectangle that the set of button creates
					if (keyboard_X < mouse[0] < (keyboard_X + (KEYBOARD_SQUARESIZE + 5) * 10 - 5)) and (keyboard_Y < mouse[1] < keyboard_Y + KEYBOARD_SQUARESIZE):
						x_keyboard = keyboard_X
						for i in range(1, 10):
							# When we find the number we check if it meets the criteria to be on the list
							if (x_keyboard < mouse[0] < x_keyboard + 70):
									selectedSquare = addNumber(str(i), selectedSquare, actualNumbers)
									break
							x_keyboard += 75
						# This means we were on the range but none of 9 numbers matched, which means we clicked on the erase button
						if mouse[0] > keyboard_X + (KEYBOARD_SQUARESIZE + 5) * 9:
							actualNumbers = deleteNumber(actualNumbers, selectedSquare)
							selectedSquare = -1
					
					# If we are not on the numbers maybe we are on the submit button
					elif (keyboard_X + (KEYBOARD_SQUARESIZE + 5) * (5 - (SUBMIT_BUTTON_WIDTH / 75) / 2) - 5 < mouse[0] < keyboard_X + (KEYBOARD_SQUARESIZE + 5) * (5 - (SUBMIT_BUTTON_WIDTH / 75) / 2) - 5 + SUBMIT_BUTTON_WIDTH) and (keyboard_Y + KEYBOARD_SQUARESIZE + 10 < mouse[1] < keyboard_Y + KEYBOARD_SQUARESIZE + 10 + SUBMIT_BUTTON_HEIGHT) and isListComplete(actualNumbers):
						permanentNumbers, scores, actualNumbers, matrixHeight, selectedSquare, showScoreTitle, endGame, win, lose = submitNumber(permanentNumbers, actualNumbers, matrixHeight, numberToGuess, scores)
					
					#### Square selector ####
					elif (left_margin < mouse[0] < left_margin + (MATRIXSQUARESIZE + 5) * CODELENGTH - 5) and (70 * matrixHeight < mouse[1] < 70 * matrixHeight + MATRIXSQUARESIZE):
						x_row = left_margin
						for i in range(0, CODELENGTH):
							if (x_row < mouse[0] < x_row + MATRIXSQUARESIZE):
								if selectedSquare != i:
									selectedSquare = i
									break
								# If the squared we pushed was already selected we deselect it
								else:
									selectedSquare = -1
									break
							x_row += MATRIXSQUARESIZE + 5
					
					# We clicked anywhere else on the screen
					else:
						selectedSquare = -1
					
				else:
					restart = True
			
			if (event.type == pygame.VIDEORESIZE):
				if (event.w >= MINIMUM_WIDTH) and (event.h >= MINIMUM_HEIGHT):
					window_X = event.w
					window_Y = event.h
					left_margin = window_X / 2 - 510/2				# 510 pixels is the aproximate width of the matrix and the scores combined
				
				screen = pygame.display.set_mode((window_X, window_Y), pygame.RESIZABLE)

		### Number Printing ###
		y = 80
		for list in permanentNumbers:
			x = left_margin + 15
			for number in list:
				numberText = number_font.render(number, True, WHITE)
				screen.blit(numberText, (x, y))
				x += MATRIXSQUARESIZE + 5
			y += 70
		
		x = left_margin + 15
		for number in actualNumbers:
			numberText = number_font.render(number, True, WHITE)
			screen.blit(numberText, (x, y))
			x += MATRIXSQUARESIZE + 5
		
		# Scores
		y = 80
		for score in scores:
			x = left_margin + 320
			inTheNumber = number_font.render(score[0], True, WHITE)
			screen.blit(inTheNumber, (x, y))
			x += 100
			inTheSamePosition = number_font.render(score[1], True, WHITE)
			screen.blit(inTheSamePosition, (x, y))
			y += 70

		pygame.display.flip()

		await asyncio.sleep(0)


asyncio.run(main(screen, window_X, window_Y))

pygame.quit()
import asyncio
import pygame
import numpy

# Constants
NUMBERS     = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
NUMBEROFTRIES = 10
X = 800
Y = 950
LEFT_MARGIN = X * 0.1875

# Colors
PINK            = (215, 65, 167)
BACKGROUND      = (58, 23, 114)
WHITE           = (205, 205, 205)
GREEN           = (33, 78, 52)

# Fonts
QAZ = "assets/fonts/Qaz.ttf"
SUNNYSPELLS = "assets/fonts/SunnySpellsBasicRegular.ttf"

pygame.init()

screen = pygame.display.set_mode((X, Y))

pygame.display.set_caption("Crack the Code")

# Fonts
title_font      = pygame.font.Font(QAZ, 48)
subtitle_font   = pygame.font.Font(QAZ, 35)
number_font     = pygame.font.Font(SUNNYSPELLS, 48)
scoreTitle_font = pygame.font.Font(QAZ, 25)


# UI Elements
title = title_font.render("Crack the Code", True, PINK)
submit = subtitle_font.render("Submit", True, WHITE)
restart_text = subtitle_font.render("To restart press R or click the screen", True, WHITE)
scoreExcelent = scoreTitle_font.render("Excellent", True, WHITE)
scoreGood = scoreTitle_font.render("Good", True, WHITE)

# Images
backArrow = pygame.image.load("assets/img/backArrow.png").convert_alpha() #convert.alpha is to keep transparency

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
		pygame.draw.rect(screen, PINK, pygame.Rect(x, y, X * 0.06875, X * 0.06875),  2, 3)
		x += X * 0.075

def createMatrix(height):
	count = 1
	while count <= height:
		createRow(70 * count)
		count += 1

def drawKeyboard():
	# Squares
	x = (X / 2) - 300
	for i in range(0,10):
		pygame.draw.rect(screen, PINK, pygame.Rect(x, 800, X * 0.06875, X * 0.06875),  2, 3)
		x += 60
	
	# Numbers / Backspace
	x = (X / 2) - 300 + 18
	y = 810
	for i in range(1, 10):
		numberText = number_font.render(str(i), True, WHITE)
		screen.blit(numberText, (x, y))
		x += 60
	screen.blit(backArrow, (640, 800))

	# Submit Button
	width = 180
	height = 50
	x = (X / 2) - (width / 2)
	y = 880
	pygame.draw.rect(screen, PINK, pygame.Rect(x, 880, width, height),  2, 3)
	x_string = (x + (width / 2)) - (getStringWidth("submit", subtitle_font) / 2) - 3
	y_string = (y + (height / 2)) - (getStringHeight("submit", subtitle_font) / 2)
	screen.blit(submit, (x_string, y_string))
	

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
				drawKeyboard()
				if showScoreTitle == True:
					screen.blit(scoreGood, (450, 40))
					screen.blit(scoreExcelent, (535, 40))
					
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				# The game is ongoing
				if endGame == False:
					if (event.unicode in NUMBERS) and (len(actualNumbers) < 4) and (event.unicode not in actualNumbers):
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
						elif matrixHeight == NUMBEROFTRIES + 1:
							endGame = True
							lose = True
				# The game is over
				elif event.key == pygame.K_r:
					restart = True
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				if endGame == False:
					mouse = pygame.mouse.get_pos()
					print(mouse[0], mouse[1])
					# We check if we are on the rectangle that the set of button creates
					if (100 < mouse[0] < 700) and (800 < mouse[1] < 855):
						x_keyboard = 100
						for i in range(1, 10):
							if (x_keyboard < mouse[0] < x_keyboard + 55):
								# When we find the number we check if it meets the criteria to be on the list
								if (str(i) not in actualNumbers)and (len(actualNumbers) < 4):
									actualNumbers.append(str(i))
								break
							x_keyboard += 60
							i += 1
						# This means we were on the range but none of 9 numbers matched, which means we clicked on the erase button
						if mouse[0] > 640:
							actualNumbers = actualNumbers[:-1]
					elif (310 < mouse[0] < 490) and (880 < mouse[1] < 930) and len(actualNumbers) == 4:
						permanentNumbers.append(actualNumbers)
						score = compareNumbers(numberToGuess, actualNumbers)
						scores.append(score)
						matrixHeight += 1
						showScoreTitle = True
						actualNumbers = []
						if score[1] == '4':
							endGame = True
							win = True
						elif matrixHeight == NUMBEROFTRIES + 1:
							endGame = True
							lose = True
				else:
					restart = True

		createMatrix(matrixHeight)

		### Number Printing ###
		y = 80
		for list in permanentNumbers:
			x = LEFT_MARGIN
			for number in list:
				numberText = number_font.render(number, True, WHITE)
				screen.blit(numberText, (x, y))
				x += X * 0.075
			y += 70
		
		x = LEFT_MARGIN
		for number in actualNumbers:
			numberText = number_font.render(number, True, WHITE)
			screen.blit(numberText, (x, y))
			x += X * 0.075
		
		# Scores
		y = 80
		for score in scores:
			x = LEFT_MARGIN + X * 0.4
			inTheNumber = number_font.render(score[0], True, WHITE)
			screen.blit(inTheNumber, (x, y))
			x += X * 0.125
			inTheSamePosition = number_font.render(score[1], True, WHITE)
			screen.blit(inTheSamePosition, (x, y))
			y += 70

		pygame.display.flip()

		await asyncio.sleep(0)


asyncio.run(main())

pygame.quit()
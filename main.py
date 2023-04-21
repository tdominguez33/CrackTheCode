import asyncio
import pygame
from auxiliaryFunctions import *

# Constants
NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
MATRIXSQUARESIZE = 55
KEYBOARD_SQUARESIZE = 70
SUBMIT_BUTTON_WIDTH = 250
SUBMIT_BUTTON_HEIGHT = 50
DIFFICULTY_BUTTON_WIDTH = 200
DIFFICULTY_BUTTON_HEIGHT = 150
DIFFICULTY_BUTTON_SEPARATION = 30

# Colors
BLACK			= (0, 0, 0)
WHITE			= (205, 205, 205)
PINK			= (215, 65, 167)
PURPLE			= (58, 23, 114)
GREY 			= (172, 165, 185)
GREY2			= (205, 205, 205)

# Font directories
QAZ 			= "assets/fonts/Qaz.ttf"
SUNNYSPELLS 	= "assets/fonts/SunnySpellsBasicRegular.ttf"

# Initial resolution values
window_X 		= 800
window_Y 		= 950

# PyGame initialization
pygame.init()
pygame.display.set_caption("Crack the Code")
screen = pygame.display.set_mode((window_X, window_Y), pygame.RESIZABLE)

# Fonts
title_font      = pygame.font.Font(QAZ, 48)
subtitle_font   = pygame.font.Font(QAZ, 35)
scoreTitle_font = pygame.font.Font(QAZ, 25)
keyboard_font   = pygame.font.Font(SUNNYSPELLS, 80)
number_font     = pygame.font.Font(SUNNYSPELLS, 48)

# Constant UI Text
title				= title_font.render("Crack the Code", True, PINK)
difficultyText 		= title_font.render("Select Difficulty:", True, WHITE)
submitWhite			= subtitle_font.render("Submit", True, GREY2)
submitPurple		= subtitle_font.render("Submit", True, PURPLE)
restart_text 		= subtitle_font.render("To restart press R or click the screen", True, WHITE)
easy				= subtitle_font.render("Easy", True, PURPLE)
easy_digits			= subtitle_font.render("(3 Digits)", True, PURPLE)
normal				= subtitle_font.render("Normal", True, PURPLE)
normal_digits		= subtitle_font.render("(4 Digits)", True, PURPLE)
hard				= subtitle_font.render("Hard", True, PURPLE)
hard_digits			= subtitle_font.render("(5 Digits)", True, PURPLE)
easy_hover			= subtitle_font.render("Easy", True, PINK)
easy_digits_hover 	= subtitle_font.render("(3 Digits)", True, PINK)
normal_hover		= subtitle_font.render("Normal", True, PINK)
normal_digits_hover	= subtitle_font.render("(4 Digits)", True, PINK)
hard_hover			= subtitle_font.render("Hard", True, PINK)
hard_digits_hover 	= subtitle_font.render("(5 Digits)", True, PINK)
scoreExcelent 		= scoreTitle_font.render("Excellent", True, WHITE)
scoreGood			= scoreTitle_font.render("Good", True, WHITE)

# Images
backspacePurple = pygame.image.load("assets/img/backspace_purple.png").convert_alpha() #convert.alpha() is to keep the transparency
backspacePink = pygame.image.load("assets/img/backspace_pink.png").convert_alpha()

#### UI ####
def createRow(y, selectedSquare, leftMargin, codeLength):
	x = leftMargin
	for i in range(0, codeLength):
		if selectedSquare == i:
			pygame.draw.rect(screen, WHITE, pygame.Rect(x, y, MATRIXSQUARESIZE, MATRIXSQUARESIZE),  2, 3)
		else:
			pygame.draw.rect(screen, PINK, pygame.Rect(x, y, MATRIXSQUARESIZE, MATRIXSQUARESIZE),  2, 3)
		x += MATRIXSQUARESIZE + 5

def createMatrix(height, selectedSquare, left_margin, codeLength):
	count = 1
	while count < height:
		createRow(70 * count, -1, left_margin, codeLength)
		count += 1
	if height != 0:
		createRow(70 * count, selectedSquare, left_margin, codeLength)

def drawKeyboard(actualNumbers, keyboard_X, keyboard_Y, submit_X, backspacePress):
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
	
	# Square and image for the backspace
	if backspacePress:
		pygame.draw.rect(screen, BLACK, pygame.Rect(x, keyboard_Y, KEYBOARD_SQUARESIZE, KEYBOARD_SQUARESIZE),  0, 3)
		screen.blit(backspacePink, (keyboard_X + (KEYBOARD_SQUARESIZE + 5) * 9, keyboard_Y))
	else:
		pygame.draw.rect(screen, PINK, pygame.Rect(x, keyboard_Y, KEYBOARD_SQUARESIZE, KEYBOARD_SQUARESIZE),  0, 3)
		screen.blit(backspacePurple, (keyboard_X + (KEYBOARD_SQUARESIZE + 5) * 9, keyboard_Y))
	
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

	# Submit Button
	x = submit_X
	y = keyboard_Y + KEYBOARD_SQUARESIZE + 10
	x_string = (x + (SUBMIT_BUTTON_WIDTH / 2)) - (getStringWidth("Submit", subtitle_font) / 2) - 3
	y_string = (y + (SUBMIT_BUTTON_HEIGHT / 2)) - (getStringHeight("Submit", subtitle_font) / 2)
	if isListComplete(actualNumbers):
		pygame.draw.rect(screen, PINK, pygame.Rect(x, y, SUBMIT_BUTTON_WIDTH, SUBMIT_BUTTON_HEIGHT),  0, 3)
		screen.blit(submitPurple, (x_string, y_string))
	else:
		pygame.draw.rect(screen, GREY, pygame.Rect(x, y, SUBMIT_BUTTON_WIDTH, SUBMIT_BUTTON_HEIGHT),  0, 3)
		screen.blit(submitWhite, (x_string, y_string))

# Screen to select difficulty
def selectDifficulty(window_X, window_Y, left_margin, buttonHover):
	screen.blit(difficultyText, (left_margin - getStringWidth("Select Difficulty:", title_font) / 2, window_Y * 0.25))
	width = DIFFICULTY_BUTTON_WIDTH
	height = DIFFICULTY_BUTTON_HEIGHT
	separation = DIFFICULTY_BUTTON_SEPARATION
	x = (window_X - 3 * width - 2 * 30) / 2
	y = window_Y * 0.5 - height / 2
	y_text = y + (height - getStringHeight("Easy", subtitle_font)) / 3

	# We draw the 3 button to choose difficulty
	if buttonHover == 1:
		pygame.draw.rect(screen, BLACK, pygame.Rect(x, y, width, height),  0, 3)
		screen.blit(easy_hover, (x + (width - getStringWidth("Easy", subtitle_font)) / 2, y_text))
		screen.blit(easy_digits_hover, (x + (width - getStringWidth("(3 Digits)", subtitle_font)) / 2, y_text + 50))
	else:
		pygame.draw.rect(screen, PINK, pygame.Rect(x, y, width, height),  0, 3)
		screen.blit(easy, (x + (width - getStringWidth("Easy", subtitle_font)) / 2, y_text))
		screen.blit(easy_digits, (x + (width - getStringWidth("(3 Digits)", subtitle_font)) / 2, y_text + 50))
	
	x += width + separation
	
	if buttonHover == 2:
		pygame.draw.rect(screen, BLACK, pygame.Rect(x, y, width, height),  0, 3)
		screen.blit(normal_hover, (x + (width - getStringWidth("Normal", subtitle_font)) / 2, y + (height - getStringHeight("Normal", subtitle_font)) / 3))
		screen.blit(normal_digits_hover, (x + (width - getStringWidth("(4 Digits)", subtitle_font)) / 2, y_text + 50))
	else:
		pygame.draw.rect(screen, PINK, pygame.Rect(x, y, width, height),  0, 3)
		screen.blit(normal, (x + (width - getStringWidth("Normal", subtitle_font)) / 2, y + (height - getStringHeight("Normal", subtitle_font)) / 3))
		screen.blit(normal_digits, (x + (width - getStringWidth("(4 Digits)", subtitle_font)) / 2, y_text + 50))
	
	x += width + separation
	
	if buttonHover == 3:
		pygame.draw.rect(screen, BLACK, pygame.Rect(x, y, width, height),  0, 3)
		screen.blit(hard_hover, (x + (width - getStringWidth("Hard", subtitle_font)) / 2, y + (height - getStringHeight("Hard", subtitle_font)) / 3))
		screen.blit(hard_digits_hover, (x + (width - getStringWidth("(5 Digits)", subtitle_font)) / 2, y_text + 50))
	else:
		pygame.draw.rect(screen, PINK, pygame.Rect(x, y, width, height),  0, 3)
		screen.blit(hard, (x + (width - getStringWidth("Hard", subtitle_font)) / 2, y + (height - getStringHeight("Hard", subtitle_font)) / 3))
		screen.blit(hard_digits, (x + (width - getStringWidth("(5 Digits)", subtitle_font)) / 2, y_text + 50))


#### Main Function ####
# Function that happens every frame
async def main(screen, window_X, window_Y):
	# Starting conditions
	starting 		= True
	run 			= True
	restart 		= True
	showText 		= True
	endGame 		= False
	win 			= False
	lose 			= False
	showScoreTitle 	= False
	matrixHeight = 1
	selectedSquare = -1
	codeLength = 4
	backspacePress = False
	buttonHover = 0

	while run:
		# UI Related - These variable depend on window_X and window_Y that can change if the window is resized
		left_margin = window_X / 2 - ((MATRIXSQUARESIZE + 5) * codeLength + getStringWidth("Good", scoreTitle_font) + 10 + getStringWidth("Excelent", scoreTitle_font))/2
		keyboard_X = int((window_X / 2) - ((((KEYBOARD_SQUARESIZE + 5) * 10) - 5) / 2))
		keyboard_Y = window_Y - 150
		submit_X = window_X / 2 - SUBMIT_BUTTON_WIDTH / 2

		# Background color
		screen.fill(PURPLE)
			
		
		#if lastValue == keys[pygame.K_BACKSPACE] == True:
			#backspacePress = True

		if starting:
			# We set a value manually so it doesn't depend on the codeLength
			left_margin = window_X / 2 - ((MATRIXSQUARESIZE + 5) * 4 + getStringWidth("Good", scoreTitle_font) + 10 + getStringWidth("Excelent", scoreTitle_font))/2
			selectDifficulty(window_X, window_Y, left_margin, buttonHover)

			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					run = False

				# Difficulty Selection
				mouse = pygame.mouse.get_pos()
				x = (window_X - 3 * DIFFICULTY_BUTTON_WIDTH - 2 * 30) / 2
				y = window_Y * 0.5 - DIFFICULTY_BUTTON_HEIGHT / 2
				if (x < mouse[0] < x + DIFFICULTY_BUTTON_WIDTH) and (y < mouse[1] < y + DIFFICULTY_BUTTON_HEIGHT):
					buttonHover = 1
				elif (x + DIFFICULTY_BUTTON_WIDTH + DIFFICULTY_BUTTON_SEPARATION < mouse[0] < x + 2 * DIFFICULTY_BUTTON_WIDTH + DIFFICULTY_BUTTON_SEPARATION) and (y < mouse[1] < y + DIFFICULTY_BUTTON_HEIGHT):
					buttonHover = 2
				elif (x + 2 * DIFFICULTY_BUTTON_WIDTH + 2 * DIFFICULTY_BUTTON_SEPARATION < mouse[0] < x + 3 * DIFFICULTY_BUTTON_WIDTH + 2 * DIFFICULTY_BUTTON_SEPARATION) and (y < mouse[1] < y + DIFFICULTY_BUTTON_HEIGHT):
					buttonHover = 3
				else: 
					buttonHover = 0
				


				if event.type == pygame.MOUSEBUTTONDOWN:
					# We check if we are on the height of the buttons
					if (y < mouse[1] < y + DIFFICULTY_BUTTON_HEIGHT):
						if (x < mouse[0] < x + DIFFICULTY_BUTTON_WIDTH):
							codeLength = 3
							starting = False
						elif (x + DIFFICULTY_BUTTON_WIDTH + DIFFICULTY_BUTTON_SEPARATION < mouse[0] < x + 2 * DIFFICULTY_BUTTON_WIDTH + DIFFICULTY_BUTTON_SEPARATION):
							codeLength = 4
							starting = False
						elif (x + 2 * DIFFICULTY_BUTTON_WIDTH + 2 * DIFFICULTY_BUTTON_SEPARATION < mouse[0] < x + 3 * DIFFICULTY_BUTTON_WIDTH + 2 * DIFFICULTY_BUTTON_SEPARATION):
							codeLength = 5
							starting = False
				
				if event.type == pygame.VIDEORESIZE:
					window_X, window_Y, screen = resize(event.w, event.h, screen)
		else:

			createMatrix(matrixHeight, selectedSquare, left_margin, codeLength)
				
			if restart == True:
				endGame = False
				lose = False
				win = False
				showText = True
				showScoreTitle = False
				numberToGuess = generateRandomNumber(codeLength)
				winText = title_font.render(getWinString(numberToGuess), True, WHITE)
				loseText = title_font.render(getLoseString(numberToGuess), True, WHITE)
				print(listToNumber(numberToGuess))
				actualNumbers = cleanList(codeLength)
				permanentNumbers = []
				scores = []
				matrixHeight = 1
				restart = False

			if endGame == True:
				showText = False
				actualNumbers = cleanList(codeLength)
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
						
			for event in pygame.event.get():
				
				if event.type == pygame.QUIT:
					run = False

				if event.type == pygame.KEYDOWN:
					# The game is ongoing
					if endGame == False:
						if (event.unicode in NUMBERS):
							selectedSquare = addNumber(event.unicode, selectedSquare, actualNumbers)
						elif event.key == pygame.K_BACKSPACE:
							if hasElementToDelete(actualNumbers):
								# We change the color of the button via the backspacePress flag
								backspacePress = True
							actualNumbers = deleteNumber(actualNumbers, selectedSquare)
							selectedSquare = -1
						elif event.key == pygame.K_r:
							restart = True
							starting = True
						elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and isListComplete(actualNumbers):
							permanentNumbers, scores, actualNumbers, matrixHeight, selectedSquare, showScoreTitle, endGame, win, lose = submitNumber(permanentNumbers, actualNumbers, matrixHeight, numberToGuess, scores, codeLength)
						elif event.key == pygame.K_ESCAPE:
							run = False
					
					# The game is over
					elif event.key == pygame.K_r:
						restart = True
						starting = True

				# Resets the color of the backspace color when the key is released
				if event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
					backspacePress = False
				
				if event.type == pygame.MOUSEBUTTONDOWN:
					# The game is ongoing
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
								if hasElementToDelete(actualNumbers):
									# We change the color of the button via the backspacePress flag
									backspacePress = True
								actualNumbers = deleteNumber(actualNumbers, selectedSquare)
								selectedSquare = -1
						
						# If we are not on the numbers maybe we are on the submit button
						elif (submit_X < mouse[0] < submit_X + SUBMIT_BUTTON_WIDTH) and (keyboard_Y + KEYBOARD_SQUARESIZE + 10 < mouse[1] < keyboard_Y + KEYBOARD_SQUARESIZE + 10 + SUBMIT_BUTTON_HEIGHT) and isListComplete(actualNumbers):
							permanentNumbers, scores, actualNumbers, matrixHeight, selectedSquare, showScoreTitle, endGame, win, lose = submitNumber(permanentNumbers, actualNumbers, matrixHeight, numberToGuess, scores, codeLength)
						
						#### Square selector ####
						elif (left_margin < mouse[0] < left_margin + (MATRIXSQUARESIZE + 5) * codeLength - 5) and (70 * matrixHeight < mouse[1] < 70 * matrixHeight + MATRIXSQUARESIZE):
							x_row = left_margin
							for i in range(0, codeLength):
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
					
					# The game is over
					else:
						restart = True
						starting = True
				
				# Resets the color of the backspace color when the click is released
				if event.type == pygame.MOUSEBUTTONUP and backspacePress:
					backspacePress = False
				
				# The size of the window was changed
				if event.type == pygame.VIDEORESIZE:
					window_X, window_Y, screen = resize(event.w, event.h, screen)
			
			if showText == True:
				screen.blit(title, (10, 10))
				# On-Screen Keyboard
				drawKeyboard(actualNumbers, keyboard_X, keyboard_Y, submit_X, backspacePress)
				if showScoreTitle == True:
					screen.blit(scoreGood, (left_margin + ((MATRIXSQUARESIZE + 5) * codeLength + getStringWidth("Good", scoreTitle_font) / 2), 40))
					screen.blit(scoreExcelent, (left_margin + ((MATRIXSQUARESIZE + 5) * codeLength + getStringWidth("Good", scoreTitle_font) + 10 + getStringWidth("Excelent", scoreTitle_font) / 2), 40))

			### Number Printing ###
			y = 80
			# Numbers the user has previously entered
			for list in permanentNumbers:
				x = left_margin + 15
				for number in list:
					numberText = number_font.render(number, True, WHITE)
					screen.blit(numberText, (x, y))
					x += MATRIXSQUARESIZE + 5
				y += 70
			
			x = left_margin + 15
			# Numbers the user inputs
			for number in actualNumbers:
				numberText = number_font.render(number, True, WHITE)
				screen.blit(numberText, (x, y))
				x += MATRIXSQUARESIZE + 5
			
			# Scores
			y = 80
			for score in scores:
				x = left_margin + ((MATRIXSQUARESIZE + 5) * codeLength + 50)
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
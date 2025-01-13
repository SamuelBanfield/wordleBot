import random, pygame, sys
pygame.init()
from pygame.locals import *

colourDict = {
	-1: (255,255,255),
	0: (128,128,128),
	1: (255,255,0),
	2: (0,255,0)
}

file = "wordlists/5letterwords.txt" #choose text file to generate word from

class GameObject:
	def __init__(self, answer, mode = 0):
		self.mode = mode
		self.answer = answer
		self.guesses = ['' for _ in range(6)] #matrix for showing the current guesses, updates livetime with key presses
		self.colourings = [[-1,-1,-1,-1,-1] for x in range(6)] #colourings update row by row as guesses are made
		self.currentGuess = 0
	def guess(self, guess):
		self.guesses[self.currentGuess] = guess
		if self.mode == 0:
			self.colourings[self.currentGuess] = compareWords(guess, self.answer)
		self.currentGuess += 1

def generateWordList(file):
	wordList = []
	with open(file, 'r') as wordFile:
		word = wordFile.readline()
		while word != '':
			wordList.append(word[:-1])
			word = wordFile.readline()

	return wordList

def compareWords(guess, answer):
	#0 is grey, 1 is yellow, 2 is green
	colouring = [0,0,0,0,0]
	if len(guess) != 5:
		print('Guess: ', guess, 'Answer: ', answer)
	for x in range(5):
		if guess[x] == answer[x]:
			colouring[x] = 2
			guess = guess[:x] + '1' + guess[x+1:]
			answer = answer[:x] + '2' + answer[x+1:]
	for x in range(5):
		for y in range(5):
			if guess[x] == answer[y]:
				colouring[x] = 1
				guess = guess[:x] + '2' + guess[x+1:]
				answer = answer[:y] + '2' + answer[y+1:]
	return colouring

def drawScreen(SCREEN, game, font, typedWord = ''):
	SCREEN.fill((255,255,255))
	
	#first iterating through drawing letters in completed guesses
	for guessPosition in range(len(game.guesses)):
		for letterIndex in range(len(game.guesses[guessPosition])):
			guess = game.guesses[guessPosition]
			letterImage = font.render(guess[letterIndex].upper(), False, (0,0,0))
			letterRect = letterImage.get_rect()
			letterRect.center = (50+letterIndex*100, 50 + guessPosition*100)
			pygame.draw.rect(SCREEN, colourDict[game.colourings[guessPosition][letterIndex]], pygame.Rect(letterIndex*100, guessPosition*100, 100, 100))
			SCREEN.blit(letterImage, letterRect)

	#second iterating through the word thats currently being typed
	for letterIndex in range(len(typedWord)):
		letterImage = font.render(typedWord[letterIndex].upper(), False, (0,0,0))
		letterRect = letterImage.get_rect()
		letterRect.center = (50+letterIndex*100, 50 + game.currentGuess*100)
		pygame.draw.rect(SCREEN, colourDict[game.colourings[guessPosition][letterIndex]], pygame.Rect(letterIndex*100, game.currentGuess*100, 100, 100))
		SCREEN.blit(letterImage, letterRect)

	#finally iterating through drawing black boxes:
	for x in range(6):
		for y in range(5):
			#pygame.draw.rect(SCREEN, colourDict[game.colourings[x][y]], pygame.Rect(y*100, x*100, 100, 100))
			pygame.draw.rect(SCREEN, (0,0,0), pygame.Rect(y*100, x*100, 100, 100), 2)

	pygame.display.flip()

def handleTyping(key, typedWord, game):
	if 97 <= key <= 122:
		#Dealing with letter key presses
		if len(typedWord) < 5:
			typedWord += chr(key)
	elif key == 8:
		#Dealing with the backspace key
		if len(typedWord) > 0:
			typedWord = typedWord[:-1]
	elif key == 13:
		#Dealing with enter
		if len(typedWord) == 5:
			game.guess(typedWord)
			print('guessing...')
			typedWord = ''
	elif key == K_SPACE:
		print(game.answer) #print('stop trying to cheat')

	return typedWord

def wordleGame(wordToGuess):
	Game = GameObject(wordToGuess)
	font = pygame.font.Font(pygame.font.get_default_font(), 100)
	width = 500
	height = 600
	SCREEN = pygame.display.set_mode((width, height))
	SCREEN.fill((255,255,255))
	running = True
	clock = pygame.time.Clock()
	FPS = 20
	playing = True
	typedWord = ''
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYUP:
				if playing and 97 <= event.key <= 122 or event.key in [8, 13, K_SPACE]:
						typedWord = handleTyping(event.key, typedWord, Game)
				elif event.key == K_1:

					wordToGuess = random.choice(generateWordList("wordlists/5letterwords.txt"))
					Game = GameObject(wordToGuess)
		drawScreen(SCREEN, Game, font, typedWord)
		clock.tick(FPS)

def main():
	words = generateWordList(file)
	print('Press 1 to reset the game, and enter to guess a word')
	wordleGame(random.choice(words))

if __name__ == '__main__':
	main()
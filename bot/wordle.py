import random, pygame, sys
pygame.init()
from pygame.locals import *

from .game import GameObject, generateWordList

colourDict = {
	-1: (255,255,255),
	0: (128,128,128),
	1: (255,255,0),
	2: (0,255,0)
}

file = "wordlists/5letterwords.txt" #choose text file to generate word from

class PygameWordleUI:

	def __init__(self, word, fps = 20):
		self.game = GameObject(word)
		self.font = pygame.font.Font(pygame.font.get_default_font(), 100)
		self.dimensions = (5 * 100, 6 * 100)
		self.screen = pygame.display.set_mode(self.dimensions)
		self.screen.fill((255,255,255))
		self.clock = pygame.time.Clock()
		self.fps = fps
		self.typedWord = ''

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == KEYUP:
					key = event.key
					if 97 <= key <= 122: # Letter keys
						if len(self.typedWord) < 5:
							self.typedWord += chr(key)
					elif key == 8: # Backspace key
						if len(self.typedWord) > 0:
							self.typedWord = self.typedWord[:-1]
					elif key == 13: # Enter key
						if len(self.typedWord) == 5:
							print(self.typedWord)
							self.game.guess(self.typedWord)
							self.typedWord = ''
					elif event.key == K_1: # Reset
						wordToGuess = random.choice(generateWordList("wordlists/5letterwords.txt"))
						self.game = GameObject(wordToGuess)
				self.draw_screen()
				self.clock.tick(self.fps)
			
	def draw_screen(self):
		self.screen.fill((255,255,255))
	
		#first iterating through drawing letters in completed guesses
		for guessPosition in range(len(self.game.guesses)):
			for letterIndex in range(len(self.game.guesses[guessPosition])):
				guess = self.game.guesses[guessPosition]
				letterImage = self.font.render(guess[letterIndex].upper(), False, (0,0,0))
				letterRect = letterImage.get_rect()
				letterRect.center = (50+letterIndex*100, 50 + guessPosition*100)
				pygame.draw.rect(self.screen, colourDict[self.game.colourings[guessPosition][letterIndex]], pygame.Rect(letterIndex * 100, guessPosition * 100, 100, 100))
				self.screen.blit(letterImage, letterRect)

		#second iterating through the word thats currently being typed
		for letterIndex in range(len(self.typedWord)):
			letterImage = self.font.render(self.typedWord[letterIndex].upper(), False, (0,0,0))
			letterRect = letterImage.get_rect()
			letterRect.center = (50+letterIndex*100, 50 + self.game.currentGuess * 100)
			pygame.draw.rect(
				self.screen,
				colourDict[self.game.colourings[guessPosition][letterIndex]],
				pygame.Rect(letterIndex*100, self.game.currentGuess * 100, 100, 100)
			)
			self.screen.blit(letterImage, letterRect)

		#finally iterating through drawing black boxes:
		for x in range(6):
			for y in range(5):
				pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(y*100, x*100, 100, 100), 2)

		pygame.display.flip()

def main():
	words = generateWordList(file)
	ui = PygameWordleUI(random.choice(words))
	ui.run()

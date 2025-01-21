import random, pygame, sys
from pygame.locals import *

from .game import GameObject, generate_word_list

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

COLOUR_DICT = {
	-1: WHITE,
	0: GREY,
	1: YELLOW,
	2: GREEN,
}

WORDLIST_FILE = "wordlists/5letterwords.txt" # Choose text file to generate word from

class PygameWordleUI:

	def __init__(self, word, fps = 20, square_size = 100):
		pygame.init()
		self.game = GameObject(word)
		self.square_size = square_size
		self.font = pygame.font.Font(pygame.font.get_default_font(), square_size)
		self.dimensions = (5 * self.square_size, 6 * self.square_size)
		self.screen = pygame.display.set_mode(self.dimensions)
		self.screen.fill(WHITE)
		self.clock = pygame.time.Clock()
		self.fps = fps
		self.typed_word = ''

	def run(self):
		while True:
			self.handle_events()
			self.draw_screen()
			self.clock.tick(self.fps)

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYUP:
				self.handle_key_up(event.key)

	def handle_key_up(self, key):
		if K_a <= key <= K_z: # Letter keys
			if len(self.typed_word) < 5:
				self.typed_word += chr(key)
		elif key == K_BACKSPACE: # Backspace key
			if len(self.typed_word) > 0:
				self.typed_word = self.typed_word[:-1]
		elif key == K_RETURN: # Enter key
			if len(self.typed_word) == 5:
				print(self.typed_word)
				self.game.guess(self.typed_word)
				self.typed_word = ''
		elif key == K_1: # Reset
			word_to_guess = random.choice(generate_word_list(WORDLIST_FILE))
			self.game = GameObject(word_to_guess)
			
	def draw_screen(self):
		self.screen.fill(WHITE)
		self.draw_guesses()
		self.draw_grid()
		pygame.display.flip()

	def draw_guesses(self):
		for guess_position, guess in enumerate([word for word in self.game.guesses if word] + [self.typed_word]):
			for letter_index, letter in enumerate(guess):
				letter_image = self.font.render(letter.upper(), True, BLACK)
				letter_rect = letter_image.get_rect()
				letter_rect.center = (
					self.square_size // 2 + letter_index * self.square_size,
					self.square_size // 2 + guess_position * self.square_size
				)
				pygame.draw.rect(
					self.screen,
					COLOUR_DICT[self.game.colourings[guess_position][letter_index] if guess_position < len(self.game.colourings) else -1],
					pygame.Rect(letter_index * self.square_size, guess_position * self.square_size, self.square_size, self.square_size)
				)
				self.screen.blit(letter_image, letter_rect)
	
	def draw_grid(self):
		for x in range(6):
			for y in range(5):
				pygame.draw.rect(
					self.screen,
					BLACK,
					pygame.Rect(y * self.square_size, x * self.square_size, self.square_size, self.square_size),
					2
				)

def main():
	words = generate_word_list(WORDLIST_FILE)
	ui = PygameWordleUI(random.choice(words))
	ui.run()

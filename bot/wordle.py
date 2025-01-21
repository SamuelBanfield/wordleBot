import random
from typing import override
from pygame.locals import *

from bot.pygame_ui import PygameWordleUI
from bot.game import GameObject, generate_word_list

WORDLIST_FILE = "wordlists/5letterwords.txt" # Choose text file to generate word from

class WordleGameUI(PygameWordleUI):

	def __init__(self, word):
		super().__init__(word)

	@override
	def handle_event(self, event):
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
			

def main():
	words = generate_word_list(WORDLIST_FILE)
	ui = WordleGameUI(random.choice(words))
	ui.run()

'''
Words that arent words: lieth, dieth, grook, shmoo, chiff, goeth
'''
import math
from pygame.locals import *

from bot.game import GameObject, compare_words, generate_word_list
from itertools import product


file = 'wordlists/bigWordFile.txt'
small_file = 'wordlists/5letterwords.txt'
official_file = 'wordlists/officialAnswerList.txt'

def f(x):
	# These constants are determined by making alog(x)+b pass through (0,1), (us,mu), (5.4, 2.7)
	mu = 3.35
	us = 10.84
	x0 = -4.5
	return 1 + (mu - 1) * math.log(1 - (x / x0), 10) / math.log(1 - (us / x0), 10)

def get_frequencies(answer, word_list):
	#generates the distribution of possible colourings for words in a word_list if the solution is answer
	patterns = []
	frequencies = []
	for word in word_list:
		pattern = compare_words(answer, word)
		if pattern in patterns:
			frequencies[patterns.index(pattern)] += 1
		else:
			patterns.append(pattern)
			frequencies.append(1)
	return frequencies

def get_entropy(frequencies, total):
	entropy = 0
	for f in frequencies:
		p = f/total
		entropy += (p)*(-math.log(p,2))
	return entropy

def get_all_entropies(answer_list, word_list):
	word_with_entropy = []
	for word in word_list:
		frequencies = get_frequencies(word, answer_list)
		word_with_entropy.append([word, get_entropy(frequencies, len(answer_list))])

	return word_with_entropy

def play_wordle_bot(answer_list, word_list, word, c_dict):
	"""
	Simulates a bot playing the Wordle game and returns the number of guesses taken to find the correct answer.
	Parameters:
	answer_list (list of str): The list of possible solutions.
	word_list (list of str): The list of allowed guesses.
	word (str): The target word to be guessed by the bot.
	c_dict (dict): A dictionary mapping colourings to the next guess word.
	Returns:
	int: The number of guesses taken to find the correct answer. Returns 100 if the bot fails to find the answer within 6 guesses.
	Notes: The bot starts with the word 'tares' as it maximizes expected entropy with no information.
	"""
	# Answer list is the list of possible solutions, test_list is the list of allowed guesses
	word_with_max_entropy = 'tares' # Always using this word as it maximises expected entropy with no information
	game = GameObject(word)
	next_guess = word_with_max_entropy
	score = 0
	while score < 6:
		game.guess(next_guess)
		score += 1
		current_colouring = game.colourings[score-1]

		# Checks if answer found
		if current_colouring == [2, 2, 2, 2, 2]:
			return score

		# Refines the word_list
		answer_list = [word for word in answer_list if current_colouring == compare_words(next_guess, word)]

		# Should never run, catches incorrect word errors
		if len(answer_list) == 0:
			raise ValueError('Word not in word list!')

		# Refreshes the entropies and selects the most entropic word as next guess
		if len(answer_list) < 3:
			next_guess = answer_list[0]
		elif score == 1:
				next_guess = c_dict[tuple(current_colouring)]
		else:
			e = get_all_entropies(answer_list, word_list)
			e.sort(reverse = False, key = lambda pair: pair[1])
			next_guess = e[-1][0]

	return 100 # Returns 100 in the case of a loss

def create_initial_colourings_file(word_list, test_words, sol):
	initial_colourings_dict = {}
	for colouring in product(range(3), repeat = 5):
		temp_ans = [word for word in test_words if colouring == tuple(compare_words(sol, word))]
		if n := len(temp_ans):
			scores = get_all_entropies(temp_ans, word_list)
			p = 1 / n
			for pair in scores:
				if pair[0] in temp_ans:
					pair[1] = 1 * p + (1 - p) * (1 + f(math.log(n, 2) - pair[1]))
				else:
					pair[1] = 1+f(math.log(n, 2)-pair[1])
			scores.sort(reverse = True, key = lambda pair: pair[1])
			initial_colourings_dict[colouring] = scores[-1][0]
			print(scores[-1][0])
		else:
			print('')

def load_colouring_dict(file):
	initial_colourings_dict = {}
	with open(file, 'r') as f:
		f.readline()
		for v, w, x, y, z in product(range(3), repeat = 5):
			initial_colourings_dict[(v,w,x,y,z)] = f.readline()[:-1]
			f.readline()
	return initial_colourings_dict

def main():
	word_list = generate_word_list(file)
	test_words = generate_word_list(small_file)
	c_dict = load_colouring_dict('colourings/initialColourings2')
	for word in word_list:
		print((word, play_wordle_bot(test_words, word_list, word, c_dict)))

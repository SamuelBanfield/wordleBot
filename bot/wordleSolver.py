'''
Words that arent words: lieth, dieth, grook, shmoo, chiff, goeth
'''
import wordle, math, pygame, sys, random, os
from pygame.locals import *


current_loc = os.path.dirname(__file__)

file = current_loc + '/wordlists/bigWordFile.txt'
small_file = current_loc + '/wordlists/5letterwords.txt'
official_file = current_loc + '/wordlists/officialAnswerList.txt'

def f(x):
	#these constants are determined by making alog(x)+b pass through (0,1), (us,mu), (5.4, 2.7)
	'''
	mu = 3.35
	us = 10.84
	x0 = -4.5

	other:
	mu = 2.4
	us = 5.2
	x0 = -0.6
	'''
	#now new number based on V2 of the bot: x0 = -0.6
	mu = 3.35
	us = 10.84
	x0 = -4.5
	return 1 + (mu - 1) * math.log(1 - (x / x0), 10) / math.log(1 - (us / x0), 10)

def get_frequencies(answer, word_list):
	#generates the distribution of possible colourings for words in a word_list if the solution is answer
	patterns = []
	frequencies = []
	for word in word_list:
		pattern = wordle.compareWords(answer, word)
		if pattern in patterns:
			frequencies[patterns.index(pattern)] += 1
		else:
			patterns.append(pattern)
			frequencies.append(1)
	return frequencies

def get_frequency_dict(answer, word_list):
	frequencies = {}
	for word in word_list:
		pattern = tuple(wordle.compareWords(word, answer))
		if pattern in frequencies:
			frequencies[pattern] += [word]
		else:
			frequencies[pattern] = [word]
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

def play_wordle_bot_v1(word_list, word):
	word_with_max_entropy = 'tares' #always using this word as it maximises expected entropy with no information
	game = wordle.GameObject(word)
	next_guess = word_with_max_entropy
	score = 0
	while score < 6:
		print(next_guess)
		game.guess(next_guess)
		score += 1
		current_colouring = game.colourings[score-1]

		#checks if answer found
		if current_colouring == [2,2,2,2,2]:
			return score

		#should never run, catches incorrect word errors
		if len(word_list) == 0:
			print('Word not in word list!')
			return

		#refines the word_list
		word_list = [word for word in word_list if current_colouring == wordle.compareWords(next_guess, word)]

		#refreshes the entropies and selects the most entropic word as next guess
		e = get_all_entropies(word_list, word_list)
		e.sort(reverse = True, key = lambda pair: pair[1])
		next_guess = e[0][0]

	return 100 #returns 100 in the case of a loss

def thin_list(l, colouring, guess):
	return [word for word in l if wordle.compareWords(guess, word) == colouring]

def play_wordle_bot_v2(answer_list, word_list, word, c_dict):
	#answer list is the list of possible solutions, test_list is the list of allowed guesses
	word_with_max_entropy = 'tares' #always using this word as it maximises expected entropy with no information
	game = wordle.GameObject(word)
	next_guess = word_with_max_entropy
	score = 0
	while score < 6:
		game.guess(next_guess)
		score += 1
		current_colouring = game.colourings[score-1]

		#checks if answer found
		if current_colouring == [2,2,2,2,2]:
			return score


		answer_list = thin_list(answer_list, current_colouring, next_guess)

		#should never run, catches incorrect word errors
		if len(answer_list) == 0:
			print('Word not in word list!')
			return

		#refreshes the entropies and selects the most entropic word as next guess
		
		elif score == 1:
			next_guess = c_dict[tuple(current_colouring)]
		else:
			scores = get_all_entropies(answer_list, word_list)
			n = len(answer_list)
			p = 1/n
			for pair in scores:
				if pair[0] in answer_list:
					pair[1] = (score+1)*(p) + (1-p)*(score+1+f(math.log(n, 2)-pair[1]))
				else:
					pair[1] = score+1+f(math.log(n, 2)-pair[1])
			scores.sort(reverse = True, key = lambda pair: pair[1])
			next_guess = scores[-1][0]

	return 100 #returns 100 in the case of a loss

def play_wordle_bot_v3(answer_list, word_list, word, c_dict):
	#answer list is the list of possible solutions, test_list is the list of allowed guesses
	word_with_max_entropy = 'tares' #always using this word as it maximises expected entropy with no information
	game = wordle.GameObject(word)
	next_guess = word_with_max_entropy
	score = 0
	while score < 6:
		game.guess(next_guess)
		score += 1
		current_colouring = game.colourings[score-1]

		#checks if answer found
		if current_colouring == [2,2,2,2,2]:
			return score

		#refines the word_list
		answer_list = [word for word in answer_list if current_colouring == wordle.compareWords(next_guess, word)]

		#should never run, catches incorrect word errors
		if len(answer_list) == 0:
			print('Word not in word list!')
			return

		#refreshes the entropies and selects the most entropic word as next guess
		if len(answer_list) < 3:
			next_guess = answer_list[0]
		elif score == 1:
				next_guess = c_dict[tuple(current_colouring)]
		else:
			e = get_all_entropies(answer_list, word_list)
			e.sort(reverse = False, key = lambda pair: pair[1])
			#print(e[:5],answer_list)
			next_guess = e[-1][0]
			#print(next_guess)

	return 100 #returns 100 in the case of a loss

def wordle_bot_with_unknown_answer1(word_list):
	word_list
	word_with_max_entropy = 'tares'
	game = wordle.GameObject('', 1)
	game.guess('tares')
	font = pygame.font.Font(pygame.font.get_default_font(), 100)
	width = 500
	height = 600
	screen = pygame.display.set_mode((width, height))
	screen.fill((255,255,255))
	running = True
	clock = pygame.time.Clock()
	fps = 20
	playing = True
	while playing:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYUP:
				if event.key == K_SPACE:
					print(game.colourings, game.guesses)
					if len(game.colourings[game.currentGuess-1]) == 5:
						colouring_complete = True
						for colouring in game.colourings[game.currentGuess-1]:
							if colouring == -1:
								colouring_complete = False
						if colouring_complete:
							word_list = [word for word in word_list if game.colourings[game.currentGuess-1] == wordle.compareWords(game.guesses[game.currentGuess-1], word)]
							word_with_entropy = get_all_entropies(word_list, word_list)
							word_with_entropy.sort(reverse = True, key = lambda pair: pair[1])
							if word_with_entropy == []:
								print('no words left in list')
							else:
								next_word = word_with_entropy[0][0]
								print(len(word_list))
								game.guess(next_word)
			if event.type == MOUSEBUTTONUP:
				mouse = pygame.mouse.get_pos()
				mouse_tile = [mouse[0]//100, mouse[1]//100]
				if mouse_tile[1] == game.currentGuess-1:
					game.colourings[mouse_tile[1]][mouse_tile[0]] += 1
					game.colourings[mouse_tile[1]][mouse_tile[0]] = game.colourings[mouse_tile[1]][mouse_tile[0]] % 3
		wordle.drawScreen(screen, game, font)
		clock.tick(fps)

def wordle_bot_with_unknown_answer2(word_list, test_list, c_dict):
	word_with_max_entropy = 'tares'
	game = wordle.GameObject('', 1)
	game.guess(word_with_max_entropy)
	font = pygame.font.Font(pygame.font.get_default_font(), 100)
	width = 500
	height = 600
	screen = pygame.display.set_mode((width, height))
	screen.fill((255,255,255))
	clock = pygame.time.Clock()
	fps = 20
	playing = True
	while playing:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYUP:
				if event.key == K_SPACE:
					print(game.colourings, game.guesses)
					if len(game.colourings[game.currentGuess-1]) == 5:
						colouring_complete = True
						for colouring in game.colourings[game.currentGuess-1]:
							if colouring == -1:
								colouring_complete = False
						if colouring_complete:
							test_list = [word for word in test_list if game.colourings[game.currentGuess-1] == wordle.compareWords(game.guesses[game.currentGuess-1], word)]
							if game.currentGuess == 1:
								next_guess = c_dict[tuple(game.colourings[game.currentGuess-1])]
							else:
								scores = get_all_entropies(test_list, word_list)
								n = len(test_list)
								if n == 0:
									'No possibilities'
								p = 1/n
								score = game.currentGuess-1
								for pair in scores:
									if pair[0] in test_list:
										pair[1] = (score+1)*(p) + (1-p)*(score+1+f(math.log(n, 2)-pair[1]))
									else:
										pair[1] = score+1+f(math.log(n, 2)-pair[1])
								scores.sort(reverse = True, key = lambda pair: pair[1])
								next_guess = scores[-1][0]

							print(len(test_list))
							game.guess(next_guess)
			if event.type == MOUSEBUTTONUP:
				mouse = pygame.mouse.get_pos()
				mouse_tile = [mouse[0]//100, mouse[1]//100]
				if mouse_tile[1] == game.currentGuess-1:
					game.colourings[mouse_tile[1]][mouse_tile[0]] += 1
					game.colourings[mouse_tile[1]][mouse_tile[0]] = game.colourings[mouse_tile[1]][mouse_tile[0]] % 3
		wordle.drawScreen(screen, game, font)
		clock.tick(fps)

def create_initial_colourings_file(word_list, test_words, sol):
	initial_colourings_dict = {}
	for v in range(3):
		for w in range(3):
			for x in range(3):
				for y in range(3):
					for z in range(3):
						colouring = (v,w,x,y,z)
						print(colouring)
						temp_ans = [word for word in test_words if colouring == tuple(wordle.compareWords(sol, word))]
						if len(temp_ans) != 0:
							scores = get_all_entropies(temp_ans, word_list)
							n = len(temp_ans)
							p = 1 / n
							for pair in scores:
								if pair[0] in temp_ans:
									pair[1] = (1)*(p) + (1-p)*(1+f(math.log(n, 2)-pair[1]))
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
		l = f.readline()
		for v in range(3):
			for w in range(3):
				for x in range(3):
					for y in range(3):
						for z in range(3):
							initial_colourings_dict[(v,w,x,y,z)] = f.readline()[:-1]
							f.readline()
	return initial_colourings_dict

def test_bot2(test_words, word_list, c_dict):
	scores = {1:0,2:0,3:0,4:0,5:0,6:0,100:0,}
	for word in range(len(test_words)):
		if word % 50 == 0:
			print(word/len(test_words))
		s = play_wordle_bot_v2(test_words, word_list, test_words[word], c_dict)
		scores[s] += 1
		print(scores)
	print(scores)

def main():
	word_list = wordle.generateWordList(file)
	#test_list = copy.copy(word_list)
	test_words = wordle.generateWordList(small_file)
	c_dict = load_colouring_dict(current_loc+'/colourings/initialColourings2')
	wordle_bot_with_unknown_answer2(test_words, word_list, c_dict)


if __name__ == '__main__':
	main()
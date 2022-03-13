'''
Words that arent words: lieth, dieth, grook, shmoo, chiff, goeth
'''
import wordle, math, pygame, sys, copy, random, os
import matplotlib.pyplot as plt
import numpy as np
from pygame.locals import *

currentLoc = os.path.dirname(__file__)
print(currentLoc)

file = currentLoc+'/wordlists/bigWordFile.txt'
smallFile = currentLoc+'/wordlists/5letterwords.txt'
officialFile = currentLoc+'/wordlists/officialAnswerList.txt'

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
	return 1+ (mu-1)*math.log(1-(x/x0), 10)/math.log(1-(us/x0), 10)

def getFrequencies(answer, wordList):
	#generates the distribution of possible colourings for words in a wordList if the solution is answer
	patterns = []
	frequencies = []
	for word in wordList:
		pattern = wordle.compareWords(answer, word)
		if pattern in patterns:
			frequencies[patterns.index(pattern)] += 1
		else:
			patterns.append(pattern)
			frequencies.append(1)
	return frequencies

	'''
	#this bit pairs frequencies and patterns, then orders the patterns by their frequencies
	patternsWithFrequencies = [[patterns[x], frequencies[x]] for x in range(len(patterns))]
	patternsWithFrequencies.sort(reverse = True, key = lambda pair: pair[1])
	'''

def getFrequencyDict(answer, wordList):
	frequencies = {}
	for word in wordList:
		pattern = tuple(wordle.compareWords(word, answer))
		if pattern in frequencies:
			frequencies[pattern] += [word]
		else:
			frequencies[pattern] = [word]
	return frequencies

def getEntropy(frequencies, total):
	entropy = 0
	for f in frequencies:
		p = f/total
		entropy += (p)*(-math.log(p,2))
	return entropy

def getAllEntropies(answerList, wordList):
	wordWithEntropy = []
	for word in wordList:
		frequencies = getFrequencies(word, answerList)
		wordWithEntropy.append([word, getEntropy(frequencies, len(answerList))])
	#wordWithEntropy.sort(reverse = True, key = lambda pair: pair[1])
	return wordWithEntropy

def playWordleBotV1(wordList, word):
	wordWithMaxEntropy = 'tares' #always using this word as it maximises expected entropy with no information
	Game = wordle.gameObject(word)
	nextGuess = wordWithMaxEntropy
	score = 0
	while score < 6:
		print(nextGuess)
		Game.guess(nextGuess)
		score += 1
		currentColouring = Game.colourings[score-1]

		#checks if answer found
		if currentColouring == [2,2,2,2,2]:
			return score

		#should never run, catches incorrect word errors
		if len(wordList) == 0:
			print('Word not in word list!')
			return

		#refines the wordList
		wordList = [word for word in wordList if currentColouring == wordle.compareWords(nextGuess, word)]

		#refreshes the entropies and selects the most entropic word as next guess
		e = getAllEntropies(wordList, wordList)
		e.sort(reverse = True, key = lambda pair: pair[1])
		nextGuess = e[0][0]

	return 100 #returns 100 in the case of a loss

def thinList(l, colouring, guess):
	return [word for word in l if wordle.compareWords(guess, word) == colouring]

def playWordleBotV2(answerList, wordList, word, cDict):
	#answer list is the list of possible solutions, testList is the list of allowed guesses
	wordWithMaxEntropy = 'tares' #always using this word as it maximises expected entropy with no information
	Game = wordle.gameObject(word)
	nextGuess = wordWithMaxEntropy
	score = 0
	while score < 6:
		Game.guess(nextGuess)
		score += 1
		currentColouring = Game.colourings[score-1]

		#checks if answer found
		if currentColouring == [2,2,2,2,2]:
			return score


		answerList = thinList(answerList, currentColouring, nextGuess)

		#should never run, catches incorrect word errors
		if len(answerList) == 0:
			print('Word not in word list!')
			return

		#refreshes the entropies and selects the most entropic word as next guess
		
		elif score == 1:
			nextGuess = cDict[tuple(currentColouring)]
		else:
			scores = getAllEntropies(answerList, wordList)
			n = len(answerList)
			p = 1/n
			for pair in scores:
				if pair[0] in answerList:
					pair[1] = (score+1)*(p) + (1-p)*(score+1+f(math.log(n, 2)-pair[1]))
				else:
					pair[1] = score+1+f(math.log(n, 2)-pair[1])
			scores.sort(reverse = True, key = lambda pair: pair[1])
			nextGuess = scores[-1][0]

	return 100 #returns 100 in the case of a loss

def playWordleBotV3(answerList, wordList, word, cDict):
	#answer list is the list of possible solutions, testList is the list of allowed guesses
	wordWithMaxEntropy = 'tares' #always using this word as it maximises expected entropy with no information
	Game = wordle.gameObject(word)
	nextGuess = wordWithMaxEntropy
	score = 0
	while score < 6:
		Game.guess(nextGuess)
		score += 1
		currentColouring = Game.colourings[score-1]

		#checks if answer found
		if currentColouring == [2,2,2,2,2]:
			return score

		#refines the wordList
		answerList = [word for word in answerList if currentColouring == wordle.compareWords(nextGuess, word)]

		#should never run, catches incorrect word errors
		if len(answerList) == 0:
			print('Word not in word list!')
			return

		#refreshes the entropies and selects the most entropic word as next guess
		if len(answerList) < 3:
			nextGuess = answerList[0]
		elif score == 1:
				nextGuess = cDict[tuple(currentColouring)]
		else:
			e = getAllEntropies(answerList, wordList)
			e.sort(reverse = False, key = lambda pair: pair[1])
			#print(e[:5],answerList)
			nextGuess = e[-1][0]
			#print(nextGuess)

	return 100 #returns 100 in the case of a loss

def wordleBotWithUnknownAnswer1(wordList):
	wordList
	wordWithMaxEntropy = 'tares'
	game = wordle.gameObject('', 1)
	game.guess('tares')
	font = pygame.font.Font(pygame.font.get_default_font(), 100)
	width = 500
	height = 600
	SCREEN = pygame.display.set_mode((width, height))
	SCREEN.fill((255,255,255))
	running = True
	clock = pygame.time.Clock()
	FPS = 20
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
						colouringComplete = True
						for colouring in game.colourings[game.currentGuess-1]:
							if colouring == -1:
								colouringComplete = False
						if colouringComplete:
							wordList = [word for word in wordList if game.colourings[game.currentGuess-1] == wordle.compareWords(game.guesses[game.currentGuess-1], word)]
							wordWithEntropy = getAllEntropies(wordList, wordList)
							wordWithEntropy.sort(reverse = True, key = lambda pair: pair[1])
							if wordWithEntropy == []:
								print('no words left in list')
							else:
								nextWord = wordWithEntropy[0][0]
								print(len(wordList))
								game.guess(nextWord)
			if event.type == MOUSEBUTTONUP:
				mouse = pygame.mouse.get_pos()
				mouseTile = [mouse[0]//100, mouse[1]//100]
				if mouseTile[1] == game.currentGuess-1:
					game.colourings[mouseTile[1]][mouseTile[0]] += 1
					game.colourings[mouseTile[1]][mouseTile[0]] = game.colourings[mouseTile[1]][mouseTile[0]] % 3
		wordle.drawScreen(SCREEN, game, font)
		clock.tick(FPS)

def wordleBotWithUnknownAnswer2(wordList, testList, cDict):
	wordWithMaxEntropy = 'tares'
	game = wordle.gameObject('', 1)
	game.guess(wordWithMaxEntropy)
	font = pygame.font.Font(pygame.font.get_default_font(), 100)
	width = 500
	height = 600
	SCREEN = pygame.display.set_mode((width, height))
	SCREEN.fill((255,255,255))
	running = True
	clock = pygame.time.Clock()
	FPS = 20
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
						colouringComplete = True
						for colouring in game.colourings[game.currentGuess-1]:
							if colouring == -1:
								colouringComplete = False
						if colouringComplete:
							testList = [word for word in testList if game.colourings[game.currentGuess-1] == wordle.compareWords(game.guesses[game.currentGuess-1], word)]
							if game.currentGuess == 1:
								nextGuess = cDict[tuple(game.colourings[game.currentGuess-1])]
							else:
								scores = getAllEntropies(testList, wordList)
								n = len(testList)
								if n == 0:
									'No possibilities'
								p = 1/n
								score = game.currentGuess-1
								for pair in scores:
									if pair[0] in testList:
										pair[1] = (score+1)*(p) + (1-p)*(score+1+f(math.log(n, 2)-pair[1]))
									else:
										pair[1] = score+1+f(math.log(n, 2)-pair[1])
								scores.sort(reverse = True, key = lambda pair: pair[1])
								nextGuess = scores[-1][0]

							print(len(testList))
							game.guess(nextGuess)
			if event.type == MOUSEBUTTONUP:
				mouse = pygame.mouse.get_pos()
				mouseTile = [mouse[0]//100, mouse[1]//100]
				if mouseTile[1] == game.currentGuess-1:
					game.colourings[mouseTile[1]][mouseTile[0]] += 1
					game.colourings[mouseTile[1]][mouseTile[0]] = game.colourings[mouseTile[1]][mouseTile[0]] % 3
		wordle.drawScreen(SCREEN, game, font)
		clock.tick(FPS)

def getScoreDistribution(testList, wordList, noWords = 1842):
	wordsWithScore = []
	if noWords == 1842:
		for word in range(len(testList)):
			if word % 50 == 0:
				print(word/1842*100)
			wordsWithScore.append([testList[word], playWordleBot(wordList, testList[word])])
	else:
		for _ in range(noWords):
			word = random.choice(testList)
			wordsWithScore.append([word, playWordleBot(wordList, word)])
	return wordsWithScore

def findF(testWords, wordList, cDict):
	uncertaintyByTurnsRemaining = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}
	noBins = 20
	turnsRemainingHistogram = {}
	for x in range(noBins+1):
		turnsRemainingHistogram[x] = []
	for x in range(1000):
		print(x)
		response = playWordleBotV2(testWords, wordList, random.choice(testWords), cDict)[1][::-1]
		if response[0] != 100:
			uncertaintyPerTurn = response
			l = len(uncertaintyPerTurn)
			for x in range(l):
				#uncertaintyByTurnsRemaining[x+1].append(uncertaintyPerTurn[x])
				turnsRemainingHistogram[int(noBins*(uncertaintyPerTurn[x]/10.847057346))].append(x+1)
	freq = [0 for x in turnsRemainingHistogram]
	for x in turnsRemainingHistogram:
		if len(turnsRemainingHistogram[x]) > 0:
			freq[x] = sum(turnsRemainingHistogram[x])/len(turnsRemainingHistogram[x])
	x = np.array([i for i in range(len(freq))])
	y = np.array(freq)
	plt.style.use('ggplot')
	print(x, y)


	x_pos = [i*10.84/noBins for i, _ in enumerate(x)]
	xTicks = [i*10.84/noBins for i, _ in enumerate(x) if i % 4 == 0]

	plt.bar(x_pos, y, color='green')
	plt.xlabel("Remaining Uncertainty")
	plt.ylabel("Expeced number of guesses")
	plt.title("Expected number of guesses by uncertainty")

	plt.xticks(xTicks)

	plt.show()

def createInitialColouringsFile(wordList, testWords, sol):
	initialColouringsDict = {}
	for v in range(3):
		for w in range(3):
			for x in range(3):
				for y in range(3):
					for z in range(3):
						colouring = (v,w,x,y,z)
						print(colouring)
						tempAns = [word for word in testWords if colouring == tuple(wordle.compareWords(sol, word))]
						if len(tempAns) != 0:
							scores = getAllEntropies(tempAns, wordList)
							n = len(tempAns)
							p = 1/n
							for pair in scores:
								if pair[0] in tempAns:
									pair[1] = (1)*(p) + (1-p)*(1+f(math.log(n, 2)-pair[1]))
								else:
									pair[1] = 1+f(math.log(n, 2)-pair[1])
							scores.sort(reverse = True, key = lambda pair: pair[1])
							initialColouringsDict[colouring] = scores[-1][0]
							print(scores[-1][0])
						else:
							print('')

def loadColouringDict(file):
	initialColouringsDict = {}
	lines = []
	with open(file, 'r') as f:
		l = f.readline()
		for v in range(3):
			for w in range(3):
				for x in range(3):
					for y in range(3):
						for z in range(3):

							initialColouringsDict[(v,w,x,y,z)] = f.readline()[:-1]
							f.readline()
	return initialColouringsDict

def testBot2(testWords, wordList, cDict):
	scores = {1:0,2:0,3:0,4:0,5:0,6:0,100:0,}
	for word in range(len(testWords)):
		if word % 50 == 0:
			print(word/len(testWords))
		s = playWordleBotV2(testWords, wordList, testWords[word], cDict)
		scores[s] += 1
		print(scores)
	print(scores)

def main():
	wordList = wordle.generateWordList(file)
	#testList = copy.copy(wordList)
	testWords = wordle.generateWordList(smallFile)
	cDict = loadColouringDict(currentLoc+'/colourings/initialColourings2')


if __name__ == '__main__':
	main()
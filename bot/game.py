def generate_word_list(file):
	word_list = []
	with open(file, 'r') as word_file:
		word = word_file.readline()
		while word != '':
			word_list.append(word[:-1])
			word = word_file.readline()

	return word_list

def compare_words(guess, answer):
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


class GameObject:
	def __init__(self, answer, mode = 0):
		self.mode = mode
		self.answer = answer
		self.guesses = ['' for _ in range(6)] #matrix for showing the current guesses, updates livetime with key presses
		self.colourings = [[-1,-1,-1,-1,-1] for x in range(6)] #colourings update row by row as guesses are made
		self.current_guess = 0
	def guess(self, guess):
		self.guesses[self.current_guess] = guess
		if self.mode == 0:
			self.colourings[self.current_guess] = compare_words(guess, self.answer)
		self.current_guess += 1

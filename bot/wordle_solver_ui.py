'''
Words that arent words: lieth, dieth, grook, shmoo, chiff, goeth
'''
import math, pygame, sys
from pygame.locals import *

from bot.game import GameObject, compare_words, generate_word_list
from bot.wordle_solver import get_all_entropies, f, file, small_file, load_colouring_dict
from bot.wordle import PygameWordleUI


class PygameWordleSolverUI(PygameWordleUI):
    
    def __init__(self, word_list, test_list, c_dict, intial_guess):
        super().__init__('cloth')
        self.game.guess(intial_guess)
        self.word_list = word_list
        self.test_list = test_list
        self.c_dict = c_dict
        
    def handle_event(self, event):
        if event.type == KEYUP and event.key == K_RETURN:
            colouring_complete = True
            for colouring in self.game.colourings[self.game.current_guess - 1]:
                if colouring == -1:
                    colouring_complete = False
            if colouring_complete:
                self.test_list = [
                    word for word in self.test_list 
                    if self.game.colourings[self.game.current_guess - 1] == compare_words(self.game.guesses[self.game.current_guess-1], word)
                ]
                if self.game.current_guess == 1:
                    next_guess = self.c_dict[tuple(self.game.colourings[self.game.current_guess-1])]
                else:
                    scores = get_all_entropies(self.test_list, self.word_list)
                    n = len(self.test_list)
                    if n == 0:
                        'No possibilities'
                    p = 1 / n
                    score = self.game.currentGuess-1
                    for pair in scores:
                        if pair[0] in self.test_list:
                            pair[1] = (score + 1)*(p) + (1 - p)*(score + 1 + f(math.log(n, 2) - pair[1]))
                        else:
                            pair[1] = score + 1 + f(math.log(n, 2) - pair[1])
                    scores.sort(reverse = True, key = lambda pair: pair[1])
                    next_guess = scores[-1][0]

                self.game.guess(next_guess)
        if event.type == MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            mouse_tile = [mouse[0] // self.square_size, mouse[1] // self.square_size]
            if mouse_tile[1] == self.game.current_guess - 1:
                self.game.colourings[mouse_tile[1]][mouse_tile[0]] = (self.game.colourings[mouse_tile[1]][mouse_tile[0]] + 1) % 3
        

def run_wordle_bot_with_unknown_answer(word_list, test_list, c_dict, initial_guess):
    ui = PygameWordleSolverUI(word_list, test_list, c_dict, initial_guess)
    ui.run()

def main():
    word_list = generate_word_list(file)
    test_words = generate_word_list(small_file)
    c_dict = load_colouring_dict('colourings/initialColourings2')
    run_wordle_bot_with_unknown_answer(test_words, word_list, c_dict, "tares")
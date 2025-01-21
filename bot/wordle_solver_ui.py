'''
Words that arent words: lieth, dieth, grook, shmoo, chiff, goeth
'''
import math, pygame, random
from typing import override
from pygame.locals import *

from bot.game import compare_words, generate_word_list
from bot.wordle_solver import get_all_entropies, expected_guesses, file, small_file, load_colouring_dict
from bot.wordle import PygameWordleUI


class PygameWordleSolverUI(PygameWordleUI):
    
    def __init__(self, word_list, test_list, c_dict, intial_guess):
        super().__init__()
        self.game.guess(intial_guess)
        self.word_list = word_list
        self.test_list = test_list
        self.c_dict = c_dict
    
    @override
    def handle_event(self, event):
        if event.type == KEYUP and event.key == K_RETURN:
            if not any([colour == -1 for colour in self.game.colourings[self.game.current_guess - 1]]):
                self.handle_guess()
        if event.type == MOUSEBUTTONUP:
            self.handle_cycle_colouring()

    def handle_guess(self):
        self.test_list = [
            word for word in self.test_list 
            if self.game.colourings[self.game.current_guess - 1] == compare_words(self.game.guesses[self.game.current_guess-1], word)
        ]
        if self.game.current_guess == 1:
            next_guess = self.c_dict[tuple(self.game.colourings[self.game.current_guess-1])]
        else:
            if not self.test_list:
                raise ValueError('No word from the answers list satisfies these clues')
            n = len(self.test_list)
            p = 1 / n
            predicted_score_for_word = lambda allowed_guess, entropy: (
                p * self.game.current_guess + (1 - p) * (self.game.current_guess + expected_guesses(math.log(n, 2) - entropy))
                if allowed_guess
                else self.game.current_guess + expected_guesses(math.log(n, 2) - entropy)
            )
            scores = [
                (word in self.test_list, predicted_score_for_word(word, entropy)) 
                for (word, entropy) in get_all_entropies(self.test_list, self.word_list)
            ]
            scores.sort(reverse = True, key = lambda pair: pair[1])
            next_guess = scores[-1][0]

        self.game.guess(next_guess)

    def handle_cycle_colouring(self):
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
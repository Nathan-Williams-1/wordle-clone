# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 02:25:38 2023

@author: njack
"""

import customtkinter as ctk
# from utils.quit import quit_game
from utils.in_work_mode import boss_is_watching
from utils.appearance import change_appearance
from utils.logic import get_colours
from utils.words import word_def_pair, get_definition
from itertools import product


# Initialise guess
GUESS_NUM = 1

WORD_LENGTH = 5
NUM_GUESSES = 6

GREEN = '#538D4E'
YELLOW = '#B59F3B'
GREY = '#3A3A3C'

BLACK = '#121213'
WHITE = '#FFFFFF'

# WHITE = '#792DC3'

# Tuple needed for dark/light mode
THEME = (BLACK, WHITE)

# Use for all text
FONT = ('Helvetica', 24, 'bold')
# Number of rows the window will have
SPAN = tuple([i for i in range(NUM_GUESSES+1)])

# Relative path to icons (should? work on any machine)
ICON_PATH = r'icons/'

class WordleGame:
    def __init__(self):
        # Initialize game parameters
        self.WORD_LENGTH = 5
        self.NUM_GUESSES = 6
        self.LETTER_COUNT = 0
        self.guess = ''
        self.GUESS_NUM = 1
        self.ks = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.target_word, self.target_definition = word_def_pair(self.WORD_LENGTH)

        # Set up GUI
        self.root = ctk.CTk()
        self.root.title("Team FinTrans Wordle")
        self.root.protocol('WM_DELETE_WINDOW', lambda: self.quit_game())

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(SPAN, weight=1)

        self.frame_1 = ctk.CTkFrame(self.root, fg_color='transparent', border_color=THEME)
        self.frame_1.grid(row=0, column=1, columnspan=self.WORD_LENGTH, rowspan=self.NUM_GUESSES)
        self.frame_1.grid_columnconfigure(1, weight=1)
        self.frame_1.grid_rowconfigure(SPAN, weight=1)

        self.frame_2 = ctk.CTkFrame(self.root, fg_color='transparent', border_color=THEME, width=170, height=490)
        self.frame_2.grid(row=0, column=0)
        self.frame_2.grid_propagate(False)
        self.frame_2.grid_columnconfigure(0, weight=1)

        self.frame_4 = ctk.CTkFrame(self.root, fg_color='transparent', border_color=THEME)
        self.frame_4.grid(row=self.NUM_GUESSES + 2, column=1)

        self.buttons = {}
        button_config = {
            'height': 80,
            'width': 80,
            'text': ' ',
            'text_color': THEME,
            'fg_color': 'transparent',
            'border_color': THEME,
            'border_width': 1,
            'corner_radius': 0,
            'font': FONT
        }
        for row in range(self.NUM_GUESSES):
            for column in range(self.WORD_LENGTH):
                coords = (row, column)
                button = ctk.CTkButton(self.frame_1, **button_config)
                button.grid(row=row, column=column, padx=1, pady=1, sticky='n')
                self.buttons[coords] = button

        self.key_coords = {}
        keys = ['QWERTYUIOP',
                'ASDFGHJKL',
                '↵ZXCVBNM⌫']
        for idx, row in enumerate(keys):
            row_frame = ctk.CTkFrame(self.frame_4, fg_color='transparent')
            row_frame.grid(row=idx + 1)
            for idy, key in enumerate(row):
                if key in ['⌫', '↵']:
                    width = 80
                    _font = ('', 24)
                    width = 80
                    padx = 0
                    if key == '↵':
                        key = 'ENTER'
                        _font = ('', 18)
                        padx = (0, 5)
                else:
                    _font = FONT
                    width = 50
                    padx = (0, 5)

                letter = ctk.CTkButton(row_frame,
                                       text=key,
                                       width=width,
                                       height=70,
                                       font=_font,
                                       fg_color=r'#787c7f',
                                       command=lambda a=key: self.key_pressed(a))
                letter.grid_propagate(False)
                letter.grid(row=idx, column=idy, padx=padx, pady=(0, 5))

                self.key_coords[(idx, idy)] = letter

        self.option_label = ctk.CTkLabel(self.frame_2, text='Options', width=50)
        self.option_label.grid(row=0, padx=20)

        self.theme_switch = ctk.StringVar(value="on")
        self.theme = ctk.CTkSwitch(self.frame_2, width=110, text="Dark mode",
                                   onvalue="Dark", offvalue="Light",
                                   border_color='transparent', variable=self.theme_switch,
                                   progress_color='#538D4E', command=lambda: self.change_appearance(self.theme_switch))
        self.theme.select()
        self.theme.grid(row=1, column=0, padx=20, pady=10)
        self.theme.grid_propagate(False)

        self.boss_switch = ctk.StringVar(value='no')
        self.boss_watch = ctk.CTkSwitch(self.frame_2, width=110, text="Boss is in?",
                                        onvalue="yes", offvalue="no",
                                        border_color='transparent', variable=self.boss_switch,
                                        progress_color='#538D4E',
                                        command=lambda: self.boss_is_watching(self.boss_switch, self.root, ICON_PATH))
        self.boss_watch.grid(row=2, column=0, padx=20)
        self.boss_watch.grid_propagate(False)

        self.root.bind('<Key>', self.key_pressed)
        self.root.geometry()
        self.root.resizable(False, False)

    def key_pressed(self, event):
        key = event
        if isinstance(event, str):
            if event == '⌦':
                key = 'BACKSPACE'
            elif event == '↵':
                key = 'RETURN'
            else:
                key = event
        else:
            key = event.keysym.upper()

        if key in self.ks and self.LETTER_COUNT < self.WORD_LENGTH:
            button = self.buttons[(self.GUESS_NUM - 1, self.LETTER_COUNT)]
            button.configure(text=key)
            self.LETTER_COUNT += 1
            self.guess += key
        elif len(self.guess) == self.WORD_LENGTH and key == 'RETURN':
            self.check_word(self.guess, self.target_word)
            self.guess = ''
            self.LETTER_COUNT = 0
            self.GUESS_NUM += 1
        elif key == 'BACKSPACE':
            if self.LETTER_COUNT > 0:
                self.LETTER_COUNT -= 1
                self.guess = self.guess[:-1]
                self.buttons[(self.GUESS_NUM - 1, self.LETTER_COUNT)].configure(text='')

    def check_word(self, word, target_word):
        if word == target_word:
            print('yay')
            self.quit_game()
        if not get_definition(word):
            print(f'{word} not a valid guess')
        else:
            if len(word) == self.WORD_LENGTH:
                status = get_colours(word, target_word)
                for idx, result in enumerate(status):
                    pos = idx
                    colour = status[idx]
                    letter = word[idx]
                    button = self.buttons[(self.GUESS_NUM - 1, pos)]

                    # Trigger button clicked animation
                    self.button_clicked_animation(button, colour)
    
                if self.GUESS_NUM > self.NUM_GUESSES:
                    self.quit_game()
                    
    def button_clicked_animation(self, button, colour):
        self.shrink_button(button)
        self.expand_button(button, colour)
        
    def shrink_button(self, button):
        new_height = 1
        while button.winfo_height() > new_height:
            button.configure(height=button.winfo_height() - 2)
            button.update()

    def expand_button(self, button, colour):
        target_height = 80
        button.configure(fg_color=colour, hover_color=colour)
        
        while button.winfo_height() < target_height:
            button.configure(height=button.winfo_height() + 2)
            button.update()

    def start_game(self):
        self.root.mainloop()

    def quit_game(self):
        self.root.destroy()

if __name__=='__main__':
    game = WordleGame()
    game.start_game()


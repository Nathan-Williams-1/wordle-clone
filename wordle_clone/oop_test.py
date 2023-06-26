# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 01:17:05 2023

@author: njack
"""
# %% Functions
import utils.constants as c
from utils.words import word_def_pair, get_definition
from utils.quit import quit_game
from utils.in_work_mode import boss_is_watching
from utils.appearance import change_appearance
from utils.logic import get_colours
import customtkinter as ctk

from itertools import product

# %% Main
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Dark by default
        ctk.set_appearance_mode('dark')
        
        self.title('Team FinTrans Wordle')
        self.configure(fg_color=(c.THEME[::-1]))
        self.protocol('WM_DELETE_WINDOW', self.end_game)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(c.SPAN, weight=1)
        
        self.guess = ''
        self.WORD_LENGTH = 5
        self.NUM_GUESSES = 6
        self.LETTER_COUNT = 0
        
        self.frame_main = ctk.CTkFrame(self, fg_color='transparent', border_color=c.THEME)
        self.frame_main.grid(row=0, column=1, columnspan=c.WORD_LENGTH, rowspan=c.NUM_GUESSES)
        self.frame_main.grid_columnconfigure(1, weight=1)
        self.frame_main.grid_rowconfigure(c.SPAN, weight=1)

        size_2 = {'width': 170, 'height': 490}
        self.frame_options = ctk.CTkFrame(self, fg_color='transparent', border_color=c.THEME, **size_2)
        self.frame_options.grid(row=0, column=0)
        
        # Stop window shrinking to fit contents
        self.frame_options.grid_propagate(False)
        self.frame_options.grid_columnconfigure(0, weight=1)
        

        # Keyboard frame
        self.frame_keyboard = ctk.CTkFrame(self, fg_color='transparent', border_color=c.THEME)
        self.frame_keyboard.grid(row=c.NUM_GUESSES+2, column=1)

        button_config = {
            'height' : 80,
            'width' : 80,
            'text': ' ', # should be blank to begin with,
            'text_color':c.THEME,
            'fg_color' : 'transparent',
            'border_color' : c.THEME,
            'border_width' : 1,
            'corner_radius' : 0,
            'font':c.FONT
            }
        
        # This will hold the coordinates of each button placed
        self.buttons = {}
        for row, column in product(range(c.NUM_GUESSES), range(c.WORD_LENGTH)):
            # Need to access buttons by position
            # to determine which letters go where
            self.coords = (row, column)
            self.button = ctk.CTkButton(self.frame_main, **button_config)
            self.button.grid(row=row, column=column, padx=1, pady=1, sticky='n') 
            self.buttons[self.coords] = self.button
    
    
        self.keys = {}
        
        for idx, row in enumerate(c.KEYBOARD):
            # Each row needs its own frame
            self.key_row = ctk.CTkFrame(self.frame_keyboard, fg_color='transparent')
            self.key_row.grid(row=idx+1)
            
            for idy, key in enumerate(row):
                # These keys don't exist in Helvetica
                if key in ['⌫','↵']:
                    width = 80
                    _font = ('', 24)

                    padx=0
                    if key == '↵':
                        key = 'ENTER'
        
                        _font = ('', 18)
                        padx = (0, 5)
                else:
                    _font = c.FONT
                    width=50
                    padx=(0,5)
                    
                self.letter = ctk.CTkButton(self.key_row, 
                                            text=key,
                                            width=width,
                                            height=70,
                                            font=_font,
                                            fg_color=r'#787c7f',
                                            # command = lambda a=key: key_pressed(a),
                                            )
                self.letter.grid_propagate(False)
                self.letter.grid(row=idx, column=idy, padx=padx, pady = (0,5))
                
                self.keys[(idx, idy)] = self.letter
   
    def key_pressed(self, event):
        global LETTER_COUNT, guess, GUESS_NUM, ks
        
        # This block handles both
        # typed keys and those
        # taken from on-screen keyboard
        # presses
        if isinstance(event, str):
            print(event)
            
            if event == '⌫':
                key = 'BACKSPACE'
            elif event == '↵':
                key = 'RETURN'
            else:
                key = event
        else:
            key = event.keysym.upper()
            
            
        if key in ks and self.LETTER_COUNT < self.WORD_LENGTH:
            button = buttons[(GUESS_NUM-1, LETTER_COUNT)] 
            button.configure(text=key)

            LETTER_COUNT += 1
            guess += key
            
        
        elif len(guess) == WORD_LENGTH and key in ['RETURN','ENTER']:
            check_word(guess, target_word)
            guess = ''
            LETTER_COUNT = 0 
            GUESS_NUM += 1
        
        elif key == 'BACKSPACE':
            if LETTER_COUNT > 0:
                LETTER_COUNT -= 1
                guess = guess[:-1]
                buttons[(GUESS_NUM-1, LETTER_COUNT)].configure(text='')
            
           
            
    def end_game(self):
        print('peace out homie')
        self.quit()
        self.destroy()
        
    def run(self):
        self.mainloop()

if __name__ == '__main__':
    App().run()




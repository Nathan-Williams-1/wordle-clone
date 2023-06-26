# -*- coding: utf-8 -*-

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

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

KEYBOARD = ['QWERTYUIOP',
            'ASDFGHJKL',
            '↵ZXCVBNM⌫']
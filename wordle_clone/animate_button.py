# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 02:37:56 2023

@author: njack
"""

import customtkinter as ctk
from itertools import product

class App(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.protocol('WM_DELETE_WINDOW', self.exit_app)
        self.word_length = 5
        self.num_guesses = 6
        self.title('Test')
        self.button_frame = ctk.CTkFrame(self, width=200, height=200)
        self.button_frame.grid()
        size = {'width': 80, 'height': 80}
        self.buttons = []
        
        for x, y in product(range(self.word_length), range(self.num_guesses)):
            button = ctk.CTkButton(self.button_frame, text='', **size, corner_radius=0)
            button.grid(row=x, column=y, padx=1, pady=1)
            button.bind('<Button-1>', self.button_clicked)
            self.buttons.append(button)
            
            # Store the original height as a custom attribute
            # self.update()
            # button.original_height = button.winfo_height()
            
    def run(self):
        self.mainloop()
        
    def exit_app(self):
        print('peace out homie')
        self.quit()
        self.destroy()
        
    def button_clicked(self, event):
        canvas = event.widget
        button = canvas.master
        
        # Shrink animation
        self.shrink_button(canvas)
        
        # Expand animation
        self.expand_button(canvas, button)
        
    def shrink_button(self, canvas):
        new_height = 1
        while canvas.winfo_height() > new_height:
            
            canvas.configure(height=canvas.winfo_height() - 2)
            canvas.update()

    def expand_button(self, canvas, button):
        target_height = 100
        button.configure(fg_color='red', hover_color='red')

        while canvas.winfo_height() < target_height:            
            canvas.configure(height=canvas.winfo_height() + 2)
            canvas.update()
        
if __name__ == '__main__':
    app = App()
    app.run()


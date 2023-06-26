# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 16:46:51 2023

@author: njack
"""

from tkinter import *
button_state = False #checks state of button
def click():
  if frame.place_info():
    frame.place_forget()
  else:
    # show the frame below the button
    x, y = button.winfo_x(), button.winfo_y()+button.winfo_height()
    # assume the final size of the frame is 100x100
    for step in range(1, 11):
      frame.place(x=x, y=y, width=step*10, height=step*10)
      frame.update_idletasks() # update the frame
      frame.after(10) # sleep for a very short period


window = Tk()
frame = Frame(window, bg='lightblue')

button = Button(window, text="menu", command=click)
button.place(x=50, y=50, anchor=CENTER)

window.mainloop()


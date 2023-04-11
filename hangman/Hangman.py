from tkinter import *
import random
import sys

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

word = None


def draw_word():
    try:
        with open("words.txt", "r") as words_file:
            lines = words_file.read().splitlines()
        global word
        word = random.choice(lines)
    except IOError:
        sys.exit("words.txt file not found!")


def guess(letter):
    print(letter.get())

def game():
    draw_word()
    global word
    print("Wylosowano:", word)


root = Tk()
root.title('Hangman')
root.iconbitmap('./window_icon.ico')
root.resizable(False, False)

photos = [PhotoImage(file="images/hang0.png"), PhotoImage(file="images/hang1.png"), PhotoImage(file="images/hang2.png"),
PhotoImage(file="images/hang3.png"), PhotoImage(file="images/hang4.png"), PhotoImage(file="images/hang5.png"),
PhotoImage(file="images/hang6.png"), PhotoImage(file="images/hang7.png"), PhotoImage(file="images/hang8.png"),
PhotoImage(file="images/hang9.png"), PhotoImage(file="images/hang10.png"), PhotoImage(file="images/hang11.png")]

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width/2 - WINDOW_WIDTH / 2)
center_y = int(screen_height/2 - WINDOW_HEIGHT / 2)

root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}')

image_label = Label(root, image=photos[11])
image_label.pack(expand=True)

letter = StringVar()
letter_entry = Entry(root, textvariable=letter, font=("lucida", 20, "bold"))
letter_entry.pack(ipady=5, expand=True)
letter_entry.focus()

submit_button = Button(root, text="Submit", command=lambda:guess(letter))
submit_button.pack(ipadx=5, ipady=5, expand=True)

game()
root.mainloop()
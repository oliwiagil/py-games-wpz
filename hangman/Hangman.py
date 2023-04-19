from tkinter import *
from tkinter import messagebox
import random
import sys

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500


def draw_word():
    word = None

    try:
        with open("words.txt", "r") as words_file:
            lines = words_file.read().splitlines()
        word = random.choice(lines)
    except IOError:
        sys.exit("words.txt file not found!")
    return word


def guess():
    global no_failed_guesses
    letter = entered_txt.get()

    letter_entry.delete(0, END)
    
    if len(letter) > 1:
        messagebox.showerror("Hangman", "You can pass only a single letter!")
        return
    if not letter.isalpha():
        messagebox.showerror("Hangman", "You can enter only letters")
        return
    
    if no_failed_guesses < 11:
        correct_letters = list(word_with_spaces)
        guessed_letters = list(word_state.get())

        # print(correct_letters)
        # print(guessed_letters)

        low_l = letter.lower()
        up_l = letter.upper()

        if low_l in correct_letters or up_l in correct_letters:
            for i in range(len(correct_letters)):
                if correct_letters[i] == low_l:
                    guessed_letters[i] = low_l
                if correct_letters[i] == up_l:
                    guessed_letters[i] = up_l

            word_state.set("".join(guessed_letters))
            if word_state.get() == word_with_spaces:
                messagebox.showinfo("Hangman", "You guessed the word!")

        else:
            no_failed_guesses += 1
            image_label.config(image=photos[no_failed_guesses])
    
    if no_failed_guesses == 11:
        messagebox.showwarning("Hangman", "You lost, game over")
        word_state.set("".join(correct_letters))

def game():
    global no_failed_guesses
    global word_with_spaces
    no_failed_guesses = 0
    image_label.config(image=photos[0])

    word = draw_word()
    word_with_spaces = " ".join(word)
    unders = "".join(["_" if c != " " else c for c in word_with_spaces])

    word_state.set(unders)
    # print("Wylosowano:", word)

def enter_pressed(event):
    guess()

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

new_game_button = Button(root, text="New game", command=game)
new_game_button.pack(ipadx=5, ipady=5, expand=True)

image_label = Label(root)
image_label.pack(expand=True)

word_state = StringVar()
word_state_label = Label(root, textvariable=word_state,font=("lucida", 20, "bold"))
word_state_label.pack(ipadx=5, ipady=5, expand=True)

entered_txt = StringVar()
letter_entry = Entry(root, textvariable=entered_txt, font=("lucida", 20, "bold"))
letter_entry.pack(ipady=5, expand=True)
letter_entry.focus()

submit_button = Button(root, text="Submit", command=guess)
submit_button.pack(ipadx=5, ipady=5, expand=True)
root.bind("<Return>", enter_pressed)

game()
root.mainloop()
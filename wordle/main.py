import tkinter as tk
import random
import os

game_directory = os.path.dirname(__file__)
os.chdir(game_directory)

with open('słowa.txt', 'r', encoding='utf-8') as file:
    words = file.readlines()
    words = [word.strip() for word in words]
    random_word = random.choice(words)
    word = random.choice(words)
    print(word)

rec_size = 80
distance = 20
num = 0
end = False


def read_text():
    global num
    global end
    if num == 6:
        return
    text = text_entry.get("1.0", "end-1c")
    if len(text) != 5:
        return
    text = text.upper()
    if text not in words:
        return
    if end is True:
        return
    canvas = tk.Canvas(root, width=500, height=100, bg="white")
    canvas.pack()
    x = 10
    y = 10
    greens = 0
    for i in range(len(text)):
        if word[i] == text[i]:
            greens += 1
            canvas.create_rectangle(x, y, x + rec_size, y + rec_size, fill="green")
            canvas.create_text(x + rec_size / 2, y + rec_size / 2, text=text[i], font=("Arial", 30), fill="white")
        elif text[i] in word:
            canvas.create_rectangle(x, y, x + rec_size, y + rec_size, fill="yellow")
            canvas.create_text(x + rec_size / 2, y + rec_size / 2, text=text[i], font=("Arial", 30), fill="white")
        else:
            canvas.create_rectangle(x, y, x + rec_size, y + rec_size, fill="black")
            canvas.create_text(x + rec_size / 2, y + rec_size / 2, text=text[i], font=("Arial", 30), fill="white")
        x += rec_size + distance

    if greens == 5:
        end = True
    num += 1

root = tk.Tk()
root.title("wordle")
root.geometry("700x700")
button = tk.Button(root, text="Sprawdź", command=lambda: read_text())
button.pack(side=tk.BOTTOM)

text_entry = tk.Text(root, height=2)
text_entry.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)

root.mainloop()

from tkinter import *
import tkinter as tk
import time
import random
global out


def startBall(ball, speed):
    s = random.randint(-speed, speed)
    x = s
    y = 0 - speed
    court.move(ball, x, y)

    for grade in range(1, 1000000):
        l, t, r, b = court.coords(ball)
        score_entry.delete(0, END)
        score_entry.insert(0, str(grade))
        if(r >= 400 and x >= 0 and y < 0): # ↗ 
            x, y = 0-speed, 0-speed
        elif(r >= 400 and x >= 0 and y >= 0): # ↘ 
            x, y = 0-speed, speed
        elif(l <= 0 and x < 0 and y < 0): # ↖ 
            x, y = speed, 0-speed
        elif(l <= 0 and x < 0 and y >= 0): # ↙ 
            x, y = speed, speed
        elif(t <= 0 and x >= 0 and y < 0): # ↗ 
            x, y = speed, speed
        elif(t <= 0 and x < 0 and y < 0): # ↖ 
            x, y = 0-speed, speed
        #ball on baselevel
        elif(b >= 385): 
            touch = l + 10 
            paddle_left, paddle_top, paddle_right, paddle_bottom = court.coords(paddle)
            if(touch >= paddle_left and touch <= paddle_right): 
                n = random.randint(-speed, speed)
                x, y = n, 0-speed
            else: 
                court.itemconfigure(label, state='normal')
                global out
                out = True
                break
        
        time.sleep(.020)
        court.move(ball, x, y)
        court.update()


def movePaddle(paddle, dir, x, y = 0):
    x1, y1, x2, y2 = court.coords(paddle)
    if ((x1 > 0 and dir == 1) or (x2 < 400 and dir == 2)):
        court.move(paddle, x, y)
        court.update()

def restart():
    global out
    if(out == True):
        out = False
        court.itemconfigure(label, state='hidden')
        court.moveto(paddle, 150, 385)
        court.moveto(ball, 190, 365)
        startBall(ball, ball_speed)


if __name__ == "__main__":
    root = Tk()
    root.title("pong game")
    root.minsize(400,400)
    paddle_speed = 10
    ball_speed = 7
    out = False

    root.bind("<KeyPress-Left>", lambda event: movePaddle(paddle, 1, 0-paddle_speed))
    root.bind("<KeyPress-Right>", lambda event: movePaddle(paddle, 2, paddle_speed))
    root.bind("<Return>", lambda event: restart())

    court = Canvas(width=400, height=400, background='#555555')
    court.pack()
    paddle = court.create_rectangle(150, 385, 250, 400, fill='#e7ffba', outline='#e7ffba')
    ball = court.create_oval(190, 365, 210, 385, fill='white', outline='white')    
    score_entry = tk.Entry(court, text='0')
    score_txt = court.create_window(350, 0, anchor='nw', window=score_entry)

    end_of_game_lbl = tk.Label(court, text='Koniec gry! Wciśniej enter by zagrać ponownie.')
    label = court.create_window(100, 190, anchor='nw', window=end_of_game_lbl)
    court.itemconfigure(label, state='hidden')
    
    startBall(ball, ball_speed)

    root.mainloop()


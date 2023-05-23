import sys
import os
from tkinter import *
from functools import partial
import random


COLORS  =[
'snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
'lavender blush', 'misty rose', 'light grey', 
'dodger blue', 'deep sky blue', 'sky blue',

'light sky blue', 'light steel blue',
'light blue', 'powder blue', 'pale turquoise',  'turquoise',
'light cyan', 'aquamarine','pale green', 'lawn green', 
'green yellow', 'yellow green', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
'light yellow', 'gold', 'light goldenrod', 'goldenrod',  'rosy brown',
'indian red','sandy brown', 'salmon', 'light salmon', 'orange', 
'coral', 'light coral', 'tomato', 'pink', 'light pink',
'pale violet red', 'thistle', 'snow2', 'snow3',

'seashell2', 'seashell3', 'AntiqueWhite1', 'AntiqueWhite2',
'AntiqueWhite3', 'bisque2', 'bisque3', 'PeachPuff2',
'PeachPuff3', 'NavajoWhite2', 'NavajoWhite3', 
'LemonChiffon2', 'LemonChiffon3', 'cornsilk2', 'cornsilk3',
'ivory2', 'ivory3', 'honeydew2', 'honeydew3',
'LavenderBlush2', 'LavenderBlush3', 'MistyRose2', 'MistyRose3',
'azure2', 'azure3', 

'SteelBlue1', 'SteelBlue2',
'SkyBlue1', 'SkyBlue2','LightSkyBlue1', 'LightSkyBlue2',
'LightSkyBlue3', 'SlateGray1', 'SlateGray2', 'SlateGray3',
 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
 'LightBlue1', 'LightBlue2', 'LightBlue3',
'LightCyan2', 'LightCyan3','PaleTurquoise1', 'PaleTurquoise2',
'PaleTurquoise3', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
'turquoise1', 'turquoise2', 'turquoise3',  'cyan2', 'cyan3',

'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
'PaleGreen3', 'SpringGreen2', 'SpringGreen3', 
'green2', 'chartreuse2', 'chartreuse3', 
'OliveDrab1', 'OliveDrab2', 'khaki1', 'khaki2', 'khaki3', 
'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 
'LightYellow2', 'LightYellow3', 'yellow2', 'yellow3',
'gold2', 'gold3', 'goldenrod1', 'goldenrod2', 'goldenrod3',
'RosyBrown1', 'RosyBrown2', 'RosyBrown3',

'IndianRed1', 'IndianRed2', 'sienna1', 'sienna2', 'burlywood1',
'burlywood2', 'burlywood3', 'wheat1', 'wheat2', 'wheat3', 'tan1',
'tan2', 'chocolate1', 'chocolate2', 'chocolate3', 'salmon1', 'salmon2',
'salmon3', 'LightSalmon2', 'LightSalmon3', 'orange2', 'orange3',
'coral1', 'coral2', 'coral3','tomato2',
'HotPink1', 'HotPink2', 'HotPink3', 

'pink1', 'pink2', 'pink3', 'LightPink1', 'LightPink2',  'PaleVioletRed1',
'PaleVioletRed2', 'orchid1', 'orchid2', 'plum1', 'plum2',
'thistle1', 'thistle2', 'thistle3',
'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']

def launch_game(command):
    os.system(command)

def score(command):
    with open(command+"\score.txt") as file:
        value=file.readlines()
        
        results_window= Toplevel(window)
        results_window.title("Highscore")
        Label(results_window, text="Your current highscore is:\n"+value[0],font=("Arial",26,"bold")).pack()


def prepare(folder):
    for root, dirs, files in os.walk(os.path.expanduser(folder)):
        if(root.startswith(".\.git")):
            continue
        for name in files:
            if(name=="main.py"):
                game_path=os.path.join(root, name)
                game_name=root.removeprefix(".\\")
                
                launch=partial(launch_game, 'python '+game_path)
                Button(window, text=game_name, command=launch, height=2, width=25, font=("Arial",26,"bold"),bg=random.sample(COLORS, 1)[0]).pack()
                show_score=partial(score, root)
                Button(window, text="highscore "+game_name, command=show_score, height=2, width=25, font=("Arial",26,"bold"),bg=random.sample(COLORS, 1)[0]).pack()


window=Tk()
window.eval('tk::PlaceWindow . center')
prepare(".")
window.mainloop()





















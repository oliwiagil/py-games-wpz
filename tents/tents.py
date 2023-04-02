import tkinter
from tkinter import *
from random import randint
from PIL import ImageTk, Image

def left_click(event,x,y):
    cell=(y-1)*size+(x-1)
   # print(open_f[cell])
    if(open_f[cell]==1 or open_f[cell]==2 or open_f[cell]==4 or open_f[cell]==5):
        return
        
    if(open_f[cell]==3):
        open_f[cell]=0
        image = Image.open("B.png")
    else:
        open_f[cell]=3
        image = Image.open("N.png")
        
    photo = ImageTk.PhotoImage(image.resize((field_size, field_size)))
    
    event.widget.configure(image=photo)
    event.widget.image=photo
    
    
   

def right_click(event,x,y): 
    cell=(y-1)*size+(x-1) 
    print(open_f[cell])
    if(open_f[cell]==1 or open_f[cell]==2 or open_f[cell]==3 or open_f[cell]==5):
        return

    #usuwamy "X" z pola
    if(open_f[cell]==4):
        open_f[cell]=0
        image = Image.open("B.png")
    #oznaczamy to pole jako "X"
    else:
        open_f[cell]=4
        image = Image.open("X.png")
        
    photo = ImageTk.PhotoImage(image.resize((field_size, field_size)))
    
    event.widget.configure(image=photo)
    event.widget.image=photo
    
    

field_size=80

trees=15
size=10

total_size=size*size



def check_tents(arguments9):
    i=0
    while(i<len(arguments9)):
        if(array[arguments9[i]]=="N"):
            return 1
        i+=1
    return 0
    
    
def check_available_place(arguments4):
    i=0
    while(i<len(arguments4)):
        if(array[arguments4[i]]=="X"):
            return 0
        i+=1
    
    return 1


def set_close(cell):
    arguments4=get_adjacent_fields_ver_4(cell)
    
    i=0
    while(i<len(arguments4)):
        if(array[arguments4[i]]!="T"):
            open_f[arguments4[i]]=0
        i+=1



def set_tree(arguments4):
    #losujemy miejsce na drzewo
    while(True):
        tmp=randint(0,len(arguments4)-1)
        if(array[arguments4[tmp]]=="X"):
            array[arguments4[tmp]]="T"
            open_f[arguments4[tmp]]=1
            set_close(arguments4[tmp])
            break

    
def get_adjacent_fields_ver_9(cell):
    row=int(cell/size)
    column=cell%size
    
    #nie jestesmy na brzegu
    if(row!=0 and row!=(size-1) and column!=0 and column!=(size-1)):
        return cell-1,cell+1,cell-size,cell+size,cell-1-size,cell-1+size,cell+1-size,cell+1+size
    #left
    elif (column==0 and row!=0 and row!=(size-1)):
        return cell+1,cell-size,cell+size,cell+1-size,cell+1+size
    #right
    elif (column==(size-1) and row!=0 and row!=(size-1)):
        return cell-1,cell-size,cell+size,cell-1-size,cell-1+size
    #up
    elif (row==0 and column!=0 and column!=(size-1)):
        return cell-1,cell+1,cell+size,cell-1+size,cell+1+size
    #down
    elif (row==(size-1) and column!=0 and column!=(size-1)):
        return cell-1,cell+1,cell-size,cell-1-size,cell+1-size
    #left up
    elif (column==0 and row==0):
        return cell+1,cell+size,cell+1+size
    #right up
    elif (column==(size-1) and row==0 ):
        return cell-1,cell+size,cell-1+size
    #left down
    elif (column==0 and row==(size-1)):
        return cell+1,cell-size,cell+1-size
    #right down
    else:
        return cell-1,cell-size,cell-1-size


def get_adjacent_fields_ver_4(cell):
    row=int(cell/size)
    column=cell%size
    
    #nie jestesmy na brzegu
    if(row!=0 and row!=(size-1) and column!=0 and column!=(size-1)):
        return cell-1,cell+1,cell-size,cell+size
    #left
    elif (column==0 and row!=0 and row!=(size-1)):
        return cell+1,cell-size,cell+size
    #right
    elif (column==(size-1) and row!=0 and row!=(size-1)):
        return cell-1,cell-size,cell+size
    #up
    elif (row==0 and column!=0 and column!=(size-1)):
        return cell-1,cell+1,cell+size
    #down
    elif (row==(size-1) and column!=0 and column!=(size-1)):
        return cell-1,cell+1,cell-size
    #left up
    elif (column==0 and row==0):
        return cell+1,cell+size
    #right up
    elif (column==(size-1) and row==0 ):
        return cell-1,cell+size
    #left down
    elif (column==0 and row==(size-1)):
        return cell+1,cell-size
    #right down
    else:
        return cell-1,cell-size
    

def prepare_game_board(number_of_trees):
    loops=0
    while(number_of_trees>0):
        cell=randint(0, total_size-1)

        if(array[cell] == "X"):
            row=int(cell/size)
            column=cell%size
            
            arguments9=get_adjacent_fields_ver_9(cell)
            arguments4=get_adjacent_fields_ver_4(cell)

            if(check_tents(arguments9)):
                continue
            if(check_available_place(arguments4)):
                continue
            set_tree(arguments4)
            
            array[cell]="N"
            row_count[column]+=1
            column_count[row]+=1
            number_of_trees-=1
            loops=0          
        
        #tyle bylo juz iteracji, ze jest najprawdopodobniej deadlock
        if(loops>4*total_size):
            return 0
        loops+=1
    
    return 1
    
    
def set_X_on_0_rows_and_columns():
    for i in range(0, size):
        if(row_count[i]==0):
            for j in range(i, total_size, size):
                if(array[j]!="T"):
                    open_f[j]=2
        if(column_count[i]==0):
            for j in range(0, size):
                if(array[i*size+j]!="T"):
                    open_f[i*size+j]=2



window=tkinter.Tk()


while(True):
    array=['X']*total_size
    open_f=[2]*total_size
    row_count=[0]*size
    column_count=[0]*size
    
    print(open_f)
    
    if(prepare_game_board(trees)):
        break

set_X_on_0_rows_and_columns()

print(array)
print(open_f)


field=Frame(window, width=field_size, height=field_size, highlightbackground="black", highlightthickness=1)

field.grid_rowconfigure(0, weight=1)
field.grid_columnconfigure(0, weight=1)
field.grid(row=0,column=0,sticky="nsew")

for x in range(1,size+1):
    field=Frame(window, width=field_size, height=field_size, background="yellow",highlightbackground="black", highlightthickness=1)
    label=Label(field, text=row_count[x-1], bg="yellow", font=("Arial", 20))
    field.grid_rowconfigure(0, weight=1)
    field.grid_columnconfigure(x, weight=1)
    field.grid(row=0,column=x, sticky="nsew")
    label.grid(row=0,column=x)
   

for y in range(1,size+1):
    field=Frame(window, width=field_size, height=field_size, background="yellow",highlightbackground="black", highlightthickness=1)
    field.grid_rowconfigure(y, weight=1)
    field.grid_columnconfigure(0, weight=1)
    label=Label(field, text=column_count[y-1], bg="yellow", font=("Arial", 20))
    field.grid(row=y,column=0,sticky="nsew")
    label.grid(row=y,column=0)

    for x in range(1,size+1):
        field=Frame(window, width=field_size, height=field_size, background="white",highlightbackground="black", highlightthickness=1)
        field.grid_rowconfigure(x, weight=1)
        field.grid_columnconfigure(y, weight=1)
        
        field.grid(row=y,column=x,sticky="nsew" )
        
        cell=(y-1)*size+(x-1)
        
        if(open_f[cell]=="tree"):
            image=Image.open("T.png")
        elif(open_f[cell]=="x_beg"):
            image=Image.open("XX.png")
        else:
            image=Image.open("B.png")
            
        photo=ImageTk.PhotoImage(image.resize((field_size, field_size)))
        label=Label(field, image=photo)
        label.image = photo
        label.pack()
        
        label.bind("<Button-1>", lambda event, y=y, x=x: left_click(event,x,y))
        label.bind("<Button-3>", lambda event, y=y, x=x: right_click(event,x,y))
        
    

window.mainloop()













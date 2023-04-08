import tkinter
from tkinter import *
from random import randint
from PIL import ImageTk, Image


def change_image(image_file, element):
    image=Image.open(image_file)
    photo=ImageTk.PhotoImage(image.resize((field_size, field_size)))
    element.configure(image=photo)
    element.image=photo


#ustawienie/usuniecie namiotu
def left_click(event,x,y):
    column=x-1
    row=y-1

    cell=row*size+column
    if(open_f[cell]==1 or open_f[cell]==2 or open_f[cell]==4 or open_f[cell]==5):
        return
        
    if(open_f[cell]==3):
        open_f[cell]=0
        change_image("B.png", event.widget)
        
        row_count[column]+=1
        column_count[row]+=1
        
        labelsX[column].config(text=row_count[column])
        labelsY[row].config(text=column_count[row])
        
        arguments=get_adjacent_fields_ver_9(cell)
        unset_all_X(arguments)
        
        if(row_count[column]==1):
            for j in range(column, total_size, size):
                if(open_f[j]==5):
                    if(not adjacent_to_tent(j) and row_count[j%size]!=0 
                    and column_count[int(j/size)]!=0):
                        open_f[j]=0
                        change_image("B.png",fields[j])

        if(column_count[row]==1):
            for j in range(0, size):
                if(open_f[row*size+j]==5):
                    tmp_cell=row*size+j
                    if(not adjacent_to_tent(tmp_cell) and row_count[tmp_cell%size]!=0 
                    and column_count[int(tmp_cell/size)]!=0):
                        open_f[tmp_cell]=0
                        change_image("B.png",fields[tmp_cell])

        
    else:
        open_f[cell]=3
        change_image("N.png", event.widget)
        
        row_count[column]-=1
        column_count[row]-=1
        
        labelsX[column].config(text=row_count[column])
        labelsY[row].config(text=column_count[row])

        arguments=get_adjacent_fields_ver_9(cell)
        set_all_to_X(arguments)
        
        if(row_count[column]==0):
           for j in range(column, total_size, size):
                if(open_f[j]==0):
                    open_f[j]=5
                    change_image("Xaut.png",fields[j])

        if(column_count[row]==0):
            for j in range(0, size):
                if(open_f[row*size+j]==0):
                    open_f[row*size+j]=5
                    change_image("Xaut.png",fields[row*size+j])

    

#ustawienie/usuniecie X-sa
def right_click(event,x,y): 
    column=x-1
    row=y-1
    
    cell=row*size+column 
    if(open_f[cell]==1 or open_f[cell]==2 or open_f[cell]==3 or open_f[cell]==5):
        return

    #usuwamy "X" z pola
    if(open_f[cell]==4):
        if(adjacent_to_tent(cell)):
            open_f[cell]=5
            change_image("Xaut.png",event.widget)
        elif(column_count[row]==0 or row_count[column]==0):
            open_f[cell]=5
            change_image("Xaut.png",event.widget)   
        else:
            open_f[cell]=0
            change_image("B.png", event.widget)
    #oznaczamy to pole jako "X"
    else:
        open_f[cell]=4
        change_image("X.png", event.widget)

    

field_size=80

trees=15
size=10

total_size=size*size


def set_all_to_X(arguments9):
    for i in arguments9:
        if(open_f[i]==0):
            open_f[i]=5
            change_image("Xaut.png",fields[i])
    return 0
    
    
def unset_all_X(arguments9):
    for i in arguments9:
        if(open_f[i]==5):
            if(not adjacent_to_tent(i) and row_count[i%size]!=0 
            and column_count[int(i/size)]!=0):
                open_f[i]=0
                change_image("B.png",fields[i])


def adjacent_to_tent(cell):
    arguments9=get_adjacent_fields_ver_9(cell)

    for i in arguments9:
        if(open_f[i]==3):
            return 1
    
    return 0


def check_tents(arguments9):
    for i in arguments9:
        if(array[i]=="N"):
            return 1
    return 0
    
    
def check_available_place(arguments4):
    for i in arguments4:
        if(array[i]=="X"):
            return 0
    
    return 1


def set_close(cell):
    arguments4=get_adjacent_fields_ver_4(cell)
    
    for i in arguments4:
        if(array[i]!="T"):
            open_f[i]=0



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

fields=list()
labelsX=list()
labelsY=list()


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
    labelsX.append(label)


for y in range(1,size+1):
    field=Frame(window, width=field_size, height=field_size, background="yellow",highlightbackground="black", highlightthickness=1)
    field.grid_rowconfigure(y, weight=1)
    field.grid_columnconfigure(0, weight=1)
    label=Label(field, text=column_count[y-1], bg="yellow", font=("Arial", 20))
    field.grid(row=y,column=0,sticky="nsew")
    label.grid(row=y,column=0)
    labelsY.append(label)

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
        
        fields.append(label)
        
    

window.mainloop()













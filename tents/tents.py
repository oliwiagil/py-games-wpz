from tkinter import *
from tkinter import messagebox

from random import randint
from PIL import ImageTk, Image


class Game(Frame):

    def change_image(self,image_file, element):
        image=Image.open(image_file)
        photo=ImageTk.PhotoImage(image.resize((self.field_size, self.field_size)))
        element.configure(image=photo)
        element.image=photo


    #ustawienie/usuniecie namiotu
    def left_click(self,event,x,y):
        column=x-1
        row=y-1

        cell=row*self.size+column
        if(self.open_f[cell]=="tree" or self.open_f[cell]=="x_beg" or self.open_f[cell]=="x_pl" or self.open_f[cell]=="x_aut"):
            return
            
        if(self.open_f[cell]=="tent"):
            self.open_f[cell]="open"
            self.change_image("B.png", event.widget)
            
            self.row_count[column]+=1
            self.column_count[row]+=1
            
            self.labelsX[column].config(text=self.row_count[column])
            self.labelsY[row].config(text=self.column_count[row])
            
            arguments=self.get_adjacent_fields_ver_9(cell)
            self.unset_all_X(arguments)
            
            if(self.row_count[column]==1):
                for j in range(column, self.total_size, self.size):
                    if(self.open_f[j]=="x_aut"):
                        if(not self.adjacent_to_tent(j) and self.row_count[j%self.size]!=0 
                        and self.column_count[int(j/self.size)]!=0):
                            self.open_f[j]="open"
                            self.change_image("B.png",self.fields[j])

            if(self.column_count[row]==1):
                for j in range(0, self.size):
                    if(self.open_f[row*self.size+j]=="x_aut"):
                        tmp_cell=row*self.size+j
                        if(not self.adjacent_to_tent(tmp_cell) and self.row_count[tmp_cell%self.size]!=0 
                        and self.column_count[int(tmp_cell/self.size)]!=0):
                            self.open_f[tmp_cell]="open"
                            self.change_image("B.png",self.fields[tmp_cell])

        else:
            self.open_f[cell]="tent"
            self.change_image("N.png", event.widget)
            
            self.row_count[column]-=1
            self.column_count[row]-=1
            
            self.labelsX[column].config(text=self.row_count[column])
            self.labelsY[row].config(text=self.column_count[row])

            arguments=self.get_adjacent_fields_ver_9(cell)
            self.set_all_to_X(arguments)
            
            if(self.row_count[column]==0):
               for j in range(column, self.total_size, self.size):
                    if(self.open_f[j]=="open"):
                        self.open_f[j]="x_aut"
                        self.change_image("Xaut.png",self.fields[j])

            if(self.column_count[row]==0):
                for j in range(0, self.size):
                    if(self.open_f[row*self.size+j]=="open"):
                        self.open_f[row*self.size+j]="x_aut"
                        self.change_image("Xaut.png",self.fields[row*self.size+j])
                        
            if(self.check_game_win()):
                self.game_won()

        

    #ustawienie/usuniecie X-sa
    def right_click(self,event,x,y): 
        column=x-1
        row=y-1
        
        cell=row*self.size+column 
        if(self.open_f[cell]=="tree" or self.open_f[cell]=="x_beg" or self.open_f[cell]=="tent" or self.open_f[cell]=="x_aut"):
            return

        #usuwamy "X" z pola
        if(self.open_f[cell]=="x_pl"):
            if(self.adjacent_to_tent(cell)):
                self.open_f[cell]="x_aut"
                self.change_image("Xaut.png",event.widget)
            elif(self.column_count[row]==0 or self.row_count[column]==0):
                self.open_f[cell]="x_aut"
                self.change_image("Xaut.png",event.widget)   
            else:
                self.open_f[cell]="open"
                self.change_image("B.png", event.widget)
        #oznaczamy to pole jako "X"
        else:
            self.open_f[cell]="x_pl"
            self.change_image("X.png", event.widget)
            

    def set_all_to_X(self,arguments9):
        for i in arguments9:
            if(self.open_f[i]=="open"):
                self.open_f[i]="x_aut"
                self.change_image("Xaut.png",self.fields[i])
        return 0
        
        
    def unset_all_X(self,arguments9):
        for i in arguments9:
            if(self.open_f[i]=="x_aut"):
                if(not self.adjacent_to_tent(i) and self.row_count[i%self.size]!=0 
                and self.column_count[int(i/self.size)]!=0):
                    self.open_f[i]="open"
                    self.change_image("B.png",self.fields[i])


    def adjacent_to_tent(self,cell):
        arguments9=self.get_adjacent_fields_ver_9(cell)

        for i in arguments9:
            if(self.open_f[i]=="tent"):
                return 1
        
        return 0


    def check_tents(self,arguments9):
        for i in arguments9:
            if(self.array[i]=="N"):
                return 1
        return 0
        
        
    def check_available_place(self,arguments4):
        for i in arguments4:
            if(self.array[i]=="X"):
                return 0
        
        return 1


    def set_close(self,cell):
        arguments4=self.get_adjacent_fields_ver_4(cell)
        
        for i in arguments4:
            if(self.array[i]!="T"):
                self.open_f[i]="open"



    def set_tree(self,arguments4):
        #losujemy miejsce na drzewo
        while(True):
            tmp=randint(0,len(arguments4)-1)
            if(self.array[arguments4[tmp]]=="X"):
                self.array[arguments4[tmp]]="T"
                self.open_f[arguments4[tmp]]="tree"
                self.set_close(arguments4[tmp])
                break

        
    def get_adjacent_fields_ver_9(self,cell):
        row=int(cell/self.size)
        column=cell%self.size
        
        #nie jestesmy na brzegu
        if(row!=0 and row!=(self.size-1) and column!=0 and column!=(self.size-1)):
            return cell-1,cell+1,cell-self.size,cell+self.size,cell-1-self.size,cell-1+self.size,cell+1-self.size,cell+1+self.size
        #left
        elif (column==0 and row!=0 and row!=(self.size-1)):
            return cell+1,cell-self.size,cell+self.size,cell+1-self.size,cell+1+self.size
        #right
        elif (column==(self.size-1) and row!=0 and row!=(self.size-1)):
            return cell-1,cell-self.size,cell+self.size,cell-1-self.size,cell-1+self.size
        #up
        elif (row==0 and column!=0 and column!=(self.size-1)):
            return cell-1,cell+1,cell+self.size,cell-1+self.size,cell+1+self.size
        #down
        elif (row==(self.size-1) and column!=0 and column!=(self.size-1)):
            return cell-1,cell+1,cell-self.size,cell-1-self.size,cell+1-self.size
        #left up
        elif (column==0 and row==0):
            return cell+1,cell+self.size,cell+1+self.size
        #right up
        elif (column==(self.size-1) and row==0 ):
            return cell-1,cell+self.size,cell-1+self.size
        #left down
        elif (column==0 and row==(self.size-1)):
            return cell+1,cell-self.size,cell+1-self.size
        #right down
        else:
            return cell-1,cell-self.size,cell-1-self.size


    def get_adjacent_fields_ver_4(self,cell):
        row=int(cell/self.size)
        column=cell%self.size
        
        #nie jestesmy na brzegu
        if(row!=0 and row!=(self.size-1) and column!=0 and column!=(self.size-1)):
            return cell-1,cell+1,cell-self.size,cell+self.size
        #left
        elif (column==0 and row!=0 and row!=(self.size-1)):
            return cell+1,cell-self.size,cell+self.size
        #right
        elif (column==(self.size-1) and row!=0 and row!=(self.size-1)):
            return cell-1,cell-self.size,cell+self.size
        #up
        elif (row==0 and column!=0 and column!=(self.size-1)):
            return cell-1,cell+1,cell+self.size
        #down
        elif (row==(self.size-1) and column!=0 and column!=(self.size-1)):
            return cell-1,cell+1,cell-self.size
        #left up
        elif (column==0 and row==0):
            return cell+1,cell+self.size
        #right up
        elif (column==(self.size-1) and row==0 ):
            return cell-1,cell+self.size
        #left down
        elif (column==0 and row==(self.size-1)):
            return cell+1,cell-self.size
        #right down
        else:
            return cell-1,cell-self.size
        

    def prepare_game_board(self,number_of_trees):
        loops=0
        
        while(number_of_trees>0):
            cell=randint(0, self.total_size-1)

            if(self.array[cell] == "X"):
                row=int(cell/self.size)
                column=cell%self.size
                
                arguments9=self.get_adjacent_fields_ver_9(cell)
                arguments4=self.get_adjacent_fields_ver_4(cell)

                if(self.check_tents(arguments9)):
                    continue
                if(self.check_available_place(arguments4)):
                    continue
                self.set_tree(arguments4)
                
                self.array[cell]="N"
                self.row_count[column]+=1
                self.column_count[row]+=1
                number_of_trees-=1
                loops=0          
            
            #tyle bylo juz iteracji, ze jest najprawdopodobniej deadlock
            if(loops>4*self.total_size):
                return 1
            loops+=1
        
        return 0
        
        
    def set_X_on_0_rows_and_columns(self):
        for i in range(0, self.size):
            if(self.row_count[i]==0):
                for j in range(i, self.total_size, self.size):
                    if(self.array[j]!="T"):
                        self.open_f[j]="x_beg"
            if(self.column_count[i]==0):
                for j in range(0, self.size):
                    if(self.array[i*self.size+j]!="T"):
                        self.open_f[i*self.size+j]="x_beg"

    def check_game_win(self):
        for i in self.row_count:
            if(i!=0):
                return 0
                
        for i in self.column_count:
            if(i!=0):
                return 0
                
        return 1


    def game_won(self):
        messagebox.showinfo("You won",  "You won")
        




    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        self.field_size=60
        trees=20
        self.size=10

        self.total_size=self.size*self.size
        
        if(trees>((self.size+1)**2)/4):
            trees=int(((self.size+1)**2)/4)

        self.fields=list()
        self.labelsX=list()
        self.labelsY=list()

        loops=0
        max_loops=500

        while(True):
            self.array=['X']*self.total_size
            self.open_f=["x_beg"]*self.total_size
            self.row_count=[0]*self.size
            self.column_count=[0]*self.size
            
            if(self.prepare_game_board(trees)):
                loops+=1
                if(loops>max_loops):
                    trees-=1
                    loops=0
            else:
                break

        self.set_X_on_0_rows_and_columns()

        field=Frame(self, width=self.field_size, height=self.field_size, highlightbackground="black", highlightthickness=1)

        field.grid_rowconfigure(0, weight=1)
        field.grid_columnconfigure(0, weight=1)
        field.grid(row=0,column=0,sticky="nsew")

        for x in range(1,self.size+1):
            field=Frame(self, width=self.field_size, height=self.field_size, background="yellow",highlightbackground="black", highlightthickness=1)
            label=Label(field, text=self.row_count[x-1], bg="yellow", font=("Arial", 20))
            field.grid_rowconfigure(0, weight=1)
            field.grid_columnconfigure(x, weight=1)
            field.grid(row=0,column=x, sticky="nsew")
            label.grid(row=0,column=x)
            self.labelsX.append(label)


        for y in range(1,self.size+1):
            field=Frame(self, width=self.field_size, height=self.field_size, background="yellow",highlightbackground="black", highlightthickness=1)
            field.grid_rowconfigure(y, weight=1)
            field.grid_columnconfigure(0, weight=1)
            label=Label(field, text=self.column_count[y-1], bg="yellow", font=("Arial", 20))
            field.grid(row=y,column=0,sticky="nsew")
            label.grid(row=y,column=0)
            self.labelsY.append(label)

            for x in range(1,self.size+1):
                field=Frame(self, width=self.field_size, height=self.field_size, background="white",highlightbackground="black", highlightthickness=1)
                field.grid_rowconfigure(x, weight=1)
                field.grid_columnconfigure(y, weight=1)
                
                field.grid(row=y,column=x,sticky="nsew" )
                
                cell=(y-1)*self.size+(x-1)
                
                if(self.open_f[cell]=="tree"):
                    image=Image.open("T.png")
                elif(self.open_f[cell]=="x_beg"):
                    image=Image.open("XX.png")
                else:
                    image=Image.open("B.png")
                    
                photo=ImageTk.PhotoImage(image.resize((self.field_size, self.field_size)))
                label=Label(field, image=photo)
                label.image=photo
                label.pack()
                
                label.bind("<Button-1>", lambda event, y=y, x=x: self.left_click(event,x,y))
                label.bind("<Button-3>", lambda event, y=y, x=x: self.right_click(event,x,y))
                
                self.fields.append(label)
                
 
 
 
 

window=Tk()
window.geometry("900x800")
Game(window).pack(expand="True")
window.mainloop()













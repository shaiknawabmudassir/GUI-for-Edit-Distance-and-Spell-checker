from tkinter import *
from tkinter.font import Font
import numpy as np

def updateBox(background, cell, dpTable):
    j,i = cell
    box_size = 50
    padding = 20
    box_gap = 10
    y = (box_gap + box_size)*(j+1) + padding
    x = (box_gap + box_size)*(i+1) + padding
    background.create_rectangle(x, y, x + box_size, y + box_size, fill = '#7d5fff', outline = "")
    text = dpTable[j,i][:-1]
    background.create_text(x+box_size/2, y+box_size/2, text = text, font = textFont)   
    root.update()

def writeInBox(x, y, cell, background):
    background.create_text(x, y, text = cell, font = textFont)
    root.update()

def printEditDistance(dist, background):
    background.create_text(w/2 + 360, h/2 - 300, text = "Total Changes Needed: " + str(dist), font = textFont)
    root.update()

def getInput(str1, str2, str3,):
    s1 = str1.get()
    s2 = str2.get()
    Operation = str3.get()
    if s1 == '' or s2 == '' or Operation == '': 
        screenError = Toplevel(root)
        screenError.geometry("250x90")
        screenError.title("Warning!")
        Label(screenError, text = "Please enter both strings").pack()
        Button(screenError, text = "OK", command = screenError.destroy).pack()
    elif not(Operation == 'yes') and not(Operation == 'no'):
        screenError = Toplevel(root)
        screenError.geometry("250x90")
        screenError.title("Warning!")
        Label(screenError, text = "Please give your Input in Yes or No only.").pack()
        Button(screenError, text = "OK", command = screenError.destroy).pack()
    elif not(s1.isalpha()) or not(s2.isalpha()) or not(Operation.isalpha()):
        screenError = Toplevel(root) 
        screenError.title("Warning!")
        Label(screenError, text = "Input should be Strings only.").pack()
        Button(screenError, text = "OK", command = screenError.destroy).pack()
    else:
        tableCreate(s1.lower(), s2.lower(),Operation.lower())

def DPTable(s1, s2,Operation):
    table = np.zeros([len(s1)+1, len(s2)+1], dtype=np.dtype('U3'))
    for i in range(len(s1)+1):
        table[i,0] = str(i) + 'i'
        
    for j in range(len(s2)+1):
        table[0,j] = str(j) + 'd'
        
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            if s1[i-1] == s2[j-1]:  
                table[i, j] = table[i-1, j-1][:-1] + 'n'
            else:
                if Operation == 'yes':  
                    if min(int(table[i-1, j-1][:-1]), int(table[i-1, j][:-1]), int(table[i, j-1][:-1])) == int(table[i-1, j-1][:-1]):
                        table[i,j] = str(int(table[i-1, j-1][:-1]) + 1) + 'r'
                    elif min(int(table[i-1, j-1][:-1]), int(table[i-1, j][:-1]), int(table[i, j-1][:-1])) == int(table[i, j-1][:-1]):
                        table[i,j] = str(int(table[i, j-1][:-1]) + 1) + 'd'
                    elif min(int(table[i-1, j-1][:-1]), int(table[i-1, j][:-1]), int(table[i, j-1][:-1])) == int(table[i-1, j][:-1]):
                        table[i,j] = str(int(table[i-1, j][:-1]) + 1) + 'i'
                elif Operation == 'no':
                    if min(int(table[i-1, j][:-1]), int(table[i, j-1][:-1])) == int(table[i, j-1][:-1]):
                        table[i,j] = str(int(table[i, j-1][:-1]) + 1) + 'd'
                    elif min(int(table[i-1, j][:-1]), int(table[i, j-1][:-1])) == int(table[i-1, j][:-1]):
                        table[i,j] = str(int(table[i-1, j][:-1]) + 1) + 'i'
    return table

def ChangesInString(s1, s2, table):    
    i = len(s1)
    j = len(s2)
    changes = []  
    path = []
    flag = 0 
    changing_string = list(s2) 
    
    while i >= 0:
        if flag == 1:
            break
        while j >= 0:
            if table[i,j][-1] == 'n':  
                path.append([i,j])
                j-=1
                i-=1
            elif table[i,j][-1] == 'r':  
                statement1 = str(s2[j-1]) + ' changes to ' + str(s1[i-1])
                changing_string[j-1] = s1[i-1]
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                path.append([i,j])
                i-=1
                j-=1
            elif table[i,j][-1] == 'i':
                statement1 = 'Insert ' + str(s1[i-1]) + ' at position ' + str(j+1) + ' in string'
                changing_string.insert(j, s1[i-1])
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                path.append([i,j])
                i-=1
            elif table[i,j][-1] == 'd':
                statement1 = 'Remove ' + str(s2[j-1])
                del changing_string[j-1]
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                path.append([i,j])
                j-=1
            if len(changes) == int(table[len(s1), len(s2)][:-1]):
                flag = 1
                break
    return changes, path


def inputScreen():
    background = Canvas(root, bg = "#DEF9FF", width = w, height = h)
    background.grid(row=0, column=0)
    background.create_text(w/2, h/2 - 375, text = "Team - 13", font = headingFont)
    background.create_text(w/2, h/2 - 300, text = "Edit Distance Uisng Dymanic Programing", font = headingFont)
    background.create_text(w/2 - 310, h/2 - 200, text = "Enter the original string: ", font = textFont)
    str1 = Entry(background)
    background.create_window(w/2 + 120, h/2 - 200, window = str1, width = w/4)

    background.create_text(w/2 - 250, h/2 - 100, text = "Enter the string you want to change: ", font = textFont)
    str2 = Entry(background)
    background.create_window(w/2 + 120, h/2 - 100, window = str2, width = w/4)
    
    background.create_text(w/2 - 260, h/2 , text = "Do you want Substitution Operation : ", font = textFont)
    str3 = Entry(background)
    background.create_window(w/2 + 120, h/2 , window = str3, width = w/4)
    
    b1 = Button(background, text = "Enter", bg = '#84A3FF', activebackground = '#FFE5CC', command=lambda:getInput(str1, str2,str3))
    background.create_window(w/2 , h/2 + 100, window = b1, width = w/8)

def tableCreate(s1, s2, Operation):
    background = Canvas(root, bg = "#DEF9FF", width = w, height = h)
    background.grid(row=0, column=0)
    box_size = 50
    box_gap = 10
    table_width = len(s1) + 2
    table_height = len(s2) + 2
    padding = 20
    animation_gap = 100

    for i in range(table_height):
        for j in range(table_width):
            if (i,j) == (0,0) or (i,j) == (1,0) or (i,j) == (0,1):
                continue
            else:
                x = (box_gap + box_size)*i + padding
                y = (box_gap + box_size)*j + padding
                background.create_rectangle(x, y, x + box_size, y + box_size, fill = '#9fe9fa', outline = "")

    for i in range(table_height-2):
        x = (box_gap + box_size)*(i+2) + padding + box_size/2
        background.create_text(x, padding + box_size/2, text = s2[i].upper(), font = textFont)

    for i in range(table_width-2):
        y = (box_gap + box_size)*(i+2) + padding + box_size/2
        background.create_text(padding + box_size/2, y, text = s1[i].upper(), font = textFont)

    background.update()

    dpTable = DPTable(s1, s2, Operation) 
    for i in range(dpTable.shape[0]):
        for j in range(dpTable.shape[1]):
            if i == 0 or j == 0:
                x = (box_gap + box_size)*(j+1) + padding + box_size/2
                y = (box_gap + box_size)*(i+1) + padding + box_size/2
                cell = dpTable[i,j][:-1]
                background.create_text(x, y, text = cell, font = textFont)

    for i in range(dpTable.shape[0]):
        for j in range(dpTable.shape[1]):
            if not(i == 0 or j == 0):
                x = (box_gap + box_size)*(j+1) + padding + box_size/2
                y = (box_gap + box_size)*(i+1) + padding + box_size/2
                cell = dpTable[i,j][:-1]
                background.after(animation_gap, writeInBox(x,y,cell,background))

    printEditDistance(dpTable[table_width-2, table_height-2][:-1], background)

    b3 = Button(background, text = "Show Changes in Detail", bg = '#84A3FF', activebackground = '#FFE5CC', command=lambda:displayChangeList(background, dpTable, s1, s2, button, animation_gap))
    button = background.create_window(w/2 + 340, h/2 - 60, window = b3, width = w/8)

def displayChangeList(background, dpTable, s1, s2,  b3, animation_gap):
    background.delete(b3)
    background.update()
    changes, path = ChangesInString(s1,s2,dpTable)
    for cell in path:
        background.after(animation_gap, updateBox(background, cell, dpTable))

    if len(changes) == 0: #
        background.create_text(w/2 + 350, h/2 - 30, text = "The strings are same, so no changes.", font = smallTextFont)
        i=1
    else:
        background.create_text(w/2 + 350, h/2 - 30, text = "The changes to be made in '" + s2 + "' are:", font = textFont)
        for i in range(len(changes)):
            statement = str(i+1) + ". " + changes[i][0] + '. ' + changes[i][1]
            background.create_text(w/2 + 370, h/2 + i*30, text = statement, font = smallTextFont)
        i+=1
    b2 = Button(background, text = "Enter Another String", bg = '#84A3FF', activebackground = '#FFE5CC', command=inputScreen)
    background.create_window(w/2 + 250, h/2 + i*32, window = b2, width = w/8)

    b3 = Button(background, text = "Quit", bg = '#84A3FF', activebackground = '#FFE5CC', command=lambda:root.destroy())
    background.create_window(w/2 + 450, h/2 + i*32, window = b3, width = w/8)


if __name__ == "__main__":
    root = Tk()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.geometry("%dx%d" % (w, h))
    root.title("Edit Distance")
    smallTextFont = Font(family = 'Bookman Old Style', size = '12')
    textFont = Font(family = 'Bookman Old Style', size = '15')
    headingFont = Font(family = 'Bookman Old Style', size = '30')
    inputScreen()
    
    root.mainloop()

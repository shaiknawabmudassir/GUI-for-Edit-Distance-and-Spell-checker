from tkinter import *
from tkinter.font import Font

def getInput(str1):
    s1 = str1.get()
    if s1 == '': 
        screenError = Toplevel(root)
        screenError.geometry("250x90")
        screenError.title("Warning!")
        Label(screenError, text = "Please enter the strings").pack()
        Button(screenError, text = "OK", command = screenError.destroy).pack()  
    elif not(s1.isalpha()):
        screenError = Toplevel(root)
        screenError.geometry("250x90")
        screenError.title("Warning!")
        Label(screenError, text = "Input should be Strings only.").pack()
        Button(screenError, text = "OK", command = screenError.destroy).pack()
    else:
        displaypossiblewords(s1.lower())
        
def editDP(s1, s2):
    len1 = len(s1)
    len2 = len(s2)
    dp = [[0 for i in range(len2 + 1)] for j in range(len1 + 1)]
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if s2[j - 1] == s1[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1], dp[i - 1][j - 1],dp[i - 1][j])
    return dp[i][j]

def inputScreen():
    background = Canvas(root, bg = "#DEF9FF", width = w, height = h)
    background.grid(row=0, column=0)
    background.create_text(w/2, h/2 - 375, text = "Team - 13", font = headingFont)
    background.create_text(w/2, h/2 - 300, text = "Spell checker", font = headingFont)
    background.create_text(w/2, h/2 - 200, text = "(Enter the word in the box given below it will give the possible corrected words for that)", font = textFont)
    background.create_text(w/2 - 310, h/2 - 100, text = "Enter the word: ", font = textFont)
    str1 = Entry(background)
    background.create_window(w/2 , h/2 - 100, window = str1, width = w/4)
    
    b1 = Button(background, text = "Enter", bg = '#84A3FF', activebackground = '#FFE5CC', command=lambda:getInput(str1))
    background.create_window(w/2 - 300 , h/2 + 100, window = b1, width = w/8)
    b2 = Button(background, text = "Quit", bg = '#84A3FF', activebackground = '#FFE5CC', command=lambda:root.destroy())
    background.create_window(w/2 + 100 , h/2 + 100, window = b2, width = w/8)
    return background
def spell_check(string):
    f = open("dict.txt", "r")
    lines=f.readlines()
    f.close()
    results = []
    for i in lines:
        word=editDP(string,i.strip())
        if word<=1:
            results.append([i.strip()])
    return results

def displaypossiblewords(string):
    background = inputScreen()
    background.create_text(w/2 + 450, h/2 - 30, text = "Possible corrected words for " + string  + " are:", font = textFont)
    changes = spell_check(string)
    for i in range(len(changes)):
        statement =  changes[i]
        background.create_text(w/2 + 450, h/2 + i*30, text = statement, font = smallTextFont)
    i+=1



if __name__ == "__main__":
    root = Tk()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.geometry("%dx%d" % (w, h))
    root.title("Spell checker")
    smallTextFont = Font(family = 'Bookman Old Style', size = '12')
    textFont = Font(family = 'Bookman Old Style', size = '15')
    headingFont = Font(family = 'Bookman Old Style', size = '30')
    inputScreen()
    root.mainloop()

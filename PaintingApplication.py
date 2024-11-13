from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import json
import math
import random
from copy import deepcopy

erase = False

image = {"canvas": "", "data":{}}
undoDic = {"canvas": "", "data":{}}

saved = True

window = Tk()
window.geometry('1000x600+100+0')
window.config(bg="#d2c3b3")

oldMousePosition = [-1, -1]
mousePosition = [0, 0]
isMouseDown = False
isCanvasReady = False
w, h = 0, 0
canvas = Canvas(window, width = 0, height = 0, borderwidth=0, highlightthickness=0)

title = Label(window, text = 'Generic, Off Brand Paint Application',font=('arial', 35),bg="#d2c3b3")
title.place(x=125,y=40)

widthLabel = Label(window, text = "Width: ",font=('arial',15),bg="#d2c3b3")
widthLabel.place(x=225,y=300)
wEntry = Entry(window,font=('arial',15),bg="#e2d5c7")
wEntry.place(x=325,y=300)
wEntry.insert(0,'620')

heightLabel = Label(window, text = "Height: ",font=('arial',15),bg="#d2c3b3")
heightLabel.place(x=225,y=400)
hEntry = Entry(window,font=('arial',15),bg="#e2d5c7")
hEntry.place(x=325,y=400)
hEntry.insert(0,'620')

def clear():
    errLabel.config(text="")
    wEntry.delete(0,END)
    hEntry.delete(0,END)
def define(number):
    clear()
    pairs = [[464, 620], [620, 620], [620, 464]]
    wEntry.insert(0,str(pairs[number-1][0]))
    hEntry.insert(0,str(pairs[number-1][1]))
def ranGen():
    global h
    global w
    h = str(random.randint(200,640))
    w = str(random.randint(200,640))
    clear()
    wEntry.insert(0,w)
    hEntry.insert(0,h)

presetRegular = Button(window,text='620x464',command= lambda: define(3),font=('arial',15),bg="#bfb8b0")
presetRegular.place(x=50,y=245) 

presetSquare = Button(window,text='620x620',command= lambda: define(2),font=('arial',15),bg="#bfb8b0")
presetSquare.place(x=50,y=345) 

presetLetter = Button(window,text='464x620',command= lambda: define(1),font=('arial',15),bg="#bfb8b0")
presetLetter.place(x=50,y=445)

ranButt = Button(window,text='Random',command=ranGen,font=('arial',15),bg="#bfb8b0")
ranButt.place(x=600,y=345)

clearButt = Button(window,text='Clear',command=clear,font=('arial',15),bg="#bfb8b0")
clearButt.place(x=713,y=345) 

errLabel = Label(window, text = '', font=('arial',15),bg="#d2c3b3") #only for pg1
errLabel.place(relx=.5, y=500, anchor = CENTER)

#---
#Here lie all the widgets/functions for the drawing screen         

drawColor = 'black'
brushSize = 5

colLabelText = Label(window, text = 'Color:', bg='#d2c3b3',font=('arial',15))
colLabel = Label(window, text='', height = 2, width = 5, bg='black')
colEntry = Entry(window, bg='#e2d5c7',font=('arial',15),width = 10)

track = 'black'
def colorChange():
    try:
        errLabel.config(text="")
        global track
        global drawColor
        track = drawColor
        drawColor = colEntry.get()
        drawColor = drawColor.strip()
        if drawColor == '':
            drawColor = 'black'
        colLabel.config(bg=drawColor)
    except:
        errLabel.config(text='Color not recognized.\nTry again.')
        drawColor = track
        colLabel.config(bg=track)

colButton = Button(window,text='Change Color', command = colorChange,font=('arial',15),bg='#d2c3b3')

def toggleErase():
    global erase
    if erase:
        erase = False
        eraseButton.config(bg='#d2c3b3')
    else:
        erase = True
        eraseButton.config(bg='#bfb8b0')

eraseButton = Button(window, text = 'Eraser', command=toggleErase, font=('arial',15),bg="#d2c3b3")

def bSizeUp():
    global brushSize
    if brushSize == 9:
        bSizeLabel.place_forget()
        bSizeLabel.place(x = 60, y = 265)
    if brushSize < 20:
        brushSize += 1
        bSizeLabel.config(text=str(brushSize))
def bSizeDown():
    global brushSize
    if brushSize == 10:
        bSizeLabel.place_forget()
        bSizeLabel.place(x = 67, y = 265)
    if brushSize > 1:
        brushSize -= 1
        bSizeLabel.config(text=str(brushSize))
bSizeLabel = Label(window, text = '5', bg='#d2c3b3',font=('arial',15))
bSizeUpBttn = Button(window, text = '+', command=bSizeUp, font=('arial',15),bg="#d2c3b3") 
bSizeDownBttn = Button(window, text = '-', command=bSizeDown, font=('arial',15),bg="#d2c3b3")

def undo():
    global image
    image = deepcopy(undoDic)
    render()
undoButton = Button(window, text = 'Undo', command=undo, font=('arial',15),bg="#d2c3b3")

def clearCanvas():
    global image
    answer = messagebox.askyesno("Clear Canvas", "Are you sure you want to clear the entire canvas?")
    if answer == True:
        image['data'] = {}
        render()

clearCanvasButton = Button(window,text='Clear Canvas', command = clearCanvas,font=('arial',15),bg='#d2c3b3')

def saveFunc():
    try:
        global saved
        file = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
        if file == None:
            return
        imageData = json.dumps(image)
        file.write(imageData)
        file.close()
        saved = True
        messagebox.showinfo("Saved", "File saved successfully!")
    except Exception as e:
        errLabel.config(text=f"ERROR: {e}")

saveButton = Button(window, text = 'Save', command = saveFunc,font=('arial',15),bg='#d2c3b3')

def closeWindow():
    global isCanvasReady
    global saved
    if (not saved) and isCanvasReady and image['data'] != {}:
        answer = messagebox.askyesno("Unsaved Changes", "You have unsaved changes, are you sure you want to quit?")
        if answer == True:
            window.destroy()
    else:
        window.destroy()

#---

def updateWindow():
    try:
        global isCanvasReady
        global h
        global w
        w = int(wEntry.get()) 
        h = int(hEntry.get())
        if w > 640 or h > 640 or w < 200 or h < 200:
            errLabel.config(text="Max width/height is 640. Min width/height is 200.")
        else:
            errLabel.config(text="")
            presetLetter.place_forget()
            presetSquare.place_forget()
            presetRegular.place_forget()
            widthLabel.place_forget()
            heightLabel.place_forget()
            title.place_forget()
            clearButt.place_forget()
            ranButt.place_forget()
            hEntry.place_forget()
            wEntry.place_forget()
            errLabel.place_forget()
            loadButton.place_forget()
            generateScreen.place_forget()
            canvas.config(background="white")
            canvas.config(width=w,height=h)
            image["canvas"] = f"{w}x{h}"
            temp_h = h
            temp_h = 300 if temp_h < 300 else temp_h
            window.geometry(str(w + 260)+'x'+str(temp_h + 20)+'+100+0') 
            errLabel.place(x = 125, y = 107, anchor = N) 
            colLabelText.place(x=20, y = 165) #Color:
            colEntry.place(x=90, y = 165)
            colLabel.place(x = 175, y = 207)
            colButton.place(x=20, y = 205)
            bSizeDownBttn.place(x = 27, y = 260)
            bSizeLabel.place(x = 67, y = 265)
            bSizeUpBttn.place(x = 97, y = 260)
            eraseButton.place(x = 150, y = 260)
            clearCanvasButton.place(x=160, y = 10, anchor = N)
            saveButton.place(x=20 , y = 10)
            undoButton.place(x = 93, y = 60)
            
            isCanvasReady = True
    except:
        errLabel.config(text='Please input a height and width.') 

def loadFunc():
    try:
        global image
        global undoDic
        filename = filedialog.askopenfilename(initialdir="/",title="Select file",filetypes=(("*.txt", "*.txt*"), ("all files", "*.*")))
        if filename == "":
            return
        with open(filename, 'r') as file:
            text = file.read()
            image = json.loads(text)
            undoDic = json.loads(text)
            imageWidth, imageHeight = image['canvas'].split('x')
            clear()
            wEntry.insert(0, imageWidth)
            hEntry.insert(0, imageHeight)
            updateWindow()
            render()
    except Exception as e:
        errLabel.config(text=e)

loadButton = Button(window, text = 'Load', font=('arial',15),bg="#bfb8b0", command=loadFunc)
loadButton.place(x = 800, y = 345)

generateScreen = Button(window,text='Start',command=updateWindow,font=('arial',15),bg="#bfb8b0")
generateScreen.place(x=885,y=345)

def render():
    canvas.delete("all")
    imageWidth, imageHeight = image['canvas'].split("x")
    canvas.config(width=imageWidth, height=imageHeight)
    for x, pixels in image['data'].items():
        for y, color in pixels.items():
            x, y = int(x), int(y)
            canvas.create_rectangle(x, y, x, y, fill=color, outline="")
            
def copy4Undo():
    global undoDic
    #global image
    undoDic = deepcopy(image)
    
def mouseDown(event):
    global isMouseDown
    copy4Undo()
    isMouseDown = True
def mouseUp(event):
    global isMouseDown
    global image
    render()
    isMouseDown = False
    
def motion(event):
    global mousePosition
    global oldMousePosition
    oldMousePosition = mousePosition
    mousePosition = [event.x, event.y]

def paint(x, y, bSize):   #Saves the x,y coordinates of what was drawn/erased and stores them in a dictionary for rendering
    global erase
    for a in range(bSize):
        for b in range(bSize):
            aa = (x-math.floor(bSize/2))+a
            bb = (y-math.ceil(bSize/2))+b
            if erase:
                if ((image['data'].get(str(aa), None) == None) or (image['data'][str(aa)].get(str(bb), None) == None)) == False:
                    del image['data'][str(aa)][str(bb)]
            else:
                if image['data'].get(str(aa), None) == None:
                    image['data'][str(aa)] = {}
                image['data'][str(aa)][str(bb)] = drawColor

def draw(x, y, bSize): #Places the temporary tkinter rectangles
    global oldMousePosition
    global erase
    if oldMousePosition[0] == -1: 
        paint(x, y, bSize)
        a = x-math.floor(bSize/2)
        b = y-math.ceil(bSize/2)
        c = x+math.floor(bSize/2)
        d = y+math.ceil(bSize/2)
        if erase:
            canvas.create_rectangle(a, b, c, d, fill='white', outline="")
        else:
            canvas.create_rectangle(a, b, c, d, fill=drawColor, outline="")
    else:
        for i in range(100): #anything higher than 100, and the algorithm gets "too excited", jumping ahead the faster you draw
            xx = math.floor(oldMousePosition[0] + (x - oldMousePosition[0])*(i/100))
            yy = math.floor(oldMousePosition[1] + (y - oldMousePosition[1])*(i/100))
            a = xx-math.floor(bSize/2)
            b = yy-math.ceil(bSize/2)
            c = xx+math.ceil(bSize/2)
            d = yy+math.floor(bSize/2)
            if erase:
                canvas.create_rectangle(a, b, c, d, fill='white', outline="")
            else:
                canvas.create_rectangle(a, b, c, d, fill=drawColor, outline="")
            paint(xx, yy, bSize)

def update():
    global saved
    x, y = mousePosition[0], mousePosition[1]
    if isMouseDown and (x > 0 and x < w and y > 0 and y < h):
        
        saved = False
        draw(x, y, brushSize)

    window.after(1, update)

canvas.bind("<Button-1>", mouseDown)
canvas.bind("<ButtonRelease-1>", mouseUp)
canvas.bind("<Motion>", motion)
canvas.focus_set()
canvas.place(x=250,y=10)
window.after(1, update)

window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", closeWindow)

window.mainloop()

from cmu_graphics import *
from PIL import Image
import os, pathlib
import math
import random

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

def onAppStart(app):
    app.marioTitle = openImage("C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\MarioPeaceTitle.png")
    marioTitleWidth, marioTitleHeight = app.marioTitle.size
    app.marioTitle = app.marioTitle.resize((marioTitleWidth//4, marioTitleHeight//4))
    app.marioTitle = CMUImage(app.marioTitle)
    app.isOnTitleScreen = True
    app.otherScreen = False

def redrawAll(app):
    if app.isOnTitleScreen == True:
        drawRect(0,0, app.width, app.height, fill = 'blue')
        drawImage(app.marioTitle, app.width//2 + 20, app.height//2, align = 'center')
        drawLabel('WELCOME TO SUPER MARIO BROS 4.5!', app.width//2, app.height//2 - 200, size = 22, bold = True)
        drawLabel('PRESS Z TO START', app.width//2, app.height//2 + 200, size = 22, bold = True)
    elif app.otherScreen == True:
        drawRect(19, 19, 19, 19, fill = 'black')

def onKeyPress(app, key):
    if app.isOnTitleScreen == True:     
        if key == 'z':
            app.isOnTitleScreen = False
            app.otherScreen = True

def main():
    runApp(width=700, height=500)

if __name__ == '__main__':
    main()
    # newX1 = x1 + width1//2
    # newY1 = y1 + height1//2
    # newX2 = x2 + width2//2
    # newY2 = y2 + height1//2

    # bottom1 = newY1 + height1
    # bottom2 = newY2 + height2
    # right1 = newX1 + width1
    # right2 = newX2 + width2

    # if (bottom1 >= y2 and bottom2 >= y1 and right1 >= x2 and right2 >= x1):
    #     return 'grouned'

from cmu_graphics import *


def onAppStart(app):
    app.rectLeft1 = 90
    app.rectTop1 = 50
    app.width1, app.height1 = 60, 60

    app.newX1 = app.rectLeft1 - app.width1//2
    app.newY1 = app.rectTop1 - app.height1//2



def redrawAll(app):
    drawRect(app.newX1, app.newY1, app.width1, app.height1, fill = 'red')
    drawRect(app.rectLeft1, app.rectTop1, app.width1, app.height1, fill = 'blue', align = 'center')


      


runApp(width = 600, height = 600)
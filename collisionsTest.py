from cmu_graphics import *

def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

def testCollision(app):
    if abs(app.rectTop1 - app.rectTop2) <= 180 and ((app.rectLeft2 - 150 <= app.rectLeft1 + 30 <= app.rectLeft2 + 150) or (app.rectLeft2 - 150 <= app.rectLeft1 - 30 <= app.rectLeft2 + 150)):
        return 'grouned'

def onAppStart(app):
    app.rectLeft1 = 90
    app.rectTop1 = 50
    app.rectLeft2 = 200
    app.rectTop2 = 300

def onKeyHold(app, keys):
    if 'right' in keys:
        app.rectLeft1 += 1
    elif 'left' in keys:
        app.rectLeft1 -= 1
    elif 'up' in keys:
        app.rectTop1 -= 1
    elif 'down' in keys:
        app.rectTop1 += 1

def onStep(app):

    if testCollision(app) != 'grouned':
        app.rectTop1 += 5

def redrawAll(app):
    drawRect(app.rectLeft1, app.rectTop1, 60, 60, fill = 'blue', align = 'center')
    drawRect(app.rectLeft2, app.rectTop2, 300, 300, fill = 'red', align = 'center')
    drawCircle(app.rectLeft1, app.rectTop1, 4)
    drawCircle(app.rectLeft2, app.rectTop2, 4)


      


runApp(width = 600, height = 600)
from cmu_graphics import *

def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

def testCollision(app):
    if abs(app.rectTop1 - app.rectTop2) <= 180 and ((app.rectLeft2 - 150 <= app.rectLeft1 + 30 <= app.rectLeft2 + 150) or (app.rectLeft2 - 150 <= app.rectLeft1 - 30 <= app.rectLeft2 + 150)):
        print('gotinside')
        return 'grouned'

def onAppStart(app):
    app.rectLeft1 = 90
    app.rectTop1 = 50
    app.dy = -4
    app.ddy = 0.12
    app.isJumpingUp = False
    app.isJumpingRight = False
    app.isMovingAtAll = False
    app.rectLeft2 = 200
    app.rectTop2 = 300

def onKeyHold(app, keys):
    # print(keys)
    if 'right' in keys:
        app.isMovingAtAll = True
        app.rectLeft1 += 8
    elif 'left' in keys:
        app.isMovingAtAll = True
        app.rectLeft1 -= 8
    elif 'up' in keys and 'right' not in keys and 'left' not in keys and testCollision(app) == 'grouned':
        app.isMovingAtAll = True
        print('in first testCase')
        # app.rectTop1 -= 1
        app.isJumpingUp = True
    elif 'up' in keys and testCollision(app) == 'grouned':
        app.isMovingAtAll = True
        print('in second testCase')
        # app.rectLeft1 += 8
        app.isJumpingRight = True

    elif 'down' in keys:
        app.rectTop1 += 1

def onKeyRelease(app, key):
    if key == 'up' and testCollision(app) == 'grouned':
        app.isJumpingUp = False
        app.isJumpingRight = False


def onStep(app):
    if testCollision(app) != 'grouned' and app.isMovingAtAll == False:
        app.rectTop1 += 5
    elif testCollision(app) != 'grouned' :
        app.dy = 0

    

def redrawAll(app):
    drawRect(app.rectLeft1, app.rectTop1, 60, 60, fill = 'blue', align = 'center')
    drawRect(app.rectLeft2, app.rectTop2, 300, 300, fill = 'red', align = 'center')
    drawCircle(app.rectLeft1, app.rectTop1, 4)
    drawCircle(app.rectLeft2, app.rectTop2, 4)


      


runApp(width = 600, height = 600)
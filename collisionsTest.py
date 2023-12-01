from cmu_graphics import *

def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

# def testCollision(app):
#     # print(f'app.rectTop1 - app.rectTop2 = {abs(app.rectTop1 - app.rectTop2)}')
#     # print(f'app.rectLeft2 - 150 = {app.rectLeft2 - 150}')
#     # print(f'app.rectLeft1 + 30 = {app.rectLeft1 + 30}')
#     # print(f'app.rectLeft2 + 150 = {app.rectLeft2 + 150}')
#     # print(f'app.rectLeft2 - 150 = {app.rectLeft2 - 150}')
#     # print(f'app.rectLeft1 - 30 = {app.rectLeft1 - 30}')
#     # print(f'app.rectLeft2 + 150 = {app.rectLeft2 + 150}')
#     if abs(app.rectTop1 - app.rectTop2) <= 180 and ((app.rectLeft2 - 150 <= app.rectLeft1 + 30 <= app.rectLeft2 + 150) or (app.rectLeft2 - 150 <= app.rectLeft1 - 30 <= app.rectLeft2 + 150)):
#         return 'grouned'


def testCollision(app, x1, y1, x2, y2, width1, height1, width2, height2):
    newX1 = x1 - width1//2
    newY1 = y1 - height1//2
    newX2 = x2 - width2//2
    newY2 = y2 - height2//2

    bottom1 = newY1 + height1
    bottom2 = newY2 + height2
    right1 = newX1 + width1
    right2 = newX2 + width2

    if (bottom1 >= newY2 and bottom2 >= newY1 and right1 >= newX2 and right2 >= newX1):
        return 'grouned'
    

def onAppStart(app):
    app.rectLeft1 = 90
    app.rectTop1 = 120
    app.width1, app.height1 = 60, 60

    app.rectLeft2 = 200
    app.rectTop2 = 300
    app.width2, app.height2 = 300, 300

    app.dy = -4
    app.ddy = 0.12
    app.jumpingdx = 4
    app.isJumpingUp = False
    app.isJumpingRight = False
    app.isJumpingLeft = False
    app.isMovingAtAll = False
    app.rectColor = 'red'


def onKeyHold(app, keys, modifiers):
    if 'right' in keys:
        app.isMovingAtAll = True
        app.rectLeft1 += 4
    if 'right' in keys and 'control' in modifiers:
        app.isMovingAtAll = True
        app.rectLeft1 += 4
    elif 'left' in keys:
        app.isMovingAtAll = True
        app.rectLeft1 -= 4
    # elif 'up' in keys and 'right' not in keys and 'left' not in keys and testCollision(app) == 'grouned':
    elif 'up' in keys and 'right' not in keys and 'left' not in keys and testCollision(app, app.rectLeft1, app.rectTop1, app.rectLeft2, app.rectTop2, app.width1, app.height1, app.width2, app.height2) == 'grouned':
        app.isMovingAtAll = True
        print('in first testCase')
        # app.rectTop1 -= 1
        app.isJumpingUp = True
        app.dy = -4
        app.ddy = 0.12
        app.rectColor = 'red'
    # elif 'up' in keys and 'right' in keys and testCollision(app) == 'grouned':
    elif 'up' in keys and 'right' in keys and 'left' not in keys and testCollision(app, app.rectLeft1, app.rectTop1, app.rectLeft2, app.rectTop2, app.width1, app.height1, app.width2, app.height2) == 'grouned':
        app.isMovingAtAll = True
        app.isJumpingRight = True
        print('in second testCase')
        # app.rectLeft1 += 8
        app.isJumpingRight = True
        app.dy = -4
        app.ddy = 0.12
        app.jumpingdx = 4
        app.rectColor = 'red'
    
    elif 'up' in keys and 'left' in keys and 'right' not in keys and testCollision(app, app.rectLeft1, app.rectTop1, app.rectLeft2, app.rectTop2, app.width1, app.height1, app.width2, app.height2) == 'grouned':
        print('in third case')
        app.isMovingAtAll = True
        app.isJumpingLeft = True
        app.dy = -8
        app.ddy = 0.12
        app.jumpingdx = 4
        app.rectColor = 'red'

    elif 'down' in keys:
        app.rectTop1 += 1

def onKeyRelease(app, key):
    # if key == 'up' and testCollision(app) == 'grouned':
    if key == 'up' or key == 'right' or key == 'left':
        app.isJumpingUp = False
        app.isJumpingRight = False
        app.isJumpingLeft = False




def onStep(app):
    if testCollision(app, app.rectLeft1, app.rectTop1, app.rectLeft2, app.rectTop2, app.width1, app.height1, app.width2, app.height2) != 'grouned':
        app.rectColor = 'green'
    elif testCollision(app, app.rectLeft1, app.rectTop1, app.rectLeft2, app.rectTop2, app.width1, app.height1, app.width2, app.height2) == 'grouned':
        app.rectColor = 'red'
    if app.isJumpingUp == True:
        app.rectTop1 += app.dy
        app.dy += app.ddy
        if app.dy <= 0:
            app.rectColor = 'green'
        # if testCollision(app) == 'grouned':
        if testCollision(app, app.rectLeft1, app.rectTop1, app.rectLeft2, app.rectTop2, app.width1, app.height1, app.width2, app.height2) == 'grouned':
            app.dy = 0 
            app.ddy = 0
            app.isJumpingUp = False
    else:
        if testCollision(app, app.rectLeft1, app.rectTop1, app.rectLeft2, app.rectTop2, app.width1, app.height1, app.width2, app.height2) != 'grouned':
            app.rectTop1 += 5

    

def redrawAll(app):
    drawRect(app.rectLeft1, app.rectTop1, 60, 60, fill = app.rectColor, align = 'center')
    drawRect(app.rectLeft2, app.rectTop2, 300, 300, fill = 'red', align = 'center')
    drawCircle(app.rectLeft1, app.rectTop1, 4)
    drawCircle(app.rectLeft2, app.rectTop2, 4)


      


runApp(width = 600, height = 600)
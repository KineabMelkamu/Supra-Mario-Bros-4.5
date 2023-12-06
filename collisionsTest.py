from cmu_graphics import *

def testCollision(app, x1, y1, x2, y2, width1, height1, width2, height2):
    newX1 = x1 - width1//2
    newY1 = y1 - height1//2
    newX2 = x2 - width2//2
    newY2 = y2 - height2//2

    bottom1 = newY1 + height1
    bottom2 = newY2 + height2
    right1 = newX1 + width1
    right2 = newX2 + width2

    if (bottom1 + 3 >= newY2 and bottom2 + 3 >= newY1 and right1 + 3 >= newX2 and right2 + 3 >= newX1):
        return 'grouned'
    

def onAppStart(app):
    app.rectLeft1 = 90
    app.rectTop1 = 120
    app.width1, app.height1 = 60, 60

    app.rectLeft2 = 200
    app.rectTop2 = 300
    app.width2, app.height2 = 300, 300

    app.dy = -6
    app.ddy = 0.3
    app.jumpingdx = 4
    app.jumpingdy = 3
    app.isJumpingUp = False
    # app.isJumpingRight = False
    # app.isJumpingLeft = False
    # app.isMovingAtAll = False
    app.rectColor = 'blue'


def onKeyHold(app, keys, modifiers):
    if 'right' in keys:
        app.rectLeft1 += 4
        app.jumpingdy = 3
    if 'right' in keys and 'control' in modifiers:
        app.rectLeft1 += 4
        app.jumpingdy = 3
    elif 'left' in keys:
        app.isMovingAtAll = True
        app.rectLeft1 -= 4
        app.jumpingdy = 3
    elif 'up' in keys and 'right' not in keys and 'left' not in keys and testCollision(app, app.rectLeft1, app.rectTop1, app.rectLeft2, app.rectTop2, app.width1, app.height1, app.width2, app.height2) == 'grouned':
        app.isJumpingUp = True
        app.dy = -6
        app.ddy = 0.3
        app.jumpingdy = 3
    elif 'down' in keys:
        app.rectTop1 += 1

def onStep(app):
    if testCollision(app, app.rectLeft1, app.rectTop1, app.rectLeft2, app.rectTop2, app.width1, app.height1, app.width2, app.height2) != 'grouned' and app.isJumpingUp == False:
        app.rectColor = 'green'
        app.rectTop1 += app.jumpingdy
        app.jumpingdy += app.ddy
        if app.jumpingdy <= 0:
            app.rectColor = 'blue'
        if testCollision(app, app.rectLeft1, app.rectTop1, app.rectLeft2, app.rectTop2, app.width1, app.height1, app.width2, app.height2) == 'grouned':
            app.dy = 0 
            app.ddy = 0
            app.isJumpingUp = False
    elif testCollision(app, app.rectLeft1, app.rectTop1, app.rectLeft2, app.rectTop2, app.width1, app.height1, app.width2, app.height2) == 'grouned':
        app.rectColor = 'yellow'
    if app.isJumpingUp == True:
        app.rectTop1 += app.dy
        app.dy += app.ddy
        if app.dy <= 0:
            app.rectColor = 'blue'
        if testCollision(app, app.rectLeft1, app.rectTop1, app.rectLeft2, app.rectTop2, app.width1, app.height1, app.width2, app.height2) == 'grouned':
            app.dy = 0 
            app.ddy = 0
            app.isJumpingUp = False

    

def redrawAll(app):
    drawRect(app.rectLeft2, app.rectTop2, 300, 300, fill = 'red', align = 'center')
    drawRect(app.rectLeft1, app.rectTop1, 60, 60, fill = app.rectColor, align = 'center')
    drawCircle(app.rectLeft1, app.rectTop1, 4)
    drawCircle(app.rectLeft2, app.rectTop2, 4)


      


runApp(width = 600, height = 600)
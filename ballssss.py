from cmu_graphics import *
import math



def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

class Ball:
    def __init__(self, x, y):
        #Position
        self.x = x
        self.y = y


        #Velocity
        self.isMovingInX = False
        self.isMovingInY = False
        self.gotToClimaxJump = False
        self.dx = 5
        self.jumpingDx = 2
        self.defaultDx = 5
        self.dy = -6
        self.defaultDy = -6

        #Acceleration
        self.ddx = 0.2

        #misc 
        self.color = 'red'
        self.isJumpingRight = False
        self.isJumpingLeft = False

    def draw(self):
        drawCircle(self.x, self.y, 20, fill = self.color)
        drawRect(self.x, self.y, 40, 40, fill = None, border = 'red', align = 'center')

    def step(self):
        #Integrate position and velocity
        if testCollison(self) != 'grounded':
            self.y += 5

        if self.isMovingInX and not self.isMovingInY :
            self.dx += self.ddx
            print(f'on step for x: x = {self.dx}, y = {self.dy}')
            
        elif self.isMovingInY and not self.isMovingInX:
            self.dy += self.ddy
            if rounded(self.dy) == 0:
                self.color = 'blue'

            print(f'on step for Y: x = {self.dx}, y = {self.dy}')
        
        elif self.isMovingInX and self.isMovingInY:
            print(f'on step for elif other: x = {self.dx}, y = {self.dy}')
            self.dx += self.ddx
            self.dy += self.ddy
            if rounded(self.dy) == 0:
                self.color = 'blue'

        self.dx = self.defaultDx
        self.dy = self.defaultDy


        
    def ballKeyHold(self, keys):
        if 'right' in keys and 'up' not in keys and 'left' not in keys:
            self.isMovingInX = True
            self.x += self.dx
            # print(self.dx)
        elif 'left' in keys and 'up' not in keys and 'right' not in keys:
            self.isMovingInX = True
            self.x -= self.dx
            # print(self.dx)
        elif 'up' in keys and 'right' in keys and 'left' not in keys and testCollison(self) == 'grounded':
            self.isJumpingRight = True
            self.isMovingInY = not self.isMovingInY
            self.isMovingInX = not self.isMovingInX
            self.y += self.dy
            self.x += self.jumpingDx
        elif 'up' in keys and 'left' in keys and 'right' not in keys and testCollison(self) == 'grounded':
            self.isJumpingLeft = True
            print('got inside el oh el')
            self.isMovingInY = not self.isMovingInY
            self.isMovingInX = not self.isMovingInX
            self.y += self.dy
            self.x -= self.jumpingDx


        elif 'up' in keys and testCollison(self) == 'grounded':
            self.isMovingInY = True
            self.y += self.dy


        
    
    def ballKeyRelease(self, key):
        if key == 'right':
            self.isMovingInX = False
            self.dx = self.defaultDx
        elif key == 'left':
            self.isMovingInX = False
            self.dx = self.defaultDx
        elif key == 'up':
            self.isMovingInY = False
            self.color = 'red'
            self.dy = self.defaultDy
    
    def ballKeyPress(self, key):
        if key == 'p':
            self.x = 20
            self.y = 380
            self.isMovingInX = False
            self.isMovingInY = False
            self.dx = self.defaultDx
            self.dy = self.defaultDy



#---Animation functions---------------------------------

def onAppStart(app):
    app.ball = Ball(20, 380)
    app.rectX = 0
    app.rectY = 400
    app.rectHeight = 900
    app.rectWidth = 400

def testCollison(app):
    if distance(0, 400, app.ball.x, app.ball.y) <= 20 + 900:
        return 'grounded'
    

def onKeyHold(app, keys):
    app.ball.ballKeyHold(keys)

def onKeyRelease(app, key):
    app.ball.ballKeyRelease(key)

def onKeyPress(app, key):
    app.ball.ballKeyPress(key)
    
def onStep(app):
    app.ball.step()

def redrawAll(app):
    drawRect(0, 400, 900, 400, fill = 'blue')
    app.ball.draw()    


runApp(width = 600, height = 600)
from cmu_graphics import *
import random

def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

class Ball:
    def __init__(self, x, y):
        #Position
        self.x = x
        self.y = y

        #Velocity
        self.isMoving = False
        self.gotToClimaxJump = False
        self.dx = 5
        self.defaultDx = 5
        self.dy = -6
        self.defaultDy = -6
        self.jumpingDy = 6

        #Acceleration
        self.ddx = 0.2
        self.ddy = -0.1

    def draw(self):
        drawCircle(self.x, self.y, 20, fill = 'red')

    def step(self):
        #Integrate position and velocity
        if self.isMoving == True:
            self.dx += self.ddx
            self.dy += self.ddy
        else:
            self.dx = self.defaultDx


        
    def ballKeyHold(self, keys):
        if 'right' in keys and 'up' not in keys and 'left' not in keys:
            self.isMoving = True
            self.x += self.dx
            # print(self.dx)
        elif 'left' in keys and 'up' not in keys and 'right' not in keys:
            self.isMoving = True
            self.x -= self.dx
            # print(self.dx)
        elif 'up' in keys:
            self.isMoving = True
            self.y += self.dy
            print(f'current shit: {self.dy}')
            if self.dy < self.defaultDy - 3:
                print('got in the loop')
                self.y += abs(self.jumpingDy)
                print(self.dy)


        
    
    def ballKeyRelease(self, key):
        if key == 'right':
            self.isMoving = False
            self.dx = self.defaultDx
        elif key == 'left':
            self.isMoving = False
            self.dx = self.defaultDx
        elif key == 'up':
            self.isMoving = False
            self.dy = self.defaultDy



#---Animation functions---------------------------------
def onAppStart(app):
    app.ball = Ball(20, 380)

def onKeyHold(app, keys):
    app.ball.ballKeyHold(keys)

def onKeyRelease(app, key):
    app.ball.ballKeyRelease(key)
    
def onStep(app):
    app.ball.step()

def redrawAll(app):
    drawLine(0, 400, 900, 400)
    app.ball.draw()    


runApp(width = 600, height = 600)
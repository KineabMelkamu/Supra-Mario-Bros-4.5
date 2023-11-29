from cmu_graphics import *

def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

def testCollision(app):
    if abs(app.rectTop1 - app.rectTop2) <= 180 and ((app.rectLeft2 - 150 <= app.rectLeft1 + 30 <= app.rectLeft2 + 150) or (app.rectLeft2 - 150 <= app.rectLeft1 - 30 <= app.rectLeft2 + 150)):
        return 'grouned'
class Ball:
    def __init__(self, x, y, speed, color):
        #Position
        self.x = x
        self.y = y
        self.dy = 
        self.speed = speed
        self.color = color

    def draw(self):
        drawCircle(self.x, self.y, 20, fill = self.color)

    def step(self):
        #Integrate position and velocity
        self.x -= self.speed


def onAppStart(app):
    app.balls = []
    ball1 = Ball(228, 331, 1, 'red')
    ball2 = Ball(228, 331, 2, 'green')
    ball3 = Ball(228, 331, 3, 'purple')
    ball4 = Ball(228, 331, 4, 'blue')
    app.balls.append(ball1)
    app.balls.append(ball2)
    app.balls.append(ball3)
    app.balls.append(ball4)


def onStep(app):
    for ball in app.balls:
        ball.step()


def redrawAll(app):
    for ball in app.balls:
        ball.draw()


      


runApp(width = 600, height = 600)
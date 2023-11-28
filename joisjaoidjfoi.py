class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y

ball1 = Ball(40, 90)

def test():
    print(ball1.x)


print(test())
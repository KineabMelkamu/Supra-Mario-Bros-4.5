from cmu_graphics import *
from PIL import Image
import os, pathlib
import math
import random

#All sprites and spritemaps resized and made on https://www.piskelapp.com/p/create/sprite

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

class Mario:
    #Lives and death value
    lives = 5
    isMarioDead = False

    def __init__(self, x, y, marioState, marioSize):
        #All Sprites Accessed from https://www.mariouniverse.com/sprites-snes-smw/
        #All Music Downloaded from https://www.zophar.net/music/nintendo-snes-spc/super-mario-world
        #All Sound Effects Downloaded from: https://www.sounds-resource.com/snes/supermarioworld/sound/19236/
        self.showHitBox = True
        self.leftConds = ['walkingLeftBig', 'idleBigLeft', 'crouchingLeftBig', 'jumpingLeftBigFrame1', 
                          'jumpingLeftBigFrame2', 'idleSmallLeft', 'walkingLeftSmall', 'crouchingLeftSmall',
                            'jumpingLeftSmallFrame1', 'jumpingLeftSmallFrame2', 'walkingLeftFire', 'idleLeftFire', 'crouchingLeftFire', 'jumpingLeftFireFrame1', 'jumpingLeftFireFrame2']
        
        self.rightConds = ['walkingRightBig', 'idle', 'crouchingRightBig', 'jumpingRightBigFrame1',
                            'jumpingRightBigFrame2', 'idleSmallRight', 'walkingRightSmall', 'crouchingRightSmall',
                              'jumpingRightSmallFrame1', 'jumpingRightSmallFrame2', 'walkingRightFire', 'idleRightFire', 'crouchingRightFire', 'jumpingRightFireFrame1', 'jumpingRightFireFrame2']
        
        #Initializing mario vals
        self.mariox, self.marioy, self.marioState, self.marioSize = x, y, marioState, marioSize
        self.isMovingRight = False
        self.isScrollingRight = False
        self.isRunning = False
        self.isInvincible = False
        self.isHit = False
        self.isJumping = False
        self.threwFireBall = False
        self.hittingWall = False
        self.numLives = 400
        self.isKpressible = False


        self.dy = -6
        self.defaultDy = -6
        self.ddy = 0.3
        self.jumpingdy = 3
        self.defaultDdy = 0.3
        self.terp = False

        self.checkpointx, self.checkpointy = None, None
        self.restartPoint1 = 100


        self.canWalkLeft, self.canWalkRight = True, True

        #MarioHitBoxes
        self.mainHitx, self.mainHity, self.mainHitWidth, self.mainHitHeight = self.mariox + 12, self.marioy+123, 45, 60   
        self.mainHitCrouchx, self.mainHitCrouchy, self.mainHitCrouchWidth, self.mainHitCrouchHeight = self.mariox + 12, self.marioy+126, 45, 45
        self.topHitx, self.topHity, self.topHitWidth, self.topHitHeight = self.mariox + 12, self.marioy+123, 45, 15
        self.bottomHitx, self.bottomHity, self.bottomHitWidth, self.bottomHitHeight = self.mariox + 12, self.marioy+146, 20, 15     

        self.mainHitBigx, self.mainHitBigy, self.mainHitBigWidth, self.mainHitBigHeight = self.mariox + 12, self.marioy+100, 50, 80  
        self.mainHitBigCrouchx, self.mainHitBigCrouchy, self.mainHitBigCrouchWidth, self.mainHitBigCrouchHeight = self.mariox, self.marioy, 50, 50 
        self.topHitBigx, self.topHitBigy, self.topHitWidthBig, self.topHitHeightBig = self.mariox + 14, self.marioy+75, 50, 15
        self.bottomHitBigx, self.bottomHitBigy, self.bottomHitWidthBig, self.bottomHitHeightBig = self.mariox + 14, self.marioy+146, 20, 15  

        #Mario Solid Surface 
        self.groundx, self.groundy, self.groundWidth, self.groundHeight, self.groundType = None, None, None, None, None
        self.wallx, self.wally, self.wallWidth, self.wallHeight = None, None, None, None
        #Mario Assets
        self.bigMarioWalkRight = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\bigMarioWalkRight.png')
        self.bigMarioWalkLeft = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\bigMarioWalkLeft.png')
        self.bigMarioIdleRight = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\bigMarioIdleRight.png')
        self.bigMarioIdleLeft = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\bigMarioIdleLeft.png')
        self.bigMarioCrouchRight = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\bigMarioCrouchRight.png')
        self.bigMarioCrouchLeft = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\bigMarioCrouchLeft.png')
        self.bigMarioJumpRight1 = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\bigMarioJumpRightFrame1.png')
        self.bigMarioJumpRight2 = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\bigMarioJumpRightFrame2.png')
        self.bigMarioJumpLeft1 = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\bigMarioJumpLeftFrame1.png')
        self.bigMarioJumpLeft2 = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\bigMarioJumpLeftFrame2.png')         

        self.smallMarioWalkRight = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\marioWalking.png')
        self.smallMarioWalkLeft = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\marioWalkingLeft.png')
        self.smallMarioDeath = openImage("C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\death.png")
        self.smallMarioIdleRight = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\marioIdle.png')
        self.smallMarioIdleLeft = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\marioLeftIdle.png')
        self.smallMarioCrouchRight = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\marioCrouchRight.png')
        self.smallMarioCrouchLeft = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\marioCrouchLeft.png')
        self.smallMarioJumpRight1 = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\marioRightFrame1.png')
        self.smallMarioJumpRight2 = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\marioRightJumpFrame2.png') 
        self.smallMarioJumpLeft1 = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\marioLeftJumpFrame1.png')
        self.smallMarioJumpLeft2 = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\jumpLeftJumpFrame2.png')

        self.fireMarioWalkRight = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\fireFlowerMario\\fireMarioWalkRight.png')
        self.fireMarioWalkLeft = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\fireFlowerMario\\fireMarioWalkLeft.png')
        self.fireMarioIdleRight = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\fireFlowerMario\idleFireMarioRight.png')
        self.fireMarioIdleLeft = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\fireFlowerMario\idleFireMarioLeft.png')
        self.fireMarioCrouchRight = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\fireFlowerMario\\fireMarioCrouchRight.png')
        self.fireMarioCrouchLeft = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\fireFlowerMario\\fireMarioCrouchLeft.png')
        self.fireMarioJumpRight1 = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\fireFlowerMario\\fireMarioJumpRightFrame1.png')
        self.fireMarioJumpRight2 = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\fireFlowerMario\\fireMarioJumpRightFrame2.png')
        self.fireMarioJumpLeft1 = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\fireFlowerMario\\fireMarioJumpLeftFrame1.png')
        self.fireMarioJumpLeft2 = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\fireFlowerMario\\fireMarioJumpLeftFrame2.png')


        fireMarioIdleRightWidth, fireMarioIdleRightHeight = self.fireMarioIdleRight.size
        self.fireMarioIdleRight = self.fireMarioIdleRight.resize((fireMarioIdleRightWidth//4, fireMarioIdleRightHeight//4))
        self.fireMarioIdleRight = CMUImage(self.fireMarioIdleRight)

        fireMarioIdleLeftWidth, fireMarioIdleLeftHeight = self.fireMarioIdleLeft.size
        self.fireMarioIdleLeft = self.fireMarioIdleLeft.resize((fireMarioIdleLeftWidth//4, fireMarioIdleLeftHeight//4))
        self.fireMarioIdleLeft = CMUImage(self.fireMarioIdleLeft)

        fireMarioCrouchRightWidth, fireMarioCrouchRightHeight = self.fireMarioCrouchRight.size
        self.fireMarioCrouchRight = self.fireMarioCrouchRight.resize((fireMarioCrouchRightWidth//4, fireMarioCrouchRightHeight//4))
        self.fireMarioCrouchRight = CMUImage(self.fireMarioCrouchRight)

        fireMarioCrouchLeftWidth, fireMarioCrouchLeftHeight = self.fireMarioCrouchLeft.size
        self.fireMarioCrouchLeft = self.fireMarioCrouchLeft.resize((fireMarioCrouchLeftWidth//4, fireMarioCrouchLeftHeight//4))
        self.fireMarioCrouchLeft = CMUImage(self.fireMarioCrouchLeft)

        fireMarioJumpRight1Width, fireMarioJumpRight1Height = self.fireMarioJumpRight1.size
        self.fireMarioJumpRight1 = self.fireMarioJumpRight1.resize((fireMarioJumpRight1Width//4, fireMarioJumpRight1Height//4))
        self.fireMarioJumpRight1 = CMUImage(self.fireMarioJumpRight1)

        fireMarioJumpRight2Width, fireMarioJumpRight2Height = self.fireMarioJumpRight2.size
        self.fireMarioJumpRight2 = self.fireMarioJumpRight2.resize((fireMarioJumpRight2Width//4, fireMarioJumpRight2Height//4))
        self.fireMarioJumpRight2 = CMUImage(self.fireMarioJumpRight2)

        fireMarioJumpLeft1Width, fireMarioJumpLeft1Height = self.fireMarioJumpLeft1.size
        self.fireMarioJumpLeft1 = self.fireMarioJumpLeft1.resize((fireMarioJumpLeft1Width//4, fireMarioJumpLeft1Height//4))
        self.fireMarioJumpLeft1 = CMUImage(self.fireMarioJumpLeft1)

        fireMarioJumpLeft2Width, fireMarioJumpLeft2Height = self.fireMarioJumpLeft2.size
        self.fireMarioJumpLeft2 = self.fireMarioJumpLeft2.resize((fireMarioJumpLeft2Width//4, fireMarioJumpLeft2Height//4))
        self.fireMarioJumpLeft2 = CMUImage(self.fireMarioJumpLeft2)


        bigMarioJumpRight1Width, bigMarioJumpRight1Height = self.bigMarioJumpRight1.size
        self.bigMarioJumpRight1 = self.bigMarioJumpRight1.resize((bigMarioJumpRight1Width//4, bigMarioJumpRight1Height//4))
        self.bigMarioJumpRight1 = CMUImage(self.bigMarioJumpRight1)

        bigMarioJumpRight2Width, bigMarioJumpRight2Height = self.bigMarioJumpRight2.size
        self.bigMarioJumpRight2 = self.bigMarioJumpRight2.resize((bigMarioJumpRight2Width//4, bigMarioJumpRight2Height//4))
        self.bigMarioJumpRight2 = CMUImage(self.bigMarioJumpRight2)

        bigMarioJumpLeft1Width, bigMarioJumpLeft1Height = self.bigMarioJumpLeft1.size
        self.bigMarioJumpLeft1 = self.bigMarioJumpLeft1.resize((bigMarioJumpLeft1Width//4, bigMarioJumpLeft1Height//4))
        self.bigMarioJumpLeft1 = CMUImage(self.bigMarioJumpLeft1)

        bigMarioJumpLeft2Width, bigMarioJumpLeft2Height = self.bigMarioJumpLeft2.size
        self.bigMarioJumpLeft2 = self.bigMarioJumpLeft2.resize((bigMarioJumpLeft2Width//4, bigMarioJumpLeft2Height//4))
        self.bigMarioJumpLeft2 = CMUImage(self.bigMarioJumpLeft2)

        smallMarioJumpRight1Width, smallMarioJumpRight1Height = self.smallMarioJumpRight1.size
        self.smallMarioJumpRight1 = self.smallMarioJumpRight1.resize((smallMarioJumpRight1Width//4, smallMarioJumpRight1Height//4))
        self.smallMarioJumpRight1 = CMUImage(self.smallMarioJumpRight1)

        smallMarioJumpRight2Width, smallMarioJumpRight2Height = self.smallMarioJumpRight2.size
        self.smallMarioJumpRight2 = self.smallMarioJumpRight2.resize((smallMarioJumpRight2Width//4, smallMarioJumpRight2Height//4))
        self.smallMarioJumpRight2 = CMUImage(self.smallMarioJumpRight2)

        smallMarioJumpLeft1Width, smallMarioJumpLeft1Height = self.smallMarioJumpLeft1.size
        self.smallMarioJumpLeft1 = self.smallMarioJumpLeft1.resize((smallMarioJumpLeft1Width//4, smallMarioJumpLeft1Height//4))
        self.smallMarioJumpLeft1 = CMUImage(self.smallMarioJumpLeft1)

        smallMarioJumpLeft2Width, smallMarioJumpLeft2Height = self.smallMarioJumpLeft2.size
        self.smallMarioJumpLeft2 = self.smallMarioJumpLeft2.resize((smallMarioJumpLeft2Width//4, smallMarioJumpLeft2Height//4))
        self.smallMarioJumpLeft2 = CMUImage(self.smallMarioJumpLeft2)                

        bigMarioIdleRightWidth, bigMarioIdleRightHeight = self.bigMarioIdleRight.size
        self.bigMarioIdleRight = self.bigMarioIdleRight.resize((bigMarioIdleRightWidth//4, bigMarioIdleRightHeight//4))
        self.bigMarioIdleRight = CMUImage(self.bigMarioIdleRight)

        bigMarioIdleLeftWidth, bigMarioIdleLeftHeight = self.bigMarioIdleLeft.size
        self.bigMarioIdleLeft = self.bigMarioIdleLeft.resize((bigMarioIdleLeftWidth//4, bigMarioIdleLeftHeight//4))
        self.bigMarioIdleLeft = CMUImage(self.bigMarioIdleLeft)

        bigMarioCrouchRightWidth, bigMarioCrouchRightHeight = self.bigMarioCrouchRight.size
        self.bigMarioCrouchRight = self.bigMarioCrouchRight.resize((bigMarioCrouchRightWidth//4, bigMarioCrouchRightHeight//4))
        self.bigMarioCrouchRight = CMUImage(self.bigMarioCrouchRight)

        bigMarioCrouchLeftWidth, bigMarioCrouchLeftHeight = self.bigMarioCrouchLeft.size
        self.bigMarioCrouchLeft = self.bigMarioCrouchLeft.resize((bigMarioCrouchLeftWidth//4, bigMarioCrouchLeftHeight//4))
        self.bigMarioCrouchLeft = CMUImage(self.bigMarioCrouchLeft)


        smallMarioIdleLeftWidth, smallMarioIdleLeftHeight = self.smallMarioIdleLeft.size
        self.smallMarioIdleLeft = self.smallMarioIdleLeft.resize((smallMarioIdleLeftWidth//4, smallMarioIdleLeftHeight//4))
        self.smallMarioIdleLeft = CMUImage(self.smallMarioIdleLeft)

        smallMarioIdleRightWidth, smallMarioIdleRightHeight = self.smallMarioIdleRight.size
        self.smallMarioIdleRight = self.smallMarioIdleRight.resize((smallMarioIdleRightWidth//4, smallMarioIdleRightHeight//4))
        self.smallMarioIdleRight = CMUImage(self.smallMarioIdleRight)

        smallMarioCrouchRightWidth, smallMarioCrouchRightHeight = self.smallMarioCrouchRight.size
        self.smallMarioCrouchRight = self.smallMarioCrouchRight.resize((smallMarioCrouchRightWidth//4, smallMarioCrouchRightHeight//4))
        self.smallMarioCrouchRight = CMUImage(self.smallMarioCrouchRight)       

        smallMarioCrouchLeftWidth, smallMarioCrouchLeftHeight = self.smallMarioCrouchLeft.size
        self.smallMarioCrouchLeft = self.smallMarioCrouchLeft.resize((smallMarioCrouchLeftWidth//4, smallMarioCrouchLeftHeight//4))
        self.smallMarioCrouchLeft = CMUImage(self.smallMarioCrouchLeft)





        self.spritesWalkingRightBig = [ ]
        self.spritesRunningRightBig = [ ]
        self.spritesWalkingRightSmall = [ ]
        self.spritesRunningRightSmall = [ ]
        self.spritesWalkingLeftBig = [ ]
        self.spritesRunningLeftBig = [ ]
        self.spritesWalkingLeftSmall = [ ]
        self.spritesRunningLeftSmall = [ ]
        self.spriteSmallMarioDeath = []
        self.spritesWalkingRightFire = []
        self.spritesWalkingLeftFire = []

        for i in range(2):
            frameWalkingRightBig = self.bigMarioWalkRight.crop((100 + 530*i, 30, 400 + 530*i, 430))
            frameWalkingRightBigWidth, frameWalkingRightBigHeight = frameWalkingRightBig.size
            frameWalkingRightBig = frameWalkingRightBig.resize((frameWalkingRightBigWidth//4, frameWalkingRightBigHeight//4))
            spriteWalkingRight = CMUImage(frameWalkingRightBig)
            self.spritesWalkingRightBig.append(spriteWalkingRight)
            self.spritesRunningRightBig.append(spriteWalkingRight)

            frameWalkingLeftBig = self.bigMarioWalkLeft.crop((100 + 480*i, 25, 400 + 480*i, 425))
            frameWalkingLeftBigWidth, frameWalkingLeftBigHeight = frameWalkingLeftBig.size
            frameWalkingLeftBig = frameWalkingLeftBig.resize((frameWalkingLeftBigWidth//4, frameWalkingLeftBigHeight//4))
            spriteWalkingLeft = CMUImage(frameWalkingLeftBig)
            self.spritesWalkingLeftBig.append(spriteWalkingLeft)
            self.spritesRunningLeftBig.append(spriteWalkingLeft)

            frameWalkingRightSmall = self.smallMarioWalkRight.crop(((20 + 290 * i, 0, 250 + 290 * i, 250)))
            frameWalkingRightSmallWidth, frameWalkingRightSmallHeight = frameWalkingRightSmall.size
            frameWalkingRightSmall = frameWalkingRightSmall.resize((frameWalkingRightSmallWidth//4, frameWalkingRightSmallHeight//4))
            spriteWalkingRightSmall = CMUImage(frameWalkingRightSmall)
            self.spritesWalkingRightSmall.append(spriteWalkingRightSmall)
            self.spritesRunningRightSmall.append(spriteWalkingRightSmall)

            frameWalkingLeftSmall = self.smallMarioWalkLeft.crop(((20 + 250 * i, 0, 250 + 290 * i, 230)))
            frameWalkingLeftSmallWidth, frameWalkingLeftSmallHeight = frameWalkingLeftSmall.size
            frameWalkingLeftSmall = frameWalkingLeftSmall.resize((frameWalkingLeftSmallWidth//4, frameWalkingLeftSmallHeight//4))
            spriteWalkingLeftSmall = CMUImage(frameWalkingLeftSmall)
            self.spritesWalkingLeftSmall.append(spriteWalkingLeftSmall)
            self.spritesRunningLeftSmall.append(spriteWalkingLeftSmall)

            frameDeath = self.smallMarioDeath.crop((40 + 300 * i, 40, 350 + 300 *i, 320))
            frameDeathWidth, frameDeathHeight = frameDeath.size
            frameDeath = frameDeath.resize((frameDeathWidth//4, frameDeathHeight//4))
            spriteFrameDeath = CMUImage(frameDeath)
            self.spriteSmallMarioDeath.append(spriteFrameDeath)

            frameWalkingRightFire = self.fireMarioWalkRight.crop((100 + 405*i, 30, 400 + 405*i, 430))
            frameWalkingRightFireWidth, frameWalkingRightFireHeight = frameWalkingRightFire.size
            frameWalkingRightFire = frameWalkingRightFire.resize((frameWalkingRightFireWidth//4, frameWalkingRightFireHeight//4))
            spriteWalkingRightFire = CMUImage(frameWalkingRightFire)
            self.spritesWalkingRightFire.append(spriteWalkingRightFire)

            frameWalkingLeftFire = self.fireMarioWalkLeft.crop((100 + 520*i, 25, 400 + 520*i, 425))
            frameWalkingLeftFireWidth, frameWalkingLeftFireHeight = frameWalkingLeftFire.size
            frameWalkingLeftFire = frameWalkingLeftFire.resize((frameWalkingLeftFireWidth//4, frameWalkingLeftFireHeight//4))
            spriteWalkingLeftFire = CMUImage(frameWalkingLeftFire)
            self.spritesWalkingLeftFire.append(spriteWalkingLeftFire)
        
        # app.spriteCounter shows which sprite (of the list) 
        # we should currently display
        self.spriteCounter = 0
        self.stepCounter = 0
        self.deathCounter = 0
        self.stepDeathCounter = 0
   
    def stepMario(self):
        if Mario.isMarioDead == True:
            self.isKpressible = True
        else:
            self.isKpressible = False
        self.stepCounter += 1
        self.stepDeathCounter += 1
        self.mainHitx, self.mainHity = self.mariox +12, self.marioy+117
        self.mainHitCrouchx, self.mainHitCrouchy = self.mariox + 12, self.marioy+126

        self.mainHitBigx, self.mainHitBigy = self.mariox+14, self.marioy+108  
        self.mainHitBigCrouchx, self.mainHitBigCrouchy = self.mariox, self.marioy+125
        self.topHitx, self.topHity = self.mariox + 12, self.marioy+95
        self.bottomHitx, self.bottomHity= self.mariox + 12, self.marioy+140

        self.topHitBigx, self.topHitBigy = self.mariox + 14, self.marioy+75 
        self.bottomHitBigx, self.bottomHitBigy = self.mariox + 14, self.marioy+140

        if self.stepCounter>= 8:
            self.spriteCounter = (1 + self.spriteCounter) % len(self.spritesWalkingRightBig)
            self.stepCounter = 0
        if self.isHit:
            tempSelfY = self.marioy
            self.isInvincible = True
            self.mariox -= 3
            self.marioy -= 3
            if self.marioy >= tempSelfY -10:
                self.marioy += 3
                if self.marioy <= tempSelfY:
                    self.isHit = False
                    self.isInvincible = False
        if self.marioSize == 'small':
            if self.wallx != None:
                if testCollision(self, self.mainHitx, self.mainHity, self.wallx, self.wally, self.mainHitWidth, self.mainHitHeight, self.wallWidth, self.wallHeight):
                    if self.marioState in self.rightConds:
                        self.mariox -= 1
                        self.canWalkRight = False
                        self.canWalkLeft = True
                    elif self.marioState in self.leftConds:
                        self.mariox += 1
                        self.canWalkLeft = False
                        self.canWalkRight = True
                else:
                    self.canWalkRight = True
                    self.canWalkLeft = True
            if not testCollision(self, self.mainHitx, self.mainHity, self.groundx, self.groundy, self.mainHitWidth, self.mainHitHeight, self.groundWidth, self.groundHeight) and self.isJumping == False and self.groundType == 'ground':
                if self.marioState in self.rightConds:
                    self.marioState = 'jumpingRightSmallFrame1'
                    self.marioy += self.jumpingdy
                    self.jumpingdy += self.ddy
                elif self.marioState in self.leftConds:
                    self.marioState = 'jumpingLeftSmallFrame1'
                    self.marioy += self.jumpingdy
                    self.jumpingdy += self.ddy
                if testCollision(self, self.mainHitx, self.mainHity, self.groundx, self.groundy, self.mainHitWidth, self.mainHitHeight, self.groundWidth, self.groundHeight) and self.groundType == 'ground':
                    self.dy =0
                    self.ddy = 0
                    self.isJumping = False
            elif testCollision(self, self.mainHitx, self.mainHity, self.groundx, self.groundy, self.mainHitWidth, self.mainHitHeight, self.groundWidth, self.groundHeight)and self.groundType == 'ground':
                if self.marioState in self.rightConds:
                    self.marioState =  'idleSmallRight'
                elif self.marioState in self.leftConds:
                    self.marioStaet = 'idleSmallLeft'
            if self.isJumping == True:
                self.marioy += self.dy
                self.dy += self.ddy
                if self.dy <= 0:
                    if self.marioState in self.rightConds:
                        self.marioState =  'idleSmallRight'
                    elif self.marioState in self.leftConds:
                        self.marioStaet = 'idleSmallLeft'
                if testCollision(self, self.mainHitx, self.mainHity, self.groundx, self.groundy, self.mainHitWidth, self.mainHitHeight, self.groundWidth, self.groundHeight):
                    self.dy =0
                    self.ddy = 0
                    self.isJumping = False

        elif self.marioSize == 'big':
            if self.wallx != None:
                if testCollision(self, self.mainHitBigx, self.mainHitBigy, self.wallx, self.wally, self.mainHitBigWidth, self.mainHitBigHeight, self.wallWidth, self.wallHeight):
                    if self.marioState in self.rightConds:
                        self.mariox -= 1
                        self.canWalkRight = False
                        self.canWalkLeft = True
                    elif self.marioState in self.leftConds:
                        self.mariox += 1
                        self.canWalkLeft = False
                        self.canWalkRight = True
                else:
                    self.canWalkRight = True
                    self.canWalkLeft = True
            if not testCollision(self, self.mainHitBigx, self.mainHitBigy, self.groundx, self.groundy, self.mainHitBigWidth, self.mainHitBigHeight, self.groundWidth, self.groundHeight) and self.isJumping == False and self.groundType == 'ground':
                if self.marioState in self.rightConds:
                    self.marioState = 'jumpingRightBigFrame1'
                    self.marioy += self.jumpingdy
                    self.jumpingdy += self.ddy
                elif self.marioState in self.leftConds:
                    self.marioState = 'jumpingLeftBigFrame1'
                    self.marioy += self.jumpingdy
                    self.jumpingdy += self.ddy
                if testCollision(self, self.mainHitBigx, self.mainHitBigy, self.groundx, self.groundy, self.mainHitBigWidth, self.mainHitBigHeight, self.groundWidth, self.groundHeight):
                    self.dy =0
                    self.ddy = 0
                    self.isJumping = False
            elif testCollision(self, self.mainHitBigx, self.mainHitBigy, self.groundx, self.groundy, self.mainHitBigWidth, self.mainHitBigHeight, self.groundWidth, self.groundHeight) and self.groundType == 'ground':
                if self.marioState in self.rightConds:
                    self.marioState =  'idle'
                elif self.marioState in self.leftConds:
                    self.marioStaet = 'idleBigLeft'
            if self.isJumping == True:
                self.marioy += self.dy
                self.dy += self.ddy
                if self.dy <= 0:
                    if self.marioState in self.rightConds:
                        self.marioState =  'idle'
                    elif self.marioState in self.leftConds:
                        self.marioStaet = 'idleBigLeft'
                if testCollision(self, self.mainHitBigx, self.mainHitBigy, self.groundx, self.groundy, self.mainHitBigWidth, self.mainHitBigHeight, self.groundWidth, self.groundHeight) and self.groundType == 'ground':
                    self.dy =0
                    self.ddy = 0
                    self.isJumping = False
        elif self.marioSize == 'fire':
            if self.wallx != None:
                if testCollision(self, self.mainHitBigx, self.mainHitBigy, self.wallx, self.wally, self.mainHitBigWidth, self.mainHitBigHeight, self.wallWidth, self.wallHeight):
                    if self.marioState in self.rightConds:
                        self.mariox -= 1
                        self.canWalkRight = False
                        self.canWalkLeft = True
                    elif self.marioState in self.leftConds:
                        self.mariox += 1
                        self.canWalkLeft = False
                        self.canWalkRight = True
                else:
                    self.canWalkRight = True
                    self.canWalkLeft = True
            if not testCollision(self, self.mainHitBigx, self.mainHitBigy, self.groundx, self.groundy, self.mainHitBigWidth, self.mainHitBigHeight, self.groundWidth, self.groundHeight) and self.isJumping == False and self.groundType == 'ground':
                if self.marioState in self.rightConds:
                    self.marioState = 'jumpingRightFireFrame1'
                    self.marioy += self.jumpingdy
                    self.jumpingdy += self.ddy
                elif self.marioState in self.leftConds:
                    self.marioState = 'jumpingLeftFireFrame1'
                    self.marioy += self.jumpingdy
                    self.jumpingdy += self.ddy
                if testCollision(self, self.mainHitBigx, self.mainHitBigy, self.groundx, self.groundy, self.mainHitBigWidth, self.mainHitBigHeight, self.groundWidth, self.groundHeight) and self.groundType == 'ground':
                    self.dy =0
                    self.ddy = 0
                    self.isJumping = False
            elif testCollision(self, self.mainHitBigx, self.mainHitBigy, self.groundx, self.groundy, self.mainHitBigWidth, self.mainHitBigHeight, self.groundWidth, self.groundHeight) and self.groundType == 'ground':
                if self.marioState in self.rightConds:
                    self.marioState =  'idleRightFire'
                elif self.marioState in self.leftConds:
                    self.marioStaet = 'idleLeftFire'
            if self.isJumping == True:
                self.marioy += self.dy
                self.dy += self.ddy
                if self.dy <= 0:
                    if self.marioState in self.rightConds:
                        self.marioState =  'idleRightFire'
                    elif self.marioState in self.leftConds:
                        self.marioStaet = 'idleLeftFire'
                if testCollision(self, self.mainHitBigx, self.mainHitBigy, self.groundx, self.groundy, self.mainHitBigWidth, self.mainHitBigHeight, self.groundWidth, self.groundHeight) and self.groundType == 'ground':
                    self.dy =0
                    self.ddy = 0
                    self.isJumping = False



        if self.numLives != 400:
            if self.numLives >= 200:
                if self.marioSize == 'fire' and not self.terp:
                    self.marioSize = 'big'
                    self.terp = True
                elif self.marioSize == 'big' and not self.terp:
                    self.marioSize = 'small'
                    self.terp = True
            elif self.numLives < 200:
                if self.marioSize != 'small':
                    self.marioSize = 'small'
            if self.numLives <= 0:
                Mario.isMarioDead = True
        
    def marioKeyPress(self, key):
        tempValue = self.marioSize
        if key == 'b':
            if tempValue == 'small':
                self.marioSize = 'big'
                self.marioState = 'idle'
            else:
                self.marioSize = 'small'
                self.marioState = 'idleSmallRight'
        elif key == 'k' and self.isKpressible == True:
            Mario.isMarioDead = False
        elif key == 'j':
            Mario.isMarioDead = True
        elif key == 'n':
            if tempValue != 'fire':
                self.marioSize = 'fire'
                self.marioState = 'idleRightFire'
            else:
                self.marioSize = 'big'
                self.marioState = 'idle'
        if self.marioSize == 'fire' and key == 'x':
            self.threwFireBall = True
        

    def marioHit(self):
        if self.marioSize == 'small':
            Mario.isMarioDead = True
        else:
            self.isHit = True
            self.marioSize = 'small'
            self.isHit = False

    def marioKeyHold(self, keys, modifiers):
        tempValue = self.marioState
        if self.marioSize == 'big':
            if 'right' in keys and 'left' not in keys and 'control' not in modifiers and self.canWalkRight:
                self.isMovingRight = True
                self.jumpingdy = 3
                if self.isScrollingRight == True:
                    self.marioState = 'walkingRightBig'
                else:
                    self.marioState = 'walkingRightBig'
                    self.mariox += 6
            elif 'right' in keys and 'left' not in keys and 'control' in modifiers and self.canWalkRight:
                self.jumpingdy = 3
                self.isRunning = True
                self.isMovingRight = True
                if self.isScrollingRight == True:
                    self.marioState = 'walkingRightBig'
                else:
                    self.marioState = 'walkingRightBig'
                    self.mariox += 15
            elif 'left' in keys and 'right' not in keys and 'control' not in modifiers and self.canWalkLeft:
                self.jumpingdy = 3
                self.isScrollingRight = False
                self.marioState = 'walkingLeftBig'
                self.mariox -= 6
            elif 'left' in keys and 'right' not in keys and 'control' in modifiers and self.canWalkLeft:
                self.jumpingdy = 3
                self.isRunning = True
                self.marioState = 'walkingLeftBig'
                self.mariox -= 15
            elif 'down' in keys and tempValue == 'idle':
                self.jumpingdy = 3
                self.marioState = 'crouchingRightBig'
            elif 'down' in keys and tempValue == 'idleBigLeft':
                self.jumpingdy = 3
                self.marioState = 'crouchingLeftBig'
            elif 'up' in keys and 'right' not in keys and 'left' not in keys and testCollision(self, self.mainHitBigx, self.mainHitBigy, self.groundx, self.groundy, self.mainHitBigWidth, self.mainHitBigHeight, self.groundWidth, self.groundHeight):
                self.isJumping = True
                self.dy = self.defaultDy
                self.ddy = self.defaultDdy
                self.jumpingdy = 3
            elif 's' in keys:
                self.marioy += 1
            elif 'w' in keys:
                self.marioy -= 1
        elif self.marioSize == 'small' and Mario.isMarioDead == False:
            if 'right' in keys and 'left' not in keys and 'control' not in modifiers and self.canWalkRight:
                self.jumpingdy = 3
                self.isMovingRight = True
                if self.isScrollingRight == True:
                    self.marioState = 'walkingRightSmall'
                else:
                    self.marioState = 'walkingRightSmall'
                    self.mariox += 6
            elif 'right' in keys and 'left' not in keys and 'control' in modifiers and self.canWalkRight:
                self.jumpingdy = 3
                self.isRunning = True
                self.isMovingRight = True
                if self.isScrollingRight == True:
                    self.marioState = 'walkingRightSmall'
                else:
                    self.marioState = 'walkingRightSmall'
                    self.mariox += 15
            elif 'left' in keys and 'right' not in keys and 'control' not in modifiers and self.canWalkLeft:
                self.jumpingdy = 3
                self.marioState = 'walkingLeftSmall'
                self.mariox -= 6
            elif 'left' in keys and 'right' not in keys and 'control' in modifiers and self.canWalkLeft:
                self.jumpingdy = 3
                self.isRunning = True
                self.marioState = 'walkingLeftSmall'
                self.mariox -= 15
            elif 'down' in keys and tempValue == 'idleSmallRight':
                self.jumpingdy = 3
                self.marioState = 'crouchingRightSmall'
            elif 'down' in keys and tempValue == 'idleSmallLeft':
                self.jumpingdy = 3
                self.marioState = 'crouchingLeftSmall'
            elif 'up' in keys and 'right' not in keys and 'left' not in keys and testCollision(self, self.mainHitx, self.mainHity, self.groundx, self.groundy, self.mainHitWidth, self.mainHitHeight, self.groundWidth, self.groundHeight):
                self.isJumping = True
                self.dy = self.defaultDy
                self.ddy = self.defaultDdy
                self.jumpingdy = 3
            elif 's' in keys:
                self.marioy += 1
            elif 'w' in keys:
                self.marioy -= 1
        elif self.marioSize == 'fire':
            if 'right' in keys and 'left' not in keys and 'control' not in modifiers and self.canWalkRight:
                self.isMovingRight = True
                self.jumpingdy = 3
                if self.isScrollingRight == True:
                    self.marioState = 'walkingRightFire'
                else:
                    self.marioState = 'walkingRightFire'
                    self.mariox += 6
            elif 'right' in keys and 'left' not in keys and 'control' in modifiers and self.canWalkRight:
                self.jumpingdy = 3
                self.isRunning = True
                self.isMovingRight = True
                if self.isScrollingRight == True:
                    self.marioState = 'walkingRightFire'
                else:
                    self.marioState = 'walkingRightFire'
                    self.mariox += 15
            elif 'left' in keys and 'right' not in keys and 'control' not in modifiers and self.canWalkLeft:
                self.jumpingdy = 3
                self.isScrollingRight = False
                self.marioState = 'walkingLeftFire'
                self.mariox -= 6
            elif 'left' in keys and 'right' not in keys and 'control' in modifiers and self.canWalkLeft:
                self.jumpingdy = 3
                self.isRunning = True
                self.marioState = 'walkingLeftFire'
                self.mariox -= 15
            elif 'down' in keys and tempValue == 'idleRightFire':
                self.jumpingdy = 3
                self.marioState = 'crouchingRightFire'
            elif 'down' in keys and tempValue == 'idleLeftFire':
                self.jumpingdy = 3
                self.marioState = 'crouchingLeftFire'
            elif 'up' in keys and 'right' not in keys and 'left' not in keys and testCollision(self, self.mainHitBigx, self.mainHitBigy, self.groundx, self.groundy, self.mainHitBigWidth, self.mainHitBigHeight, self.groundWidth, self.groundHeight):
                self.isJumping = True
                self.dy = self.defaultDy
                self.ddy = self.defaultDdy
                self.jumpingdy = 3
            elif 's' in keys:
                self.marioy += 1
            elif 'w' in keys:
                self.marioy -= 1

    def marioKeyRelease(self, key, modifier):
        if self.marioSize == 'big':
            if (key == 'right'):
                self.isMovingRight = False
                self.isRunning = False
                self.isScrollingRight = False
                self.marioState = 'idle'
            elif key == 'left':
                self.isScrollingRight = False
                self.isRunning = False
                self.marioState = 'idleBigLeft'
            elif key == 'down' and self.marioState == 'crouchingRightBig':
                self.isScrollingRight = False
                self.isRunning = False
                self.marioState = 'idle'
            elif key == 'down' and self.marioState == 'crouchingLeftBig':
                self.isScrollingRight = False
                self.isRunning = False
                self.marioState = 'idleBigLeft'
            elif modifier == 'control':
                self.isRunning = False

        elif self.marioSize == 'small':
            if (key == 'right'):
                self.isMovingRight = False
                self.isRunning = False
                self.isScrollingRight = False
                self.marioState = 'idleSmallRight'
            elif key == 'left':
                self.isScrollingRight = False
                self.isRunning = False
                self.marioState = 'idleSmallLeft'
            elif key == 'down' and self.marioState == 'crouchingRightSmall':
                self.isRunning = False
                self.isScrollingRight = False
                self.marioState = 'idleSmallRight'
            elif key == 'down' and self.marioState == 'crouchingLeftSmall':
                self.isRunning = False
                self.isScrollingRight = False
                self.marioState = 'idleSmallLeft'
            elif modifier == 'control':
                self.isRunning = False

        elif self.marioSize == 'fire':
            if (key == 'right'):
                self.isMovingRight = False
                self.isRunning = False
                self.isScrollingRight = False
                self.marioState = 'idleRightFire'
            elif key == 'left':
                self.isScrollingRight = False
                self.isRunning = False
                self.marioState = 'idleLeftFire'
            elif key == 'down' and self.marioState == 'crouchingRightFire':
                self.isScrollingRight = False
                self.isRunning = False
                self.marioState = 'idleRightFire'
            elif key == 'down' and self.marioState == 'crouchingLeftFire':
                self.isScrollingRight = False
                self.isRunning = False
                self.marioState = 'idleLeftFire'
            elif modifier == 'control':
                self.isRunning = False
        
        if key == 'x':
            self.threwFireBall = False

    def drawMario(self):
        if not Mario.isMarioDead:
            if self.showHitBox:
                color = 'red'
            else:
                color = None
            if self.marioSize == 'big':
                if self.marioState == 'walkingRightBig':
                    spriteWalkingRight = self.spritesWalkingRightBig[self.spriteCounter]
                    drawImage(spriteWalkingRight, self.mariox+6, self.marioy+ 113, align = 'center')
                    drawRect(self.mainHitBigx, self.mainHitBigy, self.mainHitBigWidth, self.mainHitBigHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitBigx, self.topHitBigy, self.topHitWidthBig, self.topHitHeightBig, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitBigx, self.bottomHitBigy, self.bottomHitWidthBig, self.bottomHitHeightBig, fill = None, border = color, align = 'center')
                elif self.marioState == 'walkingLeftBig':
                    spriteWalkingLeft = self.spritesWalkingLeftBig[self.spriteCounter]
                    drawImage(spriteWalkingLeft, self.mariox + 18, self.marioy+ 113, align = 'center')
                    drawRect(self.mainHitBigx, self.mainHitBigy, self.mainHitBigWidth, self.mainHitBigHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitBigx, self.topHitBigy, self.topHitWidthBig, self.topHitHeightBig, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitBigx, self.bottomHitBigy, self.bottomHitWidthBig, self.bottomHitHeightBig, fill = None, border = color, align = 'center')
                elif self.marioState == 'idle':
                    drawImage(self.bigMarioIdleRight, self.mariox + 15, self.marioy+ 113, align = 'center')
                    drawRect(self.mainHitBigx, self.mainHitBigy, self.mainHitBigWidth, self.mainHitBigHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitBigx, self.topHitBigy, self.topHitWidthBig, self.topHitHeightBig, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitBigx, self.bottomHitBigy, self.bottomHitWidthBig, self.bottomHitHeightBig, fill = None, border = color, align = 'center')
                elif self.marioState == 'idleBigLeft':
                    drawImage(self.bigMarioIdleLeft, self.mariox + 14, self.marioy + 113, align = 'center')
                    drawRect(self.mainHitBigx, self.mainHitBigy, self.mainHitBigWidth, self.mainHitBigHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitBigx, self.topHitBigy, self.topHitWidthBig, self.topHitHeightBig, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitBigx, self.bottomHitBigy, self.bottomHitWidthBig, self.bottomHitHeightBig, fill = None, border = color, align = 'center')
                elif self.marioState == 'crouchingRightBig':
                    drawImage(self.bigMarioCrouchRight, self.mariox, self.marioy+ 133, align = 'center')
                    drawRect(self.mainHitBigCrouchx, self.mainHitBigCrouchy, self.mainHitBigCrouchWidth, self.mainHitBigCrouchHeight, fill = None, border = color, align = 'center')
                elif self.marioState == 'crouchingLeftBig':
                    drawImage(self.bigMarioCrouchLeft, self.mariox, self.marioy+ 133, align = 'center')
                    drawRect(self.mainHitBigCrouchx, self.mainHitBigCrouchy, self.mainHitBigCrouchWidth, self.mainHitBigCrouchHeight, fill = None, border = color, align = 'center')
                elif self.marioState == 'jumpingRightBigFrame1':
                    drawImage(self.bigMarioJumpRight1, self.mariox + 10, self.marioy+ 105, align = 'center')
                    drawRect(self.mainHitBigx, self.mainHitBigy, self.mainHitBigWidth, self.mainHitBigHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitBigx, self.topHitBigy, self.topHitWidthBig, self.topHitHeightBig, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitBigx, self.bottomHitBigy, self.bottomHitWidthBig, self.bottomHitHeightBig, fill = None, border = color, align = 'center')
                elif self.marioState == 'jumpingRightBigFrame2':
                    drawImage(self.bigMarioJumpRight2, self.mariox + 10, self.marioy+ 105, align = 'center')
                    drawRect(self.mainHitBigx, self.mainHitBigy, self.mainHitBigWidth, self.mainHitBigHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitBigx, self.topHitBigy, self.topHitWidthBig, self.topHitHeightBig, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitBigx, self.bottomHitBigy, self.bottomHitWidthBig, self.bottomHitHeightBig, fill = None, border = color, align = 'center')
                elif self.marioState == 'jumpingLeftBigFrame1':
                    drawImage(self.bigMarioJumpLeft1, self.mariox + 10, self.marioy+ 105, align = 'center')
                    drawRect(self.mainHitBigx, self.mainHitBigy, self.mainHitBigWidth, self.mainHitBigHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitBigx, self.topHitBigy, self.topHitWidthBig, self.topHitHeightBig, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitBigx, self.bottomHitBigy, self.bottomHitWidthBig, self.bottomHitHeightBig, fill = None, border = color, align = 'center')
                elif self.marioState == 'jumpingLeftBigFrame2':
                    drawImage(self.bigMarioJumpRight2, self.mariox + 10, self.marioy+ 105, align = 'center')
                    drawRect(self.mainHitBigx, self.mainHitBigy, self.mainHitBigWidth, self.mainHitBigHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitBigx, self.topHitBigy, self.topHitWidthBig, self.topHitHeightBig, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitBigx, self.bottomHitBigy, self.bottomHitWidthBig, self.bottomHitHeightBig, fill = None, border = color, align = 'center')

            elif self.marioSize == 'small':
                if self.marioState == 'idleSmallLeft':
                    drawImage(self.smallMarioIdleLeft, self.mariox + 15, self.marioy+ 125, align = 'center')
                    drawRect(self.mainHitx, self.mainHity, self.mainHitWidth, self.mainHitHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitx, self.topHity, self.topHitWidth, self.topHitHeight, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitx, self.bottomHity, self.bottomHitWidth, self.bottomHitHeight, fill = None, border = color, align = 'center')
                elif self.marioState == 'idleSmallRight':
                    drawImage(self.smallMarioIdleRight, self.mariox + 15, self.marioy + 125, align = 'center')
                    drawRect(self.mainHitx, self.mainHity, self.mainHitWidth, self.mainHitHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitx, self.topHity, self.topHitWidth, self.topHitHeight, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitx, self.bottomHity, self.bottomHitWidth, self.bottomHitHeight, fill = None, border = color, align = 'center')
                elif self.marioState == 'walkingRightSmall':
                    spriteWalkingRightSmall = self.spritesWalkingRightSmall[self.spriteCounter]
                    drawImage(spriteWalkingRightSmall, self.mariox + 7, self.marioy+ 125, align = 'center')
                    drawRect(self.mainHitx, self.mainHity, self.mainHitWidth, self.mainHitHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitx, self.topHity, self.topHitWidth, self.topHitHeight, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitx, self.bottomHity, self.bottomHitWidth, self.bottomHitHeight, fill = None, border = color, align = 'center')
                elif self.marioState == 'walkingLeftSmall':
                    spriteWalkingLeftSmall = self.spritesWalkingLeftSmall[self.spriteCounter]
                    drawImage(spriteWalkingLeftSmall, self.mariox+16, self.marioy+ 125, align = 'center')
                    drawRect(self.mainHitx, self.mainHity, self.mainHitWidth, self.mainHitHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitx, self.topHity, self.topHitWidth, self.topHitHeight, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitx, self.bottomHity, self.bottomHitWidth, self.bottomHitHeight, fill = None, border = color, align = 'center')
                elif self.marioState == 'crouchingRightSmall':
                    drawImage(self.smallMarioCrouchRight, self.mariox+14, self.marioy+ 130, align = 'center')
                    drawRect(self.mainHitCrouchx, self.mainHitCrouchy, self.mainHitCrouchWidth, self.mainHitCrouchHeight, fill = None, border = color, align = 'center')
                elif self.marioState == 'crouchingLeftSmall':
                    drawImage(self.smallMarioCrouchLeft, self.mariox+5, self.marioy+ 130, align = 'center')
                    drawRect(self.mainHitCrouchx, self.mainHitCrouchy, self.mainHitCrouchWidth, self.mainHitCrouchHeight, fill = None, border = color, align = 'center')
                elif self.marioState == 'jumpingLeftSmallFrame1':
                    drawImage(self.smallMarioJumpLeft1, self.mariox+15, self.marioy+ 120, align = 'center')
                    drawRect(self.mainHitx, self.mainHity, self.mainHitWidth, self.mainHitHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitx, self.topHity, self.topHitWidth, self.topHitHeight, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitx, self.bottomHity, self.bottomHitWidth, self.bottomHitHeight, fill = None, border = color, align = 'center')
                elif self.marioState == 'jumpingLeftSmallFrame2':
                    drawImage(self.smallMarioJumpLeft2, self.mariox+15, self.marioy+ 120, align = 'center')
                    drawRect(self.mainHitx, self.mainHity, self.mainHitWidth, self.mainHitHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitx, self.topHity, self.topHitWidth, self.topHitHeight, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitx, self.bottomHity, self.bottomHitWidth, self.bottomHitHeight, fill = None, border = color, align = 'center')
                elif self.marioState == 'jumpingRightSmallFrame1':
                    drawImage(self.smallMarioJumpRight1, self.mariox+15, self.marioy+ 120, align = 'center')
                    drawRect(self.mainHitx, self.mainHity, self.mainHitWidth, self.mainHitHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitx, self.topHity, self.topHitWidth, self.topHitHeight, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitx, self.bottomHity, self.bottomHitWidth, self.bottomHitHeight, fill = None, border = color, align = 'center')
                elif self.marioState == 'jumpingRightSmallFrame2':
                    drawImage(self.smallMarioJumpRight2, self.mariox+15, self.marioy+ 120, align = 'center')
                    drawRect(self.mainHitx, self.mainHity, self.mainHitWidth, self.mainHitHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitx, self.topHity, self.topHitWidth, self.topHitHeight, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitx, self.bottomHity, self.bottomHitWidth, self.bottomHitHeight, fill = None, border = color, align = 'center')

            elif self.marioSize == 'fire':
                if self.marioState == 'walkingRightFire':
                    spriteWalkingRightFire = self.spritesWalkingRightFire[self.spriteCounter]
                    drawImage(spriteWalkingRightFire, self.mariox+20, self.marioy+ 113, align = 'center')
                    drawRect(self.mainHitBigx, self.mainHitBigy, self.mainHitBigWidth, self.mainHitBigHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitBigx, self.topHitBigy, self.topHitWidthBig, self.topHitHeightBig, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitBigx, self.bottomHitBigy, self.bottomHitWidthBig, self.bottomHitHeightBig, fill = None, border = color, align = 'center')
                elif self.marioState == 'walkingLeftFire':
                    spriteWalkingLeftFire = self.spritesWalkingLeftFire[self.spriteCounter]
                    drawImage(spriteWalkingLeftFire, self.mariox + 18, self.marioy+ 107, align = 'center')
                    drawRect(self.mainHitBigx, self.mainHitBigy, self.mainHitBigWidth, self.mainHitBigHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitBigx, self.topHitBigy, self.topHitWidthBig, self.topHitHeightBig, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitBigx, self.bottomHitBigy, self.bottomHitWidthBig, self.bottomHitHeightBig, fill = None, border = color, align = 'center')
                elif self.marioState == 'idleRightFire':
                    drawImage(self.fireMarioIdleRight, self.mariox + 15, self.marioy+ 113, align = 'center')
                    drawRect(self.mainHitBigx, self.mainHitBigy, self.mainHitBigWidth, self.mainHitBigHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitBigx, self.topHitBigy, self.topHitWidthBig, self.topHitHeightBig, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitBigx, self.bottomHitBigy, self.bottomHitWidthBig, self.bottomHitHeightBig, fill = None, border = color, align = 'center')
                elif self.marioState == 'idleLeftFire':
                    drawImage(self.fireMarioIdleLeft, self.mariox + 14, self.marioy + 113, align = 'center')
                    drawRect(self.mainHitBigx, self.mainHitBigy, self.mainHitBigWidth, self.mainHitBigHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitBigx, self.topHitBigy, self.topHitWidthBig, self.topHitHeightBig, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitBigx, self.bottomHitBigy, self.bottomHitWidthBig, self.bottomHitHeightBig, fill = None, border = color, align = 'center')
                elif self.marioState == 'crouchingRightFire':
                    drawImage(self.fireMarioCrouchRight, self.mariox, self.marioy+ 133, align = 'center')
                    drawRect(self.mainHitBigCrouchx, self.mainHitBigCrouchy, self.mainHitBigCrouchWidth, self.mainHitBigCrouchHeight, fill = None, border = color, align = 'center')
                elif self.marioState == 'crouchingLeftFire':
                    drawImage(self.fireMarioCrouchLeft, self.mariox, self.marioy+ 133, align = 'center')
                    drawRect(self.mainHitBigCrouchx, self.mainHitBigCrouchy, self.mainHitBigCrouchWidth, self.mainHitBigCrouchHeight, fill = None, border = color, align = 'center')
                elif self.marioState == 'jumpingRightFireFrame1':
                    drawImage(self.fireMarioJumpRight1, self.mariox + 10, self.marioy+ 105, align = 'center')
                    drawRect(self.mainHitBigx, self.mainHitBigy, self.mainHitBigWidth, self.mainHitBigHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitBigx, self.topHitBigy, self.topHitWidthBig, self.topHitHeightBig, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitBigx, self.bottomHitBigy, self.bottomHitWidthBig, self.bottomHitHeightBig, fill = None, border = color, align = 'center')
                elif self.marioState == 'jumpingRightFireFrame2':
                    drawImage(self.fireMarioJumpRight2, self.mariox + 10, self.marioy+ 105, align = 'center')
                    drawRect(self.mainHitBigx, self.mainHitBigy, self.mainHitBigWidth, self.mainHitBigHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitBigx, self.topHitBigy, self.topHitWidthBig, self.topHitHeightBig, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitBigx, self.bottomHitBigy, self.bottomHitWidthBig, self.bottomHitHeightBig, fill = None, border = color, align = 'center')
                elif self.marioState == 'jumpingLeftFireFrame1':
                    drawImage(self.fireMarioJumpLeft1, self.mariox + 10, self.marioy+ 105, align = 'center')
                    drawRect(self.mainHitBigx, self.mainHitBigy, self.mainHitBigWidth, self.mainHitBigHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitBigx, self.topHitBigy, self.topHitWidthBig, self.topHitHeightBig, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitBigx, self.bottomHitBigy, self.bottomHitWidthBig, self.bottomHitHeightBig, fill = None, border = color, align = 'center')
                elif self.marioState == 'jumpingLeftFireFrame2':
                    drawImage(self.fireMarioJumpLeft2, self.mariox + 10, self.marioy+ 105, align = 'center')
                    drawRect(self.mainHitBigx, self.mainHitBigy, self.mainHitBigWidth, self.mainHitBigHeight, fill = None, border = color, align = 'center')
                    drawRect(self.topHitBigx, self.topHitBigy, self.topHitWidthBig, self.topHitHeightBig, fill = None, border = color, align = 'center')
                    drawRect(self.bottomHitBigx, self.bottomHitBigy, self.bottomHitWidthBig, self.bottomHitHeightBig, fill = None, border = color, align = 'center')
        elif Mario.isMarioDead:
            spriteDeath = self.spriteSmallMarioDeath[self.spriteCounter]
            drawImage(spriteDeath, self.mariox, self.marioy + 100, align = 'center')
               
class PowerUps(Mario):
    def __init__(self, x, y, powerUp):
        self.x, self.y, self.powerUp = x, y, powerUp

        self.isPowerUpHit = False
        self.showHitBoxx = True

        #powerUpAssets
        self.oneUpMushroom = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\Items\\1upMushroom.png')
        self.fireFlower = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\Items\\fireFlower.png')
        self.coin = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\Items\coin.png')
        self.superMushroom = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\Items\mushroom.png')
        self.mysteryBlock = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\Items\\1UpBlock.png')


        oneUpMushroomWidth, oneUpMushroomHeight = self.oneUpMushroom.size
        self.oneUpMushroom = self.oneUpMushroom.resize((oneUpMushroomWidth//5, oneUpMushroomHeight//5))
        self.oneUpMushroom = CMUImage(self.oneUpMushroom)

        superMushroomWidth, superMushroomHeight = self.superMushroom.size
        self.superMushroom = self.superMushroom.resize((superMushroomWidth//5, superMushroomHeight//5))
        self.superMushroom = CMUImage(self.superMushroom)

        #Power-Up Hitboxes
        self.fireFlowerBoxX, self.fireFlowerBoxY, self.fireFlowerBoxWidth, self.fireFlowerBoxHeight = self.x, self.y, 35, 35


        self.spritesFireFlower = [ ]
        self.spritesCoin = [ ]
        self.spritesMysteryBlock = [ ]

        for i in range(2):
            frameFireFlower = self.fireFlower.crop((10 + 210*i, 40, 220 + 210*i, 230)) 
            frameFireFlowerWidth, frameFireFlowerHeight = frameFireFlower.size
            frameFireFlower = frameFireFlower.resize((frameFireFlowerWidth//5, frameFireFlowerHeight//5))
            spriteFireFlower = CMUImage(frameFireFlower)
            self.spritesFireFlower.append(spriteFireFlower)

        for i in range(3):
            frameMysteryBlock = self.mysteryBlock.crop((0 + 210*i, 23, 220 + 210*i, 200))
            frameMysteryBlockWidth, frameMysteryBlockHeight = frameMysteryBlock.size
            frameMysteryBlock = frameMysteryBlock.resize((frameMysteryBlockWidth//5, frameMysteryBlockHeight//5))
            spriteMysteryBlock = CMUImage(frameMysteryBlock)
            self.spritesMysteryBlock.append(spriteMysteryBlock)

            frameCoin = self.coin.crop((13 + 350*i, 0, 150 + 350 * i, 200))
            frameCoinWidth, frameCoinHeight = frameCoin.size
            frameCoin = frameCoin.resize((frameCoinWidth//5, frameCoinHeight//5))
            spriteFrameCoin = CMUImage(frameCoin)
            self.spritesCoin.append(spriteFrameCoin)

        self.spriteCounter = 0
        self.stepCounter = 0
        self.othaCounter = 0
        self.othaStepCounter = 0
 
    def stepPowerUp(self):
        self.stepCounter += 1
        self.othaStepCounter += 1

        if self.stepCounter >= 8:
            self.spriteCounter = (1 + self.spriteCounter) % len(self.spritesFireFlower)
            self.stepCounter = 0

        if self.othaStepCounter >=4:
            self.othaCounter = (1 + self.othaCounter) % len(self.spritesMysteryBlock)
            self.othaStepCounter = 0
        
        self.fireFlowerBoxX, self.fireFlowerBoxY = self.x, self.y


    def drawPowerUp(self):
        if self.showHitBoxx:
            color = 'blue'
        else:
            color = None
        if not self.isPowerUpHit: 
            if self.powerUp == 'fireFlower':
                spriteFrameFire = self.spritesFireFlower[self.spriteCounter]
                drawImage(spriteFrameFire, self.x, self.y, align = 'center')
                #self.fireFlowerBoxX, self.fireFlowerBoxY, self.fireFlowerBoxWidth, self.fireFlowerBoxHeight = self.x, self.y, 14, 14
                drawRect(self.fireFlowerBoxX, self.fireFlowerBoxY, self.fireFlowerBoxWidth, self.fireFlowerBoxHeight, fill = None, border = color, align = 'center')
            elif self.powerUp == 'mysteryBlock':
                spriteFrameMystery = self.spritesMysteryBlock[self.othaCounter]
                drawImage(spriteFrameMystery, self.x, self.y, align = 'center')
                drawRect(self.fireFlowerBoxX, self.fireFlowerBoxY, self.fireFlowerBoxWidth, self.fireFlowerBoxHeight, fill = None, border = color, align = 'center')
            elif self.powerUp == 'coin':
                spriteCoin = self.spritesCoin[self.othaCounter]
                drawImage(spriteCoin, self.x, self.y, align = 'center')
                drawRect(self.fireFlowerBoxX, self.fireFlowerBoxY, self.fireFlowerBoxWidth, self.fireFlowerBoxHeight, fill = None, border = color, align = 'center')
            elif self.powerUp == 'superMushroom':
                drawImage(self.superMushroom, self.x, self.y, align = 'center')
                drawRect(self.fireFlowerBoxX, self.fireFlowerBoxY, self.fireFlowerBoxWidth, self.fireFlowerBoxHeight, fill = None, border = color, align = 'center')
            elif self.powerUp == 'oneUpMushroom':
                drawImage(self.oneUpMushroom, self.x, self.y, align = 'center')
                drawRect(self.fireFlowerBoxX, self.fireFlowerBoxY, self.fireFlowerBoxWidth, self.fireFlowerBoxHeight, fill = None, border = color, align = 'center')

class enemies(Mario):
    def __init__(self, x, y, enemyState, enemyType):
        self.x, self.y, self.enemyState, self.enemyType = x, y, enemyState, enemyType
        self.marioxbox, self.marioybox, self.mariowidthbox, self.marioheightbox = None, None, None, None

        self.rexLives = 2

        self.isKilled = False

        self.isThrowingFire = False

        self.thwompFallBoxx, self.thwompFallBoxy, self.thwompFallBoxWidth, self.thwompFallBoxHeight = None, None, None, None
        self.isFalling = False
        self.reachedBottom = False
        self.reachedTop = False
        self.bottom = self.y + 200
        tempVal = self.y
        self.top = tempVal

        self.showHitBoxx = True


        self.gloombaWalkLeft = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\Enemies\gloombaFrameMap.png')
        if self.enemyType == 'gloomba':
            self.goombaXBox, self.goombaYBox, self.goombaWidthBox, self.goombaHeightBox = self.x, self.y, 50, 40
        elif self.enemyType == 'bulletBill':
            self.goombaXBox, self.goombaYBox, self.goombaWidthBox, self.goombaHeightBox = self.x, self.y, 100, 100
        elif self.enemyType == 'rex':
            self.fireRectx, self.fireRecty, self.fireRectWidth, self.fireRectxHeight = self.x - 100, self.y-10, 200, 50
            if self.enemyState == 'rexNoHit':
                self.goombaXBox, self.goombaYBox, self.goombaWidthBox, self.goombaHeightBox = self.x + 15, self.y - 10, 50, 50
            else:
                self.goombaXBox, self.goombaYBox, self.goombaWidthBox, self.goombaHeightBox = self.x, self.y, 1, 1
        elif self.enemyType == 'thwomp':
            self.goombaXBox, self.goombaYBox, self.goombaWidthBox, self.goombaHeightBox = self.x, self.y-10, 55, 90
            self.fallBoxx, self.fallBoxy, self.fallBoxwidth, self.fallBoxheight = self.x, self.y, 55, 600

        self.bulletBill = openImage("C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\Enemies\\bulletBill.png")
        bulletBillWidth, bulletBillHeight = self.bulletBill.size
        self.bulletBill = self.bulletBill.resize((bulletBillWidth*2, bulletBillHeight*2))
        self.bulletBill = CMUImage(self.bulletBill)

        self.rexframesnohit = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\Enemies\\rexframesnothit.png')
        self.rexframes1hit = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\Enemies\\rexframes1hit.png')

        self.thwompFall = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\Enemies\\thwompFall.png')
        thwompFallWidth, thwompFallHeight = self.thwompFall.size
        self.thwompFall = self.thwompFall.resize((thwompFallWidth//4, thwompFallHeight//4))
        self.thwompFall = CMUImage(self.thwompFall)

        self.thwompRest = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\Enemies\\thwompRest.png')
        thwompRestWidth, thwompRestHeight = self.thwompRest.size
        self.thwompRest = self.thwompRest.resize((thwompRestWidth//4, thwompRestHeight//4))
        self.thwompRest = CMUImage(self.thwompRest)


        self.spritesGloombaWalking = []
        self.rexWalkingNoHit = []
        self.rexWalking1Hite = []

        for i in range(2):
            frameDeath = self.gloombaWalkLeft.crop((40 + 365*i, 40, 300 + 365*i, 250))
            frameDeathWidth, frameDeathHeight = frameDeath.size
            frameDeath = frameDeath.resize((frameDeathWidth//4, frameDeathHeight//4))
            spriteFrameDeath = CMUImage(frameDeath)
            self.spritesGloombaWalking.append(spriteFrameDeath)

            frameRexno = self.rexframesnohit.crop((0 + 480*i, 100, 350 + 480*i, 500))
            frameRexnoWidth, frameRexnoHeight = frameRexno.size
            frameRexno = frameRexno.resize((frameRexnoWidth//5, frameRexnoHeight//5))
            frameRexno = CMUImage(frameRexno)
            self.rexWalkingNoHit.append(frameRexno)



        self.spriteCounter = 0
        self.stepCounter = 0
    
    def stepEnemy(self):
        if self.enemyType == 'gloomba':
            self.x -= 2
            self.goombaXBox, self.goombaYBox = self.x, self.y
            self.stepCounter += 1
            if self.stepCounter >= 8:
                self.spriteCounter = (1+self.spriteCounter) % len(self.spritesGloombaWalking)
                self.stepCounter = 0
        elif self.enemyType == 'bulletBill':
            self.x -= 6
            self.goombaXBox, self.goombaYBox = self.x, self.y
        elif self.enemyType == 'rex':
            self.x -= 2
            self.goombaXBox, self.goombaYBox = self.x + 15, self.y - 10
            self.fireRectx, self.fireRecty = self.x - 100, self.y-10
            self.stepCounter += 1
            if self.stepCounter >= 8:
                self.spriteCounter = (1+self.spriteCounter) % len(self.spritesGloombaWalking)
                self.stepCounter = 0
            if testCollision(self, self.fireRectx, self.fireRecty, self.marioxbox, self.marioybox, self.fireRectWidth, self.fireRectxHeight, self.mariowidthbox, self.marioheightbox):
                self.isThrowingFire = True
            else:
                self.isThrowingFire = False
        elif self.enemyType == 'thwomp':
            self.goombaXBox, self.goombaYBox = self.x, self.y-10
            self.fallBoxx = self.x
            if testCollision(self, self.fallBoxx, self.fallBoxy, self.marioxbox, self.marioybox, self.fallBoxwidth, self.fallBoxheight, self.mariowidthbox, self.marioheightbox):
                self.isFalling = True
            else:
                self.isFalling = False
            if self.isFalling:
                self.enemyState = 'thwompFall'
                if self.y <= self.bottom:
                    self.y +=5
                    self.isFalling = False
            else:
                self.enemyState = 'thwompRest'
                if self.y >= self.top:
                    self.y -= 5

    
    def drawEnemy(self):
        if self.showHitBoxx:
            color = 'red'
        else:
            color = None
        if self.enemyType == 'gloomba':
            if not self.isKilled:
                spriteWalkingLeftGloomba = self.spritesGloombaWalking[self.spriteCounter]
                drawImage(spriteWalkingLeftGloomba, self.x, self.y, align = 'center')
                drawRect(self.goombaXBox, self.goombaYBox, self.goombaWidthBox, self.goombaHeightBox, fill = None, border = color, align = 'center')
        elif self.enemyType == 'bulletBill':
            drawImage(self.bulletBill, self.x, self.y, align = 'center')
            drawRect(self.goombaXBox, self.goombaYBox, self.goombaWidthBox, self.goombaHeightBox, fill = None, border = color, align = 'center')
        elif self.enemyType == 'rex':
            if not self.isKilled:
                if self.enemyState == 'rexNoHit':
                    spriteNoHitRex = self.rexWalkingNoHit[self.spriteCounter]
                    drawImage(spriteNoHitRex, self.x, self.y - 5, align = 'center')
                    drawRect(self.goombaXBox, self.goombaYBox, self.goombaWidthBox, self.goombaHeightBox, fill = None, border = color, align = 'center')
                    drawRect(self.fireRectx, self.fireRecty, self.fireRectWidth, self.fireRectxHeight, fill = None, border = color, align = 'center')
        elif self.enemyType == 'thwomp':
            if self.enemyState == 'thwompFall':
                drawImage(self.thwompFall, self.x, self.y - 5, align = 'center')
                drawRect(self.goombaXBox, self.goombaYBox, self.goombaWidthBox, self.goombaHeightBox, fill = None, border = color, align = 'center')
                drawRect(self.fallBoxx, self.fallBoxy, self.fallBoxwidth, self.fallBoxheight, fill = None, border = color, align = 'center')
            elif self.enemyState == 'thwompRest':
                drawImage(self.thwompRest, self.x , self.y, align = 'center')
                drawRect(self.goombaXBox, self.goombaYBox, self.goombaWidthBox, self.goombaHeightBox, fill = None, border = color, align = 'center')
                drawRect(self.fallBoxx, self.fallBoxy, self.fallBoxwidth, self.fallBoxheight, fill = None, border = color, align = 'center')

class structures:
    def __init__(self, x, y, width, height, structureType):
        self.x, self.y, self.width, self.height, self.structureType = x, y, width, height, structureType
        self.showHitBoxx = True
    def draw(self):
        if self.showHitBoxx:
            color = 'pink'
        else:
            color = None
        drawRect(self.x, self.y, self.width, self.height, fill = None, border = color, align = 'center')

class projectiles: 
    def __init__(self, x, y, projectileType, direction, isFreindly, othay):
        self.x, self.y, self.projectileType, self.direction, self.isFreindly, self.othay = x + 40, y, projectileType, direction, isFreindly, othay
        self.exists = True
        self.randomNumber = random.randint(1,2)
        self.showHitBoxx = True        

        self.fireBall = openImage("C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\Items\\fireball.png")

        fireBallWidth, fireBallHeight = self.fireBall.size
        self.fireBall = self.fireBall.resize((fireBallWidth//12, fireBallHeight//12))
        self.fireBall = CMUImage(self.fireBall)
        self.fireBallBoxX, self.fireBallBoxY, self.fireBallBoxWidth, self.fireBallBoxHeight = self.x, self.y, 30, 30
         

    def step(self):
        if self.exists:
            self.fireBallBoxX, self.fireBallBoxY = self.x, self.y
            if self.isFreindly:
                if self.direction == 'right':
                    self.x += 5
                    self.y = 19*math.sin(1/10*self.x) + self.othay + 100
                elif self.direction == 'left':
                    self.x -= 5
                    self.y = 19*math.sin(1/10*self.x) + self.othay + 100
            else:
                if self.randomNumber == 1:
                    if self.direction == 'right':
                        self.x += 5
                        self.y = 19*math.sin(1/10*self.x) + self.othay + 100
                    elif self.direction == 'left':
                        self.x -= 5
                        self.y = 19*math.sin(1/10*self.x) + self.othay + 100
                elif self.randomNumber == 2:
                    if self.direction == 'right':
                        self.x += 5
                    elif self.direction == 'left':
                        self.x -= 5


    def onKeyPress(self, key):
        if key == 'o':
            self.exists = not self.exists

    def drawProjectile(self):
        if self.showHitBoxx:
            color = 'blue'
        else:
            color = None
        if self.exists:
            if self.projectileType == 'fireball':
                drawImage(self.fireBall, self.x, self.y, align = 'center')
                drawRect(self.fireBallBoxX, self.fireBallBoxY, self.fireBallBoxWidth, self.fireBallBoxHeight, fill = None, border = color, align = 'center')

class checkpoint(Mario):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.checkx, self.checky = x, y
        self.xBox, self.yBox, self.width, self.height = self.x, self.y, 30, 30
        self.marioxbox, self.marioybox, self.mariowidthbox, self.marioheightbox = None, None, None, None
        self.isHit = False
        self.showHitBoxx = True

        self.bowserFlag = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\checkPointFlags\\bowsaCheckPoint.png')
        bowserFlagWidth, bowserFlagHeight = self.bowserFlag.size
        self.bowserFlag = self.bowserFlag.resize((bowserFlagWidth//6, bowserFlagHeight//6))
        self.bowserFlag = CMUImage(self.bowserFlag)
        
        self.marioFlag = openImage('C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\checkPointFlags\marioCheckPoint.png')
        marioFlagWidth, marioFlagHeight = self.marioFlag.size
        self.marioFlag = self.marioFlag.resize((marioFlagWidth//6, marioFlagHeight//6))
        self.marioFlag = CMUImage(self.marioFlag)

    def onStep(self):
        self.xBox, self.yBox = self.x, self.y
        self.checkx, self.checky = self.x, self.y
        if testCollision(self, self.xBox, self.yBox, self.marioxbox, self.marioybox, self.width, self.height, self.mariowidthbox, self.marioheightbox) and not self.isHit:
            self.isHit = True

    def draw(self):
        if self.showHitBoxx:
            color = 'yellow'
        else:
            color = None
        if self.isHit:
            drawImage(self.marioFlag, self.x, self.y, align = 'center')
            drawRect(self.xBox, self.yBox, self.width, self.height, fill = None, border = color, align = 'center')
        elif not self.isHit:
            drawImage(self.bowserFlag, self.x, self.y, align = 'center')
            drawRect(self.xBox, self.yBox, self.width, self.height, fill = None, border = color, align = 'center')




#############################################################################################################
##                                     Animaton Functions                                                  ##
#############################################################################################################

#IDEA FOR COLLISION TESTER RECIVED FROM https://academy.cs.cmu.edu/exercise/12905
def testCollision(app, x1, y1, x2, y2, width1, height1, width2, height2):
    newX1 = x1 - width1//2
    newY1 = y1 - height1//2
    newX2 = x2 - width2//2
    newY2 = y2 - height2//2

    bottom1 = newY1 + height1
    bottom2 = newY2 + height2
    right1 = newX1 + width1
    right2 = newX2 + width2


    if (bottom1 + 10 >= newY2 and bottom2 + 10 >= newY1 and right1 >= newX2 and right2 >= newX1):
        return True

def onAppStart(app):
    #Accessed From https://www.pixilart.com/art/mario-peace-sign-pixel-art-a5592b56931aa23
    app.marioTitle = openImage("C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\MarioPeaceTitle.png")
    marioTitleWidth, marioTitleHeight = app.marioTitle.size
    app.marioTitle = app.marioTitle.resize((marioTitleWidth//4, marioTitleHeight//4))
    app.marioTitle = CMUImage(app.marioTitle)

    app.isPaused = False

    app.inspectorEnabled = False
    app.Mario = Mario(100, 288, 'idleSmallRight', 'small')
    app.stepCounter =  0

    app.map1 = openImage("C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\Yoshi's Island.png")
    app.map1 = CMUImage(app.map1)

    app.map2 = openImage("C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\finStage.png")
    app.map2 = CMUImage(app.map2)

    app.backround1 = openImage("C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\backrounds.png")
    app.backround1 = CMUImage(app.backround1)

    app.backround2 = openImage("C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\\backround2.png")
    app.backround2 = CMUImage(app.backround2)

    #Accessed From https://www.fontspace.com/typeface-mario-world-pixel-font-f56447
    app.titleName = openImage("C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\SuperMarioWorldTitle.png")
    titleNameWidth, titleNameHeight = app.titleName.size
    app.titleName = app.titleName.resize((titleNameWidth//2, titleNameHeight//2))
    app.titleName = CMUImage(app.titleName)
    app.endWords = openImage("C:\CMU wrk\\15-112\Supra Mario Bros 4.5\imgs\WIN SCREEN.png")
    endWordsWidth, endWordsHeight = app.endWords.size
    app.endWords = app.endWords.resize((endWordsWidth//2, endWordsHeight//2))
    app.endWords = CMUImage(app.endWords)

    app.map1x, app.map1y = app.width//2 + 4770, app.height//2 - 150
    app.backround1x, app.backround1y = app.width//2, app.height//2 - 100 
    app.stepsPerSecond = 30
    app.line1x = -100
    app.line2x = 900

    app.map2x, app.map2y = 2500, 100

    

    #Map and current State
    app.isTitleScreen = True
    app.isLevel1 = False
    app.isLevel2 = False
    app.isDeathScreen = False
    app.isNextLevelScreen = False
    app.livesScreen = False
    app.isEndScreen = False
    app.showHitBoxes = True

    #structures:
    app.grounds = []
    app.wall2 = structures(3830, 520, 150, 200, 'wall')
    app.grounds.append(app.wall2)
    app.wall3 = structures(3970, 490, 130, 200, 'wall')
    app.grounds.append(app.wall3)
    app.wall4 = structures(4080, 460, 100, 200, 'wall')
    app.grounds.append(app.wall4)
    app.wall5 = structures(4350, 430, 455, 200, 'wall')
    app.grounds.append(app.wall5)
    app.wall6 = structures(7135, 500, 295, 200, 'wall')
    app.grounds.append(app.wall6)
    app.wall7 = structures(8750, 565, 2800, 200, 'wall')
    app.grounds.append(app.wall7)




    app.ground1 = structures(765, 490, 6000, 90, 'ground')
    app.grounds.append(app.ground1)
    app.ground2 = structures(855, 340, 510, 10, 'ground')
    app.grounds.append(app.ground2)
    app.ground3 = structures(1520, 310, 220, 10, 'ground')
    app.grounds.append(app.ground3)
    app.ground4 = structures(3830, 410, 150, 10, 'ground')
    app.grounds.append(app.ground4)
    app.ground5 = structures(3970, 380, 130, 10, 'ground')
    app.grounds.append(app.ground5)
    app.ground6 = structures(4080, 350, 100, 10, 'ground')
    app.grounds.append(app.ground6)
    app.ground7 = structures(4350, 310, 455, 10, 'ground')
    app.grounds.append(app.ground7)
    app.ground8 = structures(5589, 440, 2800, 10, 'ground')
    app.grounds.append(app.ground8)
    app.ground9 = structures(6070, 350, 145, 10, 'ground')
    app.grounds.append(app.ground9)
    app.ground10 = structures(6165, 250, 235, 10, 'ground')
    app.grounds.append(app.ground10)
    app.ground11 = structures(6330, 350, 205, 10, 'ground')
    app.grounds.append(app.ground11)
    app.ground12 = structures(6935, 290, 295, 10, 'ground')
    app.grounds.append(app.ground12)
    app.ground13 = structures(7135, 380, 295, 10, 'ground')
    app.grounds.append(app.ground13)
    app.ground14 = structures(8350, 445, 2800, 10, 'ground')
    app.grounds.append(app.ground14)
    app.end1 = structures(9800, 445, 300, 60000, 'endCon')
    app.grounds.append(app.end1)

    app.checkpoints = []
    app.initcheckpoint = checkpoint(100, 410)
    app.checkpoints.append(app.initcheckpoint)
    app.checkpoint1 = checkpoint(7600, 410)
    app.checkpoints.append(app.checkpoint1)


    #powerups
    app.powerUps = []
    app.fireFlower1 = PowerUps(550, 400, 'superMushroom')
    app.fireFlower2 = PowerUps(590, 400, 'fireFlower')
    app.powerUps.append(app.fireFlower1)
    app.powerUps.append(app.fireFlower2)

    #enemies
    app.enemies = []
    app.gloomba1 = enemies(500, 425, 'thwompRest', 'gloomba')
    app.enemies.append(app.gloomba1)
    app.rex1 = enemies(1520, 425, 'rexNoHit', 'rex')
    app.enemies.append(app.rex1)
    app.gloomba2 = enemies(7435, 425, 'thwompRest', 'gloomba')
    app.enemies.append(app.gloomba2)
    app.gloomba3 = enemies(7785, 425, 'thwompRest', 'gloomba')
    app.enemies.append(app.gloomba3)
    app.rex2 = enemies(7585, 425, 'rexNoHit', 'rex')
    app.enemies.append(app.rex2)
    app.thwomp1 = enemies(9600, 200, 'thwompRest', 'thwomp')
    app.enemies.append(app.thwomp1)
    app.bulletBill1 = enemies(12000, 290, 'thwompRest', 'bulletBill')
    app.enemies.append(app.bulletBill1)

    app.enemies2 = []
    for i in range(50):
        app.enemies2.append(enemies(500 + i*80, 200, 'thwompRest', 'thwomp'))
    app.bulletBill2 = enemies(12000, 290, 'thwompRest', 'bulletBill')
    app.enemies2.append(app.bulletBill2)

    app.grounds2 = []
    app.groundV2 = structures(765, 490, 120000, 90, 'ground')
    app.grounds2.append(app.groundV2)
    app.finEndCon = structures(5000, 490, 100, 60000, 'endCon')
    app.grounds2.append(app.finEndCon)


    app.projectiles = []
    app.projectiles2 = []

    app.checkpoints2 = []

def onStep(app):
    app.stepCounter += 1
    app.Mario.showHitBox = app.showHitBoxes
    for powerup in app.powerUps:
        powerup.showHitBoxx = app.showHitBoxes
    for enemy in app.enemies:
        enemy.showHitBoxx = app.showHitBoxes
    for ground in app.grounds:
        ground.showHitBoxx = app.showHitBoxes
    for projectile in app.projectiles:
        projectile.showHitBoxx = app.showHitBoxes
    for checkpoint in app.checkpoints:
        checkpoint.showHitBoxx = app.showHitBoxes
    for enemy in app.enemies2:
        enemy.showHitBoxx = app.showHitBoxes
    for ground in app.grounds2:
        ground.showHitBoxx = app.showHitBoxes
    for projectile in app.projectiles2:
        projectile.showHitBoxx = app.showHitBoxes
    if app.isLevel1 == True:
        if app.Mario.isMarioDead:
            if app.Mario.checkpointx != None:
                app.Mario.marioSize = 'small'
                app.Mario.numLives = 400
                methVal = app.Mario.mariox - app.Mario.checkpointx
                # app.Mario.mariox += methVal
                app.line1x += methVal
                app.line2x += methVal
                app.map1x += methVal
                for ground in app.grounds:
                    ground.x += methVal
                for enemy in app.enemies:
                    enemy.x += methVal
                for checkpoint in app.checkpoints:
                    checkpoint.x += methVal
                for projectile in app.projectiles:
                    projectile.x += methVal

        if app.Mario.threwFireBall:
            if app.stepCounter%9 == 0:
                if app.Mario.marioState in app.Mario.rightConds:
                    app.projectiles.append(projectiles(app.Mario.mariox, app.Mario.marioy, 'fireball', 'right', True, app.Mario.marioy))
                if app.Mario.marioState in app.Mario.leftConds:
                    app.projectiles.append(projectiles(app.Mario.mariox, app.Mario.marioy, 'fireball', 'left', True, app.Mario.marioy))
        
                  
        for powerup in app.powerUps:
            if powerup.powerUp == 'superMushroom' and testCollision(app, app.Mario.mainHitx, app.Mario.mainHity, powerup.fireFlowerBoxX, powerup.fireFlowerBoxY, app.Mario.mainHitWidth, app.Mario.mainHitHeight, powerup.fireFlowerBoxWidth, powerup.fireFlowerBoxHeight) == True:
                app.Mario.numLives += 30
                if app.Mario.marioSize == 'big' or app.Mario.marioSize == 'small':
                    app.Mario.marioSize = 'big'
                    powerup.isPowerUpHit = True
                else:
                    app.Mario.marioSize = 'fire'
                    powerup.isPowerUpHit = True
                app.powerUps.remove(powerup)
            elif powerup.powerUp == 'fireFlower' and testCollision(app, app.Mario.mainHitx, app.Mario.mainHity, powerup.fireFlowerBoxX, powerup.fireFlowerBoxY, app.Mario.mainHitWidth, app.Mario.mainHitHeight, powerup.fireFlowerBoxWidth, powerup.fireFlowerBoxHeight) == True:
                app.Mario.marioSize = 'fire'
                powerup.isPowerUpHit = True
                app.powerUps.remove(powerup)
            elif powerup.powerUp == 'oneUpMushroom':
                if (app.Mario.numLives + 100) < 400:
                    app.Mario.numLives += 100
                else:
                    app.Mario.numLives += (400-app.Mario.numLives)

        for enemy in app.enemies:
            if enemy.isThrowingFire:
                if app.stepCounter%90 == 0:
                    app.projectiles.append(projectiles(enemy.x, enemy.y, 'fireball', 'left', False, enemy.y - 100))
            if app.Mario.marioSize == 'small':
                if app.Mario.marioState != 'crouchingRightSmall' and app.Mario.marioState != 'crouchingLeftSmall':
                    enemy.marioxbox, enemy.marioybox, enemy.mariowidthbox, enemy.marioheightbox = app.Mario.mainHitx, app.Mario.mainHity, app.Mario.mainHitWidth, app.Mario.mainHitHeight
                else:
                    enemy.marioxbox, enemy.marioybox, enemy.mariowidthbox, enemy.marioheightbox = app.Mario.mainHitCrouchx, app.Mario.mainHitCrouchy, app.Mario.mainHitCrouchWidth, app.Mario.mainHitCrouchHeight
            else:
                if app.Mario.marioState != 'crouchingRightFire' and app.Mario.marioState != 'crouchingLeftFire' and app.Mario.marioState != 'crouchingRightBig'and app.Mario.marioState != 'crouchingLeftBig':
                    enemy.marioxbox, enemy.marioybox, enemy.mariowidthbox, enemy.marioheightbox = app.Mario.mainHitBigx, app.Mario.mainHitBigy, app.Mario.mainHitBigWidth, app.Mario.mainHitBigHeight
                else:
                    enemy.marioxbox, enemy.marioybox, enemy.mariowidthbox, enemy.marioheightbox = app.Mario.mainHitBigCrouchx, app.Mario.mainHitBigCrouchy, app.Mario.mainHitBigCrouchWidth, app.Mario.mainHitBigCrouchHeight
            if app.Mario.marioSize == 'small':
                if testCollision(app, app.Mario.bottomHitx, app.Mario.bottomHity, enemy.goombaXBox, enemy.goombaYBox, app.Mario.bottomHitWidth, app.Mario.bottomHitHeight, enemy.goombaWidthBox, enemy.goombaHeightBox) and enemy.enemyType != 'bulletBill' and enemy.enemyType != 'thwomp':
                    app.Mario.marioy -= 40
                    app.enemies.remove(enemy)
                elif testCollision(app, app.Mario.mainHitx, app.Mario.mainHity, enemy.goombaXBox, enemy.goombaYBox, app.Mario.mainHitWidth, app.Mario.mainHitHeight, enemy.goombaWidthBox, enemy.goombaHeightBox):
                    app.Mario.numLives -= 10
            else:
                if testCollision(app, app.Mario.bottomHitBigx, app.Mario.bottomHitBigy, enemy.goombaXBox, enemy.goombaYBox, app.Mario.bottomHitWidthBig, app.Mario.bottomHitHeightBig, enemy.goombaWidthBox, enemy.goombaHeightBox) and enemy.enemyType != 'bulletBill' and enemy.enemyType != 'thwomp':
                    app.Mario.marioy -= 40
                    app.enemies.remove(enemy)
                elif testCollision(app, app.Mario.mainHitBigx, app.Mario.mainHitBigy, enemy.goombaXBox, enemy.goombaYBox, app.Mario.mainHitBigWidth, app.Mario.mainHitBigHeight, enemy.goombaWidthBox, enemy.goombaHeightBox):
                    app.Mario.numLives -= 10
        for checkpoint in app.checkpoints:
            if app.Mario.marioSize == 'small':
                if app.Mario.marioState != 'crouchingRightSmall' and app.Mario.marioState != 'crouchingLeftSmall':
                    checkpoint.marioxbox, checkpoint.marioybox, checkpoint.mariowidthbox, checkpoint.marioheightbox = app.Mario.mainHitx, app.Mario.mainHity, app.Mario.mainHitWidth, app.Mario.mainHitHeight
                else:
                    checkpoint.marioxbox, checkpoint.marioybox, checkpoint.mariowidthbox, checkpoint.marioheightbox = app.Mario.mainHitCrouchx, app.Mario.mainHitCrouchy, app.Mario.mainHitCrouchWidth, app.Mario.mainHitCrouchHeight
            else:
                if app.Mario.marioState != 'crouchingRightFire' and app.Mario.marioState != 'crouchingLeftFire' and app.Mario.marioState != 'crouchingRightBig'and app.Mario.marioState != 'crouchingLeftBig':
                    checkpoint.marioxbox, checkpoint.marioybox, checkpoint.mariowidthbox, checkpoint.marioheightbox = app.Mario.mainHitBigx, app.Mario.mainHitBigy, app.Mario.mainHitBigWidth, app.Mario.mainHitBigHeight
                else:
                    checkpoint.marioxbox, checkpoint.marioybox, checkpoint.mariowidthbox, checkpoint.marioheightbox = app.Mario.mainHitBigCrouchx, app.Mario.mainHitBigCrouchy, app.Mario.mainHitBigCrouchWidth, app.Mario.mainHitBigCrouchHeight
            checkpoint.onStep()
            if checkpoint.isHit == True:
                app.Mario.checkpointx, app.Mario.checkpointy = checkpoint.checkx, checkpoint.checky
        for structure in app.grounds:
            if app.Mario.marioSize == 'small':
                if testCollision(app, app.Mario.mainHitx, app.Mario.mainHity, structure.x, structure.y, app.Mario.mainHitWidth, app.Mario.mainHitHeight, structure.width, structure.height) and structure.structureType == 'wall':
                    app.Mario.wallx, app.Mario.wally, app.Mario.wallWidth, app.Mario.wallHeight = structure.x, structure.y, structure.width, structure.height
                if testCollision(app, app.Mario.mainHitx, app.Mario.mainHity, structure.x, structure.y, app.Mario.mainHitWidth, app.Mario.mainHitHeight, structure.width, structure.height) and structure.structureType == 'ground':
                    app.Mario.groundx, app.Mario.groundy, app.Mario.groundWidth, app.Mario.groundHeight, app.Mario.groundType = structure.x, structure.y, structure.width, structure.height, structure.structureType
                elif testCollision(app, app.Mario.mainHitx, app.Mario.mainHity, structure.x, structure.y, app.Mario.mainHitWidth, app.Mario.mainHitHeight, structure.width, structure.height) and structure.structureType == 'endCon':
                    app.isLevel1 = False
                    app.isNextLevelScreen = True
                    app.grounds.clear()
                    app.checkpoints.clear()
                    app.powerUps.clear()
                    app.enemies.clear()
                    app.projectiles.clear()
            if app.Mario.marioSize == 'big' or app.Mario.marioSize == 'fire':
                if testCollision(app, app.Mario.mainHitBigx, app.Mario.mainHitBigy, structure.x, structure.y, app.Mario.mainHitBigWidth, app.Mario.mainHitBigHeight, structure.width, structure.height) and structure.structureType == 'wall':
                    app.Mario.wallx, app.Mario.wally, app.Mario.wallWidth, app.Mario.wallHeight = structure.x, structure.y, structure.width, structure.height
                if testCollision(app, app.Mario.mainHitBigx, app.Mario.mainHitBigy, structure.x, structure.y, app.Mario.mainHitBigWidth, app.Mario.mainHitBigHeight, structure.width, structure.height) and structure.structureType == 'ground':
                    app.Mario.groundx, app.Mario.groundy, app.Mario.groundWidth, app.Mario.groundHeight, app.Mario.groundType = structure.x, structure.y, structure.width, structure.height, structure.structureType
                elif testCollision(app, app.Mario.mainHitBigx, app.Mario.mainHitBigy, structure.x, structure.y, app.Mario.mainHitBigWidth, app.Mario.mainHitBigHeight, structure.width, structure.height) and structure.structureType == 'endCon':
                    app.isNextLevelScreen = True
                    app.isLevel1 = False
                    app.grounds.clear()
                    app.checkpoints.clear()
                    app.powerUps.clear()
                    app.enemies.clear()
                    app.projectiles.clear()

        for projectile in app.projectiles:
            projectile.step()
            if projectile.isFreindly == False:
                if app.Mario.marioSize == 'big' or app.Mario.marioSize == 'fire':
                    if app.Mario.marioState == 'crouchingRightBig' or app.Mario.marioState == 'crouchingLeftBig' or app.Mario.marioState == 'crouchingRightFire' or app.Mario.marioState == 'crouchingLeftFire':
                        if testCollision(app, app.Mario.mainHitBigCrouchx, app.Mario.mainHitBigCrouchy, projectile.fireBallBoxX, projectile.fireBallBoxY, app.Mario.mainHitBigCrouchWidth, app.Mario.mainHitBigCrouchHeight, projectile.fireBallBoxWidth, projectile.fireBallBoxHeight):
                            app.Mario.numLives -= 60
                    else:
                        if testCollision(app, app.Mario.mainHitBigx, app.Mario.mainHitBigy, projectile.fireBallBoxX, projectile.fireBallBoxY, app.Mario.mainHitBigWidth, app.Mario.mainHitBigHeight, projectile.fireBallBoxWidth, projectile.fireBallBoxHeight):
                            app.Mario.numLives -= 60          
                else:
                    if app.Mario.marioState == 'crouchingRightSmall' or app.Mario.marioState == 'crouchingLeftSmall':
                        if testCollision(app, app.Mario.mainHitCrouchx, app.Mario.mainHitCrouchy, projectile.fireBallBoxX, projectile.fireBallBoxY, app.Mario.mainHitCrouchWidth, app.Mario.mainHitCrouchHeight, projectile.fireBallBoxWidth, projectile.fireBallBoxHeight):
                            app.Mario.numLives -= 60
                    else:
                        if testCollision(app, app.Mario.mainHitx, app.Mario.mainHity, projectile.fireBallBoxX, projectile.fireBallBoxY, app.Mario.mainHitWidth, app.Mario.mainHitHeight, projectile.fireBallBoxWidth, projectile.fireBallBoxHeight):
                            app.Mario.numLives -= 60
            else:
                for enemy in app.enemies:
                    if testCollision(app, enemy.goombaXBox, enemy.goombaYBox, projectile.fireBallBoxX, projectile.fireBallBoxY, enemy.goombaWidthBox, enemy.goombaHeightBox, projectile.fireBallBoxWidth, projectile.fireBallBoxHeight) and enemy.enemyType != 'thwomp' and enemy.enemyType != 'bulletBill':
                        app.enemies.remove(enemy)
                        app.projectiles.remove(projectile)
                
        app.Mario.stepMario()
        for powerup in app.powerUps:
            powerup.stepPowerUp()
        for enemy in app.enemies:
            enemy.stepEnemy()
        if app.Mario.mariox > app.width//2 and app.Mario.canWalkRight:
            app.Mario.isScrollingRight = True
            if app.Mario.isMovingRight == True and app.Mario.isRunning == False:
                app.line1x -= 5
                app.line2x -= 5
                app.map1x -= 5
                app.Mario.groundx -= 5
                if app.Mario.wallx != None:
                    app.Mario.wallx -= 5
                for ground in app.grounds:
                    ground.x -=5
                for enemy in app.enemies:
                    enemy.x -=5
                for powerup in app.powerUps:
                    powerup.x -= 5
                for checkpoint in app.checkpoints:
                    checkpoint.x -=5
                for projectile in app.projectiles:
                    if projectile.direction == 'left':
                        projectile.x -= 5
                    elif projectile.direction == 'right':
                        projectile.x += 5
            elif app.Mario.isMovingRight == True and app.Mario.isRunning == True:
                app.line1x -= 10
                app.line2x -= 10
                app.map1x -= 10
                app.Mario.groundx -= 10
                if app.Mario.wallx != None:
                    app.Mario.wallx -= 10
                for ground in app.grounds:
                    ground.x -=10
                for enemy in app.enemies:
                    enemy.x -=10
                for powerup in app.powerUps:
                    powerup.x -= 10
                for checkpoint in app.checkpoints:
                    checkpoint.x -=10
                for projectile in app.projectiles:
                    if projectile.direction == 'left':
                        projectile.x -= 10
                    elif projectile.direction == 'right':
                        projectile.x += 10

    elif app.isLevel2 == True:
        if app.Mario.isMarioDead:
            if app.Mario.checkpointx != None:
                app.Mario.marioSize = 'small'
                app.Mario.numLives = 400
                methVal = app.Mario.mariox - app.Mario.checkpointx
                # app.Mario.mariox += methVal
                app.line1x += methVal
                app.line2x += methVal
                app.map2x += methVal
                for ground in app.grounds2:
                    ground.x += methVal
                for enemy in app.enemies2:
                    enemy.x += methVal
                for checkpoint in app.checkpoints2:
                    checkpoint.x += methVal
                for projectile in app.projectiles2:
                    projectile.x += methVal

        if app.Mario.threwFireBall:
            if app.stepCounter%9 == 0:
                if app.Mario.marioState in app.Mario.rightConds:
                    app.projectiles2.append(projectiles(app.Mario.mariox, app.Mario.marioy, 'fireball', 'right', True, app.Mario.marioy))
                if app.Mario.marioState in app.Mario.leftConds:
                    app.projectiles2.append(projectiles(app.Mario.mariox, app.Mario.marioy, 'fireball', 'left', True, app.Mario.marioy))
        
                  

        for enemy in app.enemies2:
            if enemy.isThrowingFire:
                if app.stepCounter%90 == 0:
                    app.projectiles.append(projectiles(enemy.x, enemy.y, 'fireball', 'left', False, enemy.y - 100))
            if app.Mario.marioSize == 'small':
                if app.Mario.marioState != 'crouchingRightSmall' and app.Mario.marioState != 'crouchingLeftSmall':
                    enemy.marioxbox, enemy.marioybox, enemy.mariowidthbox, enemy.marioheightbox = app.Mario.mainHitx, app.Mario.mainHity, app.Mario.mainHitWidth, app.Mario.mainHitHeight
                else:
                    enemy.marioxbox, enemy.marioybox, enemy.mariowidthbox, enemy.marioheightbox = app.Mario.mainHitCrouchx, app.Mario.mainHitCrouchy, app.Mario.mainHitCrouchWidth, app.Mario.mainHitCrouchHeight
            else:
                if app.Mario.marioState != 'crouchingRightFire' and app.Mario.marioState != 'crouchingLeftFire' and app.Mario.marioState != 'crouchingRightBig'and app.Mario.marioState != 'crouchingLeftBig':
                    enemy.marioxbox, enemy.marioybox, enemy.mariowidthbox, enemy.marioheightbox = app.Mario.mainHitBigx, app.Mario.mainHitBigy, app.Mario.mainHitBigWidth, app.Mario.mainHitBigHeight
                else:
                    enemy.marioxbox, enemy.marioybox, enemy.mariowidthbox, enemy.marioheightbox = app.Mario.mainHitBigCrouchx, app.Mario.mainHitBigCrouchy, app.Mario.mainHitBigCrouchWidth, app.Mario.mainHitBigCrouchHeight
            if app.Mario.marioSize == 'small':
                if testCollision(app, app.Mario.bottomHitx, app.Mario.bottomHity, enemy.goombaXBox, enemy.goombaYBox, app.Mario.bottomHitWidth, app.Mario.bottomHitHeight, enemy.goombaWidthBox, enemy.goombaHeightBox) and enemy.enemyType != 'bulletBill' and enemy.enemyType != 'thwomp':
                    app.Mario.marioy -= 40
                    app.enemies.remove(enemy)
                elif testCollision(app, app.Mario.mainHitx, app.Mario.mainHity, enemy.goombaXBox, enemy.goombaYBox, app.Mario.mainHitWidth, app.Mario.mainHitHeight, enemy.goombaWidthBox, enemy.goombaHeightBox):
                    app.Mario.numLives -= 10
            else:
                if testCollision(app, app.Mario.bottomHitBigx, app.Mario.bottomHitBigy, enemy.goombaXBox, enemy.goombaYBox, app.Mario.bottomHitWidthBig, app.Mario.bottomHitHeightBig, enemy.goombaWidthBox, enemy.goombaHeightBox) and enemy.enemyType != 'bulletBill' and enemy.enemyType != 'thwomp':
                    app.Mario.marioy -= 40
                    app.enemies.remove(enemy)
                elif testCollision(app, app.Mario.mainHitBigx, app.Mario.mainHitBigy, enemy.goombaXBox, enemy.goombaYBox, app.Mario.mainHitBigWidth, app.Mario.mainHitBigHeight, enemy.goombaWidthBox, enemy.goombaHeightBox):
                    app.Mario.numLives -= 10
        for checkpoint in app.checkpoints2:
            if app.Mario.marioSize == 'small':
                if app.Mario.marioState != 'crouchingRightSmall' and app.Mario.marioState != 'crouchingLeftSmall':
                    checkpoint.marioxbox, checkpoint.marioybox, checkpoint.mariowidthbox, checkpoint.marioheightbox = app.Mario.mainHitx, app.Mario.mainHity, app.Mario.mainHitWidth, app.Mario.mainHitHeight
                else:
                    checkpoint.marioxbox, checkpoint.marioybox, checkpoint.mariowidthbox, checkpoint.marioheightbox = app.Mario.mainHitCrouchx, app.Mario.mainHitCrouchy, app.Mario.mainHitCrouchWidth, app.Mario.mainHitCrouchHeight
            else:
                if app.Mario.marioState != 'crouchingRightFire' and app.Mario.marioState != 'crouchingLeftFire' and app.Mario.marioState != 'crouchingRightBig'and app.Mario.marioState != 'crouchingLeftBig':
                    checkpoint.marioxbox, checkpoint.marioybox, checkpoint.mariowidthbox, checkpoint.marioheightbox = app.Mario.mainHitBigx, app.Mario.mainHitBigy, app.Mario.mainHitBigWidth, app.Mario.mainHitBigHeight
                else:
                    checkpoint.marioxbox, checkpoint.marioybox, checkpoint.mariowidthbox, checkpoint.marioheightbox = app.Mario.mainHitBigCrouchx, app.Mario.mainHitBigCrouchy, app.Mario.mainHitBigCrouchWidth, app.Mario.mainHitBigCrouchHeight
            checkpoint.onStep()
            if checkpoint.isHit == True:
                app.Mario.checkpointx, app.Mario.checkpointy = checkpoint.checkx, checkpoint.checky
        for structure in app.grounds2:
            if app.Mario.marioSize == 'small':
                if testCollision(app, app.Mario.mainHitx, app.Mario.mainHity, structure.x, structure.y, app.Mario.mainHitWidth, app.Mario.mainHitHeight, structure.width, structure.height) and structure.structureType == 'wall':
                    app.Mario.wallx, app.Mario.wally, app.Mario.wallWidth, app.Mario.wallHeight = structure.x, structure.y, structure.width, structure.height
                if testCollision(app, app.Mario.mainHitx, app.Mario.mainHity, structure.x, structure.y, app.Mario.mainHitWidth, app.Mario.mainHitHeight, structure.width, structure.height) and structure.structureType == 'ground':
                    app.Mario.groundx, app.Mario.groundy, app.Mario.groundWidth, app.Mario.groundHeight, app.Mario.groundType = structure.x, structure.y, structure.width, structure.height, structure.structureType
                elif testCollision(app, app.Mario.mainHitx, app.Mario.mainHity, structure.x, structure.y, app.Mario.mainHitWidth, app.Mario.mainHitHeight, structure.width, structure.height) and structure.structureType == 'endCon':
                    app.isLevel2 = False
                    app.isEndScreen = True
            if app.Mario.marioSize == 'big' or app.Mario.marioSize == 'fire':
                if testCollision(app, app.Mario.mainHitBigx, app.Mario.mainHitBigy, structure.x, structure.y, app.Mario.mainHitBigWidth, app.Mario.mainHitBigHeight, structure.width, structure.height) and structure.structureType == 'wall':
                    app.Mario.wallx, app.Mario.wally, app.Mario.wallWidth, app.Mario.wallHeight = structure.x, structure.y, structure.width, structure.height
                if testCollision(app, app.Mario.mainHitBigx, app.Mario.mainHitBigy, structure.x, structure.y, app.Mario.mainHitBigWidth, app.Mario.mainHitBigHeight, structure.width, structure.height) and structure.structureType == 'ground':
                    app.Mario.groundx, app.Mario.groundy, app.Mario.groundWidth, app.Mario.groundHeight, app.Mario.groundType = structure.x, structure.y, structure.width, structure.height, structure.structureType
                elif testCollision(app, app.Mario.mainHitBigx, app.Mario.mainHitBigy, structure.x, structure.y, app.Mario.mainHitBigWidth, app.Mario.mainHitBigHeight, structure.width, structure.height) and structure.structureType == 'endCon':
                    app.isLevel2 = False
                    app.isEndScreen = True

        for projectile in app.projectiles2:
            projectile.step()
            if projectile.isFreindly == False:
                if app.Mario.marioSize == 'big' or app.Mario.marioSize == 'fire':
                    if app.Mario.marioState == 'crouchingRightBig' or app.Mario.marioState == 'crouchingLeftBig' or app.Mario.marioState == 'crouchingRightFire' or app.Mario.marioState == 'crouchingLeftFire':
                        if testCollision(app, app.Mario.mainHitBigCrouchx, app.Mario.mainHitBigCrouchy, projectile.fireBallBoxX, projectile.fireBallBoxY, app.Mario.mainHitBigCrouchWidth, app.Mario.mainHitBigCrouchHeight, projectile.fireBallBoxWidth, projectile.fireBallBoxHeight):
                            app.Mario.numLives -= 60
                    else:
                        if testCollision(app, app.Mario.mainHitBigx, app.Mario.mainHitBigy, projectile.fireBallBoxX, projectile.fireBallBoxY, app.Mario.mainHitBigWidth, app.Mario.mainHitBigHeight, projectile.fireBallBoxWidth, projectile.fireBallBoxHeight):
                            app.Mario.numLives -= 60          
                else:
                    if app.Mario.marioState == 'crouchingRightSmall' or app.Mario.marioState == 'crouchingLeftSmall':
                        if testCollision(app, app.Mario.mainHitCrouchx, app.Mario.mainHitCrouchy, projectile.fireBallBoxX, projectile.fireBallBoxY, app.Mario.mainHitCrouchWidth, app.Mario.mainHitCrouchHeight, projectile.fireBallBoxWidth, projectile.fireBallBoxHeight):
                            app.Mario.numLives -= 60
                    else:
                        if testCollision(app, app.Mario.mainHitx, app.Mario.mainHity, projectile.fireBallBoxX, projectile.fireBallBoxY, app.Mario.mainHitWidth, app.Mario.mainHitHeight, projectile.fireBallBoxWidth, projectile.fireBallBoxHeight):
                            app.Mario.numLives -= 60
            else:
                for enemy in app.enemies:
                    if testCollision(app, enemy.goombaXBox, enemy.goombaYBox, projectile.fireBallBoxX, projectile.fireBallBoxY, enemy.goombaWidthBox, enemy.goombaHeightBox, projectile.fireBallBoxWidth, projectile.fireBallBoxHeight) and enemy.enemyType != 'thwomp' and enemy.enemyType != 'bulletBill':
                        app.enemies.remove(enemy)
                        app.projectiles.remove(projectile)
                
        app.Mario.stepMario()
        
        for enemy in app.enemies2:
            enemy.stepEnemy()
        if app.Mario.mariox > app.width//2 and app.Mario.canWalkRight:
            app.Mario.isScrollingRight = True
            if app.Mario.isMovingRight == True and app.Mario.isRunning == False:
                app.line1x -= 5
                app.line2x -= 5
                app.map2x -= 5
                app.Mario.groundx -= 5
                if app.Mario.wallx != None:
                    app.Mario.wallx -= 5
                for ground in app.grounds2:
                    ground.x -=5
                for enemy in app.enemies2:
                    enemy.x -=5
                for checkpoint in app.checkpoints2:
                    checkpoint.x -=5
                for projectile in app.projectiles2:
                    if projectile.direction == 'left':
                        projectile.x -= 5
                    elif projectile.direction == 'right':
                        projectile.x += 5
            elif app.Mario.isMovingRight == True and app.Mario.isRunning == True:
                app.line1x -= 10
                app.line2x -= 10
                app.map2x -= 10
                app.Mario.groundx -= 10
                if app.Mario.wallx != None:
                    app.Mario.wallx -= 10
                for ground in app.grounds2:
                    ground.x -=10
                for enemy in app.enemies2:
                    enemy.x -=10
                for checkpoint in app.checkpoints2:
                    checkpoint.x -=10
                for projectile in app.projectiles2:
                    if projectile.direction == 'left':
                        projectile.x -= 10
                    elif projectile.direction == 'right':
                        projectile.x += 10
        

def onKeyHold(app, keys, modifiers):
    app.Mario.marioKeyHold(keys, modifiers)

def onKeyRelease(app, key, modifier):
    app.Mario.marioKeyRelease(key, modifier)

def onKeyPress(app, key):
    if key == 'h':
        app.showHitBoxes = not app.showHitBoxes
    if app.isTitleScreen == True:
        if key == 'z':
            app.isOnTitleScreen = False
            app.isLevel1 = True
    if app.isLevel1 == True:
        app.Mario.marioKeyPress(key)
        for projectile in app.projectiles:
            projectile.onKeyPress(key)
    if app.isNextLevelScreen:
        if key == 'z':
            app.isLevel2 = True
            app.isNextLevelScreen = False
            app.isLevel1 = False
            app.isOnTitleScreen = False
    
def redrawAll(app):
    if app.isTitleScreen == True:
        drawRect(0,0, 700, 900, fill = 'yellow')
        drawImage(app.marioTitle, app.width//2 + 20, app.height//2, align = 'center')
        drawImage(app.titleName, app.width//2, app.height//2 - 200, align = 'center')
        drawLabel('PRESS Z TO START', app.width//2, app.height//2 + 200, size = 30, bold = True)
    if app.isLevel1 == True:
        drawImage(app.backround1, app.backround1x, app.backround1y, align = 'center')
        drawImage(app.map1, app.map1x, app.map1y, align = 'center')
        drawLabel(f'LIVES: {app.Mario.numLives}', 50, 20, size = 16)
        if app.Mario.isKpressible == True:
            drawLabel('PRESS K TO RESTART', app.width//2, app.height//2, size = 30)
        for ground in app.grounds:
            ground.draw()
        for powerup in app.powerUps:
            powerup.drawPowerUp()
        for enemy in app.enemies:
            enemy.drawEnemy()
        for projectile in app.projectiles:
            projectile.drawProjectile()
        for checkpoint in app.checkpoints:
            checkpoint.draw()
        app.Mario.drawMario()
    if app.isNextLevelScreen:
        drawRect(0,0, app.width, app.height, fill = 'black')
        drawLabel("APPROCHING FINAL LEVEL, PRESS Z TO ENTER...", app.width//2, app.height//2, size = 16, fill = 'white')
        drawLabel("IF YOU DARE!!!", app.width//2, app.height//2 + 60, size = 25, fill = 'white')
    if app.isLevel2:
        drawImage(app.backround2, app.backround1x, app.backround1y, align = 'center')
        drawImage(app.map2, app.map2x, app.map2y, align = 'center')
        drawLabel(f'LIVES: {app.Mario.numLives}', 50, 20, size = 16)
        if app.Mario.isKpressible == True:
            drawLabel('PRESS K TO RESTART', app.width//2, app.height//2, size = 30)
        for ground in app.grounds2:
            ground.draw()
        for enemy in app.enemies2:
            enemy.drawEnemy()
        for projectile in app.projectiles2:
            projectile.drawProjectile()
        for checkpoint in app.checkpoints2:
            checkpoint.draw()
        app.Mario.drawMario()
    if app.isEndScreen:
        drawRect(0,0, app.width, app.height, fill = 'pink')
        drawImage(app.endWords, app.width//2, app.height//2, align = 'center')
 
def main():
    runApp(width=700, height=500)

if __name__ == '__main__':
    main()
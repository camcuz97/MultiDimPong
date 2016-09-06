##Math 198 final project
##Cameron Cuzmanko Fall 2015
##Use W,A,S,D for movement! W=up, A=left, S=down, D=down, Q=into the screen, E=out of the screen. Press escape to quit program
from visual import *
from random import randint

##establishes what value the x,y, and z will have
positionNum = 20
##size of each side is twice the position
size = 2*positionNum
rad = positionNum/20

##velocity should be kept at <(1/20)*position because any higher and numerous problems may occur with bounces
##weird bounces will still occur occasionally regardless of velocity
xVelocity = .1 ##random.random()/4 for random number between 0.0 and 0.25
yVelocity = .2
zVelocity = .5

##creates the walls using the positions and size
xzBottomWall = box (pos=(0,-positionNum,0), length=size, height=0.01, width=size, color=color.blue)
xzTopWall = box (pos=(0,positionNum,0), length=size, height=0.01, width=size, color=color.blue)

yzRightWall = box (pos=(positionNum,0,0), length=.01, height=size, width=size, color=color.red)
yzLeftWall = box (pos=(-positionNum,0,0), length=.01, height=size, width=size, color=color.red)

##creates front wall as invisible wall so user can see inside
xyBackWall = box (pos=(0,0,-positionNum), length=positionNum/6, height=positionNum/6, width=0.01, color=color.green, opacity=1)
userPaddle = box (pos=(0,0,positionNum), length=positionNum/6, height=positionNum/6, width=0.01, color=color.yellow, opacity=1)

##creates ball and establishes velocity
ball = sphere (pos=(0,0,0), radius=rad, color=color.green)
ball.velocity = vector(xVelocity,yVelocity,zVelocity)
ball.visible=False

text = text(text='Click to \nBegin', align='center', depth = -.3, color=color.green, pos=(0,0,25), height = 5, width = 3)

ev = scene.waitfor('click')

#def handleKey( evt ):
   # print(evt.key)

def move(s):
    if s == 'd':
        if userPaddle.x<yzRightWall.x-(userPaddle.length/2):
            userPaddle.x +=1
    if s == 's':
        if userPaddle.y>xzBottomWall.y+(userPaddle.height/2):
            userPaddle.y -=1
    if s == 'a':
        if userPaddle.x>yzLeftWall.x+(userPaddle.length/2):
            userPaddle.x -=1
    if s == 'w':
        if userPaddle.y<xzTopWall.y-(userPaddle.length/2):
            userPaddle.y +=1
    if s == 'e':
        if userPaddle.z<positionNum:
            userPaddle.z += .5
    if s == 'q':
        if userPaddle.z>positionNum-5:
            userPaddle.z -= .5
    #escape to end
    if s == "esc":
        quit()


def collide(dir):
    if dir=='x':
        ball.velocity.x = -ball.velocity.x
    if dir=='y':
        ball.velocity.y = -ball.velocity.y
    if dir=='z':
        ball.velocity.z = -(1.05)*ball.velocity.z
        print(ball.velocity.x)
        print(ball.velocity.y)
        print(ball.velocity.z)

def moveAI():
    if ball.x > xyBackWall.x:
        xyBackWall.x += .22
    if ball.x < xyBackWall.x:
        xyBackWall.x -= .22
    if ball.y > xyBackWall.y:
        xyBackWall.y += .22
    if ball.y < xyBackWall.y:
        xyBackWall.y -= .22

userTurnToHit=True


if ev.event == 'click':
    text.visible=False
    ball.visible=True
    while True:
        ##halts computations briefly
        rate(10)
        ##changes ball position by adding velocity to position
        ##this is why a big velocity causes problems, makes position beyond borders
        ball.pos = ball.pos + ball.velocity
        ##conditionals check to see if the ball's x,y or z position is beyond the wall
        ##if one of them is, it flips that component of the velocity
        if ball.y - ball.radius < -positionNum:
            collide('y')
        if ball.y + ball.radius> positionNum:
            collide('y')
        if ball.x - ball.radius< -positionNum:
            collide('x')
        if ball.x + ball.radius> positionNum:
            collide('x')
        if ball.x-ball.radius < userPaddle.x+userPaddle.length/2 and ball.x + ball.radius > userPaddle.x-userPaddle.length/2 and ball.y - ball.radius < userPaddle.y + userPaddle.length/2 and ball.y + ball.radius > userPaddle.y - userPaddle.length/2 and ball.z+ball.radius > userPaddle.z and userTurnToHit:
            if ball.x>userPaddle.x+userPaddle.length/4 or ball.x<userPaddle.x-userPaddle.length/4:
                ball.velocity.x= (1.05)*ball.velocity.x
            if ball.y>userPaddle.y+userPaddle.height/4 or ball.y<userPaddle.y-userPaddle.length/4:
                ball.velocity.y= (1.05)*ball.velocity.y
            collide('z')
            userTurnToHit=False
        if ball.x - ball.radius < xyBackWall.x + xyBackWall.length/2 and ball.x + ball.radius > xyBackWall.x - xyBackWall.length/2 and ball. y - ball.radius < xyBackWall.y + xyBackWall.length/2 and ball.y + ball.radius > xyBackWall.y - xyBackWall.length/2 and ball.z -ball.radius < xyBackWall.z and not userTurnToHit:
            if ball.x>xyBackWall.x+xyBackWall.length/4 or ball.x<xyBackWall.x-xyBackWall.length/4:
                ball.velocity.x= (1.05)*ball.velocity.x
            if ball.y>xyBackWall.y+xyBackWall.height/4 or ball.y<xyBackWall.y-xyBackWall.length/4:
                ball.velocity.y= (1.05)*ball.velocity.y
            collide('z')
            userTurnToHit=True
        if ball.z - ball.radius < -positionNum - 2*ball.radius:
            quit()
        if ball.z + ball.radius > positionNum + 2*ball.radius:
            quit()
        ##very basic implementation of final AI
        ##will attempt to fix lag and ability of AI later on
        moveAI()
        if scene.kb.keys:
            keyPressed = scene.kb.getkey()
            move(keyPressed)
            



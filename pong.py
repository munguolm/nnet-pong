from __future__ import division
import pygame, sys, random, copy, math, pprint
from pygame.locals import *





WINDOWWIDTH = 600
WINDOWHEIGHT = 600
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20
RANDOMDIR=[-1,1]
# Set up the colours
BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)
'''
Ok, there's a lot going on in this project. First, one should take note of the modules I'm importing-- It's all basic
stuff. There's four components to this project: a multilayer perceptron, a black box optimization algorithm (Hill Climbing),
and a pong environment, and a reward function. More on each as they show up, but the last two are merged together.
I parted from a very basic pong game
(http://trevorappleton.blogspot.com/2014/04/writing-pong-using-python-and-pygame.html),
and pretty much overhauled it. If you inspect the code you'll notice the frame is similar but the mechanics are all mine,
and I also did some aesthetic tweaks.
The Hill Climbing algorithm pseudocode I obtained from wikipedia. https://en.wikipedia.org/wiki/Hill_climbing
Multilayer perceptron I made myself parting from knowledge from class.
'''


'''
this method takes a compatible perceptron layer, evaluates it over time and and returns a fitness score after a time
or negative score threshold has been reached. This is the fitness function used to train the perceptron.
This method is similar to the game but it doesn't display anything in order to make it faster
'''
def test(aartificialIntelligence):



    pygame.init()
    global DISPLAYSURF
    global ballDirX
    global ballDirY
    global score
    global time
    global speedx
    global speedy
    global col
    global ball
    speedx=3
    speedy=3
    col=0
    time = 0
    #Initiate variable and set starting positions
    #any future changes made within rectangles
    ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
    ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE)//2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE)//2
    score = 0
    #Keeps track of ball direction
    ballDirX = -1 ## -1 = left 1 = right
    ballDirY = -1 ## -1 = up 1 = down
    #Creates Rectangles for ball and paddles.
    paddle1 = pygame.Rect(PADDLEOFFSET,playerOnePosition, LINETHICKNESS,PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS,PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)
    #Draws the starting position of the Arena
    pygame.mouse.set_visible(0) # make cursor invisible

    paddlespeed=3
    while True: #main game loop
        states=(paddle1.y,ball.y,ball.x,speedx,speedy,ballDirX,ballDirY)
        #if first output is 1, and second output is 0, go up. If first output is 1 and second is 1, do nothing
        #If first is 0 and second is 1, go down.
        os=aartificialIntelligence.activate(states)
        move=os[0]-os[1]
        '''
        if move!=0:
            paddle1.y=paddle1.y+move
            print('it moves')
            score+=1
            '''
        if move==0:
            score-=1

        paddle2 = artificialIntelligence(ball, ballDirX, paddle2)
        time+=1
        if time%speedx == 0:

            checkHitBall(score, ball, paddle1, paddle2, ballDirX,speedx,0)
            checkEdgeCollision(ball, ballDirX, ballDirY)
            ball = moveBallDirX(ball, ballDirX)
        if time%speedy == 0:

            checkEdgeCollision(ball, ballDirX, ballDirY)
            ball = moveBallDirY(ball, ballDirY)
        if time >= 50:
            sum=0
            for x in aartificialIntelligence.nodesAndWeights:
                for y in x:
                    for z in y:
                        sum+=abs(z)
            return score-(sum/1000)
        '''
        if score <= -1000:
            return score
            '''




'''
pretty much the same as the original
'''
#Draws the arena the game will be played in.

def drawArena():
    DISPLAYSURF.fill((0,0,0))
    #Draw centre line
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH//2),0),((WINDOWWIDTH//2),WINDOWHEIGHT), (LINETHICKNESS//4))

'''
pretty much the same as the original
'''
#Draws the paddle
def drawPaddle(paddle):
    #Stops paddle moving too low
    if paddle.bottom > WINDOWHEIGHT:
        paddle.bottom = WINDOWHEIGHT
    #Stops paddle moving too high
    elif paddle.top < 20:
        paddle.top = 20
    #Draws paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

'''
pretty much the same as the original
'''
#draws the ball
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)
'''
pretty much the same as the original
'''
#moves the ball returns new position
def moveBallDirX(ball, ballDir):
    ball.x += ballDir
    return ball
'''
pretty much the same as the original
'''
def moveBallDirY(ball, ballDir):
    ball.y += ballDir
    return ball

'''
I remade this
'''
#Checks for a collision with a wall, and 'bounces' ball off it.
#Returns new direction
def checkEdgeCollision(ball, balldirX, balldirY):
    global ballDirY
    global ballDirX
    global speedx
    global speedy
    if ball.top <= 0:
        ballDirY = 1
        ball.top=0
    if ball.bottom >= WINDOWHEIGHT:
        ball.bottom-=1
        ballDirY = -1

    #Gotta make it spawn a new ball
    if ball.left == 0 or ball.right == WINDOWWIDTH :
        ballDirX = random.choice(RANDOMDIR)*balldirX
        ballDirY = random.choice(RANDOMDIR)*balldirY
        ball.x= WINDOWWIDTH/2 - LINETHICKNESS/2
        ball.y= random.randrange(0,WINDOWHEIGHT)
        speedx=10
        speedy=random.randrange(10,30)

#I made this
def length(obj):
    return obj.bottom-obj.top
'''
I remade this
'''
#Checks is the ball has hit a paddle, and 'bounces' ball off it.
def checkHitBall(Score1,ball, paddle1, paddle2, balldirX,speedX,Score2,notTest=0):
    global score

    global ballDirX
    global ballDirY
    global speedy
    global speedx
    global col

    if balldirX == -1 and paddle1.right == ball.left and paddle1.top < ball.bottom and paddle1.bottom > ball.top:
        col+=1
        col=col%2
        ballDirX=1
        if col==0 and speedx>2:
            speedx=speedX-2
        #hits upper half of left paddle
        if middle(ball)<middle(paddle1):
            ballDirY=(-1)

            speedy=int(((ball.bottom-paddle1.top)/(length(paddle1)/2))*(speedx+10))


        #hits lower half of left paddle
        else:
            ballDirY=1
            speedy=int(((paddle1.bottom-ball.top)/(length(paddle1)/2))*(speedx+10))
            if speedy<=speedx/2:
                speedy=speedx/2

    elif balldirX == 1 and paddle2.left == ball.right and paddle2.top < ball.bottom and paddle2.bottom > ball.top:
        col+=1
        col=col%2
        ballDirX=-1
        if col==0 and speedx>2:
            speedx=int(speedX-2)
        if middle(ball)<middle(paddle2):
            ballDirY=(-1)

            speedy=int(((ball.bottom-paddle2.top)/(length(paddle2)/2))*(speedx+10))
            if speedy<=speedx/2:
                speedy=speedx/2

        else:
            ballDirY=1
            speedy=int(((paddle2.bottom-ball.top)/(length(paddle2)/2))*(speedx+10))
            if speedy<=speedx/2:
                speedy=speedx/2
    if speedy<1:
        speedy=1
    if speedx<1:
        speedx=1

    score = checkPointScored(paddle1,ball,Score1,1)
    if notTest:
        global score2
        score2= checkPointScored(paddle2,ball,Score2)
'''
Remade this
'''
def checkPointScored(paddle,ball,score, player=0):
    if ball.left == 0:
        if player:
            return score-10
        else:
            return score+10
    #1 point for hitting the ball
    elif player==1 and paddle.right == ball.left and paddle.top < ball.bottom and paddle.bottom > ball.top:

        return score+1
    elif player ==0 and paddle.left == ball.right and paddle.top < ball.bottom and paddle.bottom > ball.top:

        return score+1
    #5 points for beating the other paddle
    elif ball.right == WINDOWWIDTH:
        if player:
            return score + 10
        else:
            return score-10
    #if no points scored, return score unchanged
    else: return score

#Made this
def middle(obj):
    return (obj.top+obj.bottom)//2

#This bot will always hit it back if it can.
def artificialIntelligence(ball, ballDirX, paddle2):
    #If ball is moving away from paddle, center bat
    if ballDirX == -1:
        if paddle2.centery < (WINDOWHEIGHT/2):
            paddle2.y += 1
        elif paddle2.centery > (WINDOWHEIGHT/2):
            paddle2.y -= 1
    #if ball moving towards bat, track its movement.
    elif ballDirX == 1:
        if paddle2.centery < ball.centery:
            paddle2.y += 1
        else:
            paddle2.y -=1
    return paddle2
def sigmoid(gamma):
        return (1 / (1 + math.exp(-gamma)))
#basic multilayer perceptron
class NeuralNet():

    def __init__(self,nodesAndWeights):
        self.nodesAndWeights=nodesAndWeights.copy()
    def sigmoid(self,gamma):
        if gamma < 0:
            if 1 - 1 / (1 + math.exp(gamma))>0:
                return 1
            else: return 0
        if 1 / (1 + math.exp(-gamma))>0:
            return 1
        else: return 0


    def activate(self, inputs):

        for layer in range(len(self.nodesAndWeights)):
            nextLayer= []
            val=0
            for weights in range(len(self.nodesAndWeights[layer])):


                for w in range(len(inputs)):
                    val+=inputs[w]*self.nodesAndWeights[layer][weights][w]
                val+=self.nodesAndWeights[layer][weights][-1]
                nextLayer.append(self.sigmoid(val))
            inputs=copy.copy(nextLayer)
        temp=[]
        for x in inputs:
            temp.append(self.sigmoid(x))
        return temp

def displayScore(score,player=0):
        resultSurf = BASICFONT.render('%s' %(score), True, WHITE)
        resultRect = resultSurf.get_rect()
        if player:

            resultRect.topleft = (WINDOWWIDTH-150, 25)
            DISPLAYSURF.blit(resultSurf, resultRect)
        else:
            resultRect.topleft = (150, 25)
            DISPLAYSURF.blit(resultSurf, resultRect)


'''
Adapted for this purpose from wikipedia
Black box optimizer
Makes a fully connected biased perceptron layer, optimizes it, and returns optimized weights for a perceptron with given
inputs, layers, and outputs
'''
def HillClimbing(steps,inputs, layers, outputs, args=0):
    if args:
        currentWeights=copy.copy(args)
    else:
        currentWeights=[]
        #initial weights
        for layer in range(layers):
            currentWeights.append([])
            for foo in range(inputs):
                currentWeights[layer].append([])
                for input in range(inputs+1):
                    currentWeights[layer][foo].append(0)
        output=[]
        currentWeights.append([])
        for y in range(inputs+1):
            output.append(0)
        for x in range(outputs):
            currentWeights[-1].append(output)

    stepSize = []
    #initial steps
    for layer in range(layers):
        stepSize.append([])
        for foo in range(inputs):
            stepSize[layer].append([])
            for input in range(inputs+1):
                stepSize[layer][foo].append(1)
    stepSize.append([])
    output=[]
    for y in range(inputs+1):
        output.append(1)
    for x in range(outputs):
        stepSize[-1].append(output)
    acceleration = 1.2
    # a value such as 1.2 is common
    candidate=[-acceleration,-1 / acceleration,0,1 / acceleration,acceleration]
    count=0
    while True:
        for currentLayer in range(len(currentWeights)):
            for i in range(len(currentWeights[currentLayer])):
                for currentweight in range(len(currentWeights[currentLayer][i])):
                    best = -1
                    bestScore = -10000
                    val=0
                    for j in range(4):         # try each of 5 candidate locations
                        currentWeights[currentLayer][i][currentweight] = currentWeights[currentLayer][i][currentweight] + stepSize[currentLayer][i][currentweight] * candidate[j]
                        temp=[]
                        for x in range(3):
                            temp.append(test(NeuralNet(currentWeights)))
                        temp=min(temp)

                        currentWeights[currentLayer][i][currentweight] = currentWeights[currentLayer][i][currentweight] - stepSize[currentLayer][i][currentweight] * candidate[j]
                        if(temp > bestScore):
                            bestScore = temp
                            best = j
                        if best ==2:
                            stepSize[currentLayer][i][currentweight] /= acceleration
                        else:
                            currentWeights[currentLayer][i][currentweight] = currentWeights[currentLayer][i][currentweight] + stepSize[currentLayer][i][currentweight] * candidate[best]
                            stepSize[currentLayer][i][currentweight] = stepSize[currentLayer][i][currentweight] * candidate[best] # accelerate


        count+=1
        print('step ',count,' score ',bestScore)
        print(currentWeights)






#Main function. You are player 2!

def main(args=0):
    if args==0:
        nnet=NeuralNet(HillClimbing(7,1,2))
    else:
        nnet=NeuralNet(args)
    pygame.init()
    global DISPLAYSURF
    global FPS
    global ballDirX
    global ballDirY
    global score

    ##Font information
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    FPS = 100000
    global speedx
    global speedy
    global col
    global score2
    speedx=8
    speedy=8
    col=0
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('Pong')
    #Initiate variable and set starting positions
    #any future changes made within rectangles
    ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
    ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE)//2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE)//2
    score = 0
    score2 = 0
    #Keeps track of ball direction
    ballDirX = -1 ## -1 = left 1 = right
    ballDirY = -1 ## -1 = up 1 = down
    #Creates Rectangles for ball and paddles.
    paddle1 = pygame.Rect(PADDLEOFFSET,playerOnePosition, LINETHICKNESS,PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS,PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)
    #Draws the starting position of the Arena
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)
    pygame.mouse.set_visible(0) # make cursor invisible
    time=0
    paddlespeed=3
    movey=0
    while True: #main game loop
        states=(paddle1.y,ball.y,ball.x,speedx,speedy,ballDirX,ballDirY)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # mouse movement commands
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                if event.type==pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        movey=-1
                    elif event.key == pygame.K_DOWN:
                        movey=1
                elif event.key in (pygame.K_UP, pygame.K_DOWN):
                    movey = 0
        if time%paddlespeed==0:
            os=nnet.activate(states)
            print(os)
            move=os[0]-os[1]
            if move!=0:
                paddle1.y=paddle1.y+move
                score-=0.001
            paddle2.y+=movey


        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        displayScore(score)
        drawBall(ball)
        time+=1
        if time%speedx == 0:
            ball = moveBallDirX(ball, ballDirX)
            checkHitBall(score, ball, paddle1, paddle2, ballDirX,speedx,score2)
            checkEdgeCollision(ball, ballDirX, ballDirY)

        if time%speedy == 0:
            ball = moveBallDirY(ball, ballDirY)
            checkEdgeCollision(ball, ballDirX, ballDirY)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        if time == 100000:
            return score

if __name__=='__main__':
    #After 3 hours of training it came up with this. For 7 inputs + bias, 1 layer, 2 outputs
    weights=[[[47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599], [47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599], [47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599], [47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599], [47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599], [47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599], [47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599, 47.49660268953599]], [[470.9810832203448, 470.9810832203448, 470.9810832203448, 470.9810832203448, 470.9810832203448, 470.9810832203448, 470.9810832203448, 470.9810832203448], [470.9810832203448, 470.9810832203448, 470.9810832203448, 470.9810832203448, 470.9810832203448, 470.9810832203448, 470.9810832203448, 470.9810832203448]]]#This will do a single run of the hillclimbing algorithm
    print(HillClimbing(10,7,1,2))
    #with this you can play against the computer as player 2 if it ever gets to run.
    main(weights)
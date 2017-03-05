import pygame, sys
from pygame.locals import *
from time import sleep

# Number of frames per second
FPS = 200

#Global Variables to be used through our program
WINDOWWIDTH = 1080
WINDOWHEIGHT = 720
LINETHICKNESS = 10
PADDLESIZE = 100
PADDLEOFFSET = 50
POWERUP_SIZE = 50

# Set up the colours
BLACK = (0  ,0  ,0  )
WHITE = (255,255,255)
RED = (255, 0, 0)

#Draws the arena the game will be played in.
def drawArena():
    DISPLAYSURF.fill((0,0,0))
    #Draw outline of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), LINETHICKNESS*2)
    #Draw centre line
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2),75),((WINDOWWIDTH/2),WINDOWHEIGHT), 1)

#Draws the paddle
def drawPaddle(paddle):
    #Stops paddle moving too low
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    #Stops paddle moving too high
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    #Draws paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

#draws the ball
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)

def drawPowerup():
    # creating a rectangle
    powerup = pygame.Rect((WINDOWWIDTH/2) - (POWERUP_SIZE/2),(WINDOWHEIGHT/2) - (POWERUP_SIZE/2), POWERUP_SIZE,POWERUP_SIZE)
    # draw powerup
    pygame.draw.rect(DISPLAYSURF, RED, powerup)

#moves the ball returns new position
def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return ball

#Checks for a collision with a wall, and 'bounces' ball off it.
#Returns new direction
def checkHitWall(ball, ballDirX, ballDirY):
    isGameOver = False

    # if ball flies off top or bottom
    if ball.top <= (LINETHICKNESS) or ball.bottom >= (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY = ballDirY * -1

    # if ball flies off left or right side
    if ball.left <= (LINETHICKNESS):
        isGameOver = True

    if ball.right >= (WINDOWWIDTH - LINETHICKNESS):
        ballDirX = ballDirX * -1

    return ballDirX, ballDirY, isGameOver

#Checks is the ball has hit a paddle, and 'bounces' ball off it.
def checkHitPaddle(ball, paddle1, paddle2, ballDirX, ballDirY):
    # if ball is going left and ball is on left paddle
    if ballDirX < 0 and paddle1.right >= ball.left and paddle1.left <= ball.right and paddle1.top <= ball.top and paddle1.bottom >= ball.bottom:
        paddle_mid = (paddle1.top + (PADDLESIZE/2))/2
        # note: this is contact point
        ball_mid = (ball.top + (LINETHICKNESS/2))/2
        ballDirY = ball_mid - paddle_mid
        return (-ballDirX, ballDirY)

    # if ball is going right and ball is on right paddle
    elif ballDirX > 0 and paddle2.left <= ball.right and paddle2.right >= ball.left and paddle2.top <= ball.top and paddle2.bottom >= ball.bottom:
        paddle_mid = (paddle2.top + (PADDLESIZE/2))/2
        # note: this is contact point
        ball_mid = (ball.top + (LINETHICKNESS/2))/2
        ballDirY = ball_mid - paddle_mid
        return (-ballDirX, ballDirY)

    else: 
        return (ballDirX, ballDirY)

def checkHitPowerup(ball, ballDirX, ballDirY, isPowerupAvailable):
    powerup_left = (WINDOWWIDTH/2) - (POWERUP_SIZE/2)
    powerup_right = powerup_left + POWERUP_SIZE
    powerup_top = (WINDOWHEIGHT/2) - (POWERUP_SIZE/2)
    powerup_bottom = powerup_top + POWERUP_SIZE

    # If powerup is available and the ball hits it
    if isPowerupAvailable and powerup_right >= ball.left and powerup_left <= ball.right and powerup_top <= ball.top and powerup_bottom >= ball.bottom:
        isPowerupAvailable = False
        ballDirX *=2
        ballDirY *=2

    return (ballDirX, ballDirY, isPowerupAvailable)

#Checks to see if a point has been scored returns new score
def checkPointScored(paddle1, ball, score, ballDirX):
    #reset points if left wall is hit
    if ball.left <= LINETHICKNESS:
        score = score
    #1 point for hitting the ball
    elif ballDirX < 0 and paddle1.right >= ball.left and paddle1.left <= ball.right and paddle1.top <= ball.top and paddle1.bottom >= ball.bottom:
        score += 1
    #5 points for beating the other paddle
    elif ball.right >= WINDOWWIDTH - LINETHICKNESS:
        score += 5

    return score

#Artificial Intelligence of computer player
def artificialIntelligence(ball, ballDirX, paddle2):
    # perfect ai
    paddle2.y = ball.y - (PADDLESIZE/2)
    return paddle2

#Displays the current score on the screen
def displayScoreBoard(score):
    header = BASICFONT.render('Andrews Amazing Game', True, WHITE)
    headerRect = header.get_rect()
    headerRect.topleft = (WINDOWWIDTH/2 - 125, 25)
    DISPLAYSURF.blit(header, headerRect)

    resultSurf = BASICFONT.render('Score: %s' %(score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH/2 - 50, 50)
    DISPLAYSURF.blit(resultSurf, resultRect)

def drawGameOver(name, score):
    DISPLAYSURF.fill((0,0,0))
    pygame.display.update()

    header = BASICFONT.render('Hi ' + name + ', Game over!', True, WHITE)
    headerRect = header.get_rect(center=(WINDOWWIDTH/2, WINDOWHEIGHT/2))
    DISPLAYSURF.blit(header, headerRect)

    resultSurf = BASICFONT.render('Score:' + score, True, WHITE)
    resultRect = resultSurf.get_rect(center=(WINDOWWIDTH/2, WINDOWHEIGHT/2 + 50))
    DISPLAYSURF.blit(resultSurf, resultRect)

#Main function
def main():
    print("Please Enter Your Name:")
    name = input()

    if name.lower() == "ethan eisenstein":
        print(name + " sucks")
    else:
        print(name + " rocks")

    pygame.init()
    global DISPLAYSURF
    ##Font information
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('Pong')

    #Initiate variable and set starting positions
    #any future changes made within rectangles
    ballX = WINDOWWIDTH/2 - LINETHICKNESS*4
    ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) /2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) /2
    score = 0

    # sign = direction, magnitude = speed
    ballDirX = -10 ## -1 = left 1 = right
    ballDirY = -5 ## -1 = up 1 = down

    # Creates Rectangles for ball and paddles.
    paddle1 = pygame.Rect(PADDLEOFFSET,playerOnePosition, LINETHICKNESS,PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS,PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

    #Draws the starting position of the Arena
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)

    pygame.mouse.set_visible(0) # make cursor invisible

    isPowerupAvailable = True
    isGameOver = False

    while True:
        for event in pygame.event.get():
            # gets all keys that are pressed
            pressed = pygame.key.get_pressed()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # mouse movement commands
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey
            elif pressed[pygame.K_w]:

                isGameOver = False
                ball.x = WINDOWWIDTH/2 - LINETHICKNESS*4
                ball.y = WINDOWHEIGHT/2 - LINETHICKNESS/2

        if not isGameOver:
            drawArena()
            drawPaddle(paddle1)
            drawPaddle(paddle2)
            drawBall(ball)

            if isPowerupAvailable:
                drawPowerup()

            ball = moveBall(ball, ballDirX, ballDirY)
            ballDirX, ballDirY, isGameOver = checkHitWall(ball, ballDirX, ballDirY)
            score = checkPointScored(paddle1, ball, score, ballDirX)
            ballDirX, ballDirY = checkHitPaddle(ball, paddle1, paddle2, ballDirX, ballDirY)
            ballDirX, ballDirY, isPowerupAvailable = checkHitPowerup(ball, ballDirX, ballDirY, isPowerupAvailable)

            # Andrew: uncomment this and comment the mouse elif statements on line 140-142 to switch to two perfect ai
            # paddle1 = artificialIntelligence (ball, ballDirX, paddle1)
            paddle2 = artificialIntelligence (ball, ballDirX, paddle2)

            displayScoreBoard(score)
        else:
            drawGameOver(name, str(score))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    pygame.quit()
    sys.exit()

# if you're running this script from the command line
if __name__=='__main__':
    main()

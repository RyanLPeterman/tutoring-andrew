import pygame, sys
from pygame.locals import *

# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 900000000000

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
def checkEdgeCollision(ball, ballDirX, ballDirY):
    # if ball flies off top or bottom
    if ball.top <= (LINETHICKNESS) or ball.bottom >= (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY = ballDirY * -1
    # if ball flies off left or right side
    if ball.left <= (LINETHICKNESS) or ball.right >= (WINDOWWIDTH - LINETHICKNESS):
        ballDirX = ballDirX * -1
    return ballDirX, ballDirY

#Checks is the ball has hit a paddle, and 'bounces' ball off it.
def checkHitBall(ball, paddle1, paddle2, ballDirX, ballDirY):
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
        return (-ballDirX, ballDirY)
    else: 
        return (ballDirX, ballDirY)

def checkHitPowerup(ball, ballDirX, ballDirY, isPowerupAvailable):
    powerup_left = (WINDOWWIDTH/2) - (POWERUP_SIZE/2)
    powerup_right = powerup_left + POWERUP_SIZE
    powerup_top = (WINDOWHEIGHT/2) - (POWERUP_SIZE/2)
    powerup_bottom = powerup_top + POWERUP_SIZE

    if isPowerupAvailable and powerup_right >= ball.left and powerup_left <= ball.right and powerup_top <= ball.top and powerup_bottom >= ball.bottom:
        isPowerupAvailable = False
        ballDirX *=2
        ballDirY *=2

    return (ballDirX, ballDirY, isPowerupAvailable)

#Checks to see if a point has been scored returns new score
def checkPointScored(paddle1, ball, score, ballDirX):
    #reset points if left wall is hit
    if ball.left <= LINETHICKNESS:
        score = 0
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

#Main function
def main():
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

    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # mouse movement commands
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey

        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)

        if isPowerupAvailable:
            drawPowerup()

        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        score = checkPointScored(paddle1, ball, score, ballDirX)
        ballDirX, ballDirY = checkHitBall(ball, paddle1, paddle2, ballDirX, ballDirY)
        ballDirX, ballDirY, isPowerupAvailable = checkHitPowerup(ball, ballDirX, ballDirY, isPowerupAvailable)

        # Andrew: uncomment this and comment the mouse elif statements on line 140-142 to switch to two perfect ai
        # paddle1 = artificialIntelligence (ball, ballDirX, paddle1)
        paddle2 = artificialIntelligence (ball, ballDirX, paddle2)

        displayScoreBoard(score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()

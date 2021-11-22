import random
import sys
import pygame
from pygame.locals import *


FPS = 32

SCREENWIDTH = 289

SCREENHEIGHT = 511

SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

GROUNDY = SCREENHEIGHT * 0.8

GAME_SPRITES = {}

PLAYER = 'gallery/sprites/bird.png'

BACKGROUND = 'gallery/sprites/background.jpg'

PIPE = 'gallery/sprites/pipe.jpg'

def welcomeScreen():

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():

            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery ))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey ))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY ))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def maingame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0


    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()


    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccvplayerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)

        if crashTest:
            return


        playerMidPos = playerx +GAME_SPRITES['PLAYER'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] =GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is{score}")
            GAME_SOUNDS['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
             playerFlapped = False
        playerHeight = GAME_SPRITES ['player'].get_height()
        player = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        for upperPipe , lowrpipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerpipe['x'] += pipeVelX

        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowePipes.append(newpipe[1])    


        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)


        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['PIPE'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['PIPE'][1], (lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digits].get_width()
        Xoffset = (SCREENWIDTH -width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['NUMBERS'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)



def isCollide(playerx, playery, upperPipes, lowePipes):
    if playery> GROUNDY -25 or player<0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperPipes:
        pipeheight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True 
    for pipe in lowerPipes:
        if (player +GAME_SPRITES['PLAYER'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
                  
    return False

def getRandomPipe():

    pipeheight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe                    
                
    




if __name__ == "__main__":

    pygame.init()

    FPSCLOCK = pygame.time.clock()

    pygame.display.set_caption('This Game By Prince')

    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/th.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/th(1).jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/th(2).jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/th(3).jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/th(4).jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/th(5).jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/th(6).jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/th(7).jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/th(8).jpg').convert_alpha(),     
        pygame.image.load('gallery/sprites/th(9).jpg').convert_alpha(),
    )


    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message.jpg').convert_alpha() 

    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.jpg') .convert_alpha()

    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180),

    pygame.image.load(PIPE).convert_alpha()
    )


    ({})['die'] = pygame.mixer.sound('gallery/audio/die.mp3')
    ({})['hit'] = pygame.mixer.sound('gallery/audio/hit.mp3')
    ({})['point'] = pygame.mixer.sound('gallery/audio/point.mp3')
    ({})['swoosh'] = pygame.mixer.sound('gallery/audio/swoosh.mp3')
    ({})['wing'] = pygame.mixer.sound('gallery/audio/wing.mp3')


    GAME_SPRITES['BACKGROUND'] = pygame.image.load(BACKGROUND).convert()

    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()
        mainGame() 



     


     




     

     

            

     

    

     


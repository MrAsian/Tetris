import os
import pygame
from TetrisBlocks import *

def draw_block(screen, block, x, y):
    for row in range(len(block.dimensions[block.direction])):
        for col in range(len(block.dimensions[block.direction][row])):
            if block.dimensions[block.direction][row][col]:
                screen.blit(block.currentColor, (col * 25 + x, row * 25 + y))

def undraw_block(screen, block, x, y):
    for row in range(len(block.dimensions[block.direction])):
        for col in range(len(block.dimensions[block.direction][row])):
            if block.dimensions[block.direction][row][col]:
                pygame.draw.rect(screen, (0, 0, 0), (col * 25 + x, row * 25 + y, 25, 25), 0)

def draw_reserve_block(screen, block, dim, backgroundColor = (0, 0 ,0)):
    pygame.draw.rect(screen, backgroundColor, dim, 0)
    drawReserveAtX = dim[0] + (dim[2] / 2) - (len(block.dimensions[block.direction][0]) * 25 / 2)
    drawReserveAtY = dim[1] + (dim[3] / 2) - (len(block.dimensions[block.direction]) * 25 / 2)
    draw_block(screen, block, drawReserveAtX, drawReserveAtY)

def draw_score(screen, score, font, dim, backgroundColor = (0, 0, 0), textColor = (255, 255, 255)):
    scoreString = str(score)
    label = font.render(scoreString, 1, textColor)
    pygame.draw.rect(screen, backgroundColor, dim, 0)
    screen.blit(label, (dim[0] + dim[2] - font.size(scoreString)[0] - 4, dim[1]))

def draw_text_label(screen, font, dimReserve = (0, 0, 0, 0), dimScore = (0, 0, 0, 0), textColor = (255, 255, 255)):
    label = font.render("Next", 1, textColor)
    textSize = font.size("Next")
    screen.blit(label, (dimReserve[0] + (dimReserve[2] / 2) - (textSize[0] / 2), dimReserve[1] - textSize[1]))
    label = font.render("Score", 1, textColor)
    textSize = font.size("Score")
    screen.blit(label, (dimScore[0] + (dimScore[2] / 2) - (textSize[0] / 2), dimScore[1] - textSize[1]))

def draw_pause(screen, font, width, height, backgroundColor = (128, 128, 128), textColor = (255, 255, 255)):
    background = pygame.Surface((width, height))
    background.set_alpha(128)
    background.fill(backgroundColor)
    screen.blit(background, (0, 0))
    label = font.render("Paused", 1, textColor)
    screen.blit(label, ((width / 2) - (font.size("Paused")[0] / 2), 200))

def draw_gameover(screen, bigFont, smallFont, dim, backgroundColor = (0, 0, 0), textColor = (255, 255, 255)):
    background = pygame.Surface((dim[2], dim[3]))
    background.set_alpha(128)
    background.fill(backgroundColor)
    screen.blit(background, (20, 20))
    label = bigFont.render("Game", 1, textColor)
    screen.blit(label, (dim[0] + (dim[2] / 2) - (bigFont.size("Game")[0] / 2), 100))
    label = bigFont.render("Over", 1, textColor)
    screen.blit(label, (dim[0] + (dim[2] / 2) - (bigFont.size("Over")[0] / 2), 100 + bigFont.size("Game")[1]))
    label = smallFont.render("Return of Ganon", 1, textColor)
    screen.blit(label, (dim[0] + (dim[2] / 2) - (smallFont.size("Return of Ganon")[0] / 2), 300))


def main():
    pygame.init()

    clock = pygame.time.Clock()

    RED = 255,0,0
    ORANGE = 255,128,0
    YELLOW = 255,255,0
    GREEN = 0,255,0
    BLUE = 0,0,255
    VIOLET = 128,0,255
    GREY = 128,128,128
    WHITE = 255,255,255
    BLACK = 0,0,0

    logo = pygame.image.load(os.path.join("Graphics", "Logo.png"))
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Tetris")

    screen_width = 400
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    startScreen = pygame.image.load(os.path.join("Graphics", "Start.png"))
    frame = pygame.image.load(os.path.join("Graphics", "Frame.png"))
    greyPlay = pygame.image.load(os.path.join("Graphics", "GreyPlay.png"))
    redPlay = pygame.image.load(os.path.join("Graphics", "RedPlay.png"))
    greyExit = pygame.image.load(os.path.join("Graphics", "GreyExit.png"))
    redExit = pygame.image.load(os.path.join("Graphics", "RedExit.png"))

    gameX = 20
    gameY = 20
    gameWidth = 250
    gameHeight = 500
    GAMESCREEN = (gameX, gameY, gameWidth, gameHeight)
    backdropReserveX = 285
    backdropReserveY = 150
    backdropReserveWidth = 100
    backdropReserveHeight = 120
    BACKDROP_RESERVE = (backdropReserveX, backdropReserveY, backdropReserveWidth, backdropReserveHeight)
    backdropScoreX = 285
    backdropScoreY = 330
    backdropScoreWidth = 100
    backdropScoreHeight = 25
    BACKDROP_SCORE = (backdropScoreX, backdropScoreY, backdropScoreWidth, backdropScoreHeight)

    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    running = True
    enterKey = False
    leftKey = False
    rightKey = False
    downKey = False
    upKey = False
    zKey = False
    xKey = False
    spaceKey = False
    upReleased = True
    downReleased = False
    falldown = False
    rowToClear = []
    startScreenOptionSelectPlay = False

    smallFont = pygame.font.SysFont("monospace", 25, True, False)
    bigFont = pygame.font.SysFont("monospace", 50, True, False)
    score = 0

    gameState = "start"
    screen.blit(startScreen, (0, 0))

    reserveBlock = TetrisBlocks.randomBlock()

    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    enterKey = not enterKey
                if event.key == pygame.K_LEFT:
                    leftKey = True
                if event.key == pygame.K_RIGHT:
                    rightKey = True
                if event.key == pygame.K_UP:
                    upKey = True
                if event.key == pygame.K_DOWN:
                    downKey = True
                if event.key == pygame.K_SPACE:
                    spaceKey = True
                if event.key == pygame.K_z:
                    zKey = True
                if event.key == pygame.K_x:
                    xKey = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    leftKey = False
                if event.key == pygame.K_RIGHT:
                    rightKey = False
                if event.key == pygame.K_UP:
                    upKey = False
                    upReleased = True
                if event.key == pygame.K_DOWN:
                    downKey = False
                    downReleased = True
                if event.key == pygame.K_SPACE:
                    spaceKey = False
                if event.key == pygame.K_z:
                    zKey = False
                if event.key == pygame.K_x:
                    xKey = False
            if event.type == pygame.USEREVENT + 1:
                falldown = True

        if gameState == "start":
            if upReleased or downReleased:
                upReleased = False
                downReleased = False
                startScreenOptionSelectPlay = not startScreenOptionSelectPlay
                if startScreenOptionSelectPlay:
                    screen.blit(redPlay, (103, 290))
                    screen.blit(greyExit, (103, 414))
                else:
                    screen.blit(greyPlay, (103, 290))
                    screen.blit(redExit, (103, 414))
            if enterKey:
                enterKey = False
                if startScreenOptionSelectPlay:
                    gameState = "game"
                    screen.blit(frame, (0, 0))
                    frameUpper = screen.subsurface((gameX, 0, gameWidth, gameY))
                    frameUpper = frameUpper.copy()
                    frameLine = screen.subsurface((gameX, 10, gameWidth, 2))
                    frameLine = frameLine.copy()
                    pygame.draw.rect(screen, BLACK, GAMESCREEN, 0)
                    draw_score(screen, score, smallFont, BACKDROP_SCORE)
                    draw_text_label(screen, smallFont, BACKDROP_RESERVE, BACKDROP_SCORE)
                else:
                    running = False

        elif gameState == "game":
            if TetrisBlocks.newBlock:
                activeBlock = reserveBlock
                reserveBlock = TetrisBlocks.randomBlock()
                TetrisBlocks.newBlock = False
                draw_reserve_block(screen, reserveBlock, BACKDROP_RESERVE)
                delayFromFalling = 1

            undraw_block(screen, activeBlock, activeBlock.rect.x, activeBlock.rect.y)

            if leftKey:
                activeBlock.moveLeft(1)
                pygame.time.delay(100)
            if rightKey:
                activeBlock.moveRight(1)
                pygame.time.delay(100)
            if downKey:
                delayFromFalling = 0
                activeBlock.moveDown(1)
                pygame.time.delay(40)
            if zKey:
                activeBlock.rotate(-1)
                pygame.time.delay(120)
            if xKey or upKey:
                activeBlock.rotate(1)
                pygame.time.delay(120)
            if spaceKey:
                while activeBlock.moveDown(1):
                    pass
                pygame.time.delay(150)

            if falldown:
                if delayFromFalling == 0:
                    activeBlock.moveDown(1)
                else:
                    delayFromFalling -= 1
                falldown = False

            draw_block(screen, activeBlock, activeBlock.rect.x, activeBlock.rect.y)
            screen.blit(frameUpper, (gameX, 0))
            screen.blit(frameLine, (gameX, 118))

            rowToClear = TetrisBlocks.checkAndClear()
            if not len(rowToClear) == 0:
                gameState = "row clear"

            if TetrisBlocks.gameOver():
                gameState = "game over"
                draw_gameover(screen, bigFont, smallFont, GAMESCREEN)

            if enterKey:
                gameState = "pause"
                currentGameScreen = screen.copy()
                draw_pause(screen, bigFont, screen_width, screen_height)

        elif gameState == "row clear":
            for row in rowToClear:
                temp = screen.subsurface((gameX, gameY + 100, gameWidth, row * 25 - 100))
                temp = temp.copy()
                screen.blit(temp, (gameX, gameY + 125))
            pygame.draw.rect(screen, BLACK, (gameX, gameY + 100, gameWidth, 25))
            score += 100 * (len(rowToClear)**2)
            if score > 999999:
                score = 999999
            draw_score(screen, score, smallFont, BACKDROP_SCORE)
            gameState = "game"

        elif gameState == "pause":
            if not enterKey:
                gameState = "game"
                screen.blit(currentGameScreen, (0, 0))

        elif gameState == "game over":
            if enterKey:
                enterKey = False
                gameState = "start"
                screen.blit(startScreen, (0, 0))
                startScreenOptionSelectPlay = False
                upReleased = True
                TetrisBlocks.resetGrid()
                score = 0

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
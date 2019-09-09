import abc
import os
import random
import pygame

class TetrisBlocks(abc.ABC):
    newBlock = True
    grid = [[False for col in range(10)] for row in range(20)]

    @staticmethod
    def resetGrid():
        for row in range(len(TetrisBlocks.grid)):
            for col in range(len(TetrisBlocks.grid[0])):
                TetrisBlocks.grid[row][col] = False

    @staticmethod
    def gameOver():
        for topRow in range(len(TetrisBlocks.grid[0])):
            if TetrisBlocks.grid[3][topRow]:
                return True;
        return False;

    @staticmethod
    def checkAndClear():
        rowToClear = []
        for row in range(len(TetrisBlocks.grid)):
            thisRowFilled = True
            for col in range(len(TetrisBlocks.grid[row])):
                thisRowFilled = thisRowFilled and TetrisBlocks.grid[row][col]
                if not thisRowFilled:
                    break
            if thisRowFilled:
                rowToClear.append(row)
                currRow = row
                while (currRow > 0):
                    TetrisBlocks.grid[currRow] = list(TetrisBlocks.grid[currRow - 1])
                    currRow -= 1
        return rowToClear

    @staticmethod
    def randomBlock():
        blockNum = random.randint(0, 6)
        if blockNum == 0:
            return Block1()
        elif blockNum == 1:
            return Block2()
        elif blockNum == 2:
            return Block3()
        elif blockNum == 3:
            return Block4()
        elif blockNum == 4:
            return Block5()
        elif blockNum == 5:
            return Block6()
        elif blockNum == 6:
            return Block7()

    @staticmethod
    def pick_color():
        colorNum = random.randint(0, 7)
        return "Block" + str(colorNum) + ".png"

    def updateBlockX(self):
        self.west = int((self.rect.x - 20) / 25)
        self.east = int(self.west + len(self.dimensions[self.direction][0]) - 1)

    def updateBlockY(self):
        self.north = int((self.rect.y - 20) / 25)
        self.south = int(self.north + len(self.dimensions[self.direction]) - 1)

    def collideBlockWest(self):
        collideWest = False
        if self.west > 0:
            for col in range(len(self.dimensions[self.direction][0])):
                westEdgeAllTrue = True
                for row in range(len(self.dimensions[self.direction])):
                    row = len(self.dimensions[self.direction]) - row - 1
                    if self.west + col - 1 >= 0 and self.dimensions[self.direction][row][col] == True:
                        collideWest = collideWest or TetrisBlocks.grid[self.north + row][self.west + col - 1]
                    if westEdgeAllTrue and self.dimensions[self.direction][row][col] == False:
                        westEdgeAllTrue = False
                if westEdgeAllTrue:
                    break
        else:
            collideWest = True
        return collideWest

    def collideBlockEast(self):
        collideEast = False
        if self.east + 1 < len(TetrisBlocks.grid[0]):
            for col in range(len(self.dimensions[self.direction][0])):
                eastEdgeAllTrue = True
                col = len(self.dimensions[self.direction][0]) - col - 1
                for row in range(len(self.dimensions[self.direction])):
                    row = len(self.dimensions[self.direction]) - row - 1
                    if self.west + col + 1 < len(TetrisBlocks.grid[0]) and self.dimensions[self.direction][row][col] == True:
                        collideEast = collideEast or TetrisBlocks.grid[self.north + row][self.west + col + 1]
                    if eastEdgeAllTrue and self.dimensions[self.direction][row][col] == False:
                        eastEdgeAllTrue = False
                if eastEdgeAllTrue:
                    break
        else:
            collideEast = True
        return collideEast

    def collideBlockSouth(self):
        collideSouth = False
        if self.south + 1 < len(TetrisBlocks.grid):
            for row in range(len(self.dimensions[self.direction])):
                southEdgeAllTrue = True
                row = len(self.dimensions[self.direction]) - row - 1
                for col in range(len(self.dimensions[self.direction][0])):
                    if self.north + row >= 0 and self.dimensions[self.direction][row][col] == True:
                        collideSouth = collideSouth or TetrisBlocks.grid[self.north + 1 + row][col + self.west]
                    if self.dimensions[self.direction][row][col] == False:
                        southEdgeAllTrue = False
                if southEdgeAllTrue:
                    break
        else:
            collideSouth = True
        return collideSouth

    def moveLeft(self, distance):
        if not self.collideBlockWest():
            self.rect = self.rect.move(-25 * distance, 0)
            self.updateBlockX()
            return True
        return False

    def moveRight(self, distance):
        if not self.collideBlockEast():
            self.rect = self.rect.move(25 * distance, 0)
            self.updateBlockX()
            return True
        return False

    def moveDown(self, distance):
        if not self.collideBlockSouth():
            self.rect = self.rect.move(0, 25 * distance)
            self.updateBlockY()
            return True
        else:
            self.imprint(TetrisBlocks.grid)
        return False

    def rotate(self, rotateDirection):
        self.direction = (self.direction + rotateDirection) % len(self.dimensions)
        if self.north + len(self.dimensions[self.direction]) > 20:
            self.direction = (self.direction - rotateDirection) % len(self.dimensions)
        else:
            for row in range(len(self.dimensions[self.direction])):
                for col in range(len(self.dimensions[self.direction][0])):
                    if self.west + len(self.dimensions[self.direction][0]) - 10 > 0:
                        shiftLeft = self.west + len(self.dimensions[self.direction][0]) - 10
                    else:
                        shiftLeft = 0
                    if TetrisBlocks.grid[self.north + row][self.west + col - shiftLeft] == True:
                        self.direction = (self.direction - rotateDirection % len(self.dimensions))
                        return
        for shiftBackIntoBounds in range(self.west + len(self.dimensions[self.direction][0]) - 10):
            if not self.moveLeft(1):
                self.moveRight(1)
                self.direction = (self.direction - rotateDirection) % len(self.dimensions)
                break
        self.updateBlockX()
        self.updateBlockY()

    def imprint(self, grid):
        for row in range(len(self.dimensions[self.direction])):
            for col in range(len(self.dimensions[self.direction][row])):
                grid[row + self.north][col + self.west] = grid[row + self.north][col + self.west] or self.dimensions[self.direction][row][col]
        TetrisBlocks.newBlock = True


class Block1(TetrisBlocks): # square block
    def __init__(self):
        self.currentColor = pygame.image.load(os.path.join("Graphics", TetrisBlocks.pick_color()))
        self.rect = pygame.Rect(120, 70, 50, 50)
        self.direction = 0
        self.dimensions = [[[True, True], [True, True]]]
        self.updateBlockX()
        self.updateBlockY()

class Block2(TetrisBlocks): # T block
    def __init__(self):
        self.currentColor = pygame.image.load(os.path.join("Graphics", TetrisBlocks.pick_color()))
        self.rect = pygame.Rect(120, 70, 75, 50)
        self.direction = 0
        self.dimensions = [[[False, True, False], [True, True, True]],
                           [[True, False], [True, True], [True, False]],
                           [[True, True, True], [False, True, False]],
                           [[False, True], [True, True], [False, True]]]
        self.updateBlockX()
        self.updateBlockY()


class Block3(TetrisBlocks): # L block
    def __init__(self):
        self.currentColor = pygame.image.load(os.path.join("Graphics", TetrisBlocks.pick_color()))
        self.rect = pygame.Rect(120, 45, 50, 75)
        self.direction = 0
        self.dimensions = [[[True, False], [True, False], [True, True]],
                           [[True, True, True], [True, False, False]],
                           [[True, True], [False, True], [False, True]],
                           [[False, False, True], [True, True, True]]]
        self.updateBlockX()
        self.updateBlockY()

class Block4(TetrisBlocks): # reverse L block
    def __init__(self):
        self.currentColor = pygame.image.load(os.path.join("Graphics", TetrisBlocks.pick_color()))
        self.rect = pygame.Rect(120, 45, 50, 75)
        self.direction = 0
        self.dimensions = [[[False, True], [False, True], [True, True]],
                           [[True, False, False], [True, True, True]],
                           [[True, True], [True, False], [True, False]],
                           [[True, True, True], [False, False, True]]]
        self.updateBlockX()
        self.updateBlockY()

class Block5(TetrisBlocks): # Z block
    def __init__(self):
        self.currentColor = pygame.image.load(os.path.join("Graphics", TetrisBlocks.pick_color()))
        self.rect = pygame.Rect(120, 45, 75, 50)
        self.direction = 0
        self.dimensions = [[[False, True], [True, True], [True, False]],
                           [[True, True, False], [False, True, True]]]
        self.updateBlockX()
        self.updateBlockY()

class Block6(TetrisBlocks): # reverse Z block
    def __init__(self):
        self.currentColor = pygame.image.load(os.path.join("Graphics", TetrisBlocks.pick_color()))
        self.rect = pygame.Rect(120, 45, 75, 50)
        self.direction = 0
        self.dimensions = [[[True, False], [True, True], [False, True]],
                           [[False, True, True], [True, True, False]]]
        self.updateBlockX()
        self.updateBlockY()

class Block7(TetrisBlocks): # straight block
    def __init__(self):
        self.currentColor = pygame.image.load(os.path.join("Graphics", TetrisBlocks.pick_color()))
        self.rect = pygame.Rect(120, 20, 25, 100)
        self.direction = 0
        self.dimensions = [[[True], [True], [True], [True]],
                           [[True, True, True, True]]]
        self.updateBlockX()
        self.updateBlockY()

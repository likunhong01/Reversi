import random
# import os
import time
import pygame

# 搜索方向
SEARCH_DIRECTIONS = [
    [-1, -1],
    [0, -1],
    [1, -1],
    [-1, 0],
    [1, 0],
    [-1, 1],
    [0, 1],
    [1, 1]
]


class Reversi:
    def __init__(self):
        self.board = [[' ' for i in range(8)] for j in range(8)]
        self.board[3][3] = 'O'
        self.board[4][4] = 'O'
        self.board[3][4] = 'X'
        self.board[4][3] = 'X'

    # def print(self):
    #   # clean screen
    #   os.system('cls' if os.name == 'nt' else 'clear')
    #
    #   nRow = len(self.board)
    #   nCol = len(self.board[0])
    #
    #   print('  ', end='')
    #   for i in range(nCol):
    #     print(str(i), end='')
    #   print()
    #   print(' +--------+')
    #   for i in range(nRow):
    #     print(str(i) + '|', end='')
    #     for j in range(nCol):
    #       print(self.board[i][j], end='')
    #     print('|')
    #   print(' +--------+')

    def __isOnBoard(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def isValidMove(self, tile, r, c):
        r = int(r)
        c = int(c)
        if not self.__isOnBoard(r, c) or self.board[r][c] != ' ':
            return False
        otherTile = 'O' if tile == 'X' else 'X' # 对手棋子
        # 翻面列表
        tilesToFlip = []
        for rd, cd in SEARCH_DIRECTIONS:
            # 对周围每个位置搜索
            rm, cm = r, c
            rm += rd
            cm += cd
            # 搜索目标在棋盘范围且是对方棋子
            while self.__isOnBoard(rm, cm) and self.board[rm][cm] == otherTile:
                # 再往这个方向走一各
                rm += rd
                cm += cd
                # 如果还在棋盘内并且是自己的棋子
                if self.__isOnBoard(rm, cm) and self.board[rm][cm] == tile:
                    # 意味着这是个有效点，两点之间的所有棋子翻面
                    while True:
                        rm -= rd
                        cm -= cd
                        if r == rm and c == cm:
                            break
                        # 该翻面目标点加入列表
                        tilesToFlip.append([rm, cm])
        if len(tilesToFlip) == 0:
            return False
        return tilesToFlip

    def getTips(self, tile):
        tips = []
        for r in range(8):
            for c in range(8):
                hasTip = reversi.isValidMove(tile, r, c)
                if hasTip:
                    tips.append([r, c])
        return tips

    # 走动
    def makeMove(self, r, c, tile):
        tilesToFlip = self.isValidMove(tile, r, c)
        if not tilesToFlip:
            return False
        self.board[r][c] = tile
        for i, j in tilesToFlip:
            self.board[i][j] = tile
        return True

    # 获取数量
    def getScroe(self):
        play1 = 0
        play2 = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 'X':
                    play1 += 1
                elif self.board[i][j] == 'O':
                    play2 += 1
        return {'X': play1, 'O': play2}


# current = 'O'
# reversi = Reversi()
# reversi.print()
# while True:
#     if len(reversi.getTips(current)) == 0:
#         break
#     if current == 'X':
#         print(current + ' ' + str(reversi.getTips(current)))
#         r, c = input().split(',')
#         r = int(r)
#         c = int(c)
#         if reversi.isValidMove(current, r, c):
#             reversi.makeMove(r, c, current)
#             current = 'X' if current == 'O' else 'O'
#     else:
#         time.sleep(0.3)
#         tips = reversi.getTips(current)
#         random.shuffle( tips )
#         computerMove = tips[0]
#         for loc in tips:
#             if len(reversi.isValidMove(current, computerMove[0],
#                                        computerMove[1])) < len(reversi.isValidMove(current, loc[0], loc[1])) :
#                 computerMove = loc
#         reversi.makeMove(computerMove[0], computerMove[1], current)
#         current = 'X' if current == 'O' else 'O'
#     reversi.print()

# 定义颜色
BLACK = (77, 51, 0)
WHITE = (204, 136, 0)
RED = (255, 200, 0)
WIN_COLOR = (175, 175, 0)
LOSE_COLOR = (0, 102, 255)
TIP_COLOR = (255, 0, 255)

# 格子数
nRow = 8
nCol = 8

# 单元格之间的空白
MARGIN = 5

# 网格的宽高
WIDTH = 60
HEIGHT = 60

# 初始化pygame
pygame.init()
pygame.mixer.init()

# 设置屏幕高度和宽度
WINDOW_SIZE = [(MARGIN + WIDTH) * nCol + MARGIN,
               (MARGIN + HEIGHT) * nRow + MARGIN + 60]
screen = pygame.display.set_mode(WINDOW_SIZE)

# 循环直到关闭
done = False
gameLock = False
# 屏幕更新
clock = pygame.time.Clock()

# 背景音乐
# pygame.mixer.music.load('BGM.wav')
# pygame.mixer.music.set_volume(0.5)
# pygame.mixer.music.play(-1, 0.0)

# win = pygame.mixer.Sound('win.wav')
# lose = pygame.mixer.Sound('lose.wav')
# down = pygame.mixer.Sound('down.wav')

# 标题
pygame.display.set_caption("黑白棋")
# 随机电脑开始或者用户开始（用户黑色棋子）
current = 'X' if random.randint(0, 100) % 2 == 1 else 'O'
# current = 'X'
canChange = False  # 可以更改下棋的一方
hasFreeArea = False  # 有空位


# 初始化游戏类
reversi = Reversi()
# 打印初始化棋盘
# reversi.print()


# -------- 游戏下棋循环 -----------
while not done:
    # 用户走
    if current == 'X':
        for event in pygame.event.get():  # 用户触发事件
            if event.type == pygame.QUIT:  # 点击关闭
                done = True  # 结束标记，退出循环
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if gameLock:
                    done = True
                # 单击鼠标，获取位置
                pos = pygame.mouse.get_pos()
                # 换算网格坐标
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # 设置位置为1
                print("点击", pos, "，对应格子里: ", row, column)
                move = (row, column)
                if reversi.isValidMove(current, move[0], move[1]):
                    reversi.makeMove(move[0], move[1], current)
                    # down.play()
                    canChange = True

    # 电脑走
    if current == 'O':
        # 获取可以走的点
        tips = reversi.getTips(current)
        time.sleep(0.3 + 0.05 * len(tips))
        # random.shuffle(tips)
        if len(tips) > 0:
            computerMove = tips[0]
            for loc in tips:
                if len(reversi.isValidMove(current, computerMove[0], computerMove[1])) < len(
                        reversi.isValidMove(current, loc[0], loc[1])):
                    computerMove = loc

            reversi.makeMove(computerMove[0], computerMove[1], current)
            # down.play()
        canChange = True

    if done:
        break
    if not gameLock:
        if current == 'X' and not canChange:
            userTips = reversi.getTips('X')
        else:
            userTips = []
        # 设置背景
        screen.fill(BLACK)
        # 字体
        font = pygame.font.SysFont('Consoles', WIDTH + 5)

        # 画网格
        hasFreeArea = len(reversi.getTips('X')) != 0 or len(
            reversi.getTips('O')) != 0
        for row in range(nRow):
            for column in range(nCol):
                if [row, column] in userTips:
                    color = RED
                else:
                    color = WHITE

                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

                if reversi.board[row][column] == 'X':
                    color = (0, 0, 0)
                    pygame.draw.circle(screen, color, [(MARGIN + WIDTH) * column + MARGIN + int(WIDTH / 2),
                                                       (MARGIN + HEIGHT) * row + MARGIN + int(HEIGHT / 2)],
                                       int(HEIGHT / 2))
                elif reversi.board[row][column] == 'O':
                    color = (255, 255, 255)
                    pygame.draw.circle(screen, color, [(MARGIN + WIDTH) * column + MARGIN + int(WIDTH / 2),
                                                       (MARGIN + HEIGHT) * row + MARGIN + int(HEIGHT / 2)],
                                       int(HEIGHT / 2))
        pygame.draw.rect(screen,
                         (154, 205, 154),
                         [0,
                          WINDOW_SIZE[1] - 60,
                          (MARGIN + WIDTH) * nCol + MARGIN,
                          60])
        pygame.draw.circle(screen, (0, 0, 0), [0 + int(HEIGHT / 2),
                                               WINDOW_SIZE[1] - 30], int(HEIGHT / 3))
        pygame.draw.circle(screen, (255, 255, 255), [int(WINDOW_SIZE[1] / 2),
                                                     WINDOW_SIZE[1] - 30], int(HEIGHT / 3))
        score = reversi.getScroe()
        text = font.render(':{}'.format(score['X']), True, (0, 0, 0))
        screen.blit(text, (0 + int(HEIGHT / 2) * 2, WINDOW_SIZE[1] - 50))
        text = font.render(':{}'.format(score['O']), True, (0, 0, 0))
        screen.blit(text, (int(WINDOW_SIZE[1] / 2) +
                           int(HEIGHT / 2), WINDOW_SIZE[1] - 50))

        # 改变下一次移动
        if canChange:
            current = 'X' if current == 'O' else 'O'
            canChange = False

        # 判断输赢
        if not hasFreeArea:
            score = reversi.getScroe()
            # 用户赢
            if score['X'] > score['O']:
                font = pygame.font.SysFont('Consoles', WIDTH + 50)
                text = font.render('你赢了', True, WIN_COLOR)
                screen.blit(text, (10, 10))
                text = font.render('离开', True, TIP_COLOR)
                screen.blit(text, (50, 60))
                pygame.mixer.music.stop()
                # win.play(1)
            # 电脑赢
            elif score['X'] < score['O']:
                font = pygame.font.SysFont('Consoles', WIDTH + 50)
                text = font.render('你输了！', True, LOSE_COLOR)
                screen.blit(text, (10, 10))
                text = font.render('离开', True, TIP_COLOR)
                screen.blit(text, (20, 60))
                pygame.mixer.music.stop()
                # lose.play(1)
            else:
                font = pygame.font.SysFont('Consoles', WIDTH + 50)
                text = font.render('平局！', True, LOSE_COLOR)
                screen.blit(text, (10, 10))
                text = font.render('离开', True, TIP_COLOR)
                screen.blit(text, (20, 60))
            gameLock = True

    # 每秒60帧
    clock.tick(60)

    # 更新画布
    pygame.display.flip()

# 退出游戏
pygame.quit()

score = reversi.getScroe()
print("用户 : {0}   电脑 : {1}".format(score['X'], score['O']))

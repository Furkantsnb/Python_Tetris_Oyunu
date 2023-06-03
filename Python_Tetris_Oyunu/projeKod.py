import pygame
import random

s_w = 800
s_h = 700
oyun_w = 300
oyun_h = 600
blok_boyu = 30
yuzey = pygame.display.set_mode((s_w, s_h))
score = 0
top_left_x = (s_w - oyun_w) // 2
top_left_y = s_h - oyun_h
pygame.font.init()


S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, T, O, L, J, I]
shape_color = [(140, 250, 30), (255, 100, 100), (255, 255, 0), (255, 165, 0),(0, 0, 255), (0, 255, 0), (255, 0, 0)]


class Parca (object):
    rows = 20
    colmns = 10

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_color[shapes.index(shape)]
        self.rotation = 0


def izgara_olustur(locked_pos={} ):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if(j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


def sekil_donustur(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions


def oyun_sahasi(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = sekil_donustur(shape)

    for position in formatted:
        if position not in accepted_pos:
            if position[1] >-1:
                return False
    return True


def oyun_bitti(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def getir_parca():
    return Parca(5, 0, random.choice(shapes))


def yazı_bicimi(text, size, color, yuzey):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    yuzey.blit(label, (top_left_x+ oyun_w/2 - (label.get_width()/2),top_left_y+oyun_h/2 -(label.get_width()/2)))


def metin(yuzey, text, size, color):
    font = pygame.font.SysFont("helvetica", size, bold=True)
    label = font.render(text, 1, color)

    sx = top_left_x - 200
    sy = top_left_y + 200

    yuzey.blit(label, (sx + 10, sy - 250))


def grey_lines(yuzey, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(yuzey, (50, 50, 50), (sx, sy + i*blok_boyu), (sx + oyun_w, sy + i*blok_boyu))
        for j in range(len(grid[i])):
            pygame.draw.line(yuzey, (50, 50, 50), (sx + j * blok_boyu, sy), (sx + j * blok_boyu, sy + oyun_h))


def sat_temizle(grid, locked):
    inc = 0
    for i in range(len(grid) -1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key = lambda  x: x[1]) [::-1]:
            x, y =key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc


def siradaki_parca(shape, yuzey):
    font = pygame.font.SysFont("comicsans", 20)
    label = font.render("Siradaki Parca", 1,(255, 255, 255))
    sx = top_left_x + oyun_w + 50
    sy = top_left_y + oyun_h / 2 - 100

    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(yuzey, shape.color, (sx + j * 30, sy + i * 30, 30,30), 0)
    yuzey.blit(label, (sx + 10, sy - 30))

def skor_guncelle(nscore):
    score = yuksek_skor()

    with open("score.txt", "w") as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def yuksek_skor():
    with open("score.txt", "r") as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score

def oyun_ekrani(yuzey, grid, score = 0, son_skor = 0):
    yuzey.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 50, bold = TabError)
    label0 = font.render('TETRİS', 1, (0, 255, 0))

    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score' + str(score), 1, (255, 0, 0))

    sx = top_left_x + oyun_w + 50
    sy = top_left_y + oyun_h / 2 -100

    yuzey.blit(label, (sx + 20, sy + 160))

    yuzey.blit(label0, (top_left_x + oyun_w / 2 - (label0.get_width() / 2), 30))
    font1 = pygame.font.SysFont('helvetica', 20, bold = TabError)
    label1 = font1.render('Yuksek Skor' + son_skor, 1, (0, 255, 0))

    sx = top_left_x - 200
    sy = top_left_y + 200

    yuzey.blit(label1, (sx - 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(yuzey, grid[i][j],
                             (top_left_x + j * blok_boyu, top_left_y + i * blok_boyu, blok_boyu, blok_boyu), 0)

    pygame.draw.rect(yuzey, (0, 255, 0), (top_left_x, top_left_y, oyun_w, oyun_h), 5)
    grey_lines(yuzey, grid)


def main(yuzey):
    son_skor = yuksek_skor()
    locked_pos = {}
    grid = izgara_olustur(locked_pos)
    change_piece = False
    oyundevam = True
    current_piece = getir_parca()
    next_piece = getir_parca()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    score = 0

    while oyundevam:
        grid = izgara_olustur(locked_pos)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > fall_speed :
            fall_time = 0
            current_piece.y +=1

            if not (oyun_sahasi(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                oyundevam = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not oyun_sahasi(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not oyun_sahasi(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y +=1
                    if not oyun_sahasi(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not oyun_sahasi(current_piece, grid):
                        current_piece.rotation -= 1
                elif event.key == pygame.K_SPACE:
                    while oyun_sahasi(current_piece ,grid):
                        current_piece.y += 1
                    current_piece.y -= 1

        shape_pos = sekil_donustur(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_pos[p] = current_piece.color
                current_piece = next_piece
                next_piece = getir_parca()
                change_piece = False
                score += sat_temizle(grid, locked_pos) * 10
                sat_temizle(grid, locked_pos)

        oyun_ekrani(yuzey, grid, score, son_skor)
        siradaki_parca(current_piece, yuzey)
        pygame.display.update()
        if oyun_bitti(locked_pos):
            yazı_bicimi('Kaybettin', 80, (250, 0, 0), yuzey)
            pygame.display.update()
            pygame.time.delay(1500)
            oyundevam = False
            skor_guncelle(score)
    pygame.display.quit()



def main_menu(yuzey):
    calistir = True
    while calistir:
        yuzey.fill((0, 0, 0))
        metin(yuzey, "Baslamak İçin Entre Basiniz", 60, (255, 255, 255))
        font = pygame.font.SysFont('comicsans', 100, bold = True)
        font1 = pygame.font.SysFont('helvetica', 50, bold = True)

        label = font.render("TETRİS", 1, (0, 255, 0))
        yuzey.blit(label, (top_left_x + oyun_w/2 - (label.get_width()/2), s_h // 3))
        isim = font1.render('Furkan TASAN', 1, (200, 45, 120))
        yuzey.blit(isim, (
            top_left_x +oyun_w/2 - (isim.get_width()/2), s_h // 2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                calistir = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main(yuzey)
        pygame.display.update()
    pygame.display.quit()

main_menu(yuzey)

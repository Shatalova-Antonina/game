import pygame
import os
pygame.init()

def path_file(file_name):
    path_folder = os.path.abspath(__file__+"/..")
    path = os.path.join(path_folder, file_name)
    return path

WIN_WIDTH = 1150
WIN_HEIGHT = 730
FPS = 40
PINK = (199, 252, 236)
BUTTON_COLOR1 = (255, 228, 196)
BUTTON_COLOR2 = (218, 189, 171)
TEXT_COLOR = (172, 117, 128)

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()
fon = pygame.image.load(path_file("fon.jpg"))
fon = pygame.transform.scale(fon, (WIN_WIDTH, WIN_HEIGHT))
fon_menu = pygame.image.load(path_file("fon_menu.png"))
fon_menu = pygame.transform.scale(fon_menu, (WIN_WIDTH, WIN_HEIGHT))
fon_player = pygame.image.load(path_file("fon_player.jpg"))
fon_player = pygame.transform.scale(fon_player, (WIN_WIDTH, WIN_HEIGHT))
win_image = pygame.image.load(path_file("you_win.jpg"))
win_image = pygame.transform.scale(win_image, (WIN_WIDTH, WIN_HEIGHT))
lose_image = pygame.image.load(path_file("game_over.jpg"))
lose_image = pygame.transform.scale(lose_image, (WIN_WIDTH, WIN_HEIGHT))



music_win = pygame.mixer.Sound(path_file("win_music.ogg"))
pygame.mixer.music.set_volume(0.02)

music_menu = pygame.mixer.Sound(path_file("music_menu.ogg"))
music_menu.set_volume(0.05)

music_loss = pygame.mixer.Sound(path_file("you_lose_music.ogg"))
music_loss.set_volume(0.05)
music_shoot = pygame.mixer.Sound(path_file("Sectumsempra_music.ogg"))

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, img):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (width, height))

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def __init__(self, x, y, width, height, img, speed):
        super().__init__(x, y, width, height, img)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIN_WIDTH or self.rect.right < 0:
            self.kill()

class Enemy(GameSprite):
    def __init__(self, x, y, width, height, file_name, speed, direction, min_coord, max_coord):
        super().__init__(x, y, width, height, file_name)
        self.speed = speed
        self.direction = direction
        self.min_coord = min_coord
        self.max_coord = max_coord

    def update(self):
        if self.direction == "left" or self.direction == "right":
            if self.direction == "left":
                self.rect.x -= self.speed
            if self.direction == "right":
                self.rect.x += self.speed

            if self.rect.right >= self.max_coord:
                self.direction = "left"
            if self.rect.left <= self.min_coord:
                self.direction = "right"

        elif self.direction == "up" or self.direction == "down":
            if self.direction == "down":
                self.rect.y += self.speed
            if self.direction == "up":
                self.rect.y -= self.speed

            if self.rect.top <= self.min_coord:
                self.direction = "down"
            if self.rect.bottom >= self.max_coord:
                self.direction = "up"

class Player(GameSprite):
    def __init__(self, x, y, width, height, img):
        super().__init__(x, y, width, height, img)
        self.speed_x = 0
        self.speed_y = 0
        self.direction = "left"
        self.image_r = self.image
        self.image_l = pygame.transform.flip(self.image, True, False)

    def update(self):
        if self.rect.left > 0 and self.speed_x < 0 or self.speed_x > 0 and self.rect.right < WIN_WIDTH:
            self.rect.x += self.speed_x
        walls_collide = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_x > 0:
            for wall in walls_collide:
                self.rect.right = min(self.rect.right, wall.rect.left)
        elif self.speed_x < 0:
            for wall in walls_collide:
                self.rect.left = max(self.rect.left, wall.rect.right)

    

        if self.rect.top > 0 and self.speed_y < 0 or self.speed_y > 0 and self.rect.bottom < WIN_HEIGHT:
            self.rect.y += self.speed_y
        walls_collide = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_y < 0:
            for wall in walls_collide:
                self.rect.top = max(self.rect.top, wall.rect.bottom)
        elif self.speed_y > 0:
            for wall in walls_collide:
                self.rect.bottom = min(self.rect.bottom, wall.rect.top)
    def shoot(self):
        if self.direction == "right":
            bullet = Bullet(self.rect.right, self.rect.centery, 10, 20, path_file("sparks.png"), 5)
            bullets.add(bullet)
        if self.direction == "left":
            bullet = Bullet(self.rect.left - 10, self.rect.centery, 10, 20, path_file("sparks.png"), -5)
            bullets.add(bullet)

class Button():
    def __init__(self, color, x, y, width, height, text):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.font30 = pygame.font.SysFont("Times New Roman", 49)
        self.text = self.font30.render(text, True, TEXT_COLOR)

    def button_show(self, px_x, px_y):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.text, (self.rect.x + px_x, self.rect.y + px_y))


button_start = Button(BUTTON_COLOR1, 300, 450, 180, 70, "start")
button_exit = Button(BUTTON_COLOR1, 680, 450, 180, 70, "exit")
button_player = Button(BUTTON_COLOR1, 300, 250, 180, 70, "player")
button_music = Button(BUTTON_COLOR1, 680, 250, 180, 70, "music")
button_rulers = Button(BUTTON_COLOR1, 505, 100, 150, 60, "rulers")
button_exit_player = Button(BUTTON_COLOR1, 10, 10, 130, 42, "<--")
button_hermiona = Button(BUTTON_COLOR1, 680, 650, 370, 55, "Hermione Granger")
button_ron = Button(BUTTON_COLOR1, 200, 650, 370, 55, "Ron Weasley")
button_harry = Button(BUTTON_COLOR1, 200, 250, 370, 55, "Harry Potter")
button_luna = Button(BUTTON_COLOR1, 680, 250, 370, 55, "Luna Lovegood")


    



bullets = pygame.sprite.Group()

enemies = pygame.sprite.Group()
filch1 = Enemy (353, 300, 64, 138, path_file("filch.png"), 3.3, "up", 50, 720)
enemies.add(filch1)
filch2 = Enemy (808, 20, 64, 138, path_file("filch.png"), 3, "right", 500, 1130)
enemies.add(filch2)
filch3 = Enemy (900, 425, 64, 138, path_file("filch.png"), 2.9, "right", 730, 1130)
enemies.add(filch3)
filch4 = Enemy (570, 425, 64, 138, path_file("filch.png"), 3, "up", 230, 720)
enemies.add(filch4)
filosofskiy_kamien = Player(1020, 640, 100, 50, path_file("stone_philosopher's.png"))

walls = pygame.sprite.Group()
wall1 = GameSprite(0, 200, 143, 41, path_file("wall_h.jpg"))
walls.add(wall1)
wall2 = GameSprite(260, 0, 41, 143, path_file("wall_v.jpg"))
walls.add(wall2)
wall3 = GameSprite(260, 143, 41, 143, path_file("wall_v.jpg"))
walls.add(wall3)
wall4 = GameSprite(260, 286, 41, 143, path_file("wall_v.jpg"))
walls.add(wall4)
wall5 = GameSprite(117, 388, 143, 41, path_file("wall_h.jpg"))
walls.add(wall5)
wall6 = GameSprite(117, 429, 41, 143, path_file("wall_v.jpg"))
walls.add(wall6)
wall7 = GameSprite(481, 600, 41, 143, path_file("wall_v.jpg"))
walls.add(wall7)
wall8 = GameSprite(481, 457, 41, 143, path_file("wall_v.jpg"))
walls.add(wall8)
wall9 = GameSprite(481, 314, 41, 143, path_file("wall_v.jpg"))
walls.add(wall9)
wall10 = GameSprite(481, 171, 41, 143, path_file("wall_v.jpg"))
walls.add(wall10)
wall11 = GameSprite(522, 171, 143, 41, path_file("wall_h.jpg"))
walls.add(wall11)
wall12 = GameSprite(665, 171, 143, 41, path_file("wall_h.jpg"))
walls.add(wall12)
wall13 = GameSprite(808, 171, 143, 41, path_file("wall_h.jpg"))
walls.add(wall13)
wall14 = GameSprite(1007, 366, 143, 41, path_file("wall_h.jpg"))
walls.add(wall14)
wall15 = GameSprite(864, 366, 143, 41, path_file("wall_h.jpg"))
walls.add(wall15)
wall16 = GameSprite(721, 366, 143, 41, path_file("wall_h.jpg"))
walls.add(wall16)
wall17 = GameSprite(680, 366, 41, 143, path_file("wall_v.jpg"))
walls.add(wall17)
wall18 = GameSprite(680, 443, 41, 143, path_file("wall_v.jpg"))
walls.add(wall18)
wall19 = GameSprite(935, 607, 41, 143, path_file("wall_v.jpg"))
walls.add(wall19)
wall20 = GameSprite(935, 585, 41, 143, path_file("wall_v.jpg"))
walls.add(wall20)

level = 0

game = True
play = True
while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if level == 0:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if button_start.rect.collidepoint(x, y):
                    button_start.color = BUTTON_COLOR2
                elif button_exit.rect.collidepoint(x, y):
                    button_exit.color = BUTTON_COLOR2
                elif button_music.rect.collidepoint(x, y):
                    button_music.color = BUTTON_COLOR2
                elif button_rulers.rect.collidepoint(x, y):
                    button_rulers.color = BUTTON_COLOR2
                elif button_player.rect.collidepoint(x, y):
                    button_player.color = BUTTON_COLOR2
                else:
                    button_start.color = BUTTON_COLOR1
                    button_exit.color = BUTTON_COLOR1
                    button_player.color = BUTTON_COLOR1
                    button_music.color = BUTTON_COLOR1
                    button_rulers.color = BUTTON_COLOR1
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_start.rect.collidepoint(x, y):
                    level = 1
                    pygame.mixer.music.load(path_file("mermaid_song.ogg"))
                    pygame.mixer.music.set_volume(0.04)
                    pygame.mixer.music.play(-1)
                elif button_exit.rect.collidepoint(x, y):
                    game = False
                if button_player.rect.collidepoint(x, y):
                    level = 2
        if level == 2:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if button_exit_player.rect.collidepoint(x, y):
                    button_exit_player.color = BUTTON_COLOR2
                elif button_luna.rect.collidepoint(x, y):
                    button_luna.color = BUTTON_COLOR2
                elif button_harry.rect.collidepoint(x, y):
                    button_harry.color = BUTTON_COLOR2
                elif button_ron.rect.collidepoint(x, y):
                    button_ron.color = BUTTON_COLOR2
                elif button_hermiona.rect.collidepoint(x, y):
                    button_hermiona.color = BUTTON_COLOR2
                else:
                    button_exit_player.color = BUTTON_COLOR1
                    button_luna.color = BUTTON_COLOR1
                    button_harry.color = BUTTON_COLOR1
                    button_ron.color = BUTTON_COLOR1
                    button_hermiona.color = BUTTON_COLOR1
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_player.rect.collidepoint(x, y):
                    level = 2
                if button_exit_player.rect.collidepoint(x, y):
                    level = 0
                if button_luna.rect.collidepoint(x, y):
                    player = Player(55, 45, 52, 125, path_file("luna.png"))
                if button_ron.rect.collidepoint(x, y):
                    player = Player(55, 45, 76, 133, path_file("ron.png"))
                if button_hermiona.rect.collidepoint(x, y):
                    player = Player(55, 45, 70, 138, path_file("germiona.png"))
                if button_harry.rect.collidepoint(x, y):
                    player = Player(55, 45, 90, 124, path_file("Harry_Potter.png"))





        elif level == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.speed_x = 5
                    player.direction = "right"
                    player.image = player.image_r
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.speed_x = -5
                    player.direction = "left"
                    player.image = player.image_l
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.speed_y = -5
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.speed_y = 5
                if event.key == pygame.K_SPACE:
                    player.shoot()
                    music_shoot.play()
            if event.type ==  pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.speed_x = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.speed_x = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.speed_y = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.speed_y = 0
    
    if level == 0:
        window.blit(fon_menu, (0, 0))
        button_start.button_show(35, 5)
        button_music.button_show(35, 5)
        button_rulers.button_show(17, 0)
        button_exit.button_show(50, 5)
        button_player.button_show(25, 5)
    elif level == 2:
        window.blit(fon_player, (0, 0))
        button_exit_player.button_show(32, 0)
        button_hermiona.button_show(0, 0)
        button_ron.button_show(55, 0)
        button_harry.button_show(60, 0)
        button_luna.button_show(30, 0)
    elif level == 1:
        if play == True:
            window.blit(fon, (0, 0))
            player.reset()
            
            enemies.draw(window)
            enemies.update()
            filosofskiy_kamien.reset()

            player.update()

            walls.draw(window)

            bullets.draw(window)
            bullets.update()

            if pygame.sprite.collide_rect(player, filosofskiy_kamien):
                play = False
                window.blit(win_image, (0, 0))
                pygame.mixer.music.stop()
                music_win.play()

            if pygame.sprite.spritecollide(player, enemies, False):
                play = False
                window.blit(lose_image, (0, 0))
                pygame.mixer.music.stop()
                music_loss.play()

        pygame.sprite.groupcollide(bullets, walls, True, False)
        pygame.sprite.groupcollide(bullets, enemies, True, True)

    clock.tick(FPS)
    pygame.display.update()

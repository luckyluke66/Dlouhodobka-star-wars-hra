import pygame
import sys  # ukoncovani programu (neni nutne ale pygame v tomhle uplne spolehlivy neni)
import os   # psani cest pro externi soubori
import random

# nasledujici 3 radky inicializuji pygamove fukce pro a) samotny pygame b) texty c) hudba a zvukove efekty
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500

# barvy v RGB
RED = (255, 0, 0)
LIGHT_BLUE = (135,206,235)
BLACK = (0, 0, 0)
WHITE = (255,255,255)
GRAY = (54, 54, 54)
YELLOW = (255, 254, 0)

# zakladni definovane promenne
FPS = 60
LASER_SPEED = 7
MAX_SHOTS = 3


HEALTH_FONT = pygame.font.SysFont('8-BIT WONDER', 40)
MENU_FONT = pygame.font.SysFont('8-BIT WONDER', 150)
WINNER_FONT = pygame.font.SysFont('8-BIT WONDER', 100)

done = 0

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)

TIE_HIT = pygame.USEREVENT + 1
XWING_HIT = pygame.USEREVENT + 2

WINNER_FONT = pygame.font.SysFont('FR73 Pixel', 100)
# zvukove efekty
FIRE_SOUND = pygame.mixer.Sound(os.path.join('blaster1.wav'))
HIT_SOUND = pygame.mixer.Sound(os.path.join('mixkit-space-impact-774.wav'))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join('Explosion Sound Effect.wav'))


# import vsech obrazku pomoci os
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('space.jpg')),(WIDTH, HEIGHT))

X_WING_IMG = pygame.image.load(os.path.join('rebellion', 'Xwing.png'))
X_WING = pygame.transform.rotate(pygame.transform.scale(X_WING_IMG, (60,60)), 0)

Y_WING_IMG = pygame.image.load(os.path.join('rebellion', 'Ywing.png'))
Y_WING = pygame.transform.rotate(pygame.transform.scale(Y_WING_IMG, (60,60)), 0)

FALCON_IMG = pygame.image.load(os.path.join('rebellion', 'MileniumFalcon.png'))
FALCON = pygame.transform.rotate(pygame.transform.scale(FALCON_IMG, (60,60)), 270)

HP_ICON_XWING_IMG = pygame.image.load(os.path.join('rebellion', 'rebel logo.png'))
HP_ICON_XWING = pygame.transform.rotate(pygame.transform.scale(HP_ICON_XWING_IMG, (40,40)), 0)

TIE_IMG = pygame.image.load(os.path.join('empire', 'TieAdvanced.png'))
TIE_ADVANCED = pygame.transform.rotate(pygame.transform.scale(TIE_IMG, (50,50)), 180)

TIE_IMG = pygame.image.load(os.path.join('empire', 'TieFighter.png'))
TIE_FIGHTER = pygame.transform.rotate(pygame.transform.scale(TIE_IMG, (50,50)), 180)

TIE_IMG = pygame.image.load(os.path.join('empire', 'TieReaper.png'))
TIE_REAPER = pygame.transform.rotate(pygame.transform.scale(TIE_IMG, (50,50)), 180)

HP_ICON_TIE_IMG = pygame.image.load(os.path.join('empire', 'empire logo.png'))
HP_ICON_TIE = pygame.transform.rotate(pygame.transform.scale(HP_ICON_TIE_IMG, (43,43)), 0)

ICON = pygame.image.load(os.path.join('logovader.jpg'))

pygame.display.set_caption("star wars hra")
pygame.display.set_icon(ICON)

class Tie:
    def __init__(self):
        self.SPEED = 5
        self.TIE = random.choice([TIE_FIGHTER,TIE_ADVANCED,TIE_REAPER])
        self.tie_rec = pygame.Rect(700, 200, 40, 40)
        self.laser_tie = []
        self.HP_tie = 4
        self.MAX_HP = 4
        self.HP_bar_width = 200
        self.HP_bar_height = 20
        self.bar_position = 663
        self.yellow_bar_width = 200

    def draw_tie(self):
        WIN.blit(self.TIE, (self.tie_rec.x, self.tie_rec.y))

    def move_tie(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] and self.tie_rec.x - self.SPEED > BORDER.x + BORDER.width:
            self.tie_rec.x -= self.SPEED
        if keys_pressed[pygame.K_UP] and self.tie_rec.y - self.SPEED > 0:
            self.tie_rec.y -= self.SPEED
        if keys_pressed[pygame.K_RIGHT] and self.tie_rec.x + self.SPEED + 40 < WIDTH:
            self.tie_rec.x += self.SPEED
        if keys_pressed[pygame.K_DOWN] and self.tie_rec.y + self.SPEED + 50 < HEIGHT:
            self.tie_rec.y += self.SPEED
    def shoot_laser_tie(self):
        FIRE_SOUND.play()
        laser = pygame.Rect(self.tie_rec.x, self.tie_rec.y + 40 // 2, 10, 5)
        self.laser_tie.append(laser)

    def draw_laser_tie(self):
        for laser in self.laser_tie:
            pygame.draw.rect(WIN, RED, laser)
        for laser in self.laser_tie:
            laser.x -= LASER_SPEED
            if Xwing.xwing_rec.colliderect(laser):
                pygame.event.post(pygame.event.Event(TIE_HIT))
                self.laser_tie.remove(laser)
            elif laser.x < 0:
                self.laser_tie.remove(laser)

    def hp_bar_tie(self):
        pygame.draw.rect(WIN, GRAY, [660, 10, 200 + 6, self.HP_bar_height + 6 ])
        pygame.draw.rect(WIN, YELLOW, [663, 13, self.yellow_bar_width, self.HP_bar_height])
        pygame.draw.rect(WIN, RED, [self.bar_position, 13, self.HP_bar_width, self.HP_bar_height])
        WIN.blit(HP_ICON_TIE, (850, 3))

Tie = Tie()

class Xwing:
    def __init__(self):
        self.SPEED = 5
        self.WING = random.choice([X_WING, Y_WING, FALCON])
        self.xwing_rec = pygame.Rect(100, 200, 60, 50)
        self.laser_xwing = []
        self.HP_xwing = 4
        self.HP_bar_width = 200
        self.HP_bar_height = 20
        self.yellow_bar_width = 200
    def draw_xwing(self):
        WIN.blit(self.WING, (self.xwing_rec.x, self.xwing_rec.y))

    def move_xwing(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and self.xwing_rec.x - self.SPEED > 0:
            self.xwing_rec.x -= self.SPEED
        if keys_pressed[pygame.K_w] and self.xwing_rec.y - self.SPEED > 0:
            self.xwing_rec.y -= self.SPEED
        if keys_pressed[pygame.K_d] and self.xwing_rec.x + self.SPEED + 60 < BORDER.x:
            self.xwing_rec.x += self.SPEED
        if keys_pressed[pygame.K_s] and self.xwing_rec.y + self.SPEED + 50 < HEIGHT:
            self.xwing_rec.y += self.SPEED
    def shoot_laser_xwing(self):
        FIRE_SOUND.play()
        laser = pygame.Rect(self.xwing_rec.x, self.xwing_rec.y + 40 // 2, 10, 5)
        self.laser_xwing.append(laser)

    def draw_laser_xwing(self):
        for laser in self.laser_xwing:
            pygame.draw.rect(WIN, LIGHT_BLUE, laser)
        for laser in self.laser_xwing:
            laser.x += LASER_SPEED
            if Tie.tie_rec.colliderect(laser):
                pygame.event.post(pygame.event.Event(XWING_HIT))
                self.laser_xwing.remove(laser)
            elif laser.x > WIDTH:
                self.laser_xwing.remove(laser)

    def HP_bar_xwing(self):
        pygame.draw.rect(WIN, GRAY, [35, 10, 200 + 6, self.HP_bar_height + 6])
        pygame.draw.rect(WIN, YELLOW, [38, 13, self.yellow_bar_width, self.HP_bar_height])
        pygame.draw.rect(WIN, RED, [38, 13, self.HP_bar_width, self.HP_bar_height])
        WIN.blit(HP_ICON_XWING, (10, 3))

Xwing = Xwing()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for number in range(1,6):
            img = pygame.image.load(f"img/exp{number}.png")
            img = pygame.transform.scale(img, (60,60))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        self.counter = 0
        self.done = 0

    def update(self):
        explosion_speed = 4
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len (self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >=  explosion_speed:
            self.kill()

explosion_group = pygame.sprite.Group()

def restart():
    Tie.__init__()
    Xwing.__init__()
    
def winner(text):
    draw_text = WINNER_FONT.render(text,1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2 ))
    pygame.display.update()
    pygame.time.delay(3000)
    restart()

def indikator(poradnik):
    vyska_indikatoru = 250 
    if poradnik == 1:
        vyska_indikatoru = 250
    if poradnik == 2:
        vyska_indikatoru = 300
    if poradnik == 3:
        vyska_indikatoru = 350
    indikator = HEALTH_FONT.render("*", 1, WHITE)
    WIN.blit(indikator, (370, vyska_indikatoru))

    pass
"""
def options_submenu():
    clock = pygame.time.Clock()
    run_options = True
    while run_options:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_options = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game(done,WIN)
                if event.key == pygame.K_e:
                    run_menu = False
                    break
                if event.key == pygame.K_o:
                    options_submenu()
       
        menu_caption = MENU_FONT.render("OPTIONS", 1, WHITE)
        menu_pl1 = HEALTH_FONT.render("Player 1 (Rebellion)", 1, WHITE)
        menu_pl2 = HEALTH_FONT.render("Player 2 (Empire)", 1, WHITE)

        WIN.blit(SPACE, (0, 0))
        WIN.blit(menu_caption, (WIDTH//2 - menu_caption.get_width()//2, 100))
        WIN.blit(menu_pl1, (WIDTH // 2 - menu_pl1.get_width()//2, 250))
        WIN.blit(menu_pl2, (WIDTH // 2 - menu_pl2.get_width()//2, 300))
        
        pygame.display.update()
"""    
def menu():
    poradnik = 1
    clock = pygame.time.Clock()
    run_menu = True
    while run_menu:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and poradnik == 1:   # spusti hru
                    game(done,WIN)
                if event.key == pygame.K_SPACE and poradnik == 2:   # nastaveni hry
                    #options_submenu()
                    pass
                if event.key == pygame.K_SPACE and poradnik == 3:   # vypne program 
                    run_menu = False
                    break
                if event.key == pygame.K_UP and poradnik > 1:
                    poradnik -= 1
                    print(poradnik)
                if event.key == pygame.K_DOWN and poradnik < 3:
                    poradnik += 1
                    print(poradnik)

        WIN.blit(SPACE, (0, 0))
        menu_caption = MENU_FONT.render("MENU", 1, WHITE)
        menu_play = HEALTH_FONT.render("Play (P)", 1, WHITE)
        menu_options = HEALTH_FONT.render("Options (O)", 1, WHITE)
        menu_quit = HEALTH_FONT.render("Quit (Q)", 1, WHITE)

        WIN.blit(menu_caption, (WIDTH//2 - menu_caption.get_width()//2, 100))
        WIN.blit(menu_play, (WIDTH // 2 - menu_play.get_width()//2, 250))
        WIN.blit(menu_options, (WIDTH // 2 - menu_options.get_width()//2, 300))
        WIN.blit(menu_quit, (WIDTH//2 - menu_quit.get_width()//2, 350))

        WIN.blit(Xwing.WING, (100, 200))
        WIN.blit(Tie.TIE, (700, 200))

        indikator(poradnik)
        pygame.display.update()
        
    pygame.quit()
    run_menu = True

def game(done, WIN):
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(Tie.laser_tie) < MAX_SHOTS:
                    Tie.shoot_laser_tie()

                if event.key == pygame.K_LCTRL and len(Xwing.laser_xwing) < MAX_SHOTS:
                    Xwing.shoot_laser_xwing()
            
            if event.type == TIE_HIT:
                Xwing.HP_xwing -= 1
                HIT_SOUND.play()
                Xwing.HP_bar_width -= 50

            if event.type == XWING_HIT:
                Tie.HP_tie -= 1
                Tie.bar_position += 50
                Tie.HP_bar_width -= 50
                HIT_SOUND.play()

        Tie.move_tie()
        Xwing.move_xwing()

        WIN.blit(SPACE, (0,0))

        Tie.draw_tie()
        Xwing.draw_xwing()

        Tie.draw_laser_tie()
        Xwing.draw_laser_xwing()

        Tie.hp_bar_tie()
        Xwing.HP_bar_xwing()



        winner_text = ""
        if Xwing.HP_xwing <= 0:
            winner_text = "Empire wins"


        if Tie.HP_tie <= 0:
            winner_text = "Rebelion wins"


        if winner_text != "":
            EXPLOSION_SOUND.play()

            if Xwing.HP_xwing <= 0:
                explosion_group.draw(WIN)
                explosion = Explosion(Xwing.xwing_rec.x, Xwing.xwing_rec.y)
                explosion_group.add(explosion)
                explosion_group.update()
                done += 1
            elif Tie.HP_tie <= 0:
                explosion_group.draw(WIN)
                explosion = Explosion(Tie.tie_rec.x, Tie.tie_rec.y)
                explosion_group.add(explosion)
                explosion_group.update()
                done += 1

            if done >= 10:
                winner(winner_text)
                menu()
                #break
                
        pygame.display.update()
    pygame.quit()
    sys.exit()
menu()

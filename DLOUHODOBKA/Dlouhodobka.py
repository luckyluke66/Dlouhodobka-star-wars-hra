import pygame
import sys  # ukoncovani programu (neni nutne ale pygame v tomhle uplne spolehlivy neni)
import os   # psani cest pro externi soubory
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

MENU_FONT = pygame.font.Font('font/8-BIT WONDER.ttf', 80)
WINNER_FONT = pygame.font.Font('font/8-BIT WONDER.ttf', 50)
HEALTH_FONT = pygame.font.Font('font/8-BIT WONDER.ttf', 20)
CHOOSE_SHIP_FONT = pygame.font.Font('font/8-BIT WONDER.ttf', 45)

done = 0
pointer = 1
clock = pygame.time.Clock()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)

TIE_HIT = pygame.USEREVENT + 1
XWING_HIT = pygame.USEREVENT + 2

#WINNER_FONT = pygame.font.SysFont('FR73 Pixel', 100)
# zvukove efekty
FIRE_SOUND = pygame.mixer.Sound(os.path.join('sounds/blaster1.wav'))
HIT_SOUND = pygame.mixer.Sound(os.path.join('sounds/impact.wav'))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join('sounds/Explosion Sound Effect.wav'))
MENU_SOUND = pygame.mixer.Sound(os.path.join('sounds/menu-change.wav'))
ENTER_SOUND = pygame.mixer.Sound(os.path.join('sounds/enter.wav'))

# import vsech obrazku pomoci os
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('textures','space.jpg')),(WIDTH, HEIGHT))

X_WING_IMG = pygame.image.load(os.path.join('textures','rebellion', 'Xwing.png'))
X_WING = pygame.transform.rotate(pygame.transform.scale(X_WING_IMG, (60,60)), 0)

Y_WING_IMG = pygame.image.load(os.path.join('textures','rebellion', 'Ywing.png'))
Y_WING = pygame.transform.rotate(pygame.transform.scale(Y_WING_IMG, (60,60)), 0)

FALCON_IMG = pygame.image.load(os.path.join('textures','rebellion', 'MileniumFalcon.png'))
FALCON = pygame.transform.rotate(pygame.transform.scale(FALCON_IMG, (60,60)), 270)

HP_ICON_XWING_IMG = pygame.image.load(os.path.join('textures','rebellion', 'rebel logo.png'))
HP_ICON_XWING = pygame.transform.rotate(pygame.transform.scale(HP_ICON_XWING_IMG, (40,40)), 0)

TIE_IMG = pygame.image.load(os.path.join('textures','empire', 'TieAdvanced.png'))
TIE_ADVANCED = pygame.transform.rotate(pygame.transform.scale(TIE_IMG, (50,50)), 180)

TIE_IMG = pygame.image.load(os.path.join('textures','empire', 'TieFighter.png'))
TIE_FIGHTER = pygame.transform.rotate(pygame.transform.scale(TIE_IMG, (50,50)), 180)

TIE_IMG = pygame.image.load(os.path.join('textures','empire', 'TieReaper.png'))
TIE_REAPER = pygame.transform.rotate(pygame.transform.scale(TIE_IMG, (50,50)), 180)

HP_ICON_TIE_IMG = pygame.image.load(os.path.join('textures','empire', 'empire logo.png'))
HP_ICON_TIE = pygame.transform.rotate(pygame.transform.scale(HP_ICON_TIE_IMG, (43,43)), 0)

ICON = pygame.image.load(os.path.join('textures','logovader.jpg'))

ARROW_IMG = pygame.image.load(os.path.join('textures',"arrow.png"))
ARROW_LEFT = pygame.transform.scale(ARROW_IMG, (55,55))
ARROW_RIGHT = pygame.transform.rotate(pygame.transform.scale(ARROW_IMG, (50,50)), 180 )
ARROW_DOWN = pygame.transform.rotate(pygame.transform.scale(ARROW_IMG, (50,50)), 90 )

RANDOM_IMG = pygame.image.load(os.path.join('textures',"random.png"))
RANDOM = pygame.transform.scale(RANDOM_IMG, (50, 50))


# tabulky stats
STATS1 = pygame.image.load(os.path.join("textures","stats", "stats1.png"))
STATS1 = pygame.transform.scale(STATS1, (550,50))

STATS2 = pygame.image.load(os.path.join("textures", "stats", "stats2.png"))
STATS2 = pygame.transform.scale(STATS2, (550,50))

STATS3 = pygame.image.load(os.path.join("textures", "stats", "stats3.png"))
STATS3 = pygame.transform.scale(STATS3, (550,50))

RANDOM_STATS = pygame.image.load(os.path.join("textures", "stats", "random_stats.png"))
RANDOM_STATS = pygame.transform.scale(RANDOM_STATS, (550,50))

HANGAR = pygame.image.load(os.path.join("textures", "hangar.png"))
HANGAR = pygame.transform.scale(HANGAR, (WIDTH, HEIGHT))

SABER = pygame.image.load(os.path.join("textures", "lightsaber2.png"))
SABER = pygame.transform.scale(SABER, (400, 30))

LOGO = pygame.image.load(os.path.join("textures", "logo.png"))
LOGO = pygame.transform.scale(LOGO, (1000,400))

pygame.display.set_caption("star wars hra")
pygame.display.set_icon(ICON)

class Tie:
    def __init__(self):
        self.SPEED = 6
        self.HP_tie = 4
        self.MAX_HP = 4
        self.max_shots = 3
        self.shot_speed = 7
        self.TIE = TIE_FIGHTER
        self.empire_ships = [TIE_FIGHTER,TIE_ADVANCED,TIE_REAPER]
        self.tie_rec = pygame.Rect(700, 200, 40, 40)
        self.laser_tie = []
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
            laser.x -= self.shot_speed
            if Xwing.xwing_rec.colliderect(laser):
                pygame.event.post(pygame.event.Event(TIE_HIT))
                self.laser_tie.remove(laser)
            elif laser.x < 0:
                self.laser_tie.remove(laser)

    def stats(self):
        if self.TIE == TIE_FIGHTER:
            self.HP_tie = 4
            self.MAX_HP = 4
            self.SPEED = 6
            self.max_shots = 3
            self.shot_speed = 7
        if self.TIE == TIE_ADVANCED:
            self.HP_tie = 5
            self.MAX_HP = 5
            self.SPEED = 4
            self.max_shots = 4
            self.shot_speed = 6
        if self.TIE == TIE_REAPER:
            self.HP_tie = 3
            self.MAX_HP = 3
            self.SPEED = 5
            self.max_shots = 5
            self.shot_speed = 8  

    def hp_bar_tie(self):
        pygame.draw.rect(WIN, GRAY, [660, 10, 200 + 6, self.HP_bar_height + 6 ])
        pygame.draw.rect(WIN, YELLOW, [663, 13, self.yellow_bar_width, self.HP_bar_height])
        pygame.draw.rect(WIN, RED, [self.bar_position, 13, self.HP_bar_width, self.HP_bar_height])
        WIN.blit(HP_ICON_TIE, (850, 3))

Tie = Tie()

class Xwing:
    def __init__(self):
        self.SPEED = 5
        self.HP_xwing = 4
        self.MAX_HP = 4
        self.max_shots = 3
        self.shot_speed = 7
        self.WING = X_WING
        self.rebellion_ships = [X_WING, Y_WING, FALCON]
        self.xwing_rec = pygame.Rect(100, 200, 60, 50)
        self.laser_xwing = []
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
            laser.x += self.shot_speed
            if Tie.tie_rec.colliderect(laser):
                pygame.event.post(pygame.event.Event(XWING_HIT))
                self.laser_xwing.remove(laser)
            elif laser.x > WIDTH:
                self.laser_xwing.remove(laser)

    def stats(self):
        if self.WING == X_WING:
            self.HP_xwing = 4
            self.MAX_HP = 4
            self.SPEED = 6
            self.max_shots = 5
            self.shot_speed = 6
        if self.WING == FALCON:
            self.HP_xwing = 3
            self.MAX_HP = 3
            self.SPEED = 4
            self.max_shots = 5
            self.shot_speed = 5
        if self.WING == Y_WING:
            self.HP_xwing = 5
            self.MAX_HP = 5
            self.SPEED = 3
            self.max_shots = 3
            self.shot_speed = 8 

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
            img = pygame.image.load(f"textures/img/exp{number}.png")
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

def indicator(orderer, width, width2, text1, text2, text3, text4):
    indicator_height = 247 
    if orderer == 1:
        indicator_height = 247
        submenu = HEALTH_FONT.render(text1, 1, BLACK)
    if orderer == 2:
        indicator_height = 297
        submenu = HEALTH_FONT.render(text2, 1, BLACK)
    if orderer == 3:
        indicator_height = 347
        submenu = HEALTH_FONT.render(text3, 1, BLACK)
    if orderer == 4:
        indicator_height = 397
        submenu = HEALTH_FONT.render(text4, 1, BLACK)

    WIN.blit(SABER, (width, indicator_height))
    WIN.blit(submenu,(width2, indicator_height + 3))

def credits_submenu():
    run_credits = True
    while run_credits:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_credits = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run_credits = False
                    menu()
                    break
        text = HEALTH_FONT.render("credits",True, WHITE)
        WIN.blit(SPACE, (0,0))
        WIN.blit(text,(100,100))
        pygame.display.update()
    pygame.quit()
    sys.exit()

def choose_ship(shipone, shiptwo, shipthree, number, pointer):
    run_choose = True
    while run_choose:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_choose = False
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    options_submenu()
                    break
                if event.key == pygame.K_LEFT and pointer > 1:
                    MENU_SOUND.play()
                    pointer -= 1
                if event.key == pygame.K_RIGHT and pointer < 4:
                    MENU_SOUND.play()
                    pointer += 1
        
        if pointer == 1 and number == 0:
            Xwing.WING = shipone
            pointerx = 270
            ShipName = "X Wing"
            stats = STATS1
        if pointer == 2 and number == 0:
            Xwing.WING = shiptwo
            pointerx = 370
            ShipName = "Milenium Falcon"
            stats = STATS2
        if pointer == 3 and number == 0:
            Xwing.WING = shipthree
            pointerx = 470
            ShipName = "Y Wing"
            stats = STATS3
        if pointer == 4 and number == 0:
            Xwing.WING = random.choice([shipone, shiptwo, shipthree])
            pointerx = 570
            ShipName = "Random"
            stats = RANDOM_STATS

        if pointer == 1 and number == 1:
            Tie.TIE = shipone
            pointerx = 270
            ShipName = "Tie Fighter"
            stats = STATS1
        if pointer == 2 and number == 1:
            Tie.TIE = shiptwo
            pointerx = 370
            ShipName = "Tie Reaper"
            stats = STATS2
        if pointer == 3 and number == 1:
            Tie.TIE = shipthree
            pointerx = 470
            ShipName = "Tie Advanced"
            stats = STATS3
        if pointer == 4 and number == 1:
            Tie.TIE = random.choice([shipone, shiptwo, shipthree])
            pointerx = 570
            ShipName = "Random"
            stats = RANDOM_STATS

        # TODO: potvrzeni vyberu lode
        shipname = HEALTH_FONT.render(ShipName, 1, WHITE)
        menu_caption = CHOOSE_SHIP_FONT.render("CHOOSE SHIP", 1, WHITE)

        WIN.blit(SPACE, (0, 0))
        WIN.blit(HANGAR, (0, 0))
        WIN.blit(menu_caption, (WIDTH//2 - menu_caption.get_width()//2 + 2, 10))
        
        WIN.blit(shipone, (270, 200))
        WIN.blit(shiptwo, (370, 200))
        WIN.blit(shipthree, (470, 200))
        WIN.blit(RANDOM, (570,200))
        
        WIN.blit(stats, (190, 430)) 
        
        WIN.blit(ARROW_LEFT, (250, 350 - ARROW_LEFT.get_height()//4))
        WIN.blit(ARROW_RIGHT, (600, 350 - ARROW_RIGHT.get_height()//4))
        WIN.blit(shipname,(WIDTH // 2 - shipname.get_width()//2, 350))
        WIN.blit(ARROW_DOWN, (pointerx, 145))
        Tie.stats()
        Xwing.stats()
        pygame.display.update()
    pygame.quit()
    sys.exit()

def options_submenu():
    options_orderer = 1
    run_options = True
    while run_options:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_options = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and options_orderer > 1:
                    MENU_SOUND.play()
                    options_orderer -= 1
                if event.key == pygame.K_DOWN and options_orderer < 3:
                    MENU_SOUND.play()
                    options_orderer += 1
                if event.key == pygame.K_SPACE and options_orderer == 1:
                    ENTER_SOUND.play()
                    choose_ship(X_WING, FALCON, Y_WING, 0, pointer)
                    break
                if event.key == pygame.K_SPACE and options_orderer == 2:
                    ENTER_SOUND.play()
                    choose_ship(TIE_FIGHTER, TIE_REAPER, TIE_ADVANCED, 1, pointer)
                    break
                if event.key == pygame.K_SPACE and options_orderer == 3:
                    ENTER_SOUND.play()
                    menu()
                    break
                    
                  
        menu_caption = MENU_FONT.render("OPTIONS", 1, WHITE)
        menu_pl1 = HEALTH_FONT.render("Rebellion", 1, WHITE)
        menu_pl2 = HEALTH_FONT.render("Empire", 1, WHITE)
        back = HEALTH_FONT.render("back", 1, WHITE)

        WIN.blit(SPACE, (0, 0))
        WIN.blit(menu_caption, (WIDTH//2 - menu_caption.get_width()//2, 100))
        WIN.blit(menu_pl1, (WIDTH // 2 - 100, 250))
        WIN.blit(menu_pl2, (WIDTH // 2 - 100, 300))
        WIN.blit(back, (WIDTH // 2 - 100, 350))
    
        indicator(options_orderer, 230, 450, "Rebellion", "Empire", "back", "nic")
        pygame.display.update()
    pygame.quit()
    sys.exit()
   
def menu():
    pygame.mixer.music.load("sounds/menusoundtrack.wav")
    pygame.mixer.music.play(-1)
    orderer = 1
    run_menu = True
    while run_menu:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and orderer == 1:   # spusti hru
                    ENTER_SOUND.play()
                    game(done,WIN)
                    break
                if event.key == pygame.K_SPACE and orderer == 2:   # nastaveni hry
                    ENTER_SOUND.play()
                    options_submenu()
                    break
                if event.key == pygame.K_SPACE and orderer == 3:   #TODO: credits menu
                    ENTER_SOUND.play()
                    credits_submenu()
                    break
                if event.key == pygame.K_SPACE and orderer == 4:   # vypne program 
                    run_menu = False
                    break
                if event.key == pygame.K_UP and orderer > 1:
                    MENU_SOUND.play()
                    orderer -= 1
                if event.key == pygame.K_DOWN and orderer < 4:
                    MENU_SOUND.play()
                    orderer += 1
    

        WIN.blit(SPACE, (0, 0))
        menu_caption = MENU_FONT.render("MENU", 1, WHITE)
        menu_play = HEALTH_FONT.render("Play", 1, WHITE)
        menu_options = HEALTH_FONT.render("Options", 1, WHITE)
        menu_credits = HEALTH_FONT.render("Credits", 1, WHITE)
        menu_quit = HEALTH_FONT.render("Quit", 1, WHITE)
        
        
        WIN.blit(menu_caption, (WIDTH//2 - menu_caption.get_width() // 2, 80))
        #WIN.blit(LOGO, (160,50))
        WIN.blit(menu_play, (WIDTH // 2 - 70, 250))
        WIN.blit(menu_options, (WIDTH // 2 - 70, 300))
        WIN.blit(menu_credits, (WIDTH // 2 - 70, 350))
        WIN.blit(menu_quit, (WIDTH//2 - 70, 400))
        
        WIN.blit(Xwing.WING, (100, 200))
        WIN.blit(Tie.TIE, (700, 200))

        indicator(orderer, 260, WIDTH // 2 - 70 + 100, "Play", "Options", "Credits", "Quit")
        pygame.display.update()
        
    pygame.quit()
    sys.exit()

def game(done, WIN):
    pygame.mixer.music.load("sounds/gamesoundtrack_louder.wav")
    pygame.mixer.music.play(-1)
    explosion_group.empty()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(Tie.laser_tie) < Tie.max_shots:
                    Tie.shoot_laser_tie()

                if event.key == pygame.K_LCTRL and len(Xwing.laser_xwing) < Xwing.max_shots:
                    Xwing.shoot_laser_xwing()
            
            if event.type == TIE_HIT:
                Xwing.HP_xwing -= 1
                HIT_SOUND.play()
                Xwing.HP_bar_width = Xwing.HP_bar_width - 200 / Xwing.MAX_HP

            if event.type == XWING_HIT:
                Tie.HP_tie -= 1
                HIT_SOUND.play()
                Tie.HP_bar_width = Tie.HP_bar_width - 200 / Tie.MAX_HP
                Tie.bar_position = Tie.bar_position + 200 / Tie.MAX_HP

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

        
        explosion_group.draw(WIN)
        explosion_group.update()


        if winner_text != "":
            EXPLOSION_SOUND.play()

            if Xwing.HP_xwing <= 0:
                x = Xwing.xwing_rec.x
                y = Xwing.xwing_rec.y
                explosion_tie = Explosion(x,y )
                explosion_group.add(explosion_tie)
                done += 1
                
            elif Tie.HP_tie <= 0:
                x = Tie.tie_rec.x
                y = Tie.tie_rec.y
                explosion_wing = Explosion(x, y)
                explosion_group.add(explosion_wing)
                done += 1

            if done >= 20:
                pygame.mixer.music.stop()
                winner(winner_text)
                menu()
                break
            
        pygame.display.update()
    pygame.quit()
    sys.exit()
menu()

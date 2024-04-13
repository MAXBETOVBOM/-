#Создай собственный Шутер!

from pygame import *
from random import randint

font.init()
font1 = font.SysFont('Arial', 40)
winner = font1.render('YOU WIN!', True, (255, 255, 255))
loser = font1.render('YOU LOSE!!', True, (180, 0, 0))

font.init()
font2 = font.SysFont('Arial', 40)
window_width = 700
window_height = 500
window = display.set_mode((window_width, window_height))
display.set_caption('Шутер')

background = transform.scale(image.load("galaxy.jpg"), (700, 500))
rocket = 'rocket.png'
ufo = 'ufo.png'

mixer.init()
fire = mixer.Sound("fire.ogg")
galaxy = mixer.Sound("space.ogg")

galaxy.play()

clock = time.Clock()
FPS = 50

# Создание класса GameSprite
class GameSprite(sprite.Sprite):
    def __init__(self, x, y, image_f, size_x, size_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(image_f), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

 
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < window_width - self.rect.width:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, 'bullet.png', 15, 20, -15)
        bullets.add(bullet)
win = 0        
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(0,700)
            self.rect.y = 0
            lost = lost + 1
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        

ufo1 = Enemy(randint(0, 700), 0, ufo, 80, 50, randint(1,3)) 
ufo2 = Enemy(randint(0, 700), 0, ufo, 80, 50, randint(1,3)) 
ufo3 = Enemy(randint(0, 700), 0, ufo, 80, 50, randint(1,3))
ufo4 = Enemy(randint(0, 700), 0, ufo, 80, 50, randint(1,3))
ufo5 = Enemy(randint(0, 700), 0, ufo, 80, 50, randint(1,3))  
monsters = sprite.Group()
monsters.add(ufo1)  
monsters.add(ufo2)
monsters.add(ufo3)
monsters.add(ufo4)    
monsters.add(ufo5)
player_sprite = Player(420, 420, rocket, 80, 80, 7)     


bullets = sprite.Group()


       
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               player_sprite.fire()
               fire.play()
    if finish != True:
        window.blit(background, (0, 0))
        player_sprite.update()
        player_sprite.reset()
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        count = font2.render("Счёт: " + str(win), 1, (255, 255, 255))
        window.blit(count, (10, 10))

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_list:
            win += 1
            ufo_t = Enemy(randint(0, 700), 0, ufo, 80, 50, randint(1,3))   
            monsters.add(ufo_t)  
        if win > 10: 
            window.blit(winner, (200, 200))
            finish = True
        if lost > 3: 
            window.blit(loser, (200, 200))
            finish = True




   
    

    display.update()
       
    clock.tick(FPS)

    #инициализация- это создание, активация, подготовка к работе
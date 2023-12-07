import pygame
import sys
import random
from threading import Thread

vec = pygame.math.Vector2

# set display
screen = pygame.display.set_mode((1000, 800))

# set world size
WIDTH = 10000
HEIGHT = 10000

# set amount of enemies
enemies_amount = 300

# set color values
GREEN = (50, 255, 60)
RANDOM_COLOR = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (170, 170, 170)
ORANGE = (225, 50, 0)

# lists
distance_list_for_basic_bullet = []
basic_bullet_list = []
grunt_list = []


class Player(pygame.sprite.Sprite):
    def __init__(self):
        player_shoot_count = 0
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (1360 / 2, 700 / 2)

    def move(self, background, enemy_list, bullet_list):
        background_offset = vec(0, 0)
        if pygame.key.get_pressed()[pygame.K_d] and self.rect.x >= (1360 / 2) + 100:
            background.rect.x -= 1
            background_offset[0] += 1
            for i in enemy_list:
                i.rect.x -= 1
                i.offset[0] += 1

        elif pygame.key.get_pressed()[pygame.K_d]:
            self.rect.x += 1

        if pygame.key.get_pressed()[pygame.K_a] and self.rect.x <= (1360 / 2) - 100:
            background.rect.x += 1
            background_offset[0] -= 1
            for i in enemy_list:
                i.rect.x += 1
                i.offset[0] -= 1

        elif pygame.key.get_pressed()[pygame.K_a]:
            self.rect.x -= 1

        if pygame.key.get_pressed()[pygame.K_w] and self.rect.y <= (700 / 2) - 100:
            background.rect.y += 1
            background_offset[1] -= 1
            for i in enemy_list:
                i.rect.y += 1
                i.offset[1] -= 1

        elif pygame.key.get_pressed()[pygame.K_w]:
            self.rect.y -= 1

        if pygame.key.get_pressed()[pygame.K_s] and self.rect.y >= (700 / 2) + 100:
            background.rect.y -= 1
            background_offset[1] += 1
            for i in enemy_list:
                i.rect.y -= 1
                i.offset[1] += 1

        elif pygame.key.get_pressed()[pygame.K_s]:
            self.rect.y += 1

    def shoot(self, bullet_list, bullet_type):
        bullet_list.append(bullet_type)


class Basic_Bullet(pygame.sprite.Sprite):
    def __init__(self, shooter, enemy_list):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 15))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.pos = vec(shooter.rect.x, shooter.rect.y)
        self.rect.center = self.pos

        for i in range(0, len(enemy_list)):
            distance_list_for_basic_bullet.append(self.pos - enemy_list[i].pos)

        distance_list_for_basic_bullet.sort(key=sqdist)

        self.vel = distance_list_for_basic_bullet[0]

        del distance_list_for_basic_bullet[:]

    def update(self, player):
        if pygame.key.get_pressed()[pygame.K_RIGHT] and player.rect.x >= (1360 / 2) + 100:
            self.pos -= vec(1, 0)
        if pygame.key.get_pressed()[pygame.K_LEFT] and player.rect.x <= (1360 / 2) - 100:
            self.pos += vec(1, 0)
        if pygame.key.get_pressed()[pygame.K_UP] and player.rect.y <= (700 / 2) - 100:
            self.pos += vec(0, 1)
        if pygame.key.get_pressed()[pygame.K_DOWN] and player.rect.y >= (700 / 2) + 100:
            self.pos -= vec(0, 1)
        self.pos -= self.vel.normalize() * 10
        self.rect.center = self.pos


class Background(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height)).convert()
        self.image.fill(color)
        self.rect = self.image.get_rect()

        for i in range(0, 2000):
            pygame.draw.rect(self.image, RANDOM_COLOR, (random.randint(0, width), random.randint(0, height), 10, 10))


class Grunt(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = vec((random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        self.rect.center = self.pos

        self.offset = vec(0, 0)

    def update(self, bullet_list):
        self.pos = self.rect.center
        for i in bullet_list:
            if abs(self.pos[0] - i.rect.x) < 10 and abs(self.pos[1] - i.rect.y) < 10:
                grunt_list.remove(self)
                bullet_list.remove(i)

    def wander(self):
        while not game_over:
            count = int(random.randint(0, 3))
            pygame.time.wait(int(random.randint(1000, 4000)))
            if count == 0:
                for o in range(0, 75):
                    pygame.time.wait(5)
                    self.rect.x += 1
            if count == 1:
                for o in range(0, 75):
                    pygame.time.wait(5)
                    self.rect.x -= 1
            if count == 2:
                for o in range(0, 75):
                    pygame.time.wait(5)
                    self.rect.y += 1
            if count == 3:
                for o in range(0, 75):
                    pygame.time.wait(5)
                    self.rect.y -= 1


def sqdist(vector):
    return sum(x * x for x in vector)


def display_sprites(player, background, enemy_list, bullet_list):
    screen.blit(background.image, background.rect)
    for i in bullet_list:
        i.update(player)
        screen.blit(i.image, i.rect)
    screen.blit(player.image, player.rect)
    for i in enemy_list:
        i.update(basic_bullet_list)
        screen.blit(i.image, i.rect)


def wander_sprites(enemy_sprites):
    for i in enemy_sprites:
        Thread(target=i.wander).start()


def eventually_destroy(list):
    for obj in list:
        if obj.rect.x <= 0:
            list.remove(obj)
        elif obj.rect.x >= WIDTH:
            list.remove(obj)
        elif obj.rect.y <= 0:
            list.remove(obj)
        elif obj.rect.y >= HEIGHT:
            list.remove(obj)


game_over = False

is_fired = False

bg = Background(WIDTH, HEIGHT, GREEN)

player = Player()

for i in range(0, enemies_amount):
    grunt_list.append((Grunt(BLUE)))

wander_sprites(grunt_list)
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if pygame.key.get_pressed()[pygame.K_SPACE] and is_fired == False:
        is_fired = True
        player.shoot(basic_bullet_list, Basic_Bullet(player, grunt_list))
    if pygame.key.get_pressed()[pygame.K_SPACE] == False:
        is_fired = False
    if pygame.key.get_pressed()[pygame.K_g]:
        x = 0
        for i in grunt_list:
            x += 1
        print(x)
        print(bg.rect.center)

    player.move(bg, grunt_list, basic_bullet_list)

    eventually_destroy(basic_bullet_list)
    display_sprites(player, bg, grunt_list, basic_bullet_list)
    pygame.display.update()

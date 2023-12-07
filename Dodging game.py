import pygame, os
import sys
import random

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

WIDTH = 800
HEIGHT = 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (125, 0, 125)
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)

RANDOM_NUMBER = 3

player_size = 50

powerup_size = 10
powerup_position = [random.randint(0, WIDTH-player_size), 0]

powered_up = False

enemy_size = 50
enemy_position = [random.randint(0, WIDTH-enemy_size), 0]

screen = pygame.display.set_mode((WIDTH, HEIGHT))

fonty = pygame.font.Font('freesansbold.ttf', 32)

powerup_count = 0 

score = 0

game_over = False

while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	if RANDOM_NUMBER != 7 and powerup_position[1] < 700:
		RANDOM_NUMBER = random.randint(0, 5000)

	player_position = pygame.mouse.get_pos()
	enemy_position = [enemy_position[0], enemy_position[1] + 0.2]

	if abs(player_position[0] - enemy_position[0]) < player_size and abs(player_position[1] - enemy_position[1]) < player_size:
		sys.exit()

	if enemy_position[1] >= 700:
		enemy_position = [random.randint(0, WIDTH-enemy_size), 0]
		score += 1

	if powerup_position[1] >=700:
		RANDOM_NUMBER = random.randint(0, 5000)

	if abs(player_position[0] - powerup_position[0]) < player_size and abs(player_position[1] - powerup_position[1]) < player_size:
		powered_up = True

	screen.fill(BACKGROUND_COLOR)

	player = pygame.draw.rect(screen, RED, (player_position[0], player_position[1], player_size, player_size))
	enemy = pygame.draw.rect(screen, BLUE, (enemy_position[0], enemy_position[1], enemy_size, enemy_size))

	if powered_up == True:
		pygame.draw.circle(screen, PURPLE, (player_position[0] + 25, player_position[1] - 25), 12)
		if abs(player_position[0] - powerup_position[0]) < player_size and abs(player_position[1] - powerup_position[1]) < player_size:
			powerup_count = 0
		if abs((player_position[0] + 25) - enemy_position[0]) < enemy_size and abs((player_position[1] - 25) - enemy_position[1]) < enemy_size:
			enemy_position = [random.randint(0, WIDTH-enemy_size), 0]
			score += 2
			powerup_count += 1
		if powerup_count == 0:
			pygame.draw.rect(screen, WHITE, (WIDTH - 100, 10, 10, 15))
			pygame.draw.rect(screen, WHITE, (WIDTH - 120, 10, 10, 15))
			pygame.draw.rect(screen, WHITE, (WIDTH - 140, 10, 10, 15))
			pygame.draw.rect(screen, WHITE, (WIDTH - 160, 10, 10, 15))
			pygame.draw.rect(screen, WHITE, (WIDTH - 180, 10, 10, 15))
		if powerup_count == 1:
			pygame.draw.rect(screen, WHITE, (WIDTH - 100, 10, 10, 15))
			pygame.draw.rect(screen, WHITE, (WIDTH - 120, 10, 10, 15))
			pygame.draw.rect(screen, WHITE, (WIDTH - 140, 10, 10, 15))
			pygame.draw.rect(screen, WHITE, (WIDTH - 160, 10, 10, 15))
		if powerup_count == 2:
			pygame.draw.rect(screen, WHITE, (WIDTH - 100, 10, 10, 15))
			pygame.draw.rect(screen, WHITE, (WIDTH - 120, 10, 10, 15))
			pygame.draw.rect(screen, WHITE, (WIDTH - 140, 10, 10, 15))
		if powerup_count == 3:
			pygame.draw.rect(screen, WHITE, (WIDTH - 100, 10, 10, 15))
			pygame.draw.rect(screen, WHITE, (WIDTH - 120, 10, 10, 15))
		if powerup_count == 4:
			pygame.draw.rect(screen, WHITE, (WIDTH - 100, 10, 10, 15))
		if powerup_count >= 5:
			powered_up = False 

	if RANDOM_NUMBER == 7 and powerup_position[1] < 700:
		RANDOM_NUMBER = 7
		pygame.draw.circle(screen, GREEN, (powerup_position[0], powerup_position[1]), powerup_size)
		powerup_position = [powerup_position[0], powerup_position[1] + 0.5]
	
	if RANDOM_NUMBER == 7 and powerup_position[1] >= 700:
		powerup_position = [random.randint(0, WIDTH-player_size), 0]
		RANDOM_NUMBER = random.randint(0, 5000)

	score = str(score)
	text = fonty.render('Score: ' + score, True, GREEN, BLUE)
	textRect = text.get_rect() 
	screen.blit(text, textRect) 
	pygame.display.update()
	if powerup_count >= 5:
		powerup_count = 0
	score = int(score)
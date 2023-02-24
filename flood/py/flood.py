#!/usr/bin/env python3

import sys, pygame
import random
import time

pygame.init()

CELL_SIZE = 32
GRID_X = 16
GRID_Y = 16
WIN_WIDTH = CELL_SIZE * GRID_X
WIN_HEIGHT = CELL_SIZE * GRID_Y

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

def pixel(surface, color, pos1, pos2):
	pygame.draw.line(surface, color, pos1, pos2)

def DrawRect(x, y, w, h, color):
	screen.fill(color, ((x,y), (w,h)))

bg_data = [None] * GRID_X * GRID_Y

for y in range (0, GRID_Y):
	for x in range (0, GRID_X):
		bg_data[GRID_Y * y + x] = random.randint(0, 5)

bg_colors = [
	0xFF0000,
	0x00FF00,
	0x0000FF,
	0xFFFF00,
	0xFF7F00,
	0x7F00FF
]

def GetColor(x, y):
	col = bg_data[GRID_Y * y + x]
	return bg_colors[col]

crawl_table = [None] * GRID_X * GRID_Y

def CrawlColors(x, y, col):
	crawl_table[GRID_Y * y + x] = True
	# Left
	if x - 1 >= 0:
		if bg_data[x - 1 + y * GRID_Y] == col and crawl_table[x - 1 + y * GRID_Y] == False:
			CrawlColors(x - 1, y, col)
	# Right
	if x + 1 < GRID_X:
		if bg_data[x + 1 + y * GRID_Y] == col and crawl_table[x + 1 + y * GRID_Y] == False:
			CrawlColors(x + 1, y, col)
	# Top
	if y - 1 >= 0:
		if bg_data[x + (y - 1) * GRID_Y] == col and crawl_table[x + (y - 1) * GRID_Y] == False:
			CrawlColors(x, y - 1, col)
	# Bottom
	if y + 1 < GRID_Y:
		if bg_data[x + (y + 1) * GRID_Y] == col and crawl_table[x + (y + 1) * GRID_Y] == False:
			CrawlColors(x, y + 1, col)

moves = 0

def DoCrawl(x, y, col):
	global moves
	moves += 1
	for w in range(0, GRID_X * GRID_Y):
		crawl_table[w] = False
	CrawlColors(x, y, bg_data[0])
	for w in range(0, GRID_X * GRID_Y):
		if crawl_table[w] == True:
			bg_data[w] = col
	orig = bg_data[0]
	won = True
	for w in range(0, GRID_X * GRID_Y):
		if bg_data[w] != orig:
			won = False
			break
	if won:
		print(f"Congrats you won! You took {moves} moves")
		sys.exit()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE: sys.exit()
			if event.key == pygame.K_1: DoCrawl(0, 0, 0)
			if event.key == pygame.K_2: DoCrawl(0, 0, 1)
			if event.key == pygame.K_3: DoCrawl(0, 0, 2)
			if event.key == pygame.K_4: DoCrawl(0, 0, 3)
			if event.key == pygame.K_5: DoCrawl(0, 0, 4)
			if event.key == pygame.K_6: DoCrawl(0, 0, 5)

	#screen.fill(0x000000)

	xx = 0
	yy = 0
	for y in range (0, GRID_Y):
		for x in range (0, GRID_X):
			DrawRect(xx, yy, CELL_SIZE, CELL_SIZE, GetColor(x, y))
			xx += CELL_SIZE
		yy += CELL_SIZE
		xx = 0

	pygame.display.flip()
	# pygame.time.delay(10)
	time.sleep(0.1)

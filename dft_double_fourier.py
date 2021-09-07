import pygame
import math
import pyautogui
import numpy as np
import sys


# Draw with argument file

def setup_input():
	
	if len(sys.argv) < 2:
		print("------> need the vector to draw as an argument <------")
		exit()

	if len(sys.argv) > 2:
		print("------> only one argument <------")
		exit()

	draw = []

	with open(sys.argv[1]) as f:
		content = f.read()

	s_content = content.split()

	for cont_iter in s_content:
		draw.extend( [tuple(float(i) for i in cont_iter.strip("()").split(","))] )

	imp_signal_x = []
	imp_signal_y = []

	if len(draw) > 2000:
		i = 0
		for p in draw:
			if i % 3 == 0:
				imp_signal_x.append(p[0])
				imp_signal_y.append(p[1])
			i += 1
	else:
		for p in draw:
				imp_signal_x.append(p[0])
				imp_signal_y.append(p[1])

	return imp_signal_x, imp_signal_y

# DFT
def dft(imp_array):
	N = len(imp_array)
	fourierT = []
	for k in range(0, N):
		re = 0
		im = 0
		for n in range(0, N):
			phi = (2 * math.pi * k * n) / N 
			re += imp_array[n] * math.cos(phi) 
			im -= imp_array[n] * math.sin(phi)	
		re = re / N
		im = im / N
		freq = k 
		amp = math.sqrt(re * re + im * im) 
		phase = math.atan2(im, re) 
		fourierT.append((re, im, freq, amp, phase))
	return fourierT

def draw_epicycles(center, fourierT, alpha, rotation):
	for i in range(len(fourierT_x)):

		n = fourierT[i][2]
		r = fourierT[i][3]
		phase = fourierT[i][4]

		x = math.cos(n * alpha + phase + rotation) * r
		y = math.sin(n * alpha + phase + rotation) * r
		end_pos = (center[0] + x, center[1] + y)

		pygame.draw.circle(screen, (100, 100, 100), center, r, 1)
		pygame.draw.line(screen, (100,100,100), center, end_pos, 1)
		pygame.draw.circle(screen, (100, 100, 100), end_pos, 2)
		center = end_pos
	return end_pos

# Main part

alpha = 0
wave = []
path = []

imp_signal_x, imp_signal_y = setup_input() 

fourierT_x = dft(imp_signal_x)
fourierT_y = dft(imp_signal_y)

# Draw

screen_w, screen_h = pyautogui.size()
screen = pygame.display.set_mode([screen_w, screen_h])
fps = pygame.time.Clock()
running = True

pygame.init()
while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT or	(event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			running = False
	screen.fill((0, 0, 0))

	# Draw epycicles
	vx = draw_epicycles((1300, 100), fourierT_x, alpha, 0)
	vy = draw_epicycles((150, 500), fourierT_y, alpha, math.pi / 2)
	v = (vx[0], vy[1])	

	path.insert(0, v)

	# Draw path
	if len(path) > 1:
		pygame.draw.aalines(screen, (255, 255, 255), 0, path)

	# Draw lines to path
	pygame.draw.line(screen, (100, 100, 100), vx, v, 1)
	pygame.draw.line(screen, (100, 100, 100), vy, v, 1)

	pygame.display.flip()
	dt = (2 * math.pi) / len(fourierT_x)
	alpha += dt
	fps.tick(60)

pygame.quit()

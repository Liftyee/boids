#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gametest.py
#  
#  Copyright 2020 Victor <victor@victor-linux>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  

import pygame
import keyboard
import math
from random import randint
from pygame.locals import *
width = 1920
height = 1080
screen = pygame.display.set_mode((width, height))
pygame.init()
clock = pygame.time.Clock()

class Object:
	def __init__(self, x, y, width=100, height=100, color=(0, 0, 255)):
		self.x = x
		self.y = y
		self.color = color
		self.width = width
		self.height = height

	def draw(self):

		pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
			


class Boid:
	def __init__(self, x, y, image, rot=0):
		self.x = x
		self.y = y
		self.image = image
		self.image = pygame.transform.scale(self.image, (32, 32))
		self.rot = rot
		
	def draw(self):
		
		# update self
		
		rotated_image = pygame.transform.rotate(self.image, self.rot-180)
		new_rect = rotated_image.get_rect(
		center=self.image.get_rect(topleft=(self.x, self.y)).center)
		screen.blit(rotated_image, new_rect.topleft)

		# self.rot += 10
	
	def withinrange(self, other, dist):
		#return self.x > other.x - dist and self.x < other.x + dist and self.y > other.y - dist and self.y < other.y + dist
		return True
	
	def getavgpos(self, dist):
		avgx = self.x
		avgy = self.y
		bcount = 0
		for b in boids:
			print("Checking boid", b)
			if b.withinrange(self, dist):
				avgx += b.x
				avgy += b.y
				bcount += 1
			
		avgx = avgx/bcount
		avgy = avgy/bcount
		print(avgx, avgy)
		print(bcount)
		return avgx, avgy
		
	def cohesion(self, dist):
		ax, ay = self.getavgpos(dist)
		relx = ax - self.x
		rely = ay - self.y
		
		rota, l = getVectorfromXY(relx, rely)
		print(rota)
		self.rot += (rota - self.rot * 0.9)
		# if relx < 0:
			# self.rot -= 1
		# elif relx > 0:
			# self.rot += 1
		
	def move(self):
		self.rot += randint(-10, 10)
		nx, ny = getXYFromVector(self.rot, 5)
		self.x += nx
		self.y += ny
	
	def update(self):
		self.cohesion(500)
		self.draw()
		self.move()

def getXYFromVector(angle, length):
	xc = length * math.sin(math.radians(angle))
	yc = length * math.cos(math.radians(angle))
	return (xc, yc)
	
def getVectorfromXY(xc, yc):
	angle = math.degrees(math.atan2(xc,yc))
	length = math.sqrt((xc ** 2) + (yc ** 2))
	return (angle, length)

center = Object(0, 0, 5, 5, (0, 0, 255))
backg = Object(0, 0, 1920, 1080, (0, 0, 0))
boids = []
boid = Boid(100, 100, pygame.image.load("boid.png"))

boids.append(Boid(randint(500, 1000), randint(500, 1000), pygame.image.load("boid.png")))
playerquit = False
main = True
while not playerquit:
	#screen.fill(128, 128, 128)
	# switchbox.draw()
	# switchlabel.draw()
	backg.draw()
	for i in boids:
		i.update()
		i.draw()
	
	center.x, center.y = boids[0].getavgpos(500)
	center.draw()
	#print(pygame.mouse.get_pos())
	#print(switch.mousex, switch.mousey)
	for event in pygame.event.get():
		if event.type == QUIT:
			main = False
			playerquit = True

	pygame.display.update()
	clock.tick(30)
pygame.quit()
	

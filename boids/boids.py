#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  boids.py
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
height = 1000
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
	def __init__(self, x, y, image, rot=0, dist=200):
		self.x = x
		self.y = y
		self.dist = dist
		self.image = image
		self.image = pygame.transform.scale(self.image, (64, 64))
		self.rot = rot
		
	def draw(self):
		
		# update self
		
		rotated_image = pygame.transform.rotate(self.image, self.rot-180)
		new_rect = rotated_image.get_rect(
		center=self.image.get_rect(topleft=(self.x%width, self.y%height)).center)
		screen.blit(rotated_image, new_rect.topleft)

		# self.rot += 10
	
	def withinrange(self, other):
		return other.x + self.dist > self.x > other.x - self.dist and other.y + self.dist > self.y > other.y - self.dist
		#return True
	
	def getavgpos(self):
		avgx = self.x
		avgy = self.y
		bcount = 1
		for b in boids:
			if b.withinrange(self):
				avgx += b.x
				avgy += b.y
				bcount += 1
			
		avgx = avgx/bcount
		avgy = avgy/bcount
		return avgx, avgy
		
	def getavgdir(self):
		avgd = self.rot
		bcount = 1
		for b in boids:
			if b.withinrange(self):
				avgd += b.rot
				bcount += 1
			
		avgd = avgd/bcount
		return avgd
	
	def cohesion(self):
		ax, ay = self.getavgpos() # average x and y
		ax -= 32
		ay -= 32
		pygame.draw.rect(screen, (0, 0, 255), (ax, ay, 5, 5)) # just draws a rectangle at where the average position is
		relx = ax - self.x
		rely = ay - self.y
		
		rota, l = getVectorfromXY(relx, rely)
		print(rota)
		rotc = ((rota - self.rot) * 0.3) # change in rotation needed: change 0.5 to other values to increase/decrease sensitivity
		if abs(rotc) >= 30: # threshold for override of rotation to stop spazzing
			self.rot += (abs(rotc) / rotc) * 30
		else:
			self.rot += rotc
		# if relx < 0:
			# self.rot -= 1
		# elif relx > 0:
			# self.rot += 1
	
	def align(self):
		arot = self.getavgdir()
		self.rot += (arot - self.rot) * 0.5
	
	def move(self):
		self.xc = self.x + 32
		self.yc = self.y + 32
		# if self.xc > 1920:
			# self.xc = 0
		# if self.yc > 1080:
			# self.yc = 0
		# if self.xc < 0:
			# self.xc = 1920
		# if self.yc < 0:
			# self.yc = 1080
		
		nx, ny = getXYFromVector(self.rot, 1)
		self.x += nx
		self.y += ny
	
	def update(self):
		self.cohesion()
		self.draw()
		self.move()
		self.align()

def getXYFromVector(angle, length):
	xc = length * math.sin(math.radians(angle))
	yc = length * math.cos(math.radians(angle))
	return (xc, yc)
	
def getVectorfromXY(xc, yc):
	angle = math.degrees(math.atan2(xc,yc))
	length = math.sqrt((xc ** 2) + (yc ** 2))
	return (angle, length)

center = Object(0, 0, 5, 5, (0, 0, 255))
backg = Object(0, 0, width, height, (0, 0, 0))

boids = []

# add boids
for i in range(25):
	boids.append(Boid(randint(0, width), randint(0, height), pygame.image.load("boid.png"), 150))
playerquit = False
main = True

while not playerquit:
	backg.draw()
	for i in boids:
		i.update()
	
	center.x, center.y = boids[0].getavgpos()
	#center.draw()
	
	for event in pygame.event.get():
		if event.type == QUIT:
			main = False
			playerquit = True

	pygame.display.update()
	clock.tick(30)
pygame.quit()
	
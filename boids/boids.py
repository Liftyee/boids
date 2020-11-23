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
		self.xc = x + 24
		self.yc = y + 24
		self.color = color
		self.width = width
		self.height = height

	def draw(self):

		pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
			
# a bunch of constants
tcs = 5 # amount it turns when it is too close to another boid
dradius = 150 # radius in which it detects another boid
dspeed = 10 # default speed before increases
closeinc = 3 # speed increase when it is too close
turninc = 3 # speed increase when it turns
turnthr = 10 # amount turn needed to trigger speed increase

class Boid:
	def __init__(self, x, y, image, rot=0, dist=200, scale=32):
		self.x = x
		self.y = y
		self.scale = scale
		self.xc = x + scale/2
		self.yc = y + scale/2
		self.dist = dist
		self.image = image
		self.image = pygame.transform.scale(self.image, (scale, scale))
		self.rot = rot
		self.moveAmount = 5
		self.rotsLeft = 0
		self.rotAmount = 0
		self.alone = False
		
	def draw(self):
		
		# update self
		
		rotated_image = pygame.transform.rotate(self.image, self.rot-180)
		new_rect = rotated_image.get_rect(
		center=self.image.get_rect(topleft=(self.x%width, self.y%height)).center)
		screen.blit(rotated_image, new_rect.topleft)

		# self.rot += 10
	
	def withinrange(self, other):
		return other.xc + self.dist > self.xc > other.xc - self.dist and other.yc + self.dist > self.yc > other.yc - self.dist
		#return True
	
	def tooclose(self, other):
		self.dist2 = self.dist/2 # change this line to change clumping distance
		self.moveAmount += closeinc
		return other.xc + self.dist2 > self.xc > other.xc - self.dist2 and other.yc + self.dist2 > self.yc > other.yc - self.dist2
		#return True
	
	def getavgpos(self):
		mousex, mousey = pygame.mouse.get_pos()
		if pygame.mouse.get_pressed()[0]:
			return mousex, mousey
		avgx = self.xc
		avgy = self.yc
		bcount = 1
		for b in boids:
			if b.withinrange(self):
				avgx += b.xc
				avgy += b.yc
				bcount += 1
			
		avgx = avgx/bcount
		avgy = avgy/bcount
		if bcount <= 2:
			self.alone = True
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
		if self.alone:
			pygame.draw.rect(screen, (0, 0, 255), (ax%width, ay%height, 5, 5))
		else:
			pygame.draw.rect(screen, (0, 0, 255), (ax%width, ay%height, 5, 5)) # just draws a rectangle at where the average position is
		relx = ax - self.x
		rely = ay - self.y
		
		rota, l = getVectorfromXY(relx, rely)
		print(rota)
		rotc = ((rota - self.rot) * 0.3) # change in rotation needed: change 0.5 to other values to increase/decrease sensitivity
		if abs(rotc) >= 948934: # threshold for override of rotation to stop spazzing
			self.rot += (abs(rotc) / rotc) * 30
		elif abs(rotc) >= turnthr:
			self.moveAmount += turninc
			self.rot += rotc
		else:
			self.rot += rotc
			
			
	def separate(self):
		for b in boids:
			if b.tooclose(self):
				x, y = getXYFromVector(self.rot, 10)
				ox, oy = getXYFromVector(b.rot, 10)
				rx = x - ox
				ry = y - oy
				
				if rx > 0 and ry > 0:
					self.rot += tcs
				elif rx > 0 and ry < 0:
					self.rot -= tcs
				elif rx < 0 and ry < 0:
					self.rot -= tcs
				else:
					self.rot += tcs
				
		
	
	
	def align(self):
		arot = self.getavgdir()
		self.rot += (arot - self.rot) * 0.5
	
	def move(self):
		self.xc = self.x + self.scale/2
		self.yc = self.y + self.scale/2
		
		nx, ny = getXYFromVector(self.rot, self.moveAmount)
		# pygame.draw.line(screen, (255, 0, 0), (self.xc, self.yc), (self.xc + nx + self.scale/2, self.yc + ny + self.scale/2), 1)
		
		self.x += nx
		self.y += ny
		
		
		if self.alone and randint(1, 10) == 1:
			self.alone = True
			self.rotsLeft = randint(5, 15)
			self.rotAmount = randint(-10, 10)
			
		if self.rotsLeft >= 0:
			self.rotsLeft -= 1
			self.rot += self.rotAmount
			
		self.x = self.x % width
		self.y = self.y % height
		
	
	def update(self):
		self.moveAmount = dspeed
		self.draw()
		self.cohesion()
		self.align()
		self.separate()
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
backg = Object(0, 0, width, height, (0, 0, 0))

boids = []

# add boids
for i in range(100):
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
	

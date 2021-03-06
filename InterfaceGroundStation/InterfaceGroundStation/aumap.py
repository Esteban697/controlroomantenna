# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 16:07:20 2017

@author: esteban struve
"""

import pygame, sys 
from pygame.locals import *
import math
import csv
import numpy as np
#Read a csv file with the angle information
file_reader= open('angles.csv', "rt")
read = csv.reader(file_reader)
co=0
#The information about the angle and slope for the map into 2 lists
listang=[0]*360
slopel=[0]*360
for row in read :
    if co!=0 and co < 360:
        listang[co]=float(row[0])
        slopel[co]=math.tan(math.radians(listang[co]))
    co+=1
# Define the colors we will use in RGB format
YELLOW = (255,   255,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
#Start the pygame interface
pygame.init()
#Initialize values for the visual interface
#Setting screen
size = width, height = 1216,830
screen = pygame.display.set_mode(size)
#Loading image objects
pygame.display.set_caption("Aarhus Map")
layer = pygame.image.load("mapaarhus.png") 
cursor=pygame.image.load("arrow.png")
circul=pygame.image.load("boy.png")
#Initializing variables for visual objects
ind=0
coordx,coordy=0,0
mousex,mousey=0,0
movex, movey=0,0
endx,endy=0,0
opx,opy=0,0
slope=0
angledeg=0
#This scale is based on the map size to point the sky correctly
scale=5
#Draw the map in the screen
screen.blit(layer,(0,0))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() #Exit execution when closing window
        elif event.type == pygame.KEYDOWN:
            if event.key == K_LEFT: #When left key gets pressed
                print "izquierda"
                if ind > 0: #safe limits
                    ind-=1
            elif event.key == K_RIGHT: #when right key gets pressed
                print angledeg, coordx, coordy, endx, endy
                if ind <359: #safe limits
                    ind+=1
    mousex,mousey=pygame.mouse.get_pos() #gets the position of the cursor
    mousex-=10
    mousey-=20 #alligns the cursor icon
    #Choose an angle and slope from the list created by the csv file
    angledeg=listang[ind]
    slope=slopel[ind]
    #Chooses the end coordinates of each line to be drawn according to angle
    #When angle between 0 and 89
    if angledeg < 90.0:
        endy=0
        endx=(width/2)-((width/2)*slope)
        opy=height
        opx=(width/2)+((width/2)*slope)
        if endx<0:
            endy=(height/2)-((height/2)/slope)
            endx=0
        #Calculate the (x,y) coordinates in the line according to inclination
        if angledeg < 45: #from 0 to 44 degrees inclincation
            if endx == width/2:
                coordx=width/2
                coordy=angledeg*((height/2)/90)
            else:
                distxgrad=((width/2)-endx)/90
                coordx=distxgrad*angledeg+endx
                coordy=((((height/2)-endy)/((width/2)-endx))*(coordx-endx))
        else: #from 45 to 89 degrees inclincation
            if angledeg==45: #correction for non-linear calc
                distxgrad=(width/2)/90
                coordx=23+distxgrad*angledeg+endx
            elif angledeg == 46: #correction for non-linear calc
                distxgrad=(width/2)/90
                coordx=14+distxgrad*angledeg+endx
            else:
                distxgrad=(width/2)/90
                coordx=distxgrad*angledeg+endx
                coordy=(((height/2)-endy)/((width/2)-endx))*(coordx-endx)+endy
    #When angle between 90 and 179
    elif angledeg < 180.0:
        if angledeg == 90:
            endy=height/2
            endx=0
            opy=height/2
            opx=width
        else:
            endy=height
            endx=(width/2)+((width/2)*slope)
            opy=0
            opx=(width/2)-((width/2)*slope)
            if endx<0:
                endy=(height/2)-((height/2)/slope)
                endx=0
        #Calculate the (x,y) coordinates in the line according to inclination
        if endy == height/2:
            coordx=angledeg*((width/2)/90)
            coordy=height/2
        #else:
            
    #When angle between 180 and 269
    elif angledeg < 270.0:
        if angledeg == 180:
            endy=height
            endx=width/2
            opy=0
            opx=width/2
        else:
            endy=height
            endx=(width/2)+((width/2)*slope)
            opy=0
            opx=(width/2)-((width/2)*slope)
            if endx>width:
                endy=(height/2)+((height/2)/slope)
                endx=width
    #When angle between 270 and 359
    elif angledeg < 360.0:
        if angledeg == 270:
            endy=height/2
            endx=width
            opy=height/2
            opx=0
        else:
            endy=0
            endx=(width/2)-((width/2)*slope)
            opy=height
            opx=(width/2)+((width/2)*slope)
            if endx>width:
                endy=(height/2)+((height/2)/slope)
                endx=width
    #When angle exactly 360
    else:
        endy=0
        endx=width/2
        opy=0
        opx=width/2
    #The screen is updated by:
    pygame.display.update()
    #Drawing map again
    screen.blit(layer,(0,0))
    #Drawing image objects
    screen.blit(cursor,(mousex,mousey))
    screen.blit(circul,(coordx,coordy))
    #Drawing the lines
    pygame.draw.line(screen,YELLOW,(width/2,height/2),(opx,opy),3)
    pygame.draw.line(screen,GREEN,(width/2,height/2),(endx,endy),3)
    
    
    


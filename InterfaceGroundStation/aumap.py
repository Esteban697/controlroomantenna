# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 16:07:20 2017

@author: esteban struve
"""

import pygame, sys 
from pygame.locals import *
import math
import csv

#Read a csv file with the angle information
original = file('angles2.csv')
reader = csv.reader(original)
listang = reader.next()
listincl = reader.next()
#The information about the slope direction of antenna in map
slopel= [0] * len(listang)
angles= [0] * len(listang)
for i in range(len(listang)):
    angles[i]=float(listang[i])
    slopel[i]=math.tan(math.radians(angles[i]))
#Store the inclination angles as floats
inclangs= [0] * len(listincl)
for j in range(len(listincl)):
    inclangs[j]=float(listincl[j])
# Define the colors we will use in RGB format
YELLOW = (255, 255,  0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
BLACK = (  0,   0,   0)
#Start the pygame interface
pygame.init()
#Initialize values for the visual interface
#Setting screen
mapsize = width, height = 930,930
screensize = 1400,930
screen = pygame.display.set_mode(screensize)
#Loading image objects
pygame.display.set_caption("Aarhus Map")
layer = pygame.image.load("mapaarhusn.png") 
cursor=pygame.image.load("arrow.png")
circul=pygame.image.load("bluecircle.png")
#Initializing variables for visual objects
m=0
ind1=0
ind2=0
coordx,coordy=0,0
mousex,mousey=0,0
movex, movey=0,0
endx,endy=0,0
opx,opy=0,0
slope=0
angledeg=0
inclang=0
myfont=pygame.font.Font(None,30)
myfont2=pygame.font.Font(None,20)
#This scale is based on the map size to point the sky correctly
scale=5
#Draw the map in the screen
screen.blit(layer,(0,0))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() #Exit execution when closing wind1ow
        #You can use the left-right keys to change de direction angle
        elif event.type == pygame.KEYDOWN:
            if event.key == K_LEFT: #When left key gets pressed
                if ind1 > 0: #safe limits
                    ind1-=1
                    print m,coordx,coordy
            elif event.key == K_RIGHT: #when right key gets pressed
                if ind1 <(len(listang)-1): #safe limits
                    ind1+=1
                    print m,coordx,coordy
            #You can use the up-down keys to change de inclination angle
            elif event.key == K_UP: #When up key gets pressed
                if ind2 > 0: #safe limits
                    ind2-=1
                    print m,coordx,coordy
            elif event.key == K_DOWN: #when down key gets pressed
                if ind2 <(len(listincl)-1): #safe limits
                    ind2+=1
                    print m,coordx,coordy
    mousex,mousey=pygame.mouse.get_pos() #gets the position of the cursor
    mousex-=10
    mousey-=20 #alligns the cursor icon
    #Choose an angle and slope from the list created by the csv file
    angledeg=angles[ind1]
    slope=slopel[ind1]
    inclang=inclangs[ind2]
    #Chooses the end coordinates of each line to be drawn according to angle
    #When angle between 0 and 89
    if angledeg < 90.0:
        endy=0
        endx=(width/2)-((width/2)*slope)
        if endx<0:
            endy=(height/2)-((height/2)/slope)
            endx=0
        opy=height-endy
        opx=width-endx
        #Calculate the (x,y) coordinates in the line according to inclination
        if (endx-opx)!=0:
            m=((endy-opy)/(endx-opx))
        coordx=endx-(((endx-opx)/180)*inclang)
        coordy=endy-((m*((endx-opx)/180))*inclang)
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
            if endx<0:
                endy=(height/2)-((height/2)/slope)
                endx=0
        opy=height-endy
        opx=width-endx
        #Calculate the (x,y) coordinates in the line according to inclination
        if (endx-opx)!=0:
            m=((endy-opy)/(endx-opx))
        coordx=endx-(((endx-opx)/180)*inclang)
        coordy=endy-((m*((endx-opx)/180))*inclang)
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
            if endx>width:
                endy=(height/2)+((height/2)/slope)
                endx=width
            opy=height-endy
            opx=width-endx
            #Calculate the (x,y) coordinates in the line according to inclination
            if (endx-opx)!=0:
                m=((endy-opy)/(endx-opx))
            coordx=endx-(((endx-opx)/180)*inclang)
            coordy=endy-((m*((endx-opx)/180))*inclang)
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
            if endx>width:
                endy=(height/2)+((height/2)/slope)
                endx=width
            opy=height-endy
            opx=width-endx
            #Calculate the (x,y) coordinates in the line according to inclination
            if (endx-opx)!=0:
                m=((endy-opy)/(endx-opx))
            coordx=endx-(((endx-opx)/180)*inclang)
            coordy=endy-((m*((endx-opx)/180))*inclang)
    #When angle exactly 360
    else:
        endy=0
        endx=width/2
        opy=0
        opx=width/2
    #The screen is updated by:
    pygame.display.update()
    #Black background
    screen.fill(BLACK)
    #Draw map again
    screen.blit(layer,(0,0))
    #Draw the lines
    pygame.draw.line(screen,YELLOW,(width/2,height/2),(opx,opy),3)
    pygame.draw.line(screen,GREEN,(width/2,height/2),(endx,endy),3)
    #Draw text right side of screen
    textang1=myfont.render("Angle 1: "+str(angledeg)+" degrees",0,GREEN)
    textang2=myfont.render("Angle 2: "+str(inclang)+" degrees",0,BLUE)
    textcirc=myfont2.render(str(inclang),0,BLUE)
    screen.blit(textang1,(1000,80))
    screen.blit(textang2,(1000,110))
    #Draw image objects
    screen.blit(cursor,(mousex,mousey))
    screen.blit(circul,(coordx-30,coordy-30))
    #Draw text for angles insode circle
    screen.blit(textcirc,(coordx,coordy))
    
    
    


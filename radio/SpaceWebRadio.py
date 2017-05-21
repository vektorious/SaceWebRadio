#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 14:20:33 2016

@author: Alex
"""

import pygame
import datetime, time
import sys
from pygame.locals import *
import subprocess
import os
import mpd

pygame.init()

touchscreen = True
size = "7inch"  # 7inch oder 3.5inch possible

if size is "3.5inch":
    display_width = 480
    display_height = 320
    button_width = 75
    button_height = 40
    next_width = 35
    next_height = 40
    skinpath = "/home/pi/SpaceWebRadio/radio/skin/3.5inch/"

if size is "7inch":
    display_width = 1024
    display_height = 600
    button_width = 112
    button_height = 60
    next_width = 53
    next_height = 60
    skinpath = "/home/pi/SpaceWebRadio/radio/skin/7inch/"

height_radiostations = (display_height/10)*8
width_radiobuttons = ((display_width/10)*9)-(display_width/10) - next_width
radiobuttons_per_bar = 5
radiobutton_distance = (width_radiobuttons/5)

#init MPC
mpc = mpd.MPDClient(use_unicode=True)
mpc.timeout = 10
mpc.idletimeout = None
mpc.connect("localhost", 6600)

#Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (150, 0, 0)
green = (0, 150, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
graywhite = (189, 216, 245)

#Fonts
if size is "3.5inch":
    largeText = pygame.font.SysFont("freeserif", 25, bold=1)
    mediumText = pygame.font.SysFont("freeserif", 20, bold=1)
    smallText = pygame.font.SysFont("freeserif", 15, bold=0)
    smallTextb = pygame.font.SysFont("freeserif", 16, bold=1)

if size is "7inch":
    largeText = pygame.font.SysFont("freeserif", 27, bold=1)
    mediumText = pygame.font.SysFont("freeserif", 22, bold=1)
    smallText = pygame.font.SysFont("freeserif", 17, bold=0)
    smallTextb = pygame.font.SysFont("freeserif", 18, bold=1)

#init clock
clock = pygame.time.Clock()

#hide Cursor
pygame.mouse.set_cursor((8,8), (4,4), (0,0,0,0,0,0,0,0), (0,0,0,0,0,0,0,0))

timenow = ""

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def txt(text, font, color, x, y, kill=False, killline=False, center=True):
    if kill is True:
        if center is True:
            if killline is False:
                TextSurf, TextRect = text_objects(text, font, color)
                TextRect.center = (x, y)
                pygame.draw.rect(screen, black, TextRect)
            else:
                TextSurf, TextRect = text_objects(text, font, color)
                pygame.draw.rect(screen, black, (0, y - 0.5 * TextRect[3], display_width, TextRect[3] + 20))

            TextSurf, TextRect = text_objects(text, font, color)
            TextRect.center = (x, y)
            screen.blit(TextSurf, TextRect)
        else:
            if killline is False:
                TextSurf, TextRect = text_objects(text, font, color)
                pygame.draw.rect(screen, black, (x, y, TextRect[2] + x, TextRect[3] + y))
            else:
                TextSurf, TextRect = text_objects(text, font, color)
                pygame.draw.rect(screen, black, (0, y, display_width, TextRect[3] + 20))

            TextSurf, TextRect = text_objects(text, font, color)
            screen.blit(TextSurf, (x, y))
    else:
        if center is True:
            TextSurf, TextRect = text_objects(text, font, color)
            TextRect.center = (x, y)
            screen.blit(TextSurf, TextRect)
        else:
            TextSurf, TextRect = text_objects(text, font, color)
            screen.blit(TextSurf, (x, y))

def button(msg, x, y, w, h, tc, frame=None, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        txt(msg, smallTextb, tc, (x + (w / 2)), (y + (h / 2)))
        if click[0] is 1 and action is not None:
            action()
            clock.tick(15)
    else:
        txt(msg, smallText, tc, (x + (w / 2)), (y + (h / 2)))

    if frame is not None:
        buttonbg = Background(frame, [x, y])
        screen.blit(buttonbg.image, buttonbg.rect)


def radiobutton(sender, x, y, tc, plnum, frame=True):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + button_width > mouse[0] > x and y + button_height > mouse[1] > y:
        txt(sender, smallTextb, tc, (x + (button_width/ 2)), (y + (button_height/ 2)))
        if click[0] is 1:
            mpc.play(plnum)
            playingatm = mpc.currentsong().get("title")
            clock.tick(60)
    else:
        txt(sender, smallText, tc, (x + (button_width / 2)), (y + (button_height / 2)))

    if frame is True:
        buttonbg = Background(skinpath + "buttonbg.png", [x, y])
        screen.blit(buttonbg.image, buttonbg.rect)


def do():
    print "mpc.play(1)"
    global playingatm
    playingatm = "update"#mpc.currentsong().get("title")


def dont():
    print "mpc.play(0)"
    global playingatm
    playingatm = "update"#mpc.currentsong().get("title")


def quitit():
    mpc.stop()
    global running
    running = False

def nextr():
    global rs_screen
    rs_screen += 1

def nextl():
    global rs_screen
    rs_screen -= 1

#init screen
if touchscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Space Web Radio")
back = Background(skinpath + "bg.jpg", [0, 0])
screen.blit(back.image, back.rect)

num_of_rs_screens = 2
rs_screen = 0

running = True
try:
    while running:
        screen.fill([255, 255, 255])
        screen.blit(back.image, back.rect)

        #playingatm = "dummydummy" + str(datetime.datetime.now())[17:19]
        playingatm = mpc.currentsong().get("title")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if rs_screen is 0:
            radiobutton("FM4", (display_width/10) + next_width/2 - button_width/2 + radiobutton_distance*1, height_radiostations, white, 0)
            radiobutton("EgoFM", (display_width/10) + next_width/2 - button_width/2 + radiobutton_distance*2, height_radiostations, white, 1)
            radiobutton("BR3", (display_width/10) + next_width/2 - button_width/2 + radiobutton_distance*3, height_radiostations, white, 2)
            radiobutton("DR", (display_width/10) + next_width/2 - button_width/2 + radiobutton_distance*4, height_radiostations, white, 3)
            button("", ((display_width/10)*9)-next_width, height_radiostations, next_width, next_height, white, frame=skinpath + "rnext.png", action=nextr)

        elif rs_screen is 1:
            button("", (display_width/10), height_radiostations, next_width, next_height, white, frame=skinpath + "lnext.png", action=nextl)
            radiobutton("DRW", (display_width/10) + next_width/2 - button_width/2 + radiobutton_distance*1, height_radiostations, white, 4)
            radiobutton("FhE", (display_width/10) + next_width/2 - button_width/2 + radiobutton_distance*2, height_radiostations, white, 6)
            radiobutton("PlanetR", (display_width/10) + next_width/2 - button_width/2 + radiobutton_distance*3, height_radiostations, white, 6)
            radiobutton("RA", (display_width/10) + next_width/2 - button_width/2 + radiobutton_distance*4, height_radiostations, white, 6)
            button("", ((display_width/10)*9)-next_width, height_radiostations, next_width, next_height, white, frame=skinpath + "rnext.png", action=nextr)

        elif rs_screen is 2:
            button("", (display_width/10), height_radiostations, next_width, next_height, white, frame=skinpath + "lnext.png", action=nextl)
            radiobutton("M94,5", (display_width/10) + next_width/2 - button_width/2 + radiobutton_distance*1, height_radiostations, white, 0)
            radiobutton("VW", (display_width/10) + next_width/2 - button_width/2 + radiobutton_distance*2, height_radiostations, white, 1)
            radiobutton("XY", (display_width/10) + next_width/2 - button_width/2 + radiobutton_distance*3, height_radiostations, white, 2)
            radiobutton("Z", (display_width/10) + next_width/2 - button_width/2 + radiobutton_distance*4, height_radiostations, white, 3)

        button("Quit", (display_width/10)*9, (display_height/50), button_width, button_height, white, action=quitit)

        txt("SpaceWebRadio", largeText, graywhite, (display_width / 2), (display_height / 10))

        timenow = str(datetime.datetime.now())[0:19]
        txt(timenow, mediumText, graywhite, (display_width / 2), (display_height / 5))

        txt("Radiostations:", mediumText, graywhite, (display_width / 20), display_height*0.7, center=False)

        txt("Playing:", mediumText, graywhite, (display_width / 20), display_height*0.3, center=False)

        txt(playingatm, mediumText, graywhite, (display_width / 20), ((display_height / 3) + 50), killline=True, center=False)

        pygame.display.update()
        clock.tick(15)

    pygame.quit()

except SystemExit:
    pygame.quit()

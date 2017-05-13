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

path = "/home/pi/SpaceWebRadio"

display_width = 480
display_height = 320


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
largeText = pygame.font.SysFont("freeserif", 25, bold=1)
mediumText = pygame.font.SysFont("freeserif", 20, bold=1)
smallText = pygame.font.SysFont("freeserif", 15, bold=0)
smallTextb = pygame.font.SysFont("freeserif", 16, bold=1)

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

    if x + 75 > mouse[0] > x and y + 40 > mouse[1] > y:
        txt(sender, smallTextb, tc, (x + (75/ 2)), (y + (40/ 2)))
        if click[0] is 1:
            mpc.play(plnum)
            playingatm = mpc.currentsong().get("title")
            clock.tick(60)
    else:
        txt(sender, smallText, tc, (x + (75 / 2)), (y + (40 / 2)))

    if frame is True:
        buttonbg = Background(path + "/radio/skin/buttonbg.png", [x, y])
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
#screen = pygame.display.set_mode((display_width, display_height))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Dem Alex sein Radio")
back = Background(path + "/radio/skin/bg.jpg", [0, 0])
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
            radiobutton("FM4", 75, 250, white, 0)
            radiobutton("EgoFM", 160, 250, white, 1)
            radiobutton("BR3", 245, 250, white, 2)
            radiobutton("DR", 330, 250, white, 3)
            button("", (display_width - 50), 250, 35, 40, white, frame=path + "/radio/skin/rnext.png", action=nextr)

        elif rs_screen is 1:
            button("", 15, 250, 35, 40, white, frame=path + "/radio/skin/lnext.png", action=nextl)
            radiobutton("DRW", 75, 250, white, 4)
            radiobutton("FhE", 160, 250, white, 6)
            radiobutton("PlanetR", 245, 250, white, 6)
            radiobutton("RA", 330, 250, white, 6)
            #button("", (display_width - 50), 250, 35, 40, white, frame="/Users/Alex/Desktop/skin/rnext.png", action=nextr)

        elif rs_screen is 2:
            button("", 15, 250, 35, 40, white, frame=path + "/radio/skin/lnext.png", action=nextl)
            radiobutton("M94,5", 75, 250, white, 0)
            radiobutton("VW", 160, 250, white, 1)
            radiobutton("XY", 245, 250, white, 2)
            radiobutton("Z", 330, 250, white, 3)

        button("Quit", (display_width - 75), 20, 75, 40, white, action=quitit)

        txt("Dem Alex sein Radio", largeText, graywhite, (display_width / 2), (display_height / 10))

        timenow = str(datetime.datetime.now())[0:19]
        txt(timenow, mediumText, graywhite, (display_width / 2), (display_height / 5))

        txt("Radiostations:", mediumText, graywhite, 15, 200, center=False)

        txt("Playing:", mediumText, graywhite, 15, 100, center=False)

        txt(playingatm, mediumText, graywhite, 15, ((display_height / 3) + 50), killline=True, center=False)

        pygame.display.update()
        clock.tick(15)

    pygame.quit()

except SystemExit:
    pygame.quit()

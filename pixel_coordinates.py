#!/usr/bin/env python

from __future__ import print_function
import pygame

spamRect = pygame.Rect(10, 20, 200, 300)
a = spamRect == (10, 20, 200, 300)
print(a)
print (spamRect.right)

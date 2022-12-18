#!/usr/bin/env python
__author__ = 'juan camilo carmona sanchez'

"""
This is an attempt to recreate the first level of
Super Mario Bros for the NES.
"""

import sys
import pygame as pg
from data.genetic_algorithm_mario import main
import cProfile
import sys


if __name__=='__main__':
    if len(sys.argv) != 1:
        main(sys.argv[1])
    else:
        main(" ")
    pg.quit()
    sys.exit()
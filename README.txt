|    _________                              _____               .__            _____      .________ |
|   /   _____/__ ________   ___________    /     \ _____ _______|__| ____     /  |  |     |   ____/ |
|   \_____  \|  |  \____ \_/ __ \_  __ \  /  \ /  \\__  \\_  __ \  |/  _ \   /   |  |_    |____  \  |
|   /        \  |  /  |_> >  ___/|  | \/ /    Y    \/ __ \|  | \/  (  <_> ) /    ^   /    /       \ |
|  /_______  /____/|   __/ \___  >__|    \____|__  (____  /__|  |__|\____/  \____   | /\ /______  / |
|         \/      |__|        \/                \/     \/                       |__| \/        \/   |
|__________________________________________________________________________________________________ |

DESCRIPTION:
Super Mario 4.5 is a clone of the game Super Mario World, that shares some mechanics of Super Mario World but only 2 levels. Level 1 is inspired by World 1-1, and Level 2 is similar to the Bowser level of Super Mario World. It will include powerups and different enemies, with the player's goal being to get to the end level.

HOW TO RUN THE PROJECT:
.NOTE THAT THE OPEN IMAGES FILE PATHS ARE DIRECT PATHS ON MY COMPUTER, CHANGE
FILE PATH SO THAT IT MATCHES YOUR COMPUTER

.Imports:
	.from cmu_graphics import *
	.from PIL import Image
	.import os, pathlib
	.import math
	.import random

.Useful keybinds:
	.k to kill mario
	.h to show hitboxes
	.b to switch mario from small to big or vice versa
	.n to switch mario to fire mario
	.x to throw fireball
IMPORTANT NOTES:
	.Level 2 does not have a checkpoint to spawn to, so dying will cause issues
	.Due to load, sometimes mario phases through ground or wall, so you may have to
	 spam jump up

import RPi.GPIO as G
import sys
import random
import time
import colorsys
import math

G.setwarnings(False)
G.setmode(G.BOARD)
r = 11
g = 13
b = 15
u = 7

G.setup(r, G.OUT)
G.setup(g, G.OUT)
G.setup(b, G.OUT)
G.setup(u, G.IN, pull_up_down=G.PUD_DOWN)

def setColor(rr, gg, bb):
    G.output(r, abs(rr-1))
    G.output(g, abs(gg-1))
    G.output(b, abs(bb-1))

def setColorHex(color, bandwidth):
    rc = int((float((color >> 16) & 255) / 255.0) * float(bandwidth))
    gc = int((float((color >> 8) & 255) / 255.0) * float(bandwidth))
    bc = int((float((color >> 0) & 255) / 255.0) * float(bandwidth))
    setColorRGB(rc, gc, bc, bandwidth)

def pqt(p, q, t):
    if(t < 0):
        t += 1
    if(t > 1):
        t -= 1
    if(t < 1.0/6.0):
        return p + (q - p) * 6 * t
    if(t < 1.0/2.0):
        return q
    if(t < 2.0/3.0):
            return p + (q - p) * (2.0/3.0 - t) * 6
    return p

def setColorRGB(rc, gc, bc, bandwidth):
    sector = 0
    print("RGB: " + str(rc) + " " + str(gc) + " " + str(bc))
    while(rc > 0 or gc > 0 or bc > 0):
        sector+=1

        if(sector % 3 == 0 and rc > 0 and gc > 0):
            setColor(1, 1, 0)
            rc-=1
            gc-=1
            continue
        if(sector % 3 == 0 and rc > 0 and bc > 0):
            setColor(1, 0, 1)
            rc-=1
            bc-=1
            continue
        if(sector % 3 == 1 and gc > 0 and bc > 0):
            setColor(0, 1, 1)
            gc-=1
            bc-=1
            continue
        if(sector % 3 == 1 and gc > 0 and rc > 0):
            setColor(1, 1, 0)
            gc-=1
            rc-=1
            continue
        if(sector % 3 == 2 and bc > 0 and rc > 0):
            setColor(1, 0, 1)
            bc-=1
            rc-=1
            continue
        if(sector % 3 == 2 and bc > 0 and gc > 0):
            setColor(0, 1, 1)
            bc-=1
            gc-=1
            continue
        if(sector % 3 == 0 and rc > 0):
            setColor(1, 0, 0)
            rc-=1
            continue
        if(sector % 3 == 1 and gc > 0):
            setColor(0, 1, 0)
            gc-=1
            continue
        if(sector % 3 == 2 and bc > 0):
            setColor(0, 0, 1)
            bc-=1
            continue


def setColorHue(h, bandwidth):
    r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
    print("Hue is " + str(h) + " into " + str(r) + " "+ str(g) + " " + str(b))

    setColorRGB(r * bandwidth, g * bandwidth, b * bandwidth, bandwidth)


def rbool():
    return bool(random.getrandbits(1))

def setRandomColor():
    setColor(rbool(), rbool(), rbool())

setColor(1,1,1)
theBand = int(sys.argv[1])
theSpeed = int(sys.argv[2])
count = 0
h = 0
active = False

while(True):
    if G.input(u) == G.HIGH:
        active = not active
        time.sleep(1)
    if(active):
        count += 1
        setColorHue(float(count % 3600) / 3600.0, theBand)

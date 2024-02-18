# A UnexpectedMaker BLING demo program in Circuitpython 
# based on https://github.com/disq/galactic_effects
# which is based on https://github.com/tuupola/pico_effects
#
# Get your own BLING: https://unexpectedmaker.com/bling
# More BLING On github: https://github.com/UnexpectedMaker/bling
#
# Steven Cogswell February 2024

import board
import digitalio
import neopixel
import time
import math
import adafruit_imageload
import BLING
import random
import rainbowio

def intro():
    """
    All good demos need an intro screen, right?
    """
    FONTS="/fonts/"
    font = FONTS+"font5x8.bin"
    message = "BLING Galactic Effects Demo"
    max_w = 8 * len(message)
    for i in range(max_w):
        the_bling.fill(rainbowio.colorwheel(i*5))
        the_bling.text(message,font,the_bling.width-i,0,color_foreground=(0,0,0))
        the_bling.show()

    # turn off individual pixels
    u=0
    for i in range(bling_num_pixels*2):
        x = random.randint(0,the_bling.width-1)
        y = random.randint(0,the_bling.height-1)
        the_bling.setpixel(x,y,0x00000)
        if u > 5:
            u=0
            the_bling.show()
        u+=1

def plasma_demo():
    """
    Like from https://github.com/disq/galactic_effects but different 
    """
    SPEED=4
    # Plasma Init
    # Generate nice continous palette.
    palette = []
    for i in range(256):
        r = 128+128*math.sin((math.pi * i/128.0)+1)
        g = 128+128*math.sin((math.pi * i/64.0) +1)
        b = 64
        palette.append((r,g,b))

    rounds=5
    for _ in range(rounds):
        bling_palette = []

        f1 = random.random()*7+4.0
        f2 = random.random()*7+2.0
        f3 = random.random()*7+2.0

        for y in range(the_bling.height):
            for x in range(the_bling.width):
                # Generate three different sinusoids.
                v1 = 128+(128.0*math.sin(x / f1))
                v2 = 128+(128.0*math.sin(y / f2))
                v3 = 128+(128.0*math.sin(math.sqrt(x*x + y*y)/f3))
                color = int((v1+v2+v3)/3)
                bling_palette.append(color)
        the_bling.show()

        cycles = 200
        for r in range(cycles):

            p=0
            for y in range(the_bling.height):
                for x in range(the_bling.width):
                    index = (bling_palette[p]+SPEED) % 256
                    bling_palette[p]=index
                    p += 1

            for i in range(len(bling_palette)):
                BLING_raw[i]=palette[bling_palette[i]]
            the_bling.show()
            time.sleep(0.02)

def rotozoom_demo():
    """
    Like from https://github.com/disq/galactic_effects but different 
    """
    rounds = 1000
    SPEED=2
    angle=0
    image, palette = adafruit_imageload.load("bmps/blinga.bmp")
    texture_width = image.width
    texture_height = image.height

    blinka = []
    for i in range(image.width):
        for j in range(image.height):
            blinka.append(palette[image[image.width-i-1,image.height-j-1]])

    sinlut=[]
    coslut=[]
    for i in range(360):
        sinlut.append(math.sin(i*math.pi/180))
        coslut.append(math.cos(i*math.pi/180))

    bound = 20
    x_c = random.randint(-bound,the_bling.width+bound)
    y_c = random.randint(-bound,the_bling.height+bound)
    for _ in range(rounds):
        s = sinlut[angle]
        c = coslut[angle]
        z = s * 2.4
        p=0
        for y in range(the_bling.height):
            for x in range(the_bling.width):
                xn = x-x_c
                yn = y-y_c
                u =abs(int(((xn*s - yn*c)*z-2) % texture_width))
                v =int(((xn*c + yn*s)*z+10) % texture_height)
                # u = abs(u)
                if (v < 0):
                    v += texture_height
                BLING_raw[p]=blinka[u+v*texture_width]
                p+=1
        the_bling.show()
        angle = (angle + SPEED) % 360;
        if (0<= angle < SPEED):
            x_c = random.randint(-bound,the_bling.width+bound)
            y_c = random.randint(-bound,the_bling.height+bound)


def metaballs_demo():
    """
    Like from https://github.com/disq/galactic_effects but different 
    """
    class Ball(object):
        def __init__(self,position_x, position_y ,velocity_x,velocity_y ,radius,color):
            self.position_x = position_x
            self.position_y = position_y
            self.velocity_x = velocity_x
            self.velocity_y = velocity_y
            self.radius = radius
            self.color = color

    NUM_BALLS = random.randint(2,5)
    MIN_VELOCITY = 0.1
    MAX_VELOCITY = 1.5
    MIN_RADIUS = 1
    MAX_RADIUS = 5
    balls = []
    for i in range(NUM_BALLS):
        radius = random.randint(MIN_RADIUS,MAX_RADIUS)
        color = 0xffffff
        position_x = random.randint(0,the_bling.width)
        position_y = random.randint(0,the_bling.height)
        velocity_x = random.random()*MAX_VELOCITY+MIN_VELOCITY
        velocity_y = random.random()*MAX_VELOCITY+MIN_VELOCITY

        b = Ball(position_x,position_y, velocity_x, velocity_y, radius, color)
        balls.append(b)

    rounds = 400
    for round in range(rounds):
        for i in range(NUM_BALLS):
            balls[i].position_x = balls[i].position_x+balls[i].velocity_x
            balls[i].position_y = balls[i].position_y+balls[i].velocity_y

            if balls[i].position_x < 0 or balls[i].position_x > the_bling.width:
                balls[i].velocity_x = -balls[i].velocity_x

            if balls[i].position_y < 0 or balls[i].position_y > the_bling.height:
                balls[i].velocity_y = -balls[i].velocity_y

        p=0
        for y in range(the_bling.height):
            for x in range(the_bling.width):
                sum1 = 0.0
                for i in range(NUM_BALLS):
                    dx = x - balls[i].position_x
                    dy = y - balls[i].position_y

                    d2 = dx*dx + dy*dy
                    if d2 == 0:
                        d2 = 1
                    sum1 += balls[i].radius * balls[i].radius / d2

                    if sum1 > 0.65:
                        color = 0x000000
                    elif sum1 > 0.5:
                        color = rainbowio.colorwheel(round)
                    elif sum1 > 0.4:
                        color = rainbowio.colorwheel(round+5)
                    elif sum1 > 0.3:
                        color = rainbowio.colorwheel(round+10)
                    elif sum1 > 0.2: 
                        color=rainbowio.colorwheel(round+20)
                    else:
                        color = 0x000000

                BLING_raw[p] = color
                p += 1
        the_bling.show()
        time.sleep(0.01)

def plasmazoom_demo():
    """
    Like from https://github.com/disq/galactic_effects but different 

    Everybody must get BLING'd
    """
    rounds = 500
    SPEED=2
    SPEED_PLASMA=4
    angle=0
    image, palette = adafruit_imageload.load("bmps/blinga.bmp")
    texture_width = image.width
    texture_height = image.height

    blinka = []
    for i in range(image.width):
        for j in range(image.height):
            blinka.append(palette[image[image.width-i-1,image.height-j-1]])

    sinlut=[]
    coslut=[]
    for i in range(360):
        sinlut.append(math.sin(i*math.pi/180))
        coslut.append(math.cos(i*math.pi/180))

    # Plasma Init
    # Generate nice continous palette.
    palette = []
    for i in range(256):
        r = 128+128*math.sin((math.pi * i/128.0)+1)
        g = 128+128*math.sin((math.pi * i/64.0) +1)
        b = 64
        palette.append((r,g,b))

    bling_palette = []

    f1 = random.random()*7+4.0
    f2 = random.random()*7+2.0
    f3 = random.random()*7+2.0

    for y in range(the_bling.height):
        for x in range(the_bling.width):
            # Generate three different sinusoids.
            v1 = 128+(128.0*math.sin(x / f1))
            v2 = 128+(128.0*math.sin(y / f2))
            v3 = 128+(128.0*math.sin(math.sqrt(x*x + y*y)/f3))
            color = int((v1+v2+v3)/3)
            bling_palette.append(color)

    bound=20
    x_c = random.randint(-bound,the_bling.width+bound)
    y_c = random.randint(-bound,the_bling.height+bound)
    for _ in range(rounds):
        s = sinlut[angle]
        c = coslut[angle]
        z = s * 2.4
        p=0
        for y in range(the_bling.height):
            for x in range(the_bling.width):

                index = (bling_palette[p]+SPEED_PLASMA) % 256
                bling_palette[p]=index
                
                xn = x-x_c
                yn = y-y_c
                u =abs(int(((xn*s - yn*c)*z-2) % texture_width))
                v =int(((xn*c + yn*s)*z+10) % texture_height)
                if (v < 0):
                    v += texture_height
                BLING_raw[p]=blinka[u+v*texture_width]
                if blinka[u+v*texture_width]==0:
                    BLING_raw[p] = palette[bling_palette[p]]
                p+=1

        the_bling.show()
        angle = (angle + SPEED) % 360;
        if (0<= angle < SPEED):
            x_c = random.randint(-bound,the_bling.width+bound)
            y_c = random.randint(-bound,the_bling.height+bound)


#--------------------------------------------------------------------------------------
# Main Program Execution starts here
#

# BLING is very bright.   It also consumes a lot of current when very bright.
BLING_BRIGHTNESS = 0.08

# Enable power to BLING pixel display
bling_power = digitalio.DigitalInOut(board.MATRIX_POWER)
bling_power.switch_to_output()
bling_power.value=True

# Setup BLING neopixel and PixelFrameBuffer objects
bling_pixel_width, bling_pixel_height = BLING.display.pixel_size()
bling_num_pixels = bling_pixel_width * bling_pixel_height
BLING_raw = neopixel.NeoPixel(board.MATRIX_DATA,bling_num_pixels,brightness=BLING_BRIGHTNESS,auto_write=False)

# In the demo the BLING display object is named "the_bling" so you can see
# where the derived object is used more easily.
the_bling = BLING.display(matrix=BLING_raw,rotation=2)

intro()

while True:

    metaballs_demo()

    rotozoom_demo()

    plasma_demo()

    plasmazoom_demo()


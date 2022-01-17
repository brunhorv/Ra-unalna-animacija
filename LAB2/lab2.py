import pyglet
import math
import numpy as np
import random
from pyglet.gl import *

pos = [0, 0, -20]

e = [0, 0, 0]
os = [0, 0, 0]

config = Config(sample_buffers=1, samples=8)
app = pyglet.window.Window(height=500, width=500, config=config)
app.set_caption('Računalna animacija - 2. laboratorijska vježba')
clk = 0

all_shapes = list()


def create_shapes(n, index=None):
    for _ in range(n):
        vel_x = random.uniform(-0.2, 0.2)
        vel_y = random.uniform(-0.2, 0.2)
        x = random.uniform(-2, 2)
        y = random.uniform(-2, 2)
        z = 0
        t = random.uniform(0, 100)
        r = 0
        g = 1.0
        b = 0
        if index is not None:
            all_shapes[index] = [x, y, z, vel_x, vel_y, t, [r, g, b], 0.8/t, 1]
        else:
            all_shapes.append([x, y, z, vel_x, vel_y, t, [r, g, b], 0.8/t, 1])


def calc(i):
    e[0] = all_shapes[i][0] - pos[0]
    e[1] = all_shapes[i][1] - pos[1]
    e[2] = all_shapes[i][2] - pos[2]

    s = [0.0, 0.0, -1.0]

    os[0] = s[1] * e[2] - e[1] * s[2]
    os[1] = e[0] * s[2] - s[1] * e[2]
    os[2] = s[0] * e[1] - s[1] * e[0]

    s_norm = math.sqrt(s[0] ** 2 + s[1] ** 2 + s[2] ** 2)
    e_norm = math.sqrt(e[0] ** 2 + e[1] ** 2 + e[2] ** 2)

    dot = s[0] * e[0] + s[1] * e[1] + s[2] * e[2]

    cos_phi = dot / (s_norm * e_norm)
    angle_rad = np.arccos(cos_phi)
    angle = 180 * angle_rad / np.pi
    angle = 180 - angle

    all_shapes[i][0] = all_shapes[i][0] + all_shapes[i][3]
    all_shapes[i][1] = all_shapes[i][1] + all_shapes[i][4]

    return angle, os


@app.event
def on_draw():

    app.clear()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(*pos)

    for i in range(len(all_shapes)):

        angle, os = calc(i)
        if all_shapes[i][5] <= 0:
            create_shapes(1, index=i)

        glPushMatrix()
        glTranslatef(all_shapes[i][0], all_shapes[i][1], 0)
        glRotatef(angle, os[0], os[1], os[2])

        glColor3f(all_shapes[i][6][0],
                  all_shapes[i][6][1],
                  all_shapes[i][6][2])
        glBegin(GL_POLYGON)

        size = all_shapes[i][8] - all_shapes[i][7]
        all_shapes[i][8] = size

        glVertex3f(-size + all_shapes[i][0], -size + all_shapes[i][1], 0)
        glVertex3f(size + all_shapes[i][0], -size + all_shapes[i][1], 0)
        glVertex3f(size + all_shapes[i][0], size + all_shapes[i][1], 0)
        glVertex3f(-size + all_shapes[i][0], size + all_shapes[i][1], 0)
        glEnd()
        glPopMatrix()

        all_shapes[i][5] -= 1
        all_shapes[i][6][1] -= all_shapes[i][7]

    glFlush()


def update(interval):
    global clk
    clk += 1


create_shapes(50)
pyglet.clock.schedule_interval(update, interval=0.05)
pyglet.app.run()

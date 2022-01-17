import pyglet
from pyglet import graphics as graphics
from pyglet.gl import Config, GL_LINE_LOOP, GL_LINE_STRIP, glViewport,  \
                  glMatrixMode, GL_PROJECTION, glLoadIdentity, glOrtho, \
                  GL_MODELVIEW, gluPerspective, glTranslatef, glRotatef, \
                  glPushMatrix, glScalef, GL_LINES, glPopMatrix, glFlush
from pyglet.window import Window
from load_file import load_elements, load_spline
from parameters import *
import argparse


def parse():
    parser = argparse.ArgumentParser(description='Program to draw B-Spline.')
    parser.add_argument("--object_file", help="File containing verticies and polygons of object.", default=object_file)
    parser.add_argument("--verticies_file", help="File with verticies of B-Spline.", default=verticies_file)
    parser.add_argument("--screen_resolution", help="Resolution of screen for plot", default=window_dim)
    parser.add_argument("--dot_number", help="Number of B-Spline dots to calculate.", default=dot_number)
    args = parser.parse_args()
    return args


def calculate():

    counter = 0

    for i in range(len(spline_verticies) - 3):
        r_vectors = np.vstack(
            (spline_verticies[i], spline_verticies[i + 1], spline_verticies[i + 2], spline_verticies[i + 3])
        )

        for t in t_values:

            derivative = p_t_derivative(t) @ N_cubbic_coeff_derivative @ r_vectors
            derivatives[counter] = derivative

            p_t = t_cubbic_coeff(t) @ N_cubbic_coeff @ r_vectors
            points[counter] = p_t
            counter+=1


args = parse()

object_file, verticies_file, dot_number, window_dim = args.object_file, args.verticies_file, \
                                          int(args.dot_number), int(args.screen_resolution)

app = Window(width=window_dim, height=window_dim, config=Config(sample_buffers=1, samples=0), resizable=True)
clk=0
t_values = [x for x in np.arange(0, 1, 1 / dot_number)]

body=graphics.Batch()
bspline=graphics.Batch()

spline_verticies = load_spline(verticies_file)


verticies, polygons = load_elements(object_file)

for poly in polygons:

    vrh1, vrh2, vrh3 = poly

    body.add(3, GL_LINE_LOOP, None,
             ("v3f", (verticies[vrh1][x_coord], verticies[vrh1][y_coord], verticies[vrh2][z_coord],
                      verticies[vrh2][x_coord], verticies[vrh2][y_coord], verticies[vrh2][z_coord],
                      verticies[vrh3][x_coord], verticies[vrh3][y_coord], verticies[vrh3][z_coord])),
             ('c3B', (255, 255, 51, 0, 0, 221, 255, 255, 51)))



points = np.zeros(shape=(len(t_values) * (len(spline_verticies) - 3),3))
derivatives = np.zeros(shape=(len(t_values) * (len(spline_verticies) - 3), 3))

calculate()

bspline.add(len(points), GL_LINE_STRIP, None, ("v3f", points.flatten()))

@app.event
def on_resize(width, height):
    print(f'Window resized: h,w={height},{width}')
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)


@app.event
def on_draw():
    app.clear()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(50, 1, 5, 150)
    glRotatef(30, 1, 0, 0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, -30, -70)
    glRotatef(-40, 1, 0, 0)
    glTranslatef(-5, -20, 0)

    point = points[clk]

    glPushMatrix()
    glTranslatef(point[x_coord], point[y_coord], point[z_coord])
    glScalef(scale,scale,scale)

    derivative_vec = derivatives[clk]

    x_vec = point[x_coord] + derivative_vec[x_coord]
    y_vec = point[y_coord] + derivative_vec[y_coord]
    z_vec = point[z_coord] + derivative_vec[z_coord]

    bspline.add(2, GL_LINES, None, ("v3f", [point[x_coord], point[y_coord], point[z_coord],
                                            x_vec,
                                            y_vec,
                                            z_vec]),
                                            ("c4B", (0, 255, 0, 0, 255, 0, 0, 0)))

    e_vec=derivatives[clk]
    rotation_vec = np.cross(s_vec, e_vec, axis=0)

    cos_phi = np.dot(s_vec, e_vec) / (np.linalg.norm(s_vec) * np.linalg.norm(e_vec))
    angle_rad = np.arccos(cos_phi)
    angle = 180 * angle_rad / np.pi

    glRotatef(angle, rotation_vec[x_coord], rotation_vec[y_coord], rotation_vec[z_coord])
    body.draw()

    glPopMatrix()
    bspline.draw()
    glFlush()


def update(interval):
    global clk
    clk+=1
    if clk==len(points):
        clk=0


pyglet.clock.schedule_interval(update, interval=0.05)
pyglet.app.run()

if __name__ == "__main__":
    pass

import logging
from parameters import x_coord, y_coord, z_coord


def load_elements(path):
    verticies, polygons = list(), list()
    try:
        f = open(path, 'r')
    except Exception:
        logging.exception(f'Could not opet file \"{path}\", please check its name again.')
        exit(1)

    for line in f.readlines():
        if (line[0] == 'v'):
            elements = line.split()
            list_elem = list()
            list_elem.append(float(elements[1]))
            list_elem.append(float(elements[2]))
            list_elem.append(float(elements[3]))
            verticies.append(list_elem)

    try:
        f = open(path, 'r')
    except Exception:
        logging.exception(f'Could not opet file \"{path}\", please check its name again.')
        exit(1)

    for line in f.readlines():
        if (line[0] == 'f'):
            elements = line.split()
            polygon = list()
            polygon.append(int(elements[1]) - 1)
            polygon.append(int(elements[2]) - 1)
            polygon.append(int(elements[3]) - 1)
            polygons.append(polygon)
    return verticies, polygons


def load_spline(path):

    try:
        f = open(path, 'r')
    except Exception:
        logging.exception(f'Could not opet file \"{path}\", please check its name again.')
        exit(1)

    verticies = list()

    for line in f.readlines():
        elements = line.split()
        list_elem = []
        list_elem.append(float(elements[x_coord]))
        list_elem.append(float(elements[y_coord]))
        list_elem.append(float(elements[z_coord]))
        verticies.append(list_elem)
    return verticies
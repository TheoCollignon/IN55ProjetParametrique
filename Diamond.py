import pygame
import math
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


# xc et yc et zc = coordoonées du cercle // n le nombre de point répartit // r le rayon du cercle
def circle(xc, yc, n, r, zc):
    listCoord = []
    for k in range(n):
        x = xc + r * math.cos(k * ((2 * math.pi) / n))
        y = yc + r * math.sin(k * ((2 * math.pi) / n))
        # optionals if
        if (1 ** -10 > x > 0) or (-1 ** -10 < x < 0):
            x = 0
        if (1 ** -10 > y > 0) or (-1 ** -10 < y < 0):
            y = 0
        listCoord.append([x, y, zc])

    return listCoord


# Diamant v1 :
# topCircle = circle(0, 0, 6, 3, 8)
# middleCircle = circle(0, 0, 6, 6, 6)
# bottomCircle = circle(0, 0, 1, 0, 0)

# Diamant v2 :
# topCircle = circle(0, 0, 6, 3, 8)
# middleCircle = circle(0, 0, 12, 6, 6)
# bottomCircle = circle(0, 0, 1, 0, 0)

# Diamant v3 :
# shinyCircle = circle(0, 0, 9, 3, 9)
# topCircle = circle(0, 0, 9, 7, 8)
# middleCircle = circle(0, 0, 18, 10, 6)
# bottomCircle = circle(0, 0, 1, 0, -5)

# Diamant v4 :
shinyCircle = circle(0, 0, 8, 3, 9)
topCircle = circle(0, 0, 8, 7, 8)
middleCircle = circle(0, 0, 16, 10, 6)
bottomCircle = circle(0, 0, 1, 0, -5)

if True:  # si on veut le diamant v4 turn this to true
    topCircle = circle(0, 0, 16, 7, 8)
    topCircleBis = []
    for i in range(len(topCircle)):
        if i % 2 != 0:
            topCircleBis.append(topCircle[i])
    topCircle = topCircleBis

# Goutte
# topCircle = circle(0, 0, 1, 0, 12)
# middleCircle = circle(0, 0, 5, 4, 2)
# bottomCircle = circle(0, 0, 1, 0, 0)

verticies = []
for x in bottomCircle:
    verticies.append(x)
for x in middleCircle:
    verticies.append(x)
for x in topCircle:
    verticies.append(x)
for x in shinyCircle:
    verticies.append(x)

nbBottomPts = 1
nbMiddlePts = len(middleCircle)
nbTopPts = len(topCircle)
nbShinyPts = len(shinyCircle)

edges = []

# Point du bas vers le milieu
for x in range(nbMiddlePts + 1):
    edges.append([0, x])

# Couronne du milieu
for x in range(1, nbMiddlePts):
    edges.append([x, x + 1])
edges.append([1, nbMiddlePts])

# Couronne du haut
for x in range(1, nbTopPts):
    edges.append([nbMiddlePts + x, nbMiddlePts + x + 1])
edges.append([nbMiddlePts + 1, nbMiddlePts + nbTopPts])

# Couronne supplémentaire du diamant v3
for x in range(1, nbShinyPts):
    edges.append([nbMiddlePts + nbTopPts + x, nbMiddlePts + nbTopPts + x + 1])
edges.append([nbMiddlePts + nbTopPts + 1, nbMiddlePts + nbTopPts + nbShinyPts])

# Milieu vers le haut
if nbMiddlePts == nbTopPts:  # Même nombre de points
    for x in range(1, nbMiddlePts + 1):
        edges.append([x, nbMiddlePts + x])

# elif nbMiddlePts == nbTopPts * 2:  # Deux fois plus de points au milieu avec espacement base
#     temp = 1
#     for x in range(1, nbTopPts + 1):
#         edges.append([temp, nbMiddlePts + x])
#         edges.append([temp + 1, nbMiddlePts + x])
#         temp = temp + 2

elif nbMiddlePts == nbTopPts * 2:  # Deux fois plus de points au milieu sans espacements base
    temp = 1
    for x in range(1, nbTopPts + 1):
        edges.append([temp, nbMiddlePts + x])
        edges.append([temp + 1, nbMiddlePts + x])
        edges.append([temp + 2, nbMiddlePts + x])
        temp = temp + 2
    edges.append([temp + nbTopPts - 1, 1])



elif nbMiddlePts == nbTopPts * 3:  # trois fois plus de points au milieu
    temp = 0
    for x in range(1, nbTopPts + 1):
        if temp == 0:
            edges.append([nbMiddlePts + (x - 1), nbMiddlePts + x])
        else:
            edges.append([temp, nbMiddlePts + x])
        edges.append([temp + 1, nbMiddlePts + x])
        edges.append([temp + 2, nbMiddlePts + x])
        temp = temp + 3

# from top to shiny avec points séparé
# if nbShinyPts == nbTopPts:  # Même nombre de points
#     for x in range(1, nbShinyPts + 1):
#         edges.append([nbMiddlePts + x, nbMiddlePts + nbTopPts + x])

# from top to shiny avec points collé
if nbShinyPts == nbTopPts:  # Même nombre de points
    for x in range(1, nbShinyPts + 1):
        if x != 1:
            edges.append([nbMiddlePts + x - 1, nbMiddlePts + nbTopPts + x])
        edges.append([nbMiddlePts + x, nbMiddlePts + nbTopPts + x])
    edges.append([nbMiddlePts + nbShinyPts +1, nbMiddlePts + nbTopPts ])


elif nbMiddlePts + nbTopPts == nbShinyPts * 2:  # Deux fois plus de points au milieu
    temp = 1
    for x in range(1, nbShinyPts + 1):
        edges.append([temp, nbMiddlePts + nbTopPts + x])
        edges.append([temp + 1, nbMiddlePts + nbTopPts + x])
        temp = temp + 2

# Un seul point du haut
elif nbTopPts == 1:
    for x in range(nbMiddlePts + 1):
        edges.append([x, nbMiddlePts + 1])


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.5, 70.0)

    glTranslatef(0.0, 0.0, -40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()

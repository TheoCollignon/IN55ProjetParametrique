import random

import pygame
import math

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

colorsBlue = (
    (0, 0, 1, 0),
    (0.7, 0.7, 1, 0),
    (0, 1, 1, 0),
    (0, 1, 1, 0),
    (0, 0, 1, 0),
    (0, 0, 1, 0),
    (0.2, 0.2, 0.7, 0),
    (0, 1, 0.7, 0),
    (0, 1, 1, 0),
)

colorsRed = (
    (0.9, 0.2, 0, 0),
    (0.8, 0.5, 0, 0),
    (1, 0, 0, 0),
    (1, 0, 0, 0),
    (0.9, 0.2, 0, 0),
    (1, 0.5, 0, 0),
    (0.8, 0.6, 0.3, 1),
    (1, 0.5, 0.2, 0),
    (1, 0.2, 0.2, 0),
)

colorsGreen = (
    (0, 1, 1, 0),
    (0.2, 0.7, 0.2, 0),
    (0, 0.7, 0, 0),
    (0, 1, 0, 0),
    (0.2, 0.7, 0.2, 0),
    (0, 0.7, 0, 0),
    (0.5, 1, 0.5, 0),
    (0, 1, 0.7, 0),
    (0.3, 1, 0, 0),
)


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


def createDiamond(diamond, listCoeff, listBool):
    coeffHeight = listCoeff[0]
    coeffRayonBottom = listCoeff[1]
    coeffRayonMiddle = listCoeff[2]
    coeffRayonTop = listCoeff[3]
    coeffRayonShiny = listCoeff[4]
    addNbVerticies = listCoeff[5]

    if addNbVerticies < -4:
        addNbVerticies = -4

    # Diamant v1 :
    if diamond == 1:
        topCircle = circle(0, 0, 6 + addNbVerticies, 3 * (coeffRayonTop + 1), 6 * (coeffHeight + 1))
        middleCircle = circle(0, 0, 6 + addNbVerticies, 6 * (coeffRayonMiddle + 1), 4 * (coeffHeight + 1))
        bottomCircle = circle(0, 0, 1, 0 * (coeffRayonBottom + 1), -2 * (coeffHeight + 1))
        shinyCircle = []

    # Diamant v2 :
    if diamond == 2:
        shinyCircle = []
        topCircle = circle(0, 0, 6 + addNbVerticies, 3 * (coeffRayonTop + 1), 6 * (coeffHeight + 1))
        middleCircle = circle(0, 0, 12 + addNbVerticies*2, 6 * (coeffRayonMiddle + 1), 4 * (coeffHeight + 1))
        bottomCircle = circle(0, 0, 1, 0 * (coeffRayonBottom + 1), -2 * (coeffHeight + 1))

    # Diamant v3 :
    if diamond == 3:
        shinyCircle = circle(0, 0, 9 + addNbVerticies, 3 * (coeffRayonShiny + 1), 9 * (coeffHeight + 1))
        topCircle = circle(0, 0, 9+ addNbVerticies, 7 * (coeffRayonTop + 1), 8 * (coeffHeight + 1))
        middleCircle = circle(0, 0, 18 + addNbVerticies*2, 10 * (coeffRayonMiddle + 1), 6 * (coeffHeight + 1))
        bottomCircle = circle(0, 0, 1, 0 * (coeffRayonBottom + 1), -5 * (coeffHeight + 1))

    if diamond == 4:
        # Diamant v4 :
        shinyCircle = circle(0, 0, 8+ addNbVerticies, 3 * (coeffRayonShiny + 1), 9 * (coeffHeight + 1))
        topCircle = circle(0, 0, 16 + addNbVerticies * 2 , 7 * (coeffRayonTop + 1), 8 * (coeffHeight + 1))
        middleCircle = circle(0, 0, 16 + addNbVerticies * 2, 10 * (coeffRayonMiddle + 1), 6 * (coeffHeight + 1))
        bottomCircle = circle(0, 0, 1, 0 * (coeffRayonBottom + 1), -5 * (coeffHeight + 1))

        topCircleBis = []
        for i in range(len(topCircle)):
            if i % 2 != 0:
                topCircleBis.append(topCircle[i])
        topCircle = topCircleBis

    # Goutte
    if diamond == 5:
        shinyCircle = []
        topCircle = circle(0, 0, 1, 0 * (coeffRayonShiny + 1), 7 * (coeffHeight + 1))
        middleCircle = circle(0, 0, 6 + addNbVerticies, 4 * (coeffRayonShiny + 1), -3 * (coeffHeight + 1))
        bottomCircle = circle(0, 0, 1, 0 * (coeffRayonShiny + 1), -5 * (coeffHeight + 1))

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
    if 5 > diamond >= 3:
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
        edges.append([nbMiddlePts + nbShinyPts + 1, nbMiddlePts + nbTopPts])


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

    # Trying some stuff with colors :
    colors = (
        (0, 0, 1, 0),
        (1, 1, 1, 0),
        (0, 1, 1, 0),
        (0, 1, 1, 0),
        (0, 0, 1, 0),
        (0, 0, 1, 0),
        (1, 1, 1, 0),
        (0, 1, 0.7, 0),
        (0, 1, 1, 0),
    )

    surfaces = []
    # bot to mid
    for x in range(1, nbMiddlePts):
        surfaces.append([0, x, x + 1])
    surfaces.append([0, nbMiddlePts, 1])

    # edges
    for x in range(1, nbMiddlePts):
        surfaces.append([0, x, x + 1])
    surfaces.append([0, nbMiddlePts, 1])

    if diamond == 1:
        compt = 1
        for x in range(1, nbTopPts):
            surfaces.append([compt, compt + 1, x + nbMiddlePts])
            surfaces.append([x + nbMiddlePts, x + nbMiddlePts + 1, compt + 1])
            compt = compt + 1
        surfaces.append([nbMiddlePts + nbTopPts, nbMiddlePts + 1, compt])
        surfaces.append([1, nbMiddlePts, nbMiddlePts + 1])

    if diamond == 2:
        compt = 1
        for x in range(1, nbTopPts):
            surfaces.append([compt, compt + 1, x + nbMiddlePts])
            surfaces.append([compt + 1, compt + 2, x + nbMiddlePts])
            compt = compt + 2
        surfaces.append([compt, compt + 1, nbMiddlePts + nbTopPts])
        surfaces.append([compt + 1, 1, nbMiddlePts + nbTopPts])

        surfaces.append([1, nbMiddlePts + nbTopPts, nbMiddlePts + 1])
        compt = 3
        for x in range(1, nbTopPts):
            surfaces.append([compt, x + nbMiddlePts, x + nbMiddlePts + 1])
            compt = compt + 2
        # top circle

    if 2 < diamond < 5:
        compt = 1
        for x in range(1, nbTopPts):
            surfaces.append([compt, compt + 1, x + nbMiddlePts])
            surfaces.append([compt + 1, compt + 2, x + nbMiddlePts])
            compt = compt + 2
        surfaces.append([compt, compt + 1, nbMiddlePts + nbTopPts])
        surfaces.append([compt + 1, 1, nbMiddlePts + nbTopPts])

        surfaces.append([1, nbMiddlePts + nbTopPts, nbMiddlePts + 1])
        compt = 3
        for x in range(1, nbTopPts):
            surfaces.append([compt, x + nbMiddlePts, x + nbMiddlePts + 1])
            compt = compt + 2

        for x in range(1, nbTopPts):
            surfaces.append([x + nbMiddlePts, x + nbMiddlePts + 1, x + nbMiddlePts + nbTopPts + 1])
        surfaces.append([nbMiddlePts + nbTopPts, nbMiddlePts + 1, nbMiddlePts + nbTopPts + 1])

        for x in range(1, nbTopPts):
            surfaces.append([x + nbMiddlePts, x + nbMiddlePts + nbTopPts, x + nbMiddlePts + nbTopPts + 1])
        surfaces.append([nbMiddlePts + nbTopPts + nbShinyPts, nbMiddlePts + nbTopPts + 1, nbMiddlePts + nbTopPts])
    if diamond == 5:
        max = nbMiddlePts + 1
        for x in range(1, nbMiddlePts):
            surfaces.append([max, x, x + 1])
        surfaces.append([max, nbMiddlePts, 1])

    numberDiamond = diamond
    return [surfaces, colors, verticies, edges, middleCircle, topCircle, shinyCircle, numberDiamond, addNbVerticies]


# def Cube():
#     glBegin(GL_LINES)
#     for edge in edges:
#         for vertex in edge:
#             glVertex3fv(verticies[vertex])
#     glEnd()


def Cube(x, diamond, colors):
    surfaces = diamond[0]
    verticies = diamond[2]
    nbShinyPts = len(diamond[6])
    nbMiddlePts = len(diamond[4])
    nbTopPts = len(diamond[5])
    edges = diamond[3]

    glBegin(GL_TRIANGLES)
    for surface in surfaces:
        for vertex in surface:
            x = (x + 1) % 9
            y = colors[x]

            glColor4f(y[0], y[1], y[2], y[3])
            glVertex3fv(verticies[vertex])

    glEnd()

    # Make the circle on the top of the diamond
    glBegin(GL_POLYGON)
    circlePts = []
    if diamond[7] >= 3:
        for x in range(nbShinyPts):
            circlePts.append(nbMiddlePts + nbTopPts + x + 1)
        for pointCircle in circlePts:
            glVertex3fv(verticies[pointCircle])
    else:
        for x in range(nbTopPts):
            circlePts.append(nbMiddlePts + x + 1)
        for pointCircle in circlePts:
            glVertex3fv(verticies[pointCircle])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    colors = colorsBlue
    gluPerspective(45, (display[0] / display[1]), 0.1, 70.0)
    # allow to enable, or disable the tranparency
    # glEnable(GL_DEPTH_TEST)

    glTranslatef(0.0, 0.0, -40)
    x = random.randint(1, 10)
    rayonBottom, rayonMiddle, rayonTop, rayonShiny, transparency, height, verticies = False, False, False, False, True, True, False
    coeffRayonBottom, coeffRayonMiddle, coeffRayonTop, coeffRayonShiny, coeffHeight, addNbVerticies = 0, 0, 0, 0, 0, 0
    print(rayonBottom)
    glPushMatrix()
    diamond = createDiamond(4, [0, 0, 0, 0, 0, 0], [True, False, False, False, False, False])
    diamondNumber = 4
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    transparency = not transparency
                if event.key == pygame.K_ESCAPE:
                    glPopMatrix()
                    glPushMatrix()
                if event.key == pygame.K_s:
                    glPushMatrix()
                # display the right diamond
                if event.key == pygame.K_1:
                    diamondNumber = 1
                elif event.key == pygame.K_2:
                    diamondNumber = 2
                elif event.key == pygame.K_3:
                    diamondNumber = 3
                elif event.key == pygame.K_4:
                    diamondNumber = 4
                elif event.key == pygame.K_5:
                    diamondNumber = 5
                elif event.key == pygame.K_r:
                    colors = colorsRed
                elif event.key == pygame.K_g:
                    colors = colorsGreen
                elif event.key == pygame.K_b:
                    colors = colorsBlue
                elif event.key == pygame.K_h:
                    height = True
                    rayonBottom = False
                    rayonMiddle = False
                    rayonTop = False
                    rayonShiny = False
                    verticies = False
                elif event.key == pygame.K_KP1:
                    height = False
                    rayonBottom = True
                    rayonMiddle = False
                    rayonTop = False
                    rayonShiny = False
                    verticies = False
                elif event.key == pygame.K_KP2:
                    height = False
                    rayonBottom = False
                    rayonMiddle = True
                    rayonTop = False
                    rayonShiny = False
                    verticies = False
                elif event.key == pygame.K_KP3:
                    height = False
                    rayonBottom = False
                    rayonMiddle = False
                    rayonTop = True
                    rayonShiny = False
                    verticies = False
                elif event.key == pygame.K_KP4:
                    height = False
                    rayonBottom = False
                    rayonMiddle = False
                    rayonTop = False
                    verticies = False
                    if diamondNumber >= 3:
                        rayonShiny = True
                elif event.key == pygame.K_v:
                    height = False
                    rayonBottom = False
                    rayonMiddle = False
                    rayonTop = False
                    rayonShiny = False
                    verticies = True



                if event.key == pygame.K_KP_PLUS:
                    if height:
                        coeffHeight += 0.1
                    elif rayonBottom:
                        coeffRayonBottom += 0.1
                    elif rayonMiddle:
                        coeffRayonMiddle += 0.1
                    elif rayonTop:
                        coeffRayonTop += 0.1
                    elif rayonShiny:
                        coeffRayonShiny += 0.1
                    elif verticies:
                        addNbVerticies += 1
                elif event.key == pygame.K_KP_MINUS:
                    if height:
                        coeffHeight -= 0.1
                    elif rayonBottom:
                        coeffRayonBottom -= 0.1
                    elif rayonMiddle:
                        coeffRayonMiddle -= 0.1
                    elif rayonTop:
                        coeffRayonTop -= 0.1
                    elif rayonShiny:
                        coeffRayonShiny -= 0.1
                    elif verticies:
                        if addNbVerticies > -3:
                            addNbVerticies -= 1


        rayonBool = [height, rayonBottom, rayonMiddle, rayonTop, rayonShiny]
        coeffs = [coeffHeight, coeffRayonBottom, coeffRayonMiddle, coeffRayonTop, coeffRayonShiny, addNbVerticies]
        diamond = createDiamond(diamondNumber, coeffs, rayonBool)
        if transparency:
            glEnable(GL_DEPTH_TEST)
        else:
            glDisable(GL_DEPTH_TEST)
        # glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # get keys
        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_UP]:
            glRotatef(3, 1, 1, 1)
        if keypress[pygame.K_RIGHT]:
            glRotatef(1, 3, 1, 1)
        if keypress[pygame.K_LEFT]:
            glRotatef(1, -3, 1, 1)
        if keypress[pygame.K_DOWN]:
            glRotatef(1, 1, 1, 3)

        if keypress[pygame.K_F1]:
            glTranslatef(-1, 0, 0)
        if keypress[pygame.K_F2]:
            glTranslatef(1, 0, 0)
        if keypress[pygame.K_F3]:
            glTranslatef(0, -1, 0)
        if keypress[pygame.K_F4]:
            glTranslatef(0, 1, 0)
        if keypress[pygame.K_F5]:
            glTranslatef(0, 0, -1)
        if keypress[pygame.K_F6]:
            glTranslatef(0, 0, 1)
        Cube(x, diamond, colors)
        print(addNbVerticies)
        # Ground
        glColor4f(0.5, 0.5, 0.5, 1)
        glBegin(GL_QUADS)
        glVertex3f(-30, -30, -5 * (1 + coeffHeight))
        glVertex3f(30, -30, -5 * (1 + coeffHeight))
        glVertex3f(30, 30, -5 * (1 + coeffHeight))
        glVertex3f(-30, 30, -5 * (1 + coeffHeight))
        glEnd()
        # Ground
        pygame.display.flip()
        pygame.time.wait(10)


main()

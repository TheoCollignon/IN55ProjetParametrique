# -*- coding: utf-8 -*-
"""
@author: LAMBALOT Luka & Théo COLLIGNON
"""
import random

from opengl_fcts import *

# some data
x = 0
y = 0
z = 0
diamondForm = 4
currentForm = 4
currentCoeff = [0, 0, 0, 0, 0, 0]


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
        topCircle = circle(0, 0, 6 + addNbVerticies, 3 * (coeffRayonTop + 1), 4 * (coeffHeight + 1))
        middleCircle = circle(0, 0, 6 + addNbVerticies, 6 * (coeffRayonMiddle + 1), 2 * (coeffHeight + 1))
        bottomCircle = circle(0, 0, 1, 0 * (coeffRayonBottom + 1), -5 * (coeffHeight + 1))
        shinyCircle = []

    # Diamant v2 :
    if diamond == 2:
        shinyCircle = []
        topCircle = circle(0, 0, 6 + addNbVerticies, 3 * (coeffRayonTop + 1), 3 * (coeffHeight + 1))
        middleCircle = circle(0, 0, 12 + addNbVerticies * 2, 6 * (coeffRayonMiddle + 1), 1 * (coeffHeight + 1))
        bottomCircle = circle(0, 0, 1, 0 * (coeffRayonBottom + 1), -5 * (coeffHeight + 1))

    # Diamant v3 :
    if diamond == 3:
        shinyCircle = circle(0, 0, 9 + addNbVerticies, 3 * (coeffRayonShiny + 1), 9 * (coeffHeight + 1))
        topCircle = circle(0, 0, 9 + addNbVerticies, 7 * (coeffRayonTop + 1), 8 * (coeffHeight + 1))
        middleCircle = circle(0, 0, 18 + addNbVerticies * 2, 10 * (coeffRayonMiddle + 1), 6 * (coeffHeight + 1))
        bottomCircle = circle(0, 0, 1, 0 * (coeffRayonBottom + 1), -5 * (coeffHeight + 1))

    if diamond == 4:
        # Diamant v4 :
        shinyCircle = circle(0, 0, 8 + addNbVerticies, 3 * (coeffRayonShiny + 1), 9 * (coeffHeight + 1))
        topCircle = circle(0, 0, 16 + addNbVerticies * 2, 7 * (coeffRayonTop + 1), 8 * (coeffHeight + 1))
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
    colors = getColors()

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
    # adding the ground coordinate
    groundCoordinate = [
        [-30, -30, -5 * (coeffHeight + 1)],
        [30, -30, -5 * (coeffHeight + 1)],
        [30, 30, -5 * (coeffHeight + 1)],
        [-30, 30, -5 * (coeffHeight + 1)],
    ]
    for x in groundCoordinate:
        verticies.append(x)
    return [surfaces, colors, verticies, edges, middleCircle, topCircle, shinyCircle, numberDiamond, addNbVerticies]


def setupDiamond():
    diamond = createDiamond(diamondNumber, currentCoeff, [True, False, False, False, False, False])
    diamondVertices = []
    vertices = diamond[2]
    num = 1
    greyColor = (
        (0.5, 0.5, 0.5)
    )
    for x in vertices:
        for i in x:
            diamondVertices.append(i)
            randomValue = random.randint(0, 7)
        if num < (len(vertices) - 5) :
            for i in colors[randomValue]:
                diamondVertices.append(i)
        else:
            for i in greyColor:
                diamondVertices.append(i)
        num += 1



    vertices = [
        -0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
        0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
        0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
        -0.5, 0.5, 0.5, 1.0, 1.0, 1.0,

        -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
        0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
        0.5, 0.5, -0.5, 0.0, 0.0, 1.0,
        -0.5, 0.5, -0.5, 1.0, 1.0, 1.0
    ]
    vertices = diamondVertices

    indices = [0, 1, 2,
               2, 3, 0,
               4, 5, 6,
               6, 7, 4,
               4, 5, 1,
               1, 0, 4,
               6, 7, 3,
               3, 2, 6,
               5, 6, 2,
               2, 1, 5,
               7, 4, 0,
               0, 3, 7]

    diamondEdges = []
    for i in diamond[0]:
        for x in i:
            diamondEdges.append(x)

    indices = diamondEdges

    # top of the diamond :
    circlePts = []
    nbShinyPts = len(diamond[6])
    nbTopPts = len(diamond[5])
    nbMiddlePts = len(diamond[4])
    if diamond[7] >= 3:
        for x in range(nbShinyPts):
            circlePts.append(nbMiddlePts + nbTopPts + x + 1)
    else:
        for x in range(nbTopPts):
            circlePts.append(nbMiddlePts + x + 1)

    # Ground
    groundIndices = []
    for x in range(4):
        groundIndices.append(1 + nbMiddlePts + nbTopPts + nbShinyPts + x)


    primitives = [
        (GL_TRIANGLES, indices),
        (GL_POLYGON, circlePts),
        (GL_POLYGON, groundIndices)
    ]
    return [vertices, primitives]


class RainbowCube(Object3D):
    def __init__(self):
        super().__init__()
        data = setupDiamond()
        vertices = data[0]
        primitives = data[1]
        self.Shader = ColorPositionShader(vertices, primitives)

    def updateTRSMatrices(self):
        direction = getDirection()
        viewUpdate = False
        global x, y, colors, window, diamondNumber, currentForm, currentCoeff
        diamondNumber = getDiamondNumer()
        listCoeff = getListCoeff()
        if listCoeff != currentCoeff:
            currentCoeff = listCoeff
            rc = RainbowCube()
            rc.translate((x, y, 0.0))
            objects = [rc]
            updateDiamond(objects)


        if currentForm != diamondNumber:
            currentForm = diamondNumber
            rc = RainbowCube()
            rc.translate((x, y, 0.0))
            objects = [rc]
            updateDiamond(objects)


        if colors != getColors():
            colors = getColors()
            rc = RainbowCube()
            rc.translate((x, y, 0.0))
            objects = [rc]
            updateDiamond(objects)


        if direction[0]:
            x -= 0.001
            rot_x = pyrr.Matrix44.from_x_rotation(x)
            rot_y = pyrr.Matrix44.from_y_rotation(y)
            self.R = np.matmul(rot_x, rot_y)
        if direction[1]:
            x += 0.001
            rot_x = pyrr.Matrix44.from_x_rotation(x)
            rot_y = pyrr.Matrix44.from_y_rotation(y)
            self.R = np.matmul(rot_x, rot_y)
        if direction[2]:
            y -= 0.001
            rot_x = pyrr.Matrix44.from_x_rotation(x)
            rot_y = pyrr.Matrix44.from_y_rotation(y)
            self.R = np.matmul(rot_x, rot_y)
        if direction[3]:
            y += 0.001
            rot_x = pyrr.Matrix44.from_x_rotation(x)
            rot_y = pyrr.Matrix44.from_y_rotation(y)
            self.R = np.matmul(rot_x, rot_y)

        if direction[4]:  # not moving
            rot_x = pyrr.Matrix44.from_x_rotation(x)
            rot_y = pyrr.Matrix44.from_y_rotation(y)
            self.R = np.matmul(rot_x, rot_y)

        # time = glfw.get_time()
        # rot_x = pyrr.Matrix44.from_x_rotation(0.5 * time)
        # rot_y = pyrr.Matrix44.from_y_rotation(0.8 * time)


window = ""


def main():
    global window
    window = Window(1024, 768, "Sujet 1 : Objet parametrique Groupe : Luka LAMBALOT, Theo COLLIGNON")

    if not window.Window:
        return

    window.initViewMatrix(eye=[0, 0, 25])

    rc = RainbowCube()
    rc.translate((0, 0, 0.0))

    objects = [rc]

    window.render(objects)


if __name__ == "__main__":
    main()

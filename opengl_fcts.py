# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 16:24:18 2020

@author: LAURI
"""

import random
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import pyrr
import math

nb_vert_infos_size = 6
updateView = False
item = ""


class Window:
    def __init__(self, width, height, title):
        self.Window = None

        if not glfw.init():
            return

        self.Window = glfw.create_window(width, height, title, None, None)

        if not self.Window:
            glfw.terminate()
            return

        glfw.set_key_callback(self.Window, key_input_clb)

        glfw.make_context_current(self.Window)

        self.updateProjectionMatrix(width, height)

    def updateProjectionMatrix(self, width, height):
        fov = 60
        aspect_ratio = width / height
        near_clip = 0.1
        far_clip = 100

        # create a perspective matrix
        self.ProjectionMatrix = pyrr.matrix44.create_perspective_projection(
            fov,
            aspect_ratio,
            near_clip,
            far_clip
        )

        glViewport(0, 0, width, height)

    def initViewMatrix(self, eye=[0, 0, 2]):
        eye = np.array(eye)
        target = np.array([0, 0, 0])
        up = np.array([0, 1, 0])
        self.ViewMatrix = pyrr.matrix44.create_look_at(eye, target, up)

    def render(self, objects):
        global item, updateView
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)

        v = self.ViewMatrix
        p = self.ProjectionMatrix
        vp = np.matmul(v, p)

        while not glfw.window_should_close(self.Window):
            glfw.poll_events()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            w, h = glfw.get_framebuffer_size(self.Window)
            self.updateProjectionMatrix(w, h)
            if getItem() != objects and updateView:
                print(objects)
                print(item)
                updateView = False
            else:
                item = objects

            for o in item:
                o.updateTRSMatrices()
                o.updateModelMatrix()
                mvp = np.matmul(o.ModelMatrix, vp)
                o.Shader.draw(mvp)

            glfw.swap_buffers(self.Window)

        self.CloseWindow()

    def CloseWindow(self):
        glfw.terminate()


class Object3D:
    def __init__(self):
        self.translate((0, 0, 0))
        self.scale((1, 1, 1))
        self.R = pyrr.matrix44.create_identity()

    def translate(self, vec):
        self.T = pyrr.matrix44.create_from_translation(vec)

    def scale(self, fac):
        self.S = pyrr.matrix44.create_from_scale(fac)

    def updateModelMatrix(self):
        self.ModelMatrix = np.matmul(np.matmul(self.S, self.R), self.T)

    def updateTRSMatrices(self):
        pass


def updateDiamond(objects):
    global updateView, item
    updateView = True
    print("update")
    print(objects)
    print(item)
    item = objects
    print(item)
    print(" end update")


def setItem(i):
    item = i


def getItem():
    return item


def getUpdate():
    return updateView


forward = False
backward = False
leftward = False
rightward = False


def changeForwardValue():
    global forward, backward, leftward, rightward
    forward = not forward
    backward, leftward, rightward = False, False, False


def changeBackwardValue():
    global forward, backward, leftward, rightward
    backward = not backward
    forward, leftward, rightward = False, False, False


def changeleftwardValue():
    global forward, backward, leftward, rightward
    leftward = not leftward
    backward, forward, rightward = False, False, False


def changerightwardValue():
    global forward, backward, leftward, rightward
    rightward = not rightward
    backward, leftward, forward = False, False, False


currentDirection = "none"


def getDirection():
    global currentDirection
    if forward:
        currentDirection = "forward"
    elif backward:
        currentDirection = "backward"
    elif rightward:
        currentDirection = "rightward"
    elif leftward:
        currentDirection = "leftward"
    else:
        currentDirection = "none"
    return [forward, backward, leftward, rightward, currentDirection]


colorsBlue = (
    (0, 0, 1),
    (0.7, 0.7, 1),
    (0, 1, 1),
    (0, 1, 1),
    (0, 0, 1),
    (0, 0, 1),
    (0.2, 0.2, 0.7),
    (0, 1, 0.7),
    (0, 1, 1),
)

colorsRed = (
    (0.9, 0.2, 0),
    (0.8, 0.5, 0),
    (1, 0, 0),
    (1, 0, 0),
    (0.9, 0.2, 0),
    (1, 0.5, 0),
    (0.8, 0.6, 0.3),
    (1, 0.5, 0.2),
    (1, 0.2, 0.2),
)

colorsGreen = (
    (0, 1, 1),
    (0.2, 0.7, 0.2),
    (0, 0.7, 0),
    (0, 1, 0),
    (0.2, 0.7, 0.2),
    (0, 0.7, 0),
    (0.5, 1, 0.5),
    (0, 1, 0.7),
    (0.3, 1, 0),
)

x = random.randint(1, 10)
rayonBottom, rayonMiddle, rayonTop, rayonShiny, transparency, height, vertices = False, False, False, False, True, True, False
coeffRayonBottom, coeffRayonMiddle, coeffRayonTop, coeffRayonShiny, coeffHeight, addNbVerticies = 0, 0, 0, 0, 0, 0
diamondNumber = 4
colors = colorsBlue


def getColors():
    return colors


def key_input_clb(window, key, scancode, action, mode):
    # default data
    global diamondNumber, currentDirection, colors, colorsBlue, x, rayonBottom, rayonMiddle, rayonTop, rayonShiny, \
        transparency, height, vertices, coeffRayonBottom, coeffRayonMiddle, coeffRayonTop, coeffRayonShiny, coeffHeight, addNbVerticies, colorsRed, colorsBlue, colorsGreen

    # if key == glfw.KEY_W and action == glfw.PRESS:
    #     print("lalalalla")
    # elif key == glfw.KEY_W and action == glfw.RELEASE:
    #     forward = False
    # display the right diamond
    if key == glfw.KEY_1:
        diamondNumber = 1
    elif key == glfw.KEY_2:
        diamondNumber = 2
    elif key == glfw.KEY_3:
        diamondNumber = 3
    elif key == glfw.KEY_4:
        diamondNumber = 4
    elif key == glfw.KEY_5:
        diamondNumber = 5
    elif key == glfw.KEY_R:
        colors = colorsRed
    elif key == glfw.KEY_G:
        colors = colorsGreen
    elif key == glfw.KEY_B:
        colors = colorsBlue
    elif key == glfw.KEY_H:
        height, rayonBottom, rayonMiddle, rayonTop, rayonShiny, vertices = True, False, False, False, False, False
    elif key == glfw.KEY_KP_1:
        height, rayonBottom, rayonMiddle, rayonTop, rayonShiny, vertices = False, True, False, False, False, False
    elif key == glfw.KEY_KP_2:
        height, rayonBottom, rayonMiddle, rayonTop, rayonShiny, vertices = False, False, True, False, False, False
    elif key == glfw.KEY_KP_3:
        height, rayonBottom, rayonMiddle, rayonTop, rayonShiny, vertices = False, False, False, True, False, False
    elif key == glfw.KEY_KP_4:
        height, rayonBottom, rayonMiddle, rayonTop, rayonShiny, vertices = False, False, False, False, False, False
        if diamondNumber >= 3:
            rayonShiny = True
    elif key == glfw.KEY_V:
        height, rayonBottom, rayonMiddle, rayonTop, rayonShiny, vertices = False, False, False, False, False, True


    elif key == glfw.KEY_KP_ADD and action == glfw.PRESS:
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
        elif vertices:
            addNbVerticies += 1
    elif key == glfw.KEY_KP_SUBTRACT and action == glfw.PRESS:
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
        elif vertices:
            if addNbVerticies > -3:
                addNbVerticies -= 1

    if key == glfw.KEY_UP and action == glfw.PRESS and currentDirection != "backward" and currentDirection != "rightward" and currentDirection != "leftward":
        changeForwardValue()
    elif key == glfw.KEY_UP and action == glfw.RELEASE and currentDirection != "backward" and currentDirection != "rightward" and currentDirection != "leftward" and currentDirection != "none":
        currentDirection = "none"
        changeForwardValue()
    if key == glfw.KEY_RIGHT and action == glfw.PRESS and currentDirection != "backward" and currentDirection != "forward" and currentDirection != "leftward":
        changerightwardValue()
    elif key == glfw.KEY_RIGHT and action == glfw.RELEASE and currentDirection != "backward" and currentDirection != "forward" and currentDirection != "leftward" and currentDirection != "none":
        currentDirection = "none"
        changerightwardValue()
    if key == glfw.KEY_LEFT and action == glfw.PRESS and currentDirection != "backward" and currentDirection != "rightward" and currentDirection != "forward":
        changeleftwardValue()
    elif key == glfw.KEY_LEFT and action == glfw.RELEASE and currentDirection != "backward" and currentDirection != "rightward" and currentDirection != "forward" and currentDirection != "none":
        currentDirection = "none"
        changeleftwardValue()
    if key == glfw.KEY_DOWN and action == glfw.PRESS and currentDirection != "forward" and currentDirection != "rightward" and currentDirection != "leftward":
        changeBackwardValue()
    elif key == glfw.KEY_DOWN and action == glfw.RELEASE and currentDirection != "forward" and currentDirection != "rightward" and currentDirection != "leftward" and currentDirection != "none":
        currentDirection = "none"
        changeBackwardValue()


def CreateShader(name):
    vs_file = open(name + '.vs.txt', 'r')
    VERTEX_SHADER = vs_file.read()
    vs_file.close()

    fs_file = open(name + '.fs.txt', 'r')
    FRAGMENT_SHADER = fs_file.read()
    fs_file.close()

    # Compile The Program and shaders
    return OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
                                            OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER))


class PositionShader:
    def __init__(self, vertices, primitives, color=(1.0, 1.0, 1.0)):
        self.Vertices = vertices
        self.Primitives = primitives
        self.Shader = CreateShader('position')
        self.Color = color
        self.createBuffers()

    def createBuffers(self):
        vertices = np.array(self.Vertices, dtype=np.float32)

        self.NbVertices = int(len(vertices) / nb_vert_infos_size)

        # Create Buffer object in gpu
        self.VBO = glGenBuffers(1)
        # Bind the buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.NbVertices * nb_vert_infos_size * 4, vertices, GL_STATIC_DRAW)

    def use(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        positionLoc = glGetAttribLocation(self.Shader, 'position')
        glVertexAttribPointer(positionLoc, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(positionLoc)

        glUseProgram(self.Shader)

    def draw(self, mvp):
        self.use()
        transformLoc = glGetUniformLocation(self.Shader, "mvp")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, mvp)
        colorLoc = glGetUniformLocation(self.Shader, "Color")
        glUniform3fv(colorLoc, 1, self.Color)
        for p in self.Primitives:
            nb_indices = len(p[1])
            glDrawElements(p[0], nb_indices, GL_UNSIGNED_INT, p[1])


class ColorPositionShader:
    def __init__(self, vertices, primitives):
        self.Vertices = vertices
        self.Primitives = primitives
        self.Shader = CreateShader('default')
        self.createBuffers()

    def createBuffers(self):
        vertices = np.array(self.Vertices, dtype=np.float32)

        self.NbVertices = int(len(vertices) / nb_vert_infos_size)

        # Create Buffer object in gpu
        self.VBO = glGenBuffers(1)
        # Bind the buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.NbVertices * nb_vert_infos_size * 4, vertices, GL_STATIC_DRAW)

    def use(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        position = glGetAttribLocation(self.Shader, 'position')
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, nb_vert_infos_size * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)

        color = glGetAttribLocation(self.Shader, 'color')
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, nb_vert_infos_size * 4, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        glUseProgram(self.Shader)

    def draw(self, mvp):
        self.use()
        transformLoc = glGetUniformLocation(self.Shader, "mvp")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, mvp)
        for p in self.Primitives:
            nb_indices = len(p[1])
            glDrawElements(p[0], nb_indices, GL_UNSIGNED_INT, p[1])


def addVertex(tab, p, c):
    tab.extend(p)
    tab.extend(c)

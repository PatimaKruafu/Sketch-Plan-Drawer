if __name__ == '__build__':
	raise Exception

import sys

from OpenGL.GL.VERSION import GL_1_0
from OpenGL.raw.GLUT import STRING
import msvcrt 
from random import randint
from random import uniform
from random import choice

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ('''ERROR: PyOpenGL not installed properly.''')

# import numpy as np
import math
import color
from WindowGL import *
 
left = -20.0
right = 20.0
bottom = -10.0
top = 10.0
near = -20.0
far = 20.0

#window size
windowSize = [800,800]
#window position
windowPosition = [100,100]

#window position
win_x = 100
win_y = 100

polygonMode = GL_FILL

vertices = [
  [-1.0, -1.0, -1.0],
  [1.0, -1.0, -1.0],
  [1.0, 1.0, -1.0],
  [-1.0, 1.0, -1.0],
  [-1.0, -1.0, 1.0],
  [1.0, -1.0, 1.0],
  [1.0, 1.0, 1.0],
  [-1.0, 1.0, 1.0]
]
def polygon(a, b, c, d, color = [1.0,1.0,1.0]):
  global vertices
  glColor3fv(color)
  glBegin(GL_POLYGON)
  glVertex3fv(vertices[a])
  glVertex3fv(vertices[b])
  glVertex3fv(vertices[c])
  glVertex3fv(vertices[d])
  glEnd()

def cube():
  polygon(0,3,2,1, color.RED)
  polygon(0,4,7,3, color.BLUE)
  polygon(1,2,6,5, color.YELLOW) #right
  polygon(4,5,6,7, color.GREEN) #front
  polygon(3,7,6,2, color.MAGENTA)#top
  polygon(0,1,5,4, color.CYAN) #bottom

def cubeInstance(x, y, z):
  glPushMatrix()
  glTranslatef(x,y,z)
  cube()
  glPopMatrix()

def init(): 
  #define background color
  glClearColor (0,0,0,0) 
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  #define display mode to orthographics
  glOrtho(left, right, bottom, top, near, far)
  glShadeModel(GL_SMOOTH)
  glEnable(GL_DEPTH_TEST)

def draw_arrow():
  # X
  glColor3f(1,0,0)
  glBegin(GL_LINES)
  glVertex3f(0,0,0)
  glVertex3f(3,0,0)
  glEnd()
  glBegin(GL_TRIANGLES)
  glVertex3f(3, 0, 0)
  glVertex3f(2.7, 0.2, 0)
  glVertex3f(2.7, -0.2, 0)
  glEnd()

  # Y
  glColor3f(0,1,0)
  glBegin(GL_LINES)
  glVertex3f(0,0,0)
  glVertex3f(0,3,0)
  glEnd()
  glBegin(GL_TRIANGLES)
  glVertex3f(0, 3, 0)
  glVertex3f(0.2, 2.7, 0)
  glVertex3f(-0.2, 2.7, 0)
  glEnd()

  # Z
  glColor3f(0,0,1)
  glBegin(GL_LINES)
  glVertex3f(0,0,0)
  glVertex3f(0,0,3)
  glEnd()
  glBegin(GL_TRIANGLES)
  glVertex3f(0, 0, 3)
  glVertex3f(0, 0.2, 2.7)
  glVertex3f(0, -0.2, 2.7)
  glEnd()

rho = 2
theta = 0
thetaX = 0
thetaY=0
thetaZ =0
phi = math.pi/4

#text for textfield in future
text = ''

# ADD Yot Camera Code

Camera_Far = 5
Camera_A_Order = 0
Camera_B_Order = 0
Camera_angle = 0.785469415042 # (math.sqrt(5/2))/2
Angle_plus = 1.570938830084 # math.sqrt(5/2)
Angle_sum = 0.785469415042

EyeX, EyeY, EyeZ = 0.0, 0.0, 0.0
AtX, AtY, AtZ = 0.0, 0.0, 0.0
UpX, UpY, UpZ = 0.0, 1.0, 0.0

scale_speed = 1

def display():
  global polygonMode, EyeX, EyeY, EyeZ, AtX, AtY, AtZ, UpX, UpY, UpZ
  global vertices, theta, rho, numSize
  global thetaX, thetaY, thetaZ

  glClear (GL_COLOR_BUFFER_BIT |GL_DEPTH_BUFFER_BIT)
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity ()             # clear the matrix 
  glPolygonMode(GL_FRONT_AND_BACK, polygonMode)
  gluLookAt(EyeX, EyeY, EyeZ, AtX, AtY, AtZ, UpX, UpY, UpZ)

  draw_arrow()
  glTranslatef(0,0,0)
  cube()
  

  glFlush()
  glutSwapBuffers()
  glMatrixMode(GL_PROJECTION)

def reshape (w, h):
  global left, right, bottom, top, near, far
  glViewport (0, 0, w, h)
  glMatrixMode (GL_PROJECTION)
  glLoadIdentity ()
  k = (right-left)/(top-bottom)
  # a : aspect ratio
  a = float(w)/h
  
  leftAspect = left
  rightAspect = right
  bottomAspect = bottom
  topAspect = top
  if a>=1.0:
    leftAspect = left*a
    rightAspect= right*a
  else:
    bottomAspect = bottom/a
    topAspect = top/a
  if k>=1:
    leftAspect /= k
    rightAspect /=k
  else:
    bottomAspect *= k
    topAspect *=k
  glOrtho(leftAspect,rightAspect,bottomAspect,topAspect,near,far)
  glutPostRedisplay()

  # window.size = [w,h]

def addText(texts, alpha):
  character = str(alpha)
  texts = texts + character
  pass

def keyboard(key, x, y):
  global Camera_A_Order, Camera_B_Order, Camera_angle, Angle_sum, Angle_plus
  global text

  # Button ">"
  if key == '.'.encode() : 
    Angle_sum = Angle_sum + Angle_plus
    Camera_A_Order = 1
  # Button "<"
  if key == ','.encode() : 
    Angle_sum = Angle_sum - Angle_plus
    Camera_B_Order = 1

#   # test
#   if key == 'l'.encode() : 
#     Camera_angle = Camera_angle + 1.570938830084 # math.sqrt(5/2)
#   if key == 'k'.encode() : 
#     Camera_angle = Camera_angle - 1.570938830084 # math.sqrt(5/2)
  

  if key == chr(27): #escape
    import sys
    sys.exit(0)
  if key == chr(8) : #backspace
    pass
  if key == chr(127): #delete
    pass
  if key == chr(13): #carriage return
    pass
  else:
    alpha = str(key,'utf-8')

    text += alpha
    print('text is ' + text)
    print("EyeX :" + str(EyeX) + "  EyeY :" + str(EyeY) + "  EyeZ :" + str(EyeZ))
    print("AtX :" + str(AtX) + "  AtY :" + str(AtY) + "  AtZ :" + str(AtZ))
    print("UpX :" + str(UpX) + "  UpY :" + str(UpY) + "  UpZ :" + str(UpZ))
    print("Camera_A_Order, Camera_B_Order : " + str(Camera_A_Order) + " || " + str(Camera_B_Order) )

def mouse(button, state, x, y):
  global polygonMode
  if(state == GLUT_DOWN):
    if (button==GLUT_LEFT_BUTTON):
      pass
    if (button==GLUT_MIDDLE_BUTTON):
      pass
    if(button==GLUT_RIGHT_BUTTON):
      pass
  if(state == GLUT_UP):
    if (button==GLUT_LEFT_BUTTON):
      pass
    if (button==GLUT_MIDDLE_BUTTON):
      pass
    if(button==GLUT_RIGHT_BUTTON):
      pass

  glutPostRedisplay()

def idle():
  global Camera_Far, Camera_A_Order, Camera_B_Order, EyeX, EyeY, EyeZ, AtX, AtY, AtZ, UpX, UpY, UpZ, Camera_angle, thetaX, Angle_plus, Angle_sum
    # 0.785469415042 # (math.sqrt(5/2))/2
    # 1.570938830084 # math.sqrt(5/2)

  EyeX, EyeY, EyeZ = Camera_Far * math.cos(Camera_angle), Camera_Far, Camera_Far * math.sin(Camera_angle)
  AtX, AtY, AtZ = 0.0, 0.0, 0.0
  UpX, UpY, UpZ = 0.0, 1.0, 0.0

  if Camera_A_Order == 1:
    if Angle_sum > Camera_angle:
      Camera_angle = Camera_angle + Angle_plus/1000
    if Angle_sum == Camera_angle:
      Camera_A_Order = 0

  if Camera_B_Order == 1:
    if Angle_sum < Camera_angle:
      Camera_angle = Camera_angle - Angle_plus/1000
    if Angle_sum == Camera_angle:
      Camera_B_Order = 0

  glutPostRedisplay()

def motion():
  pass
  glutPostRedisplay()

def mouseWheel():
  pass
  glutPostRedisplay()

glutInit(sys.argv)
# window = WindowGL(GLUT_DOUBLE|GLUT_RGB|GLUT_DEPTH, windowSize, windowPosition, "Window GL")
glutInitDisplayMode(GLUT_RGB|GLUT_SINGLE)
glutInitWindowPosition(windowPosition[0],windowPosition[1]) 
glutInitWindowSize(windowSize[0],windowSize[1])
glutCreateWindow("my strange window".encode())

init ()
#callback registers
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutMotionFunc(motion)
glutIdleFunc(idle)# idle routine
glutMouseWheelFunc(mouseWheel)
glutMainLoop()

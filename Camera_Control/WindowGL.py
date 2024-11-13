from OpenGL.GL.VERSION import GL_1_0
from OpenGL.raw.GLUT import STRING
import msvcrt 
try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ('''ERROR: PyOpenGL not installed properly.''')

print("hello world")
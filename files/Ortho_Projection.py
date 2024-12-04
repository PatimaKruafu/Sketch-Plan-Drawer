from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Initialize the 3D matrix
matrix_3d = [
    [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
    [[0, 0, 1], [1, 0, 0], [1, 1, 0]]
]

# Convert the list to a numpy array for easier manipulation
array_3d = np.array(matrix_3d)

# Create projections
front_view = np.max(array_3d, axis=0)
top_view = np.max(array_3d, axis=1)
side_view = np.max(array_3d, axis=2)

window_width = 800
window_height = 600

viewport_width = int(window_width / 2)
viewport_height = int(window_height / 2)

def init():
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)

def draw_projection(projection):
    glLoadIdentity()
    glOrtho(-1, len(projection[0]), -1, len(projection), -1, 1)

    glPointSize(5)
    glBegin(GL_POINTS)
    for y in range(len(projection)):
        for x in range(len(projection[y])):
            if projection[y][x] > 0:
                z = projection[y][x]
                glVertex3f(x, y, z)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw front view
    glViewport(0, viewport_height, viewport_width, viewport_height)
    draw_projection(front_view)

    # Draw top view
    glViewport(viewport_width, viewport_height, viewport_width, viewport_height)
    draw_projection(top_view)

    # Draw side view
    glViewport(0, 0, viewport_width, viewport_height)
    draw_projection(side_view)

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("3D Cube Projections")
    glutDisplayFunc(display)
    glutIdleFunc(display)  # Ensure the display function is called continuously
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()
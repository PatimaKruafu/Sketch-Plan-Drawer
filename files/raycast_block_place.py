from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

# Window dimensions
window_width, window_height = 800, 600
selected_block = None
mouse_x, mouse_y = 0, 0
grid_pos = None

# Initialize OpenGL and GLUT
def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, window_width / window_height, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.2, 0.3, 0.4, 1.0)  # Background color

# Draw grid
def draw_grid():
    glColor3f(0.5, 0.5, 0.5)  # Grid color
    glBegin(GL_LINES)
    for i in range(-10, 11):
        glVertex3f(i, 0, -10)
        glVertex3f(i, 0, 10)
        glVertex3f(-10, 0, i)
        glVertex3f(10, 0, i)
    glEnd()

# Draw cube at specified position
def draw_cube(x, y, z, highlight=False):
    glPushMatrix()
    glTranslatef(x, y, z)
    if highlight:
        glColor3f(1.0, 1.0, 0.0)  # Highlight color
    else:
        glColor3f(1.0, 0.0, 0.0)  # Cube color
    glutSolidCube(1)
    glPopMatrix()

# Ray creation from mouse position
# Have numpy error in 'numpy.dtype size changed, may indicate binary incompatibility.'
def get_ray_from_mouse(x, y):
    try:
        viewport = glGetIntegerv(GL_VIEWPORT)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        winX = float(x)
        winY = float(viewport[3] - y)
        winZ = glReadPixels(x, int(winY), 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
        pos = gluUnProject(winX, winY, winZ[0][0], modelview, projection, viewport)
        return pos
    except Exception as e:
        print(f"Error in get_ray_from_mouse: {e}")
        return None

# Calculate grid position from mouse coordinates and snap to grid
def get_grid_position(mouse_x, mouse_y):
    ray = get_ray_from_mouse(mouse_x, mouse_y)
    if ray is None:
        return None
    # Assuming the grid is at y = 0 plane
    if ray[1] == 0:
        return None
    t = -ray[1] / ray[1]
    grid_x = round(ray[0] * t)
    grid_y = 0
    grid_z = round(ray[2] * t)
    return [grid_x, grid_y, grid_z]

# Check intersection with cube
def check_intersection(x, y):
    global selected_block
    ray = get_ray_from_mouse(x, y)
    if ray is None:
        selected_block = None
        return
    # Assuming the cube is at (0, 0.5, 0) with size 1
    cube_min = np.array([-0.5, 0, -0.5])
    cube_max = np.array([0.5, 1, 0.5])
    if np.all(cube_min <= ray) and np.all(ray <= cube_max):
        selected_block = (0, 0.5, 0)
    else:
        selected_block = None

def mouse_motion(x, y):
    global mouse_x, mouse_y, grid_pos
    mouse_x, mouse_y = x, y
    grid_pos = get_grid_position(x, y)
    if grid_pos:
        print(f"Mouse Position: ({x}, {y}), Grid Position: ({grid_pos[0]:.2f}, {grid_pos[1]:.2f}, {grid_pos[2]:.2f})")
    else:
        print(f"Mouse Position: ({x}, {y}), Grid Position: None")
    check_intersection(x, y)
    glutPostRedisplay()

def draw_text(x, y, text):
    glWindowPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 5, 10, 0, 0, 0, 0, 1, 0)

    # Draw grid
    draw_grid()

    # Draw cube at (0, 0, 0)
    draw_cube(0, 0.5, 0, highlight=(selected_block is not None))

    # Draw text
    glColor3f(1.0, 1.0, 1.0)
    # Show X,Y location
    draw_text(10, window_height - 20, f"Mouse: ({mouse_x}, {mouse_y})")
    if grid_pos:
        draw_text(10, window_height - 40, f"Grid Coords: ({grid_pos[0]}, {grid_pos[1]}, {grid_pos[2]})")

    glutSwapBuffers()

def reshape(w, h):
    global window_width, window_height
    window_width, window_height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w / h, 0.5, 60.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Ray Casting Example")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutPassiveMotionFunc(mouse_motion)
    glutMainLoop()

if __name__ == "__main__":
    main()

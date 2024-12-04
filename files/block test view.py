from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

# Window dimensions
window_width, window_height = 800, 600
grid_size = 10  # Grid size (10x10x10)
grid = np.zeros((grid_size, grid_size, grid_size), dtype=int)  # 3D grid initialized with 0

# Cursor position
cursor_x, cursor_y, cursor_z = grid_size // 2, 0, grid_size // 2  # Start in the middle of the grid
view_mode = 'top'  # Default view mode: 'top', 'side', 'front'

# Initialize OpenGL and GLUT
def init():
    glClearColor(0.2, 0.3, 0.4, 1.0)  # Background color
    glEnable(GL_DEPTH_TEST)

# Function to set the camera based on the current view mode
def set_camera():
    glLoadIdentity()
    if view_mode == 'top':
        # Top view (X-Z plane)
        gluLookAt(0, 20, 0, 0, 0, 0, 0, 0, -1)
    elif view_mode == 'side':
        # Side view (Y-Z plane)
        gluLookAt(20, 0, 0, 0, 0, 0, 0, 1, 0)
    elif view_mode == 'front':
        # Front view (X-Y plane)
        gluLookAt(0, 0, 20, 0, 0, 0, 0, 1, 0)

# Draw grid
def draw_grid():
    glColor3f(0.5, 0.5, 0.5)  # Grid color
    glBegin(GL_LINES)
    for i in range(-grid_size, grid_size + 1):
        glVertex3f(i, 0, -grid_size)
        glVertex3f(i, 0, grid_size)
        glVertex3f(-grid_size, 0, i)
        glVertex3f(grid_size, 0, i)
    glEnd()

# Draw cubes based on the 3D grid
def draw_blocks():
    for x in range(grid_size):
        for y in range(grid_size):
            for z in range(grid_size):
                if grid[x, y, z] == 1:
                    draw_cube(x - grid_size // 2, y, z - grid_size // 2)

# Draw a cube at a specified position
def draw_cube(x, y, z, highlight=False):
    glPushMatrix()
    glTranslatef(x, y, z)
    if highlight:
        glColor3f(1.0, 1.0, 0.0)  # Highlight color for the cursor
    else:
        glColor3f(1.0, 0.0, 0.0)  # Red color for cubes
    glutSolidCube(1)
    glPopMatrix()

# Display callback
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    set_camera()

    # Draw grid
    draw_grid()

    # Draw blocks
    draw_blocks()

    # Highlight the current cursor position
    draw_cube(cursor_x - grid_size // 2, cursor_y, cursor_z - grid_size // 2, highlight=True)

    glutSwapBuffers()

# Keyboard interaction handler
def key_press(key, x, y):
    global cursor_x, cursor_y, cursor_z, view_mode
    key = key.decode("utf-8").lower()

    if key == 'w':  # Move north
        cursor_z = max(0, cursor_z - 1)
    elif key == 's':  # Move south
        cursor_z = min(grid_size - 1, cursor_z + 1)
    elif key == 'a':  # Move west
        cursor_x = max(0, cursor_x - 1)
    elif key == 'd':  # Move east
        cursor_x = min(grid_size - 1, cursor_x + 1)
    elif key == '1':  # Top view
        view_mode = 'top'
    elif key == '2':  # Side view
        view_mode = 'side'
    elif key == '3':  # Front view
        view_mode = 'front'
    elif key == '\r':  # Enter key to place/remove block
        if grid[cursor_x, cursor_y, cursor_z] == 0:  # Place block
            grid[cursor_x, cursor_y, cursor_z] = 1
        else:  # Remove block
            grid[cursor_x, cursor_y, cursor_z] = 0

    glutPostRedisplay()

# Reshape callback
def reshape(w, h):
    global window_width, window_height
    window_width, window_height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w / h, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# Main function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"2D Block Placement - Top, Side, and Front Views")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(key_press)
    glutMainLoop()

if __name__ == "__main__":
    main()

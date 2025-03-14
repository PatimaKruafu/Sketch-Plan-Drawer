from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18
import numpy as np

# Window dimensions
window_width, window_height = 800, 600

# Grid dimensions and data (3D grid)
grid_size = 10  # Grid size (10x10x10)
grid = np.zeros((grid_size, grid_size, grid_size), dtype=int)  # 3D grid initialized with 0

# Cursor position
cursor_x, cursor_y, cursor_z = grid_size // 2, 0, grid_size // 2  # Start in the middle of the grid

# Selected block for mouse interaction
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


# Draw grid on the ground (y = 0 plane)
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


# Ray casting to obtain position from mouse
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


# Calculate grid position from mouse coordinates
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


# Mouse passive motion callback
def mouse_motion(x, y):
    global mouse_x, mouse_y, grid_pos
    mouse_x, mouse_y = x, y
    grid_pos = get_grid_position(x, y)
    glutPostRedisplay()


# Keyboard interaction handler
def key_press(key, x, y):
    global cursor_x, cursor_y, cursor_z
    key = key.decode("utf-8").lower()

    if key == 'w':  # Move north
        cursor_z = max(0, cursor_z - 1)
    elif key == 's':  # Move south
        cursor_z = min(grid_size - 1, cursor_z + 1)
    elif key == 'a':  # Move west
        cursor_x = max(0, cursor_x - 1)
    elif key == 'd':  # Move east
        cursor_x = min(grid_size - 1, cursor_x + 1)
    elif key == 'r':  # Move up
        cursor_y = min(cursor_y + 1, grid_size - 1)
    elif key == 'f':  # Move down
        cursor_y = max(cursor_y - 1, 0)
    elif key == '\r':  # Enter key to place/remove block
        if grid[cursor_x, cursor_y, cursor_z] == 0:  # Place block
            grid[cursor_x, cursor_y, cursor_z] = 1
        else:  # Remove block
            grid[cursor_x, cursor_y, cursor_z] = 0

    glutPostRedisplay()


# Draw text on the screen
def draw_text(x, y, text):
    glWindowPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

# Initialize a 3D list to store block data
block_data = [[[0 for _ in range(grid_size)] for _ in range(grid_size)] for _ in range(grid_size)]

def draw_block_function():
    draw_grid()
    draw_blocks()
    draw_cube(cursor_x - grid_size // 2, cursor_y, cursor_z - grid_size // 2, highlight=True)

# Draw block in orthographic projection
def draw_block_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect_ratio = (window_width // 2) / (window_height // 2)
    if aspect_ratio > 1:
        glOrtho(-grid_size * aspect_ratio, grid_size * aspect_ratio, -grid_size, grid_size, -grid_size, grid_size)
    else:
        glOrtho(-grid_size, grid_size, -grid_size / aspect_ratio, grid_size / aspect_ratio, -grid_size, grid_size)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Front view
    glViewport(0, window_height // 2, window_width // 2, window_height // 2)
    glLoadIdentity()
    draw_block_function()
    draw_text(10, window_height // 2 + 20, "Front View")

    # Top view
    glViewport(window_width // 2, window_height // 2, window_width // 2, window_height // 2)
    glLoadIdentity()
    glRotatef(90, 1, 0, 0)
    draw_block_function()
    draw_text(window_width // 2 + 10, window_height // 2 + 20, "Top View")

    # Left side view
    glViewport(0, 0, window_width // 2, window_height // 2)
    glLoadIdentity()
    glRotatef(90, 0, 1, 0)
    draw_block_function()
    draw_text(10, window_height // 2 - window_height // 2 + 20, "Left Side View")

    # Right side view
    glViewport(window_width // 2, 0, window_width // 2, window_height // 2)
    glLoadIdentity()
    glRotatef(-90, 0, 1, 0)
    draw_block_function()
    draw_text(window_width // 2 + 10, window_height // 2 - window_height // 2 + 20, "Right Side View")

    # Save block data to 3D list
    for x in range(grid_size):
        for y in range(grid_size):
            for z in range(grid_size):
                if is_block_present(x, y, z):
                    block_data[x][y][z] = 1

    # Print block data to console
    print_block_data()


def print_block_data():
    for x in range(grid_size):
        for y in range(grid_size):
            for z in range(grid_size):
                if block_data[x][y][z] == 1:
                    print(f"Block present at ({x}, {y}, {z})")


# Check if a block is present at the given coordinates
def is_block_present(x, y, z):
    if 0 <= x < grid_size and 0 <= y < grid_size and 0 <= z < grid_size:
        return grid[x][y][z] == 1
    return True


def instructions_text():
    # Draw text
    glColor3f(1.0, 1.0, 1.0)
    draw_text(10, window_height - 20, f"Cursor: ({cursor_x}, {cursor_y}, {cursor_z})")
    draw_text(10, window_height - 40, f"Mouse: ({mouse_x}, {mouse_y}), Grid Pos: {grid_pos}")
    draw_text(10, window_height - 60, "Controls: W (North), S (South), A (West), D (East), R (Up), F (Down), Enter (Place/Remove Block)")

# Display callback
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    instructions_text()

    # Draw block in orthographic projection
    draw_block_ortho()

    glutSwapBuffers()

def pers_display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 10, 20, 0, 0, 0, 0, 1, 0)

    instructions_text()

    draw_block_function()

    glutSwapBuffers()

# Reshape callback
def reshape(w, h):
    global window_width, window_height
    window_width, window_height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w / h, 0.5, 60.0)
    glMatrixMode(GL_MODELVIEW)

# Main function
def main():
    global main_window, pers_window, window_width, window_height
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)

    glutInitWindowPosition(100, 100)
    main_window = glutCreateWindow(b"3D Block Placement - Orthographic Projection")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(key_press)
    glutPassiveMotionFunc(mouse_motion)

    glutInitWindowPosition(100 + window_width, 100)
    pers_window = glutCreateWindow(b"3D Block Placement - Perspective Projection")
    glutDisplayFunc(pers_display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(key_press)
    glutPassiveMotionFunc(mouse_motion)

    def update_windows():
        glutSetWindow(main_window)
        glutPostRedisplay()
        glutSetWindow(pers_window)
        glutPostRedisplay()

    # Set the idle function to update both windows
    glutIdleFunc(update_windows)

    glutMainLoop()


if __name__ == "__main__":
    main()

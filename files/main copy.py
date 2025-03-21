from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import math

import json
import tkinter as tk
from tkinter import filedialog, messagebox

# Window dimensions
window_width, window_height = 800, 600

# Grid dimensions and data (3D grid)
GRID_SIZE = 10  # Grid size (10x10x10)
grid = np.zeros((GRID_SIZE, GRID_SIZE, GRID_SIZE), dtype=int)  # 3D grid initialized with 0

# Cursor position
cursor_x, cursor_y, cursor_z = GRID_SIZE // 2, 0, GRID_SIZE // 2  # Start in the middle of the grid

# Selected block for mouse interaction
selected_block = None
mouse_x, mouse_y = 0, 0
grid_pos = None

#--------------------newcode----------------------

CUBE_SIZE = 1
CUBE_OFFSET = CUBE_SIZE/2

#--------------------newcode----------------------

#--------------------Init----------------------
# Initialize OpenGL and GLUT
def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluPerspective(45, window_width / window_height, 0.1, 50.0)
    glOrtho(-GRID_SIZE, GRID_SIZE, -GRID_SIZE, GRID_SIZE, -100, 100)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.2, 0.3, 0.4, 1.0)  # Background color
#--------------------Init----------------------


#--------------------Draw Blocks----------------------
# Draw grid on the ground (y = 0 plane)
def draw_grid():
    HALF_GRID = int(GRID_SIZE/2)
    glColor3f(0.5, 0.5, 0.5)  # Grid color
    glBegin(GL_LINES)
    for i in range(-HALF_GRID, HALF_GRID + 1):
        glVertex3f(i, 0, -HALF_GRID)
        glVertex3f(i, 0, HALF_GRID)
        glVertex3f(-HALF_GRID, 0, i)
        glVertex3f(HALF_GRID, 0, i)
    glEnd()


# Draw cubes based on the 3D grid
def draw_blocks():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            for z in range(GRID_SIZE):
                if grid[x, y, z] == 1:
                    draw_cube(x - GRID_SIZE // 2, y, z - GRID_SIZE // 2)


# Draw a cube at a specified position
def draw_cube(x, y, z, highlight=False):
    glPushMatrix()
    glTranslatef(x + CUBE_OFFSET, y + CUBE_OFFSET, z + CUBE_OFFSET)
    if highlight:
        glColor3f(1.0, 1.0, 0.0)  # Highlight color for the cursor
    else:
        glColor3f(1.0, 0.0, 0.0)  # Red color for cubes
    glutSolidCube(CUBE_SIZE)
    glPopMatrix()


def draw_block_function():
    draw_grid()
    draw_blocks()
    draw_cube(cursor_x - GRID_SIZE // 2, cursor_y, cursor_z - GRID_SIZE // 2, highlight=True)


#--------------------Draw Blocks----------------------

#--------------------Ortho----------------------------
# Draw block in orthographic projection
def draw_block_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect_ratio = (window_width // 2) / (window_height // 2)
    if aspect_ratio > 1:
        glOrtho(-GRID_SIZE * aspect_ratio, GRID_SIZE * aspect_ratio, -GRID_SIZE, GRID_SIZE, -GRID_SIZE, GRID_SIZE)
    else:
        glOrtho(-GRID_SIZE, GRID_SIZE, -GRID_SIZE / aspect_ratio, GRID_SIZE / aspect_ratio, -GRID_SIZE, GRID_SIZE)
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
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            for z in range(GRID_SIZE):
                if is_block_present(x, y, z):
                    #block_data[x][y][z] = 1
                    grid[x][y][z] = 1

# Check if a block is present at the given coordinates
def is_block_present(x, y, z):
    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and 0 <= z < GRID_SIZE:
        return grid[x][y][z] == 1
    return True

#--------------------Ortho----------------------------







#--------------------Ray Casting 3D Selection----------------------
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
#--------------------Ray Casting 3D Selection----------------------

# Keyboard interaction handler
def key_press(key, x, y):
    global cursor_x, cursor_y, cursor_z, fovy
    key = key.decode("utf-8").lower()
    camera = (1 % 4) + 1


    if key == 'w':  # Move north
        cursor_z = max(0, cursor_z - 1)
    elif key == 's':  # Move south
        cursor_z = min(GRID_SIZE - 1, cursor_z + 1)
    elif key == 'a':  # Move west
        cursor_x = max(0, cursor_x - 1)
    elif key == 'd':  # Move east
        cursor_x = min(GRID_SIZE - 1, cursor_x + 1)
    elif key == '\r':  # Enter key to place/remove block
        if grid[cursor_x, cursor_y, cursor_z] == 0:  # Place block
            grid[cursor_x, cursor_y, cursor_z] = 1
        else:  # Remove block
            grid[cursor_x, cursor_y, cursor_z] = 0

    # Button ">"
    elif key == '.':
        camera += 1
        #SelectCamera(camera)
        pass
    # Button "<"
    elif key == ',':
        camera += 1
        #SelectCamera(camera)
        pass

    glutPostRedisplay()


# Draw text on the screen
def draw_text(x, y, text):
    glWindowPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))








#--------------------Camera Control----------------------

#at_position = [b, a, +-10]
#or
#at_position = [+-10, a, b]

eye_width = GRID_SIZE
eye_depth = GRID_SIZE
eye_height = GRID_SIZE * math.tan( math.radians( 90 - math.degrees( math.asin(1/math.sqrt(3)) ) ) )
eye_position = [GRID_SIZE, eye_height, GRID_SIZE]
new_eye_position = [GRID_SIZE, eye_height, GRID_SIZE]
#4 iso
#EYE_position = [10, Y, 10]   1
#EYE_position = [10, Y, -10]  2
#EYE_position = [-10, Y, 10]  3
#EYE_position = [-10, Y, -10] 4

CAMERA_ROTATE_SPEED = 10

def SelectCamera(cam):
    global new_eye_position
    match cam:
        case 1 :
            new_eye_position = [GRID_SIZE, eye_height, GRID_SIZE]
        case 2 :
            new_eye_position = [GRID_SIZE, eye_height, -GRID_SIZE]
        case 3 :
            new_eye_position = [-GRID_SIZE, eye_height, GRID_SIZE]
        case 4 :
            new_eye_position = [-GRID_SIZE, eye_height, -GRID_SIZE]

    return new_eye_position

def RotateCamera(pos, newpos):
    pos[0] += newpos[0] - pos[0] / CAMERA_ROTATE_SPEED
    pos[1] += newpos[1] - pos[1] / CAMERA_ROTATE_SPEED

#--------------------Camera Control----------------------

def display_ortho():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Draw block in orthographic projection
    draw_block_ortho()

    glutSwapBuffers()

# Display callback
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    #gluLookAt(0, 10, 20, 0, 0, 0, 0, 1, 0)
    #gluLookAt(EyeX, EyeY, EyeZ, 0, 0, 0, 0, 1, 0)
    gluLookAt(eye_position[0], eye_position[1], eye_position[2], 0, 0, 0, 0, 1, 0)
    
    #gluLookAt(LOOKAT_POSITION[0], LOOKAT_POSITION[1], LOOKAT_POSITION[2], 0, 0, 0, 0, 1, 0)

    draw_block_function()

    # Highlight the current cursor position
    draw_cube(cursor_x - GRID_SIZE // 2, cursor_y, cursor_z - GRID_SIZE // 2, highlight=True)

    # Draw text
    glColor3f(1.0, 1.0, 1.0)
    draw_text(10, window_height - 20, f"Cursor: ({cursor_x}, {cursor_y}, {cursor_z})")
    draw_text(10, window_height - 40, f"Mouse: ({mouse_x}, {mouse_y}), Grid Pos: {grid_pos}")
    draw_text(10, window_height - 60, "Controls: W (North), S (South), A (West), D (East), Enter (Place/Remove Block)")

    #RotateCamera(eye_position, new_eye_position)
    glutSwapBuffers()

# Main function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)

    glutInitWindowPosition(100, 100)
    ortho_window = glutCreateWindow(b"Orthographic Projection")
    init()
    glutDisplayFunc(display_ortho)
    glutKeyboardFunc(key_press)
    glutPassiveMotionFunc(mouse_motion)

    glutInitWindowPosition(100 + window_width, 100)
    main_window = glutCreateWindow(b"Sketch Plan Drawer")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(key_press)
    glutPassiveMotionFunc(mouse_motion)
    def update_windows():
        glutSetWindow(main_window)
        glutPostRedisplay()
        glutSetWindow(ortho_window)
        glutPostRedisplay()

    # Set the idle function to update both windows
    glutIdleFunc(update_windows)

    glutMainLoop()


if __name__ == "__main__":
    main()





#---------------------tk UI---------------------
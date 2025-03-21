from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18
import numpy as np
from numpy import interp
import math
import pickle

# Window dimensions
window_width, window_height = 800, 600

# Grid dimensions and data (3D grid)
GRID_SIZE = 10  # Grid size (10x10x10)
grid = np.zeros((GRID_SIZE, GRID_SIZE, GRID_SIZE), dtype=int)  # 3D grid initialized with 0

# Selected block for mouse interaction
selected_block = None
mouse_x, mouse_y = 0, 0
grid_pos = None
layer = 0

CUBE_SIZE = 1
CUBE_OFFSET = CUBE_SIZE/2

#--------------------Save And Load Function--------------------
# Dictionary to store multiple grid states
grid_data = {}
current_slot = 0

is_saved = False

file_status = "loaded from"

def save_grid(slot):
    global current_slot, is_saved, file_status

    """Save the current grid state to a slot."""
    grid_data[slot] = np.copy(grid)
    current_slot = slot
    save_grid_to_file(grid_data)
    is_saved = True
    file_status = "saved"
    print(f"Grid saved to slot {slot}")

def load_grid(slot):
    """Load the grid state from a slot."""
    global grid, current_slot, file_status
    grid = load_grid_from_file(slot)
    file_status = "loaded"
    current_slot = slot

# Save grid to file
def save_grid_to_file(gridData):
    with open('grid_save.pkl', 'wb') as f:
        pickle.dump(gridData, f)
    print("Grid saved to grid_save.pkl")

# Load grid from file
def load_grid_from_file(slot):
    try:
        with open('grid_save.pkl', 'rb') as f:
            gridDataLoaded = pickle.load(f)
            if slot in gridDataLoaded:
                gridLoaded = gridDataLoaded[slot]
            else:
                gridLoaded = np.zeros((GRID_SIZE, GRID_SIZE, GRID_SIZE), dtype=int)
        return gridLoaded
              
    except FileNotFoundError:
        print("No save file found.")
#--------------------Save And Load Function--------------------

#--------------------Init----------------------
# Initialize OpenGL and GLUT
def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluPerspective(45, window_width / window_height, 0.1, 50.0)
    glOrtho(-GRID_SIZE, GRID_SIZE, -GRID_SIZE, GRID_SIZE, -10 * GRID_SIZE, 10 * GRID_SIZE)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.2, 0.3, 0.4, 1.0)  # Background color
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
#--------------------Init----------------------


#--------------------Draw Blocks----------------------

# Draw grid on the ground (y = 0 plane)
def draw_grid():
    HALF_GRID = int(GRID_SIZE/2)
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINES)
    for i in range(-HALF_GRID, HALF_GRID + 1):
        glVertex3f(i, 0, -HALF_GRID)
        glVertex3f(i, 0, HALF_GRID)
        glVertex3f(-HALF_GRID, 0, i)
        glVertex3f(HALF_GRID, 0, i)
    glEnd()

    #this causes lag because too much square is being drawn at once
    #change into a small circle around cursor seems to be good
    glColor4f(0.0, 0.0, 0.0, 0.5)
    for i in range(-HALF_GRID, HALF_GRID):
        for j in range(-HALF_GRID, HALF_GRID):
            glBegin(GL_QUADS)
            glVertex3f(i, 0, j)
            glVertex3f(i + 1, 0, j)
            glVertex3f(i + 1, 0, j + 1)
            glVertex3f(i, 0, j + 1)
            glEnd()

def draw_reference_line():
    HALF_GRID = int(GRID_SIZE/2)
    glColor3f(0, 0, 1)
    glBegin(GL_LINES)
    glVertex3f(-HALF_GRID, 0, -HALF_GRID)
    glVertex3f(-HALF_GRID, 0, HALF_GRID)
    glEnd()

    glColor3f(1, 0, 0)
    glBegin(GL_LINES)
    glVertex3f(-HALF_GRID, 0, -HALF_GRID)
    glVertex3f(HALF_GRID, 0, -HALF_GRID)
    glEnd()

    glColor3f(0, 1, 0)
    glBegin(GL_LINES)
    glVertex3f(-HALF_GRID, -HALF_GRID, -HALF_GRID)
    glVertex3f(-HALF_GRID, HALF_GRID, -HALF_GRID)
    glEnd()

# Check if a block is present at the given coordinates
def is_block_present(x, y, z):
    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and 0 <= z < GRID_SIZE:
        return grid[x][y][z] == 1
    return True

def cubeColor():
    global draw_mode_num
        # change color based on draw modes
    match draw_mode_num:
        case 0:
            glColor3f(232/255, 66/255, 32/255)
        case 1:
            glColor3f(222/255, 222/255, 47/255)

# Draw cubes based on the 3D grid
def draw_blocks():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            for z in range(GRID_SIZE):
                if grid[x, y, z] == 1:
                    draw_cube(x - GRID_SIZE // 2, y, z - GRID_SIZE // 2)

# Draw a cube at a specified position
def draw_cube(x, y, z, highlight=False):
    glColor3f(79/255, 194/255, 152/255) #cube color

    glPushMatrix()
    glTranslatef(x + CUBE_OFFSET, y + CUBE_OFFSET, z + CUBE_OFFSET)   
    glutSolidCube(CUBE_SIZE)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(x + CUBE_OFFSET, y + (CUBE_OFFSET * 2), z + CUBE_OFFSET)   
    glutSolidCube(CUBE_SIZE)
    glPopMatrix()

def cursor_cube(x, y, z, drawMode):
    cubeColor()
    glPushMatrix()
    glTranslatef(x + CUBE_OFFSET, y + CUBE_OFFSET, z + CUBE_OFFSET)   
    glutSolidCube(CUBE_SIZE)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(x + CUBE_OFFSET, y + 2*CUBE_OFFSET, z + CUBE_OFFSET)   
    glutSolidCube(CUBE_SIZE)
    glPopMatrix()

def draw_block_function():
    global draw_mode_num
    #cursor
    if grid_pos is not None:
        cursor_cube(grid_pos[0] - GRID_SIZE // 2, grid_pos[1], grid_pos[2] - GRID_SIZE // 2, draw_mode_num)

    draw_grid()
    draw_blocks()

    #if eye_position != new_eye_position:
        
def place_block(x, y, z):
    global draw_mode_num
    if draw_mode_num == 0:  # Remove block
        grid[grid_pos[0], grid_pos[1], grid_pos[2]] = 0
    elif draw_mode_num == 1:  # Place block
        grid[grid_pos[0], grid_pos[1], grid_pos[2]] = 1

#--------------------Draw Blocks----------------------





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

def map_to_new_range(value, old_min, old_max, new_min, new_max):
    # Linear transformation formula
    #return new_min + (value - old_min) * (new_max - new_min) / (old_max - old_min)
    return np.interp(value, [old_min, old_max], [new_min, new_max])

# Calculate grid position from mouse coordinates
def get_grid_position(mouse_x, mouse_y):
    global layer, CUBE_SIZE
    ray = get_ray_from_mouse(mouse_x, mouse_y)
    if ray is None:
        return None
    # Assuming the grid is at y = 0 plane
    if ray[1] == 0:
        return None
    t = -ray[1] / ray[1]
    
    #grid_x = round(ray[0] * t)
    grid_x = math.floor(ray[0] * t)
    grid_y = layer
    grid_z = round( (ray[2] * t) - CUBE_SIZE / 4 ) 

    """ if grid_pos is not None:
        grid_y = grid_pos[1]
    else:
        grid_y = 0 """
    
    #debug
    # debug1 = ray[2] * t
    # debug2 = round(debug1 - CUBE_SIZE / 4)
    # debug3 = map_to_new_range(debug2, -GRID_SIZE/2, GRID_SIZE/2, GRID_SIZE-1, 0)
    # debug4 = math.floor(debug3)
    # debug5 = int(debug4)

    # print("-------------")
    # print(f"debug ray[2] : {ray[2]}")
    # print(f"debug t : {t}")
    # print(f"debug1 : {debug1}")
    # print(f"debug2 : {debug2}")
    # print(f"debug3 : {debug3}")
    # print(f"debug4 : {debug4}")
    # print(f"debug5 : {debug5}")
    # print("-------------")
    #debug


    # Map grid positions
    grid_x = map_to_new_range(grid_x, -GRID_SIZE/2, GRID_SIZE/2, GRID_SIZE-1, 0)
    grid_z = map_to_new_range(grid_z, -GRID_SIZE/2, GRID_SIZE/2, GRID_SIZE-1, 0)

    if (abs(grid_x) > GRID_SIZE or abs(grid_y) > GRID_SIZE or abs(grid_z) > GRID_SIZE):
        grid_x = None
        grid_z = None

        grid_x = None
        grid_y = None
        grid_z = None
        return None
    else:
        grid_x = math.floor(grid_x)
        grid_z = math.floor(grid_z)

        grid_x = int(grid_x) 
        grid_y = int(grid_y)
        grid_z = int(grid_z)
    
    return [grid_x, grid_y, grid_z]


# Mouse passive motion callback
def mouse_motion(x, y):
    global mouse_x, mouse_y, grid_pos
    mouse_x, mouse_y = x, y
    grid_pos = get_grid_position(x, y)
    if grid_pos is None:
        return None
    if (abs(grid_pos[0]) > GRID_SIZE or abs(grid_pos[1]) > GRID_SIZE or abs(grid_pos[2]) > GRID_SIZE):
        pass
    """ else:
        if grid[grid_pos[0]][grid_pos[1]][grid_pos[2]] == 1:
            if abs(grid_pos[1]) < GRID_SIZE:
                grid_pos[1] += 1 """
    
    glutPostRedisplay()

def OnMouseClick(button, state, x, y):
    global clicked, file_status
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if grid_pos is not None:
            place_block(grid_pos[0], grid_pos[1], grid_pos[2])
        clicked = True
        file_status = "not saved"

    else:
        clicked = False

# draw mode
draw_mode_num = 1
draw_mode = "Add"

def drawMode(num):
    if num == 0:
        drawMode = "Delete"
    elif num == 1:
        drawMode = "Add"
    return drawMode
#draw mode



#--------------------Ray Casting 3D Selection----------------------

camera = 0

sketch_view = "front"

# Keyboard interaction handler
def key_press(key, x, y):
    global cursor_y, camera, layer, draw_mode_num
    key = key.decode("utf-8").lower()

    #camera control
    if key == 'q':
        camera += 1
    elif key == 'e':
        camera -= 1

    #layer control
    elif key == 'z':  # Down
        #cursor_y = min(GRID_SIZE - 1, cursor_y - 1)
        layer = min(GRID_SIZE - 1, layer - 1)
    elif key == 'c':  # Up
        #cursor_y = min(GRID_SIZE - 1, cursor_y + 1)
        layer = min(GRID_SIZE - 1, layer + 1)

    #draw mode control (toggle)
    elif key == 'w':
        draw_mode_num += 1
        draw_mode_num = draw_mode_num % 2

    # Save grid to slot
    elif key == '1':
        save_grid('slot1')
    elif key == '2':
        save_grid('slot2')
    elif key == '3':
        save_grid('slot3')

    # Load grid from slot
    elif key == '4':
        load_grid('slot1')
    elif key == '5':
        load_grid('slot2')
    elif key == '6':
        load_grid('slot3')

    layer = layer % GRID_SIZE
    camera = (camera % 4)

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
    global new_eye_position, eye_position
    match cam:
        case 0 :
            new_eye_position = [GRID_SIZE, eye_height, GRID_SIZE]
        case 1 :
            new_eye_position = [-GRID_SIZE, eye_height, GRID_SIZE]
        case 2 :
            new_eye_position = [-GRID_SIZE, eye_height, -GRID_SIZE]
        case 3 :
            new_eye_position = [GRID_SIZE, eye_height, -GRID_SIZE]

    return new_eye_position

def RotateCamera(pos, newpos):
    pos[0] += (newpos[0] - pos[0]) / CAMERA_ROTATE_SPEED
    pos[2] += (newpos[2] - pos[2]) / CAMERA_ROTATE_SPEED

    return pos

#--------------------Camera Control----------------------

def display_ortho():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Draw block in orthographic projection
    draw_block_ortho()

    glutSwapBuffers()

#--------------------Main Display----------------------------
def display():
    global eye_position, new_eye_position, draw_mode_num
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    SelectCamera(camera)
    eye_position = RotateCamera(eye_position, new_eye_position)
    gluLookAt(eye_position[0], eye_position[1], eye_position[2], 0, 0, 0, 0, 1, 0)

    draw_reference_line()

    draw_block_function()

    

    # Draw text
    glColor3f(1.0, 1.0, 1.0)
    draw_text(10, window_height - 40, f"Mouse: ({mouse_x}, {mouse_y}), Grid Pos: {grid_pos}, Draw Layer: {layer}")
    draw_text(10, window_height - 60, f"Draw mode : {drawMode(draw_mode_num)}")
    draw_text(10, window_height - 80, f"Save Slot : {current_slot}")
    
    if file_status == "saved":
        draw_text(10, window_height - 100, f"Saved At Slot : {current_slot}")
    elif file_status == "loaded":
        draw_text(10, window_height - 100, f"Loaded From Slot : {current_slot}")
    elif file_status == "not saved":
        draw_text(10, window_height - 100, f"Not Saved")

    draw_text(window_width - 300, window_height - 20, "Press '1', '2', '3' to Save to Slots")
    draw_text(window_width - 300, window_height - 40, "Press '4', '5', '6' to Load from Slots")

    draw_text(window_width - 630, 0 + 0, "Pree W to toggle between Drawing modes")
    draw_text(window_width - 630, 0 + 20, "Press Q or E to Rotate Camera Counter Clockwise or Clockwise")
    draw_text(window_width - 630, 0 + 40, "Press Z or C to Change Vertical Drawing Layer down 1 layer or up 1 layer")

    glutSwapBuffers()



#--------------------Main Display----------------------------

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
                    grid[x][y][z] = 1



#--------------------Ortho----------------------------

# Driver function
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
    glutMouseFunc(OnMouseClick) # mouse clicking function

    glutInitWindowPosition(100 + window_width, 100)
    main_window = glutCreateWindow(b"Sketch Plan Drawer")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(key_press)
    glutPassiveMotionFunc(mouse_motion)
    glutMouseFunc(OnMouseClick) # mouse clicking function

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
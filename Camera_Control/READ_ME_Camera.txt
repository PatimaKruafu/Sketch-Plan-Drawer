***Camera Control Setup***

ยศได้เพื่ม "Code" => ในส่วนต่อไปนี้

-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

1.) ส่วน init start (นอกfunction)

left = -20.0
right = 20.0
bottom = -10.0
top = 10.0
near = -20.0
far = 20.0

Camera_Far = 5
Camera_A_Order = 0
Camera_B_Order = 0
Camera_angle = 0.785469415042 # (math.sqrt(5/2))/2
Angle_plus = 1.570938830084 # math.sqrt(5/2)
Angle_sum = 0.785469415042

EyeX, EyeY, EyeZ = 0.0, 0.0, 0.0
AtX, AtY, AtZ = 0.0, 0.0, 0.0
UpX, UpY, UpZ = 0.0, 1.0, 0.0

-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

2.) ส่วนของ def display()

global EyeX, EyeY, EyeZ, AtX, AtY, AtZ, UpX, UpY, UpZ

# ใส่เอาไว้บนสุดในบรรดา Objects
  gluLookAt(EyeX, EyeY, EyeZ, AtX, AtY, AtZ, UpX, UpY, UpZ) 

-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

3.) ส่วนของ def keyboard(key, x, y)

global Camera_A_Order, Camera_B_Order, Camera_angle, Angle_sum, Angle_plus

# Button ">"
  if key == '.'.encode() : 
    Angle_sum = Angle_sum + Angle_plus
    Camera_A_Order = 1
# Button "<"
  if key == ','.encode() : 
    Angle_sum = Angle_sum - Angle_plus
    Camera_B_Order = 1

-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

4.) ส่วนของ def idle()

  global Camera_Far, Camera_A_Order, Camera_B_Order, EyeX, EyeY, EyeZ, AtX, AtY, AtZ, UpX, UpY, UpZ, Camera_angle, Angle_plus, Angle_sum


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

-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*




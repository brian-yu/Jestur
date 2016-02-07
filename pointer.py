import sys
from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap
# posx = float(sys.argv[1])
# posy = float(sys.argv[2])
def mousedown(posx, posy):
    mouseEvent(kCGEventMouseMoved, posx,posy);
    mouseEvent(kCGEventLeftMouseDown, posx,posy);
def mouseup(posx, posy):
    mouseEvent(kCGEventMouseMoved, posx,posy);
    mouseEvent(kCGEventLeftMouseUp, posx,posy);
def mouseEvent(type, posx, posy):
        theEvent = CGEventCreateMouseEvent(
                    None, 
                    type, 
                    (posx,posy), 
                    kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, theEvent)

def mousemove(posx,posy):
        mouseEvent(kCGEventMouseMoved, posx,posy);

def mouseclick(posx,posy):
        # uncomment this line if you want to force the mouse 
        # took-Pro-2:VRInterface davidsun$ Davids-MacBook-Pro-2:VRInterface davidsun$ Davids-MacBook-Pro-2:VRInterface davidsun$ -bash: -rw-r--r--@:: command not found
        mouseEvent(kCGEventMouseMoved, posx,posy);
        mouseEvent(kCGEventLeftMouseDown, posx,posy);
        mouseEvent(kCGEventLeftMouseUp, posx,posy);
for a in range(20):
    mousedown(100, 200)
    mouseup(100, 200)
# while True:
#     for x in range(0, 1500, 100):
#         for y in range(0, 900, 5):
#             mousemove(x, y)
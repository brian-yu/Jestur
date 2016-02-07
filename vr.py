import Leap, sys, thread, time

from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventRightMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGEventRightMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGMouseButtonRight
from Quartz.CoreGraphics import kCGHIDEventTap

from math import sqrt, pow

from appscript import app, k

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
canClick = True

def mouseEvent(type, posx, posy):
        theEvent = CGEventCreateMouseEvent(None, type, (posx,posy), kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, theEvent)
def rightEvent(type, posx, posy):
        theEvent = CGEventCreateMouseEvent(None, type, (posx,posy), kCGMouseButtonRight)
        CGEventPost(kCGHIDEventTap, theEvent)

def mousemove(posx,posy):
        mouseEvent(kCGEventMouseMoved, posx,posy);

def mouseclick(posx,posy):
        # uncomment this line if you want to force the mouse 
        # to MOVE to the click location first (I found it was not necessary).
        mouseEvent(kCGEventMouseMoved, posx,posy);
        mouseEvent(kCGEventLeftMouseDown, posx,posy);
        mouseEvent(kCGEventLeftMouseUp, posx,posy);
        
def rightclick(posx,posy):
        # uncomment this line if you want to force the mouse 
        # to MOVE to the click location first (I found it was not necessary).
        rightEvent(kCGEventMouseMoved, posx,posy);
        rightEvent(kCGEventRightMouseDown, posx,posy);
        rightEvent(kCGEventRightMouseUp, posx,posy);
        
def mousedown(posx, posy):
    #mouseEvent(kCGEventMouseMoved, posx,posy);
    mouseEvent(kCGEventLeftMouseDown, posx,posy);
def mouseup(posx, posy):
    #mouseEvent(kCGEventMouseMoved, posx,posy);
    mouseEvent(kCGEventLeftMouseUp, posx,posy);
    
def rightdown(posx, posy):
    #mouseEvent(kCGEventMouseMoved, posx,posy);
    rightEvent(kCGEventRightMouseDown, posx,posy);
def rightup(posx, posy):
    #mouseEvent(kCGEventMouseMoved, posx,posy);
    rightEvent(kCGEventRightMouseUp, posx,posy);
    
'''
x = (-200, 200)
y = (100, 340)
z = 0
'''        

scale = 3.75
xconst = 750
yconst = 1375


def distance(x1, y1, z1, x2, y2, z2):
    return sqrt(pow((x1-x2),2)+pow((y1-y2),2)+pow((z1-z2),2))

canDown = True
class SampleListener(Leap.Listener):

    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        global canDown
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
#               frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            # print "  %s, id %d, position: x=%f y=%f z=%f" % (
#                 handType, hand.id, hand.palm_position[0], hand.palm_position[1], hand.palm_position[2])
            #if xconst+(scale*hand.palm_position[0]) < 10:
            if handType == "Right hand":
                mousemove((xconst+(scale*hand.palm_position[0])),(yconst-(scale*hand.palm_position[1])))

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Get fingers
            if hand.is_right:
                clicky = ["Index", "Thumb"]
                clickFingers = [finger for finger in hand.fingers if self.finger_names[finger.type] in clicky]
            
                if len(clickFingers) == 2:
                    x1 = clickFingers[0].tip_position[0]
                    y1 = clickFingers[0].tip_position[1]
                    z1 = clickFingers[0].tip_position[2]

                    x2 = clickFingers[1].tip_position[0]
                    y2 = clickFingers[1].tip_position[1]
                    z2 = clickFingers[1].tip_position[2]
                    
                    dist = distance(x1, y1, z1, x2, y2, z2) 
                        
                    if dist < 25 and canDown:
                        print("Mouse down, %f" % dist)
                        mousedown((xconst+(scale*hand.palm_position[0])),(yconst-(scale*hand.palm_position[1])))
                        prev = ((xconst+(scale*hand.palm_position[0])),(yconst-(scale*hand.palm_position[1])))
                        print(prev)
                        canDown = False
                    if dist > 25 and not canDown:
                        print("Mouse up, %f" % dist)
                        canDown = True
                        prev = ((xconst+(scale*hand.palm_position[0])),(yconst-(scale*hand.palm_position[1])))
                        print(prev)
                        mouseup((xconst+(scale*hand.palm_position[0])),(yconst-(scale*hand.palm_position[1])))
                
                rightclicky = ["Pinky", "Thumb"]
                rightclickFingers = [finger for finger in hand.fingers if self.finger_names[finger.type] in rightclicky]
                if len(rightclickFingers) == 2:
                    x1 = rightclickFingers[0].tip_position[0]
                    y1 = rightclickFingers[0].tip_position[1]
                    z1 = rightclickFingers[0].tip_position[2]

                    x2 = rightclickFingers[1].tip_position[0]
                    y2 = rightclickFingers[1].tip_position[1]
                    z2 = rightclickFingers[1].tip_position[2]
                    
                       
                    dist = distance(x1, y1, z1, x2, y2, z2) 
                    if dist < 25:
                        rightdown((xconst+(scale*hand.palm_position[0])),(yconst-(scale*hand.palm_position[1])))
                    # if dist > 25:
#                         rightup((xconst+(scale*hand.palm_position[0])),(yconst-(scale*hand.palm_position[1])))


        # Get tools
        for tool in frame.tools:

            print "  Tool id: %d, position: %s, direction: %s" % (
                tool.id, tool.tip_position, tool.direction)

        # Get gestures
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                # Determine clock direction using the angle between the pointable and the circle normal
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                    if circle.radius > 50:
                        app('System Events').keystroke('w', using=k.command_down)
                else:
                    clockwiseness = "counterclockwise"
                    if circle.radius > 50:
                        app('System Events').keystroke('m', using=k.command_down)

                # Calculate the angle swept since the last frame
                swept_angle = 0
                if circle.state != Leap.Gesture.STATE_START:
                    previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                    swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                        gesture.id, self.state_names[gesture.state],
                        circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                        gesture.id, self.state_names[gesture.state],
                        swipe.position, swipe.direction, swipe.speed)
                if swipe.direction[1] > 0: #and abs(swipe.direction[0]) < 0.5 and abs(swipe.direction[2]) < 0.5:              
                    app('System Events').key_code(126)
                    app('System Events').key_code(126)
                    app('System Events').key_code(126)
                if swipe.direction[1] < 0: #and abs(swipe.direction[0]) < 0.5 and abs(swipe.direction[2]) < 0.5:
                    app('System Events').key_code(125)
                    app('System Events').key_code(125)
                    app('System Events').key_code(125)

            # if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
#                 keytap = KeyTapGesture(gesture)
#                 print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
#                         gesture.id, self.state_names[gesture.state],
#                         keytap.position, keytap.direction )
#
#             if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
#                 screentap = ScreenTapGesture(gesture)
#                 print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
#                         gesture.id, self.state_names[gesture.state],
#                         screentap.position, screentap.direction )

        # if not (frame.hands.is_empty and frame.gestures().is_empty):
        #     print ""

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    global canClick
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    controller.set_policy(Leap.Controller.POLICY_IMAGES)
    controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()

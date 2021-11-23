# Link to video of function test.  https://youtu.be/9ag_VQeoAOg
# This is a Bluetooth communication module based on PyGame sample. 
# We connect a flightstick joystick on COM9 to send commands via Bluetooth on !!!WIN10!!! 
# To check the function we use connect Arduino Serial Monitor on COM5
# That is how we can initiate two way serial communication over Bluetooth. 
# I hope I will be able to troubleshoot C part of Arduino Roomba Control to show the setup in action. 
# Github Repo pending... 
# The project DEPLOYED BY Vadims Stojans 14/11/2021 
# - as a coursework of "Python programmēšanas valoda" @ Riga Technical univercity further educational program.  
# Inspired by: Valdis S Coding  https://www.youtube.com/channel/UCG8gD5r27KNwhai4PoLUaZg/featured

import pygame
import serial
import time

# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')

# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

pygame.init()

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((500, 700))
pygame.display.set_caption("Vadims Roomba control station for Python course in Rtu")

# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates.
clock = pygame.time.Clock()
# Initialize the joysticks.
pygame.joystick.init()
# Get ready to print.
textPrint = TextPrint()
# <---- Initialize serial_Bt connection  ----> 
serialPort = serial.Serial(
    port="COM9", baudrate=115200, bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE)
serialString = ""  # Used to hold data coming over UART
# -------- Main Program Loop -----------
while not done:
    
    if serialPort.in_waiting > 0:

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        # Print the contents of the serial data
        try:
            print(serialString.decode("Ascii"))
            
        except:
            pass
    #
    # EVENT PROCESSING STEP
    #
    # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
    # JOYBUTTONUP, JOYHATMOTION
    for event in pygame.event.get(): # User did something.
        if event.type == pygame.QUIT: # If user clicked close.
            done = True # Flag that we are done so we exit this loop.
        elif event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    #
    # DRAWING STEP
    #
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks.
    joystick_count = pygame.joystick.get_count()

    # textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
    # textPrint.indent()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        try:
            jid = joystick.get_instance_id()
        except AttributeError:
            # get_instance_id() is an SDL2 method
            jid = joystick.get_id()
        # textPrint.tprint(screen, "Joystick {}".format(jid))
        # textPrint.indent()

        # Get the name from the OS for the controller/joystick.
        name = joystick.get_name()
        # textPrint.tprint(screen, "Joystick name: {}".format(name))

        try:
            guid = joystick.get_guid()
        except AttributeError:
            # get_guid() is an SDL2 method
            pass
        else:
            textPrint.tprint(screen, "Joystick connected") #"GUID: {}".format(guid))

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        # textPrint.tprint(screen, "Number of axes: {}".format(axes))
        textPrint.indent()

        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis))
        textPrint.unindent()

        buttons = joystick.get_numbuttons()
        # textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()

        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.tprint(screen,"Button {:>2} value: {}".format(i, button))
            if i == 11 and button == 1:
                done = True
                print("quit program")
            elif i == 6 and button ==1:  #7.poga radar ON
                serialPort.write(b"r\r\n")
            elif i == 7 and button ==1:  #8.poga radar OFF
                serialPort.write(b"b\r\n")  
            elif i == 8 and button ==1:  #9.poga Ultrasonic straight ON
                serialPort.write(b"u\r\n")           
            elif i == 9 and button ==1:  #10.poga Ultrasonic OFF
                serialPort.write(b"i\r\n")
            elif i == 10 and button ==1:  #11.poga Motors stop
                serialPort.write(b"f\r\n")
            elif i == 1 and button ==1:  #2.poga BT test message
                serialPort.write(b"test Btn Msg\r\n")                
        textPrint.unindent()

        hats = joystick.get_numhats()
        # textPrint.tprint(screen, "Number of hats: {}".format(hats))
        textPrint.indent()

        # Hat position. All or nothing for direction, not a float like
        # get_axis(). Position is a tuple of int values (x, y).
        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.tprint(screen, "Hat {} value: {}".format(i, str(hat)))
        textPrint.unindent()
    #
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    #

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second.
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
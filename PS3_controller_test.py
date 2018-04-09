import pygame

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print 'Initialised Joystick : %s' % joystick.get_name()
print 'Press ESC to stop'

screen = pygame.display.set_mode((100,100))

# get count of joysticks=1, axes=27, buttons=19 for DualShock 3

joystick_count = pygame.joystick.get_count()
print("joystick_count")
print(joystick_count)
print("--------------")

numaxes = joystick.get_numaxes()	# get the number of axes on a Joystick
print("numaxes")
print(numaxes)
print("--------------")

numbuttons = joystick.get_numbuttons()	# get the number of buttons on a Joystick
print("numbuttons")
print(numbuttons)
print("--------------")

clock = pygame.time.Clock()
loopQuit = False
while loopQuit == False:

# test joystick axes
# 0: left_x	1: left_y	2: right_x	3: right_y
        for i in range(0,4):
                pygame.event.pump()
                axis = joystick.get_axis(i)
                print("Axis " + str(i) + " = " + str(axis))
        print("--------------")

# test controller buttons
# 0: SELECT,PS	3: START		
# 4: up		5: right	6: down		7: right
# 8: left_2	9: right_2	10: left_1	11: right_1
# 12: triangle	13: circular	14: Fork	15: square
        for i in range(0,numbuttons):
                pygame.event.pump()
                button = joystick.get_button(i)
                print("Button " + str(i) + " = " + str(button))
        print("--------------")

# quit if escape pressed
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                                loopQuit = True
        clock.tick(60)
        pygame.display.update()

pygame.quit()

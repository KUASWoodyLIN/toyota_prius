import pygame


class Joystick(object):
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        print 'Connect Joystick'
        print 'Initialised Joystick : %s' % self.joystick.get_name()
        print 'Press ESC to stop'

        self.screen = pygame.display.set_mode((100, 100))
        self.clock = pygame.time.Clock()

    def update(self):
        # controller joystick axes
        left_y = -self.joystick.get_axis(1)   # left_y
        right_y = -self.joystick.get_axis(3)  # right_y

        # controller buttons
        stop = self.joystick.get_button(0)   # SELECT,PS
        start = self.joystick.get_button(3)  # START

        print('Left: %s', str(left_y))
        print('right: %s', str(right_y))
        print('Start: %s', str(start))
        print('Exit: %s', str(stop))
        print("--------------")

        # quit if escape pressed
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop = True

        pygame.display.update()
        self.clock.tick(60)
        if stop:
            self.shutdown()

        return left_y, right_y, start, stop

    @staticmethod
    def shutdown():
        print('Shutdown')
        pygame.quit()

import numpy as np

from common.canbus import Prius
from common.joystick import Joystick
from common.realtime import Ratekeeper

#SERIAL = u'1f0032000651363038363036'    # recv
SERIAL = u'520039000651363038363036'    # send


def main(rate=100):

  prius_can = Prius()
  joystick = Joystick()
  rk = Ratekeeper(rate, print_delay_threshold=2. / 1000)
  loopQuit = False

  # Send CAN Bus 100Hz
  while not loopQuit:
    left_y, right_y, start, loopQuit = joystick.update()
    if left_y > 0:
      speed = np.ceil(left_y * 65535)
    else:
      speed = 0
    prius_can.send(speed=speed)
    print 'Speed: {}'.format(speed * 0.0062)
    rk.keep_time()


if __name__ == '__main__':
  main()

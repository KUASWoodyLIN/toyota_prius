from __future__ import print_function
import struct
from panda import Panda


#serial = u'1f0032000651363038363036'    # recv
#serial = u'520039000651363038363036'    # send


def binary_show(bytes):
  fmt = '!'
  for i in range(len(bytes)):
    fmt += 'B'
  output_int = struct.unpack(fmt, bytes)
  return ' '.join('{:02X}'.format(b) for b in output_int)


def add_checksum(addr, msg):
  IDH = (addr & 0xff00) >> 8
  IDL = addr & 0xff
  checksum = IDH + IDL + len(msg) + 1
  for byte in msg:
    checksum += ord(byte)
  return struct.pack('B', checksum & 0xff)


def create_speedometer(frame, addr, speed, bus, cks=False):
  """
  :param frame: frequency if CAN Bus
  :param addr: CAN Bus ID Address
  :param speed: Input the fake speed
  :param bus: Choose which CAN Bus want to use (0,1,2)
  :param cks: True add checksum else don't.
  :return:
  """
  counter = frame & 0xff # fix
  msg = struct.pack('!BBBBBH', 0x00, 0x00, 0x00, 0x00, counter, speed)
  if cks:
    check = add_checksum(addr, msg)
    msg = msg + check
  return [addr, 0, msg, bus]


class Prius(object):
  def __init__(self):
    panda_list = Panda.list()
    # choose panda serial prot
    if len(panda_list) > 1:
      for i, s in enumerate(panda_list, 1):
        print('{}) {}'.format(i, s))
      serial = panda_list[input('Please input 1, 2,.... or 10 number: ') - 1]
    else:
      serial = panda_list[0]

    # Connect to panda
    if serial in panda_list:
      self.panda = Panda(serial)
      self.panda.set_safety_mode(Panda.SAFETY_ALLOUTPUT)
      self.panda.can_clear(0)
      self.frame = 0
      print('Connect Panda [Send]')
    else:
      print('Not Panda connect')
      exit()

  def send(self, speed=0):
    can_send = []
    # speedometer
    can_send.append(create_speedometer(self.frame, 0xB4, speed, 0, True))
    self.frame += 1
    self.panda.can_send_many(can_send)

  def recv(self, identifier='all'):
    can_msgs = self.panda.can_recv()
    can_msgs_bytes = []
    for address, _, dat, src in can_msgs:
      if identifier == 'all':
        can_msgs_bytes.append((address, 0, bytes(dat), src))
        print("Address: {}\t Data: {}\t src: {}".format(address, binary_show(dat), src))

      elif identifier == address:
        can_msgs_bytes.append((address, 0, bytes(dat), src))
        print("Address: {}\t Data: {}\t src: {}".format(address, binary_show(dat), src))



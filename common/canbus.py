from __future__ import print_function
import struct
from panda import Panda
import numpy as np


# serial = u'1f0032000651363038363036'    # recv
# serial = u'520039000651363038363036'    # send


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
    counter = frame & 0xff  # fix
    counter = 0x00
    msg = struct.pack('!BBBBBH', 0x00, 0x00, 0x00, 0x00, counter, speed)
    if cks:
        check = add_checksum(addr, msg)
        msg = msg + check
    return [addr, 0, msg, bus]


def create_speedometer2(frame, addr, speed, bus, cks=False):
    """
  :param frame: frequency if CAN Bus
  :param addr: CAN Bus ID Address
  :param speed: Input the fake speed
  :param bus: Choose which CAN Bus want to use (0,1,2)
  :param cks: True add checksum else don't.
  :return:
  """
    msg = struct.pack('!HBBB', speed, 0x00, 0x00, 0x39)
    if cks:
        check = add_checksum(addr, msg)
        msg = msg + check
    return [addr, 0, msg, bus]


def create_speedometer3(frame, addr, speed, bus, cks=False):
    """
  :param frame: frequency if CAN Bus
  :param addr: CAN Bus ID Address
  :param speed: Input the fake speed
  :param bus: Choose which CAN Bus want to use (0,1,2)
  :param cks: True add checksum else don't.
  :return:
  """
    msg = struct.pack('!HBBB', speed, 0x00, 0x00, 0x39)
    if cks:
        check = add_checksum(addr, msg)
        msg = msg + check
    return [addr, 0, msg, bus]


def create_speedometer4(frame, addr, speed, bus, cks=False):
    """
  :param frame: frequency if CAN Bus
  :param addr: CAN Bus ID Address
  :param speed: Input the fake speed
  :param bus: Choose which CAN Bus want to use (0,1,2)
  :param cks: True add checksum else don't.
  :return:
  """
    speed = np.ceil(speed / 255)
    msg = struct.pack('!BBBBB', 0x00, 0x21, speed, 0x00, 0xfc)
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

    def send_speed(self, speed=0):
        can_send = []
        # speedometer
        can_send.append(create_speedometer(self.frame, 0xB4, speed, 0, True))
        can_send.append(create_speedometer2(self.frame, 0xB1, speed, 0, True))
        can_send.append(create_speedometer3(self.frame, 0xB3, speed, 0, True))
        can_send.append(create_speedometer4(self.frame, 0x3ca, speed, 0))
        self.frame += 1
        self.panda.can_send_many(can_send)

    def send_door_lock(self, lock=True):
        can_send = []
        if lock:
            msg = struct.pack('!BBB', 0xe4, 0x81, 0x00)
            can_send.append([0x5B6, 0, msg, 0])
            self.panda.can_send_many(can_send)
        else:
            msg = struct.pack('!BBB', 0xe4, 0x00, 0x00)
            can_send.append([0x5B6, 0, msg, 0])
            self.panda.can_send_many(can_send)

    def recv(self):
        can_msgs = self.panda.can_recv()
        can_msgs_bytes = []
        for address, _, dat, src in can_msgs:
            can_msgs_bytes.append((address, 0, bytes(dat), src))
            if address == 0xb4:
                print("Address: {}\t Data: {}\t src: {}".format(address, binary_show(dat), src))

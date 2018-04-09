from common.canbus import Prius
from common.realtime import Ratekeeper


def main(rate=100):
    prius_can = Prius()
    rk = Ratekeeper(rate, print_delay_threshold=2. / 1000)

    while 1:
        prius_can.recv()
        rk.keep_time()


if __name__ == '__main__':
    main()

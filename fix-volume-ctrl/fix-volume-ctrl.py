#!/usr/bin/env python

import argparse
import os
import struct
import time
from fcntl import ioctl


def __ioctl_val(val):
    # workaround for OverFlow bug in python 2.4
    if val & 0x80000000:
        return -((val^0xffffffff)+1)
    return val


IOCTL_INFO = __ioctl_val(0x80dc4801)
IOCTL_PVERSION = __ioctl_val(0x80044810)
IOCTL_VERB_WRITE = __ioctl_val(0xc0084811)


def set(fd, nid, verb, param):
    verb = (nid << 24) | (verb << 8) | param
    ioctl(fd, IOCTL_VERB_WRITE, struct.pack('II', verb, 0))


def set_audio():
    fd = None
    try:
        fd = os.open("/dev/snd/hwC0D0", os.O_RDONLY)
        info = struct.pack('Ii64s80si64s', 0, 0, '', '', 0, '')
        res = ioctl(fd, IOCTL_INFO, info)
        name = struct.unpack('Ii64s80si64s', res)[3]
        if not name.startswith('HDA Codec'):
            raise IOError, "unknown HDA hwdep interface"
        res = ioctl(fd, IOCTL_PVERSION, struct.pack('I', 0))
        version = struct.unpack('I', res)
        if version < 0x00010000:	# 1.0.0
            raise IOError, "unknown HDA hwdep version"

        # initialization sequence starts here...
        set(fd, 0x17, 0x701, 0x00) # 0x17070100 (SET_CONNECT_SEL)
    finally:
        if fd is not None:
            os.close(fd)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--interval', type=int, default=60)
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    return parser.parse_args()


def main(interval, verbose):
    while True:
        if verbose: print('begin setting audio config')
        set_audio()
        if verbose: print('done setting audio config')
        time.sleep(interval)


if __name__ == '__main__':
    main(**vars(get_args()))

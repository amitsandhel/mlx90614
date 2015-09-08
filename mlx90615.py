#!/bin/bash
from smbus import SMBus
import time
import subprocess


def x():
	bus = SMBus(1)
	bus.open(1)
	a = bus.write_word_data(0x00, 0x5b, 1)
	time.sleep(1)
	print 'a: ', a 
	addr=0x5b<<1
	for x in range(129):
		try:
			b=bus.open(1)
			addr=x<<1
			val = bus.read_word_data(addr+1, 0x27)
			time.sleep(0.5)
			print x
			print val
			print b
			print bus.pec.bit_length()
		except IOError:
			print 'err'
			time.sleep(0.5)

##################################################################
if __name__ == '__main__':
	x()
EOF=True
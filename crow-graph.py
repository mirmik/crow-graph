#!/usr/bin/env python3

import pycrow

import matplotlib.pyplot as plt
import numpy as np

import time
import threading

pycrow.create_udpgate(12, 0)
crowker = pycrow.set_crowker(".12.127.0.0.1:10009")

plt.ion() ## Note this correction
fig=plt.figure()

n = 0
i = 0
def handler(pack):
	global n
	n = int(pack.data())

def c():
	while(1):
		pycrow.libcrow.onestep()
		time.sleep(0.0000001)

thr = threading.Thread(target=c, args=[])
thr.start()

pycrow.subscribe("mic", handler, ack=0, ackquant=0, rack=0, rackquant=0)


while 1:
	plt.scatter(i, n)
	plt.show()
	plt.pause(0.0000001) #Note this correction
	i+=1

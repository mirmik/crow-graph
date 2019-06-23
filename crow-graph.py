#!/usr/bin/env python3

import pycrow

import matplotlib.pyplot as plt
import numpy as np

import time
import threading

import matplotlib.animation as anim

import python_speech_features
from bringbuf.bringbuf import bRingBuf

pycrow.create_udpgate(12, 0)
crowker = pycrow.set_crowker(".12.127.0.0.1:10009")

#plt.ion() ## Note this correction
fftarr = None
arr = None
arr3 = None
arr4 = None
fftfreq = None

fig = plt.figure()
ax1 = fig.add_subplot(4,1,1)
ax2 = fig.add_subplot(4,1,2)
ax3 = fig.add_subplot(4,1,3)
ax4 = fig.add_subplot(4,1,4)

buff = []
buff_i = 0

bring = bRingBuf(64000)

SAMPLE_LEN = 500

n = 0
i = 0

def handler(pack):
	global arr
	global arr3
	global arr4
	global fftarr
	global buff
	global buff_i
	global fftfreq


	bring.enqueue(pack.data())

	if (bring.len > SAMPLE_LEN):
		prearr = bring.dequeue(SAMPLE_LEN)

		arr = np.frombuffer(prearr, dtype=np.int16)

		if (arr is None):
			return
		
		fftarr = np.abs(np.fft.rfft(arr))

		arr3 = fftarr
		fftfreq = np.fft.rfftfreq(len(arr), d=1 / 8000)

		#fftfreq = np.fft.fftshift(fftfreq)

		arr4 = python_speech_features.mfcc(arr, samplerate=8000)
		arr4 = arr4[0]


	#buff_i += 1

	#if (buff_i < 4):
	
	#buff.extend(prearr)

	#if (buff_i == 4):
	#buff.extend(prearr)	
	#arr = np.concatenate((prearr,prearr,prearr,prearr))	
	#fftarr = np.fft.rfft(arr)
	#fftarr = np.abs(fftarr)
	#buff = []
	#buff_i = 0

	##fftarr = python_speech_features.mfcc(arr, samplerate=8000,winlen=0.05,winstep=0.01,numcep=13,
    #             nfilt=26,nfft=512,lowfreq=0,highfreq=None,preemph=0.97,
    # ceplifter=22,appendEnergy=True)

	#fftarr = fftarr[0]



	#print(fftarr)

	#fftarr = fftarr[:len(fftarr)//2]
	#print("a")
	#print(fftarr)

def c():
	while(1):
		pycrow.libcrow.onestep()
		time.sleep(0.0000001)

thr = threading.Thread(target=c, args=[])
thr.start()

pycrow.subscribe("mic", handler, ack=0, ackquant=0, rack=0, rackquant=0)


fftarr_min = 0
fftarr_max = 0
def update(i):
	global arr
	global fftarr
	global fftarr_max
	global fftarr_min

	if arr is None:
		return

	sarr = arr

	m = np.max(fftarr)
	if fftarr_max < m: fftarr_max = m 

	m = np.min(fftarr)
	if fftarr_min > m: fftarr_min = m 
	
	xarr = range(len(arr))
	fxarr = range(len(fftarr))
	x3arr = range(len(arr3))
	x4arr = range(len(arr4))

	#print(fftarr)
	#print(fftarr_min, fftarr_max)
	
	ax1.clear()
	ax2.clear()
	ax3.clear()
	ax4.clear()
	
	ax1.set_ylim(-6000, 6000)
	ax1.plot(xarr, sarr)

	ax2.set_ylim(1, 1000000)
	ax2.set_yscale("log")
	ax2.plot(fftfreq, fftarr)

	ax3.set_ylim(-150000, 150000)
	ax3.plot(fftfreq, arr3)

	ax4.set_ylim(-30, 30)
	ax4.plot(x4arr, arr4)

	time.sleep(0.0000001)
	#print("b")


a = anim.FuncAnimation(fig, update)
plt.show()
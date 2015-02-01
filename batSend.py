#!/usr/bin/python27

'''
Class containing methods for communicating with GPRS
Since timing with GPRS shield is very dependent on the response time of AT commands,
This class will parse responses and ensure robustness
'''

import time
import multiprocessing
import serial

#Set constants

APN = "epc.tmobile.com"
HOSTSERVER = "api.xively.com"
HOSTPORT = 8081

class BatSend(multiprocessing.Process):

	def __init__(self, batQ, finishQ):
		multiprocessing.Process.__init__(self)
		self.batQ = batQ
		self.finishQ = finishQ
		self.usbPort = '/dev/tty.usbserial-A603QHNB'
		self.sp = serial.Serial(self.usbPort, 19200, timeout=0)

	def powerOn(self):
		self.sp.write(b'power')

	def close(self):
		self.sp.close()

	def timedOut(self, timeOut):
		if float(time.strftime("%s", time.localtime())) >= (timeOut + 30):
			print('tcpGSM timed out')
			return 1

	# Method for getting an IP address and to initiate TCP communication
	def tcpGSM(self):
		self.sp.write(b'AT+CGATT?\r\n')
		self.timeOut = float(time.strftime("%s", time.localtime()))
		while timedOut(self.timeOut) is not 1:
			response = self.sp.readline()
			if response is not None:
				print(response)
				if response is 'OK':
					break

		self.sp.write(b'AT+CSTT=\"" + APN + "\"\r\n')
		time.sleep(1)
		if self.timedOut() is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		self.sp.write(b'AT+CIICR\r\n')
		time.sleep(1)
		if self.timedOut is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		self.sp.write(b'AT+CIFSR\r\n')
		time.sleep(1)
		if self.timedOut is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		self.sp.write(b'AT+CIPSPRT=0\r\n')
		time.sleep(1)
		if self.timedOut is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		self.sp.write(b'AT+CIPSTART=\"tcp\",\"" + HOSTSERVER + "\",\"" + HOSTPORT + "\"\r\n')
		time.sleep(1)
		if self.timedOut is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		self.sp.write(b'AT+CIPSEND\r\n')
		time.sleep(1)
		if self.timedOut is not 1:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		print "Ready to send!"

		return 1

	def run(self):
		self.sp.flushInput()

		while True:

			if not self.batQ.empty():
				message = self.batQ.get()
				if self.tcpGSM() is 1:

					self.sp.write(message)
					while not self.batQ.empty():
						message = self.batQ.get()
						self.sp.write(message)
						time.sleep(1)
					self.sp.write(chr(26))

					if self.timedOut() is 1:
						return 1

					resp2 = self.sp.readline()

					if response is "ERROR":
						return 0

					self.sp.write(b'AT+CIPCLOSE\r\n')
					time.sleep(1)
					self.finishQ.put("Finished")





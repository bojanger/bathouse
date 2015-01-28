#!/usr/bin/python27

import time
import multiprocessing
import serial

'''

def main():






if __name__ == "__main__":
	main()
'''
#Set APN

APN = "epc.tmobile.com"
HOSTSERVER = "api.xively.com"
HOSTPORT = 8081

class BatSend(multiprocessing.Process):
	def __init__(self, batQ, finishQ):
		self.batQ = batQ
		self.finishQ = finishQ
		self.usbPort = '/dev/ttyACM0'
		self.sp = serial.Serial(self.usbPort, 9600, timeout=1)

	def __exit__(self, type, value, traceback):

	def __enter__(self):
		return self


	def close(self):
		self.sp.close()

	def timedOut(self):
		timeOut = float(time.strftime("%s", time.localtime()))
		while self.sp.inWaiting() is not 1:
			if float(time.strftime("%s", time.localtime())) => (timeOut + 30):
				print "tcpGSM timed out"
				return 0
		return 1

	def tcpGSM(self):
		self.sp.write("AT+CGATT?")
		if self.timedOut() is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		self.sp.write("AT+CSTT=\"" + APN + "\"")
		if self.timedOut() is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		self.sp.write("AT+CIICR")
		if self.timedOut is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		self.sp.write("AT+CIFSR")
		if self.timedOut is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		self.sp.write("AT+CIPSPRT=0")
		if self.timedOut is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		self.sp.write("AT+CIPSTART=\"tcp\",\"" + HOSTSERVER + "\",\"" + HOSTPORT + "\"")
		if self.timedOut is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		self.sp.write("AT+CIPSEND")
		if self.timedOut is 0:
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
					self.sp.write("(char)26")
					if self.timedOut is 0:
						return
					response = self.sp.readline()
					if response is "ERROR":
						return
					self.sp.write("AT+CIPCLOSE")
					self.finishQ.put("Finished")





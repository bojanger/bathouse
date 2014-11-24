import multiprocessing
import time
import serialServer

def main():

	taskQ = multiprocessing.Queue()
	resultQ = multiprocessing.Queue()
	sp = serialServer.SerialProcess(taskQ, resultQ)
	sp.daemon = True
	sp.start()

	while True:

		if not resultQ.empty():
			result = resultQ.get()
			print "Received data from bathouse: " + result

			# Write code to deal with data






if __name__ == '__main__':
	main()

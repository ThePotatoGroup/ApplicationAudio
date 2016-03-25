import socket
import threading
import time
import Queue
from AudioConstants import *

TCP_IP = '127.0.0.1'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, DATA_TCP_PORT))

pendingSamples = 0
totalBufferLength = 1500
samplesBuffer = Queue.Queue(maxsize=totalBufferLength)
threadLock = threading.Lock()


def playSamples():
    global pendingSamples
    while 1:
        if not samplesBuffer.empty():
            samplesBuffer.get()
            print "Buffer has: {0}".format(samplesBuffer.qsize())
        else:
            print("Buffer is empty!")

        if (samplesBuffer.qsize() + pendingSamples) <= totalBufferLength / 2:
            count = totalBufferLength - (samplesBuffer.qsize() + pendingSamples)
            with threadLock:
                pendingSamples += count
            print 'sounding: ', count
            s.sendall(struct.pack('i', count))

        time.sleep(0.01)


t = threading.Thread(target=playSamples)
t.daemon = True
t.start()

while True:
    receivedSamples = DATA_TRANSFER_STRUCT.unpack(s.recv(SAMPLES_PER_TRANSFER * BYTES_PER_SAMPLE))
    print 'Got {0} samples over TCP'.format(len(receivedSamples))
    for sample in receivedSamples:
        samplesBuffer.put(sample)

    with threadLock:
        pendingSamples -= len(receivedSamples)

s.close()

import SocketServer
from AudioConstants import *


class Message(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value


class AudioConnection(object, SocketServer.BaseRequestHandler):
    """
    This class represents a TCP connection to the embedded device that will be playing the audio.
    """

    def __init__(self, request, client_address, server):

        self.messageQueue = server.connectionQueues[client_address]
        self.done = False
        self.data = []
        self.samplesRequested = 0
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)

    def processQueueMessage(self, message):
        if message.key == 'samples':
            self.data += message.value

    def handle(self):
        while not self.done:

            while self.samplesRequested >= SAMPLES_PER_PACKET:
                if len(self.data) > SAMPLES_PER_PACKET:
                    self.request.sendall(DATA_TRANSFER_STRUCT.pack(*self.data[0:SAMPLES_PER_PACKET]))
                    self.data = self.data[SAMPLES_PER_PACKET:-1]
                    self.samplesRequested -= SAMPLES_PER_PACKET
                else:
                    if not self.messageQueue.empty():
                        self.processQueueMessage(self.messageQueue.get())

            print '{0} samples are being put on hold because they cannot fill a packet'.format(self.samplesRequested)

            sampleRequest = self.request.recv(EMBEDDED_REQUEST_STRUCT.size)
            if len(sampleRequest) > 0:
                sampleCountRequested, = EMBEDDED_REQUEST_STRUCT.unpack(sampleRequest)
                print "Got a request for: {0} samples.".format(sampleCountRequested)
                self.samplesRequested += sampleCountRequested

import time
import AudioConnection as AC
import threading
import SocketServer
import Queue
import wave
from AudioConstants import *
import struct



class AudioServer(object, SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is used to manage connections to audio player embedded systems. It it opens sockets and then listens
    for connections. When a connection is made, a new instance of AudioConnection is created and its handle method is
    called in a new thread.
    """

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.connections = []
        self.connectionQueues = {}

    def process_request(self, request, client_address):
        self.connectionQueues[client_address] = Queue.Queue()
        self.connections.append(client_address)
        super(AudioServer, self).process_request(request, client_address)

    def sendSamplesToClient(self, samples, client_address):
        self.connectionQueues[client_address].put(AC.Message('samples', samples))

    def sendAudioFileToClient(self, filename, client_address):
        print 'Sending wave file to connection'
        sampleFormats = {1: 'c', 2: 'h', 4: 'i'}
        waveFile = wave.open(filename, 'r')
        samples = []
        for i in range(waveFile.getnframes()):
            samples += struct.unpack(sampleFormats[waveFile.getsampwidth()] * waveFile.getnchannels(),
                                     waveFile.readframes(1))

        self.connectionQueues[client_address].put(AC.Message('samples', samples))


if __name__ == "__main__":

    server = AudioServer(SERVER_ADDRESS, AC.AudioConnection)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(5)
    server.sendAudioFileToClient('data.wav', server.connections[0])
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()

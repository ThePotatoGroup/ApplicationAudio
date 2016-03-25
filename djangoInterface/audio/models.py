from __future__ import unicode_literals

from django.db import models
import threading
from AudioServer import AudioServer, AudioConstants, AudioConnection


class AudioServerModel(models.base.ModelBase):
    server = AudioServer.AudioServer(AudioConstants.SERVER_ADDRESS, AudioConnection.AudioConnection)
    serverLock = threading.Lock()

    @classmethod
    def getConnections(cls):
        serversList = cls.server.connections
        return serversList


    # def some_action(self):
    #     # core code
    #     self.increment_counter()
# Create your models here.

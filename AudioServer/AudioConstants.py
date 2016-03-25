import struct

SAMPLES_PER_PACKET = 512 # TODO fix this number

DATA_TCP_PORT = 5004
SAMPLES_PER_TRANSFER = 512
BYTES_PER_SAMPLE = 4

DATA_TRANSFER_FORMAT = 'i' * SAMPLES_PER_TRANSFER
"""
{
    int samples[SAMPLES_PER_TRANSFER]
}
"""
DATA_TRANSFER_STRUCT = struct.Struct(DATA_TRANSFER_FORMAT)

EMBEDDED_REQUEST_FORMAT = 'i'
"""
{
    int numberOfSamplesRequested
}
"""
EMBEDDED_REQUEST_STRUCT = struct.Struct(EMBEDDED_REQUEST_FORMAT)

AUDIO_PROPERTIES_FORMAT = 'iii'
"""
{
    int samplingFrequency
    int nChannels
    int bitsPerChannel
}
"""
AUDIO_PROPERTIES_STRUCT = struct.Struct(AUDIO_PROPERTIES_FORMAT)


SERVER_ADDRESS = ("localhost", 5004)
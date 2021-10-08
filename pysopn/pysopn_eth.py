# Module for RAW Socket Handling


from rawsocketpy import RawSocket


class RawSocket:

    # Init RAW Socket on Interface and Port
    def __init__(self, interface, port):
        self.socket = RawSocket(interface, port)

    # Send Frame
    def send(self, data):
        self.socket.send(data, dest="\xAA\xBB\xCC\xDD\xEE\xFF")

#! /usr/bin/python


class PySopn:

    # Initialize instance
    def __init__(self, iface, port):
        self.interface = interface
        self.port = port
        self.socket = PySopn_eth(iface, port)

    # Set configuration
    def configSet(self, config):
        pass

    # Open
    def open(self):
        self.flgopen = True

#! /usr/bin/python
import os

from socket import socket
from socket import AF_PACKET
from socket import SOCK_RAW
from socket import IPPROTO_RAW


#######################################################################
# Constants #
#######################################################################
SRC_MAC = bytearray(b"\xb4\xe9\xa3\x00\x00\x00")

ETHERTYPE_PN = bytearray(b"\x88\x92")

FRAME_ID_DCP = bytearray(b"\xfe\xfd")
FRAME_ID_IDENT_ALL = bytearray(b"\xfe\xfe")

FRAME_ID_X = bytearray(b"\x10\x00\x00\x01")
FRAME_0 = bytearray(b"\x00\x00")

SERVICE_ID_SET_REQ = bytearray(b"\x04\x00")
SERVICE_ID_IDENT_REQ = bytearray(b"\x05\x00")


#######################################################################
# Public Funtions #
#######################################################################
def config_set(interface):
    self.interface = interface

# send request to set ip
def dut_ip_set(self, dut_mac, ip_addr, netmask, gw, perm_flag):
    dcp_block = bytearray(b"")
    # extend by generic header and set ip
    dcp_block = self._header_build(dcp_block, dut_mac, SERVICE_ID_SET_REQ)
    # extend by dcp block specifica
    dcp_block.extend(b"\x00\x12") # framelength
    dcp_block.extend(b"\x01\x02") # option ip suboption ip parameter
    dcp_block.extend(b"\x00\x0e") # blocklength 14
    # permanent 0x0001, else 0x0000
    perm_flag = b"\x00\x01" if True == perm_flag else b"\x00\x00"
    dcp_block.extend(perm_flag)
    dcp_block.extend(ip_addr)
    dcp_block.extend(netmask)
    dcp_block.extend(gw)
    self.send(dcp_block)

# send request to set name
def dut_name_set(self, dut_mac, name, perm_flag):
    dcp_block = bytearray(b"")
    # extend by generic header and set name
    dcp_block = self._header_build(dcp_block, dut_mac, SERVICE_ID_SET_REQ)
    dcp_block.extend(b"\x00\x0a") # framelength
    dcp_block.extend(b"\x02\x02") # option dev. prop. suboption name
    dcp_block.extend(b"\x00\x05") # blocklength 5
    # permanent 0x0001, else 0x0000
    perm_flag = b"\x00\x01" if True == perm_flag else b"\x00\x00"
    dcp_block.extend(perm_flag)
    dcp_block.extend(name)
    dcp_block.extend(b"\x00") # padding
    self.send(dcp_block)

# send identify all
def identify_all(self):
    dcp_block = bytearray(b"")
    dcp_block.extend(b"\x01\x0e\xcf\x00\x00\x00")
    dcp_block.extend(SRC_MAC)
    dcp_block.extend(ETHERTYPE_PN)
    dcp_block.extend(FRAME_ID_IDENT_ALL)
    dcp_block.extend(SERVICE_ID_IDENT_REQ)
    dcp_block.extend(FRAME_ID_X)
    dcp_block.extend(b"\x00\x01") # response delay
    dcp_block.extend(b"\x00\x04") # framelength
    dcp_block.extend(b"\xff\xff") # option dev. prop. suboption name
    self.send(dcp_block)

# open RAW socket
def open(self):
    self.sock = socket(AF_PACKET, SOCK_RAW, IPPROTO_RAW)

# send data through socket
def send(self, data):
    self.sock.sendto(data, (self.interface, 0))

# close socket
def close(self):
    self.sock.close()


#######################################################################
# Private Funtions #
#######################################################################
# build dcp header
def _header_build(self, dcp_block, dut_mac, service_id):
    dcp_block.extend(dut_mac)
    dcp_block.extend(SRC_MAC)
    dcp_block.extend(ETHERTYPE_PN)
    dcp_block.extend(FRAME_ID_DCP)
    dcp_block.extend(service_id)
    dcp_block.extend(FRAME_ID_X)
    dcp_block.extend(FRAME_0)
    return dcp_block


#######################################################################
# Main #
#######################################################################
if __name__ == "__main__":
    print('INFO: Debugging Mode')
    print('INFO: Sending Data through Raw Socket')

    dut_mac = bytearray(b"\x02\x00\x00\x00\x00\x02")
    ip_address = bytearray(b"\xc3\x88\xc2\xa8")
    netmask = bytearray(b"\x02\xc3\xbf\xc3")
    gw = bytearray(b"\xbf\xc3\xbf\x00")
    name = bytearray("dut", "utf-8")
    permanent_flag = False

    # create instance
    req_set_ip = Dcp("enp0s3")
    # open socket
    req_set_ip.open()
    # send request
    req_set_ip.dut_ip_set(dut_mac, \
                          ip_address, \
                          netmask, \
                          gw, \
                          permanent_flag)
    # send request
    req_set_ip.dut_name_set(dut_mac, \
                            name, \
                            permanent_flag)
    # close socket
    req_set_ip.close()

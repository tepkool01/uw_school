import socket, sys
from struct import *
import os

#by jason tsang mui chung - a simple script to receive raw TCP headers
# This script was written in python version 3.7.9, as such run it using python3
listenport = "40"

if os.name == "nt":
    print("using windows")
    s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_IP)
    s.bind(("127.0.0.1",40)) #port doesnt matter, technically the python process will automatically bind to its own port anyway
    s.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
    s.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)
else:
    print("using linux")
    s=socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))

# receive a packet
while True:
    
    packet = s.recvfrom(65565) # buf_size - Receive the data > https://wiki.python.org/moin/UdpCommunication
    packet = packet[0]
    ip_header = packet[0:20] # 20 for the ip header section first
    #===========================================================================
    #  "Binary" files are any files where the format isn't made up of readable characters.
    #  packed binary data means bit combinations are used to "encode" some values
    #  while the state of "unpacked" means that some bit combinations remain unused
    #  "pack" data = Return a bytes object, packed according to the format string format
    #  "unpack" data = result is a tuple, when you actively unpack packed data, you Unpack from the buffer according to the format string format
    #  use python "structs" library to pack and unpack > Interpret bytes as packed binary data, handling binary data stored in files or from network connections, 
    #  conversions between Python values and C structs > https://docs.python.org/3/library/struct.html
    #===========================================================================
    iph = unpack('!BBHHHBBH4s4s' , ip_header) #
    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF
    iph_length = (ihl * 4) 
    
    ttl = iph[5]
    protocol = iph[6]
    s_addr = socket.inet_ntoa(iph[8]);
    d_addr = socket.inet_ntoa(iph[9]);
    
    tcp_header = packet[iph_length:iph_length+20]
    tcph = unpack('!HHLLBBHHH' , tcp_header)
    '''
    IP header
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |Version|  IHL  |Type of Service|          Total Length         |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |         Identification        |Flags|      Fragment Offset    |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |  Time to Live |    Protocol   |         Header Checksum       |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                       Source Address                          |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                    Destination Address                        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                    Options                    |    Padding    |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    
    TCP header
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |          Source Port          |       Destination Port        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                        Sequence Number                        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                    Acknowledgment Number                      |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |  Data |           |U|A|P|R|S|F|                               |
    | Offset| Reserved  |R|C|S|S|Y|I|            Window             |
    |       |           |G|K|H|T|N|N|                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |           Checksum            |         Urgent Pointer        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                    Options                    |    Padding    |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                             data                              |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    '''
    
    source_port = tcph[0]
    dest_port = tcph[1]
    sequence = tcph[2]
    acknowledgement = tcph[3]
    doff_reserved = tcph[4]
    Window = tcph[5]
    Checksum  = tcph[6]
    UrgentPointer  = tcph[7]
    Options  = tcph[8]
    tcph_length = doff_reserved >> 4


    if(listenport == str(dest_port)):
        print("HEREEEE")
        print(tcph[4])
        print(tcph[5])
        print(tcph[6])
        print('[Version : ' + str(version) + '] [IP Header Length : ' + str(ihl) + '] [TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + '] [Source Address : ' + str(s_addr) + '] [Destination Address : ' + str(d_addr) +']')
        print('[Source Port : ' + str(source_port) + '] [Dest Port : ' + str(dest_port) + '] [Sequence Number : ' + str(sequence) + '] [Acknowledgement : ' + str(acknowledgement) + '] [(offset) TCP header length : ' + str(tcph_length) + ']')
        print('[(reserved & Control) Window : ' + str(Window) + '] [Checksum : ' + str(Checksum) + '] [UrgentPointer : ' + str(UrgentPointer) + '] [Options : ' + str(Options) + ']')
        print('')
        
    '''
    #print all packets
    print(str(tcp_header))
    print('Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr))
    print('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length))
    print(' doff_reserved : ' + str(doff_reserved) + ' Window : ' + str( Window) + ' Checksum : ' + str(Checksum) + ' UrgentPointer : ' + str(UrgentPointer) + ' Options : ' + str(Options))
    print('')
    '''
    h_size = iph_length + tcph_length * 4
    data_size = len(packet) - h_size
    
    #dont care about the data atm
    '''
    #get data from the packet
    data = packet[h_size:]
    try:
        if(listenport in str(dest_port)):
            print('Data : ' + data.decode("utf-8") )
    except:
        print("An exception occurred")
    '''
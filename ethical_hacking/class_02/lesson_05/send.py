import socket
#by jason tsang mui chung - a simple script to send raw TCP headers
# in this example we purposely let python and the OS handle the IP header of the packet and build only the TCP section
# This script was written in python version 3.7.9, as such run it using python3
'''
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

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.SOCK_DGRAM)

#what are bits? > "binary digit" 0 or 1 > https://whatis.techtarget.com/definition/bit-binary-digit
#hex to decimal? > https://www.binaryhexconverter.com/hex-to-decimal-converter
#decimal to hex? > https://www.binaryhexconverter.com/decimal-to-hex-converter 
#decimal to binary (bits)? > https://www.binaryhexconverter.com/decimal-to-binary-converter
tcp_header  = b'\x40\x01\x00\x28'  #[source port (1-2) 16 bits][destination port (3-4) 16 bits]           
tcp_header += b'\xcb\xcd\x01\x00'  #[seq number (1-4) 32 bits]
tcp_header += b'\x50\x06\xa7\xec'  #[ack (1-4) 32 bits]
tcp_header += b'\x0b\x0d\x0a\x02'  #TODO find me!
tcp_header += b'\x0c\x0a\x0a\x02'  #[urgent(1-2) 16 bits][options(3-4) variable]

packet = tcp_header

for i in range(1):
    print('sending packet...')
    s.sendto(packet,('127.0.0.1',9999)) #port doesnt matter, technically the python process will automatically bind to its own port anyway + we write random values in the tcp headaer
    print('send')

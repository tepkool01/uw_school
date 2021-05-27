import http.server
import socketserver
import urllib.request
import base64
"""By: Jason Tsang Mui Chung"""
"""
You could easily decode the string below to see what the code is doing
However that is not the point of the assignment
Doing so would only rob yourself of a educations
This assignment is meant only for you to run this script and to interact with it from your web browser
visit http://127.0.0.1:8000  to start the assignment, your goal is to steal the password of the admin
DO NOT visit port 8002 in your browser - again you could easil do it - but you would only be hurting your own education.

This starts up a local webserver on "localhost"
e.g: http.server.HTTPServer(('localhost', PORT), MyHandler)
If you really need to you can modify the port, but be sure to update the "run_hidden" script "port2" to match
This script was written in python version 3.7.9, as such run it using python3
"""
PORT2 = 8002

def exec_code(): 
    encoded_code = ("Y2xhc3MgTXlIYW5kbGVyMihodHRwLnNlcnZlci5CYXNlSFRUUFJlcXVlc3RIYW5kbGVyKToKICAgIGRlZiBkb19IRUFEKHNlbGYpOgogICAgICAgIHNlbGYuc2VuZF9yZXNwb25zZSgyMDApCiAgICAgICAgc2VsZi5zZW5kX2hlYWRlcigiQ29udGVudC10eXBlIiwgInRleHQvaHRtbCIpCiAgICAgICAgc2VsZi5lbmRfaGVhZGVycygpCiAgICBkZWYgZG9fR0VUKHNlbGYpOgogICAgICAgIHNlbGYuc2VuZF9yZXNwb25zZSgyMDApCiAgICAgICAgc2VsZi5zZW5kX2hlYWRlcigiQ29udGVudC10eXBlIiwgInRleHQvaHRtbCIpCiAgICAgICAgc2VsZi5lbmRfaGVhZGVycygpCiAgICAgICAgcHJpbnQoc2VsZi53ZmlsZSkKICAgICAgICAjIElmIHNvbWVvbmUgd2VudCB0byAiaHR0cDovL3NvbWV0aGluZy5zb21ld2hlcmUubmV0L2Zvby9iYXIvIiwKICAgICAgICAjIHRoZW4gcy5wYXRoIGVxdWFscyAiL2Zvby9iYXIvIi4KICAgICAgICB0cnk6CiAgICAgICAgICAgIHBhdGh6ID0gc2VsZi5wYXRoCiAgICAgICAgZXhjZXB0IEtleWJvYXJkSW50ZXJydXB0OgogICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKCgiPHA+RXJyb3IgZ2V0dGluZzogJXM8L3A+IiAlICBwYXRoeikuZW5jb2RlKCJ1dGYtOCIpKQogICAgICAgIGlmICgiP2hpbnQ9aGVscG1lIiBpbiBwYXRoeik6CiAgICAgICAgICAgIHNlbGYud2ZpbGUud3JpdGUoKCI8cD48dWw+SW0gYSBpbnRlcm5hbCBuZXR3b3JrIG9ubHkgQVBJISAtIEFjY2Vzc2luZzogJXM8L3VsPjwvcD4iICUgc2VsZi5wYXRoKS5lbmNvZGUoInV0Zi04IikpCiAgICAgICAgZWxzZToKICAgICAgICAgICAgc2VsZi53ZmlsZS53cml0ZSgoIjxwPjx1bD5JbSBhIGludGVybmFsIG5ldHdvcmsgb25seSBBUEkhIikuZW5jb2RlKCJ1dGYtOCIpKQogICAgICAgIGlmICgocGF0aHogPT0gKCIvcHVibGljLyIpKSBvciAocGF0aHogPT0gKCIvcHVibGljLz9oaW50PWhlbHBtZSIpKSk6CiAgICAgICAgICAgIHNlbGYud2ZpbGUud3JpdGUoIjxoNT48dWw+VGhpcyBpcyB0aGUgY29vbGVzdCBhcGkgZXZlciEgaXQgaGFzIHNvIG11Y2ggaW5mbywgZm9yIGV4YW1wbGUgZGlkIHlvdSBrbm93IHRoZSBlbGVwaGFudCBpcyB0aGUgb25seSBhbmltYWwgd2l0aCA0IGtuZWVzPyA8L3VsPjxoNS8+Ii5lbmNvZGUoInV0Zi04IikpCiAgICAgICAgZWxpZiAocGF0aHouc3RhcnRzd2l0aCgiL3B1YmxpYy9pbmZvIikpOgogICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKCI8aDU+PHVsPklmIHlvdSBoYXZlIDMgcXVhcnRlcnMsIDQgZGltZXMsIGFuZCA0IHBlbm5pZXMsIHlvdSBoYXZlICQxLjE5LiBZb3UgYWxzbyBoYXZlIHRoZSBsYXJnZXN0IGFtb3VudCBvZiBtb25leSBpbiBjb2lucyB3aXRob3V0IGJlaW5nIGFibGUgdG8gbWFrZSBjaGFuZ2UgZm9yIGEgZG9sbGFyLiA8L3VsPjxoNS8+Ii5lbmNvZGUoInV0Zi04IikpCiAgICAgICAgZWxpZiAocGF0aHouc3RhcnRzd2l0aCgiL3B1YmxpYy9kYXRlIikpOgogICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKCI8aDU+PHVsPlRoZSBmaXJzdCBrbm93biBjb250cmFjZXB0aXZlIHdhcyBjcm9jb2RpbGUgZHVuZywgdXNlZCBieSBFZ3lwdGlhbnMgaW4gMjAwMCBCLkMuIDwvdWw+PGg1Lz4iLmVuY29kZSgidXRmLTgiKSkKICAgICAgICBlbGlmIChwYXRoei5zdGFydHN3aXRoKCIvcHVibGljL2hlbGxvIikpOgogICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKCI8aDU+PHVsPkNhdHMgY2FuIGhlYXIgdWx0cmFzb3VuZC4gPGg1Lz4iLmVuY29kZSgidXRmLTgiKSkKICAgICAgICBlbGlmIChwYXRoei5zdGFydHN3aXRoKCIvcHVibGljL2hpbnQiKSk6CiAgICAgICAgICAgIHNlbGYud2ZpbGUud3JpdGUoIjxoNT48dWw+U2luY2UgaW0gYSBpbnRlbnJhbCBBUEksIHRoZSBnYXRld2F5IHByb3RlY3RzIG1lLCBpIGRvbnQgaGF2ZSB0byBwcm90ZWN0IG15c2VsZiBhbmQgc2ltcGx5IGdpdmUgdGhlIGdhdGV3YXkgd2hhdCBpdCBhc2tzIGZvci4gKHNlY3VyaXR5ICdleHBlY3RhdGlvbnMnIG9mIHRoaXMgcGFydGljdWxhciBkZXZlbG9wZXIpPC91bD48dWw+YWxzbyBoYXZlIHlvdSBzZWVuIHRoZSBjb29sIHB1YmxpYyBpbmZvIHdlIG9mZmVyPyBjaGVjayBvdXQgL2luZm8/dGVzdD1cIm1vbmV5X2ZhY3RzXCIlMjUyMiUyNTI1MjI8L3VsPjxoNS8+Ii5lbmNvZGUoInV0Zi04IikpCiAgICAgICAgZWxpZiAocGF0aHouc3RhcnRzd2l0aCgiL2FkbWluL2dldC91c2VycyIpKToKICAgICAgICAgICAgc2VsZi53ZmlsZS53cml0ZSgiPGgxPjx1bD5hZG1pbjwvdWw+PGgxLz48aDE+PHVsPnB1YmxpYzwvdWw+PGgxLz4iLmVuY29kZSgidXRmLTgiKSkKICAgICAgICBlbGlmIChwYXRoei5zdGFydHN3aXRoKCIvYWRtaW4vZ2V0L3Bhc3N3b3JkcyIpKToKICAgICAgICAgICAgc2VsZi53ZmlsZS53cml0ZSgiPGgxPjx1bD5hZG1pbjogYXRSNEZMbkF6bTQ2V0c1eVdLUllHSEtCOTdzOU1aREhDRkJzUlJZPC91bD48aDEvPjxoMT48dWw+cHVibGljOiBudWxsPC91bD48aDEvPiIuZW5jb2RlKCJ1dGYtOCIpKQogICAgICAgIGVsc2U6CiAgICAgICAgICAgIGlmICgiP2hpbnQ9aGVscG1lIiBpbiBwYXRoeik6CiAgICAgICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKCgiPHA+PHVsPkltIGEgaW50ZXJuYWwgbmV0d29yayBvbmx5IEFQSSEiKS5lbmNvZGUoInV0Zi04IikpCiAgICAgICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKCI8YnIvPjxici8+PGg0PkVycm9yIEFQSSBub3QgZm91bmQ8L2g0PiBBUElzIGF2YWlsYWJsZSBhcmU6PGJyLz4iLmVuY29kZSgidXRmLTgiKSkKICAgICAgICAgICAgICAgIHNlbGYud2ZpbGUud3JpdGUoIi0gL3B1YmxpYy9pbmZvPzxici8+Ii5lbmNvZGUoInV0Zi04IikpCiAgICAgICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKCItIC9wdWJsaWMvZGF0ZT88YnIvPiIuZW5jb2RlKCJ1dGYtOCIpKQogICAgICAgICAgICAgICAgc2VsZi53ZmlsZS53cml0ZSgiLSAvcHVibGljL2hlbGxvPzxici8+Ii5lbmNvZGUoInV0Zi04IikpCiAgICAgICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKCItIC9wdWJsaWMvaGludD88YnIvPiIuZW5jb2RlKCJ1dGYtOCIpKQogICAgICAgICAgICAgICAgc2VsZi53ZmlsZS53cml0ZSgiLSAvYWRtaW4vZ2V0L3VzZXJzPyA8Yj5bYmxvY2tlZCBmb3IgYWRtaW4gb25seSBhY2Nlc3NdPC9iPjxici8+Ii5lbmNvZGUoInV0Zi04IikpCiAgICAgICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKCItIC9hZG1pbi9nZXQvcGFzc3dvcmRzPyA8Yj5bYmxvY2tlZCBmb3IgYWRtaW4gb25seSBhY2Nlc3NdPC9iPjxici8+Ii5lbmNvZGUoInV0Zi04IikpCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKCI8YnIvPjxiPk9wcHMgdGhhdCBBUEkgd2FzIG5vdCBmb3VuZCwgZGlkIHlvdSBtZWFuIHRvIGxvb2sgZm9yIHNvbWV0aGluZyBsaWtlIFwiL2luZm9cIj88L2I+PGJyLz4iLmVuY29kZSgidXRmLTgiKSkKICAgICAgICBzZWxmLndmaWxlLndyaXRlKCI8L2JvZHk+PC9odG1sPiIuZW5jb2RlKCJ1dGYtOCIpKQogICAgICAgIHNlbGYud2ZpbGUuY2xvc2UoKQoKdHJ5OgogICAgc2VydmVyMiA9IGh0dHAuc2VydmVyLkhUVFBTZXJ2ZXIoKCdsb2NhbGhvc3QnLCBQT1JUMiksIE15SGFuZGxlcjIpCiAgICBwcmludCgnU3RhcnRlZCBodHRwIHNlcnZlcjInKQogICAgc2VydmVyMi5zZXJ2ZV9mb3JldmVyKCkKZXhjZXB0IEtleWJvYXJkSW50ZXJydXB0OgogICAgcHJpbnQoJ15DIHJlY2VpdmVkLCBzaHV0dGluZyBkb3duIHNlcnZlcicpCiAgICBzZXJ2ZXIyLnNvY2tldC5jbG9zZSgp")
    decoded_code = base64.b64decode(encoded_code)
    exec(decoded_code) 
exec_code() 
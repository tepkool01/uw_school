import http.server
import socketserver
import urllib.request
from urllib.parse import unquote
from urllib.parse import urljoin
import base64
"""By: Jason Tsang Mui Chung"""
"""
You could easily decode the string below to see what the code is doing
However that is not the point of the assignment
Doing so would only rob yourself of a educations
This assignment is meant only for you to run both "run_hidden" and "run_2hidden" at the same time to interact with it from your web browser
visit http://127.0.0.1:8000 in your web browser to start the assignment after running the scripts, your goal is to steal the password of the admin
DO NOT visit port 8002 in your browser - again you could easil do it - but you would only be hurting your own education.

This starts up a local webserver on "localhost"
e.g: http.server.HTTPServer(('localhost', PORT), MyHandler)
If you really need to you can modify the port, but be sure to update the "run_2hidden" script "port2" to match
This script was written in python version 3.7.9, as such run it using python3
"""
PORT = 8000
PORT2 = 8002

def exec_code(): 
    encoded_code = ("Y2xhc3MgTXlIYW5kbGVyKGh0dHAuc2VydmVyLkJhc2VIVFRQUmVxdWVzdEhhbmRsZXIpOgogICAgZGVmIGRvX0hFQUQoc2VsZik6CiAgICAgICAgc2VsZi5zZW5kX3Jlc3BvbnNlKDIwMCkKICAgICAgICBzZWxmLnNlbmRfaGVhZGVyKCJDb250ZW50LXR5cGUiLCAidGV4dC9odG1sIikKICAgICAgICBzZWxmLmVuZF9oZWFkZXJzKCkKICAgIGRlZiBkb19HRVQoc2VsZik6CiAgICAgICAgc2VsZi5zZW5kX3Jlc3BvbnNlKDIwMCkKICAgICAgICBzZWxmLnNlbmRfaGVhZGVyKCJDb250ZW50LXR5cGUiLCAidGV4dC9odG1sIikKICAgICAgICBzZWxmLmVuZF9oZWFkZXJzKCkKICAgICAgICBwcmludChzZWxmLndmaWxlKQogICAgICAgIHNlbGYud2ZpbGUud3JpdGUoIjxodG1sPjxoZWFkPjx0aXRsZT5UaGlzIGlzIGEgUHVibGljIENsb3VkIFBBQVMgb2ZmZXJpbmcgYSBmdW4gZmFjdHMgQVBJITwvdGl0bGU+PC9oZWFkPjwvaHRtbD4iLmVuY29kZSgidXRmLTgiKSkKICAgICAgICBzZWxmLndmaWxlLndyaXRlKCI8Ym9keT48cD5JIGFtIGEgZ2F0ZXdheSBpbmZyb250IG9mIGEgaW50ZXJuYWwgbmV0d29yay48L3A+PHA+SW4gdGhlIGludGVucmFsIG5ldHdvcmsgdGhlcmUgYXJlIG1pY3Jvc2VydmljZXMgdGhhdCBoYXZlIGEgdmFyaWV0eSBvZiBBUElzIHRoYXQgSSBleHBvc2UuIDxici8+QnV0IGRvbnQgd29ycnkgYWJvdXQgdGhhdCwgaXRzIG9uIGEgcHJpdmF0ZSBuZXR3b3JrIHRoYXQgeW91IGNhbid0IGFjY2VzcyBmcm9tIHRoZSBpbnRlcm5ldCwgdGhlIGdhdGV3YXkgd2lsbCBnaXZlIHlvdSB0aGUgYXBwcm9wcmlhdGUgY29udGVudDwvcD4iLmVuY29kZSgidXRmLTgiKSkKICAgICAgICAjIElmIHNvbWVvbmUgd2VudCB0byAiaHR0cDovL3NvbWV0aGluZy5zb21ld2hlcmUubmV0L2Zvby9iYXIvIiwKICAgICAgICAjIHRoZW4gcy5wYXRoIGVxdWFscyAiL2Zvby9iYXIvIi4KICAgICAgICBjb250ZW50cyA9ICIiCiAgICAgICAgdHJ5OgogICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKCgiPHA+PGI+cmVzdWx0cyBmb3IgcGF0aDogJXM8L2I+PC9wPiIgJSBzZWxmLnBhdGgpLmVuY29kZSgidXRmLTgiKSkKICAgICAgICAgICAgcGF0aHogPSAoc2VsZi5wYXRoKQogICAgICAgICAgICBwYXRoeiA9IHVucXVvdGUocGF0aHopCiAgICAgICAgICAgIHBhdGh4ID0gdXJsam9pbigiaHR0cDovL2xvY2FsaG9zdDolcyIgJSBQT1JUMiwiL3B1YmxpYyIrcGF0aHopIAogICAgICAgICAgICBjb250ZW50cyA9IHVybGxpYi5yZXF1ZXN0LnVybG9wZW4ocGF0aHgpLnJlYWQoKQogICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKChjb250ZW50cykpCiAgICAgICAgZXhjZXB0IEtleWJvYXJkSW50ZXJydXB0OgogICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKCgiPHA+RXJyb3IgZ2V0dGluZzogJXM8L3A+IiAlIHNlbGYucGF0aCkuZW5jb2RlKCJ1dGYtOCIpKQoKICAgICAgICBpZihsZW4oY29udGVudHMpID09IDApOgogICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKCI8YnIvPjxici8+IFRoYXQgd2FzIG5vdCBnb29kLCBzb21ldGhpbmcgcmVhbGx5IGJyb2tlPGJyLz4iLmVuY29kZSgidXRmLTgiKSkgCiAgICAgICAgc2VsZi53ZmlsZS53cml0ZSgiPC9ib2R5PjwvaHRtbD4iLmVuY29kZSgidXRmLTgiKSkKICAgICAgICBzZWxmLndmaWxlLmNsb3NlKCkKICAgICAgICAKCnRyeToKICAgIHNlcnZlciA9IGh0dHAuc2VydmVyLkhUVFBTZXJ2ZXIoKCdsb2NhbGhvc3QnLCBQT1JUKSwgTXlIYW5kbGVyKQogICAgcHJpbnQoJ1N0YXJ0ZWQgaHR0cCBzZXJ2ZXInKQogICAgc2VydmVyLnNlcnZlX2ZvcmV2ZXIoKQpleGNlcHQgS2V5Ym9hcmRJbnRlcnJ1cHQ6CiAgICBwcmludCgnXkMgcmVjZWl2ZWQsIHNodXR0aW5nIGRvd24gc2VydmVyJykKICAgIHNlcnZlci5zb2NrZXQuY2xvc2UoKQ==")
    decoded_code = base64.b64decode(encoded_code)
    exec(decoded_code) 
exec_code() 
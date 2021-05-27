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
Doing so would only rob yourself of a education
This assignment is meant only for you to run "run_hidden" to interact with it from your web browser
visit http://localhost:8000 in your web browser to start the assignment after running the script, your goal is to find the vulnerbility

Here is a hint if you need it. It will make the scenario a bit less realistic if you use it, but it would still be educational. 
Afterall in a real world scenario you do not know what you are looking for before hand.
based64 decode to see the Hint: WW91IGFyZSBsb29raW5nIGZvciBhIFhTUywgeW91ciBnb2FsIGlzIHRvIHBvcCB1cCBhIGFsZXJ0KCkgYm94IHdpdG
hvdXQgdGhlIHZpY3RpbSBtYW51YWxseSBkb3dubG9hZGluZyBhbmQgb3BlbmluZyBhIGZpbGUuCkFzIGFuIGF0dGFja2VyIHlvdSB3YW50IHRvIGJlIGFibGUg
dG8gZ2l2ZSB0aGUgdmljdGltIGEgbGluayB0byB2aXNpdCB0byB0aGVuIGludGVyYWN0IHdpdGggdGhlIGFwcCwgYW5kIHRoZSB4c3MgYXR0YWNrcyB0aGVtLi
BUaGlzIHdheSB0aGUgeHNzIGV4ZWN1dGVzIG9uIHRoZSAiZG9tYWluIiBvZiB0aGUgYXBwbGljYXRpb24uIA==

This starts up a local webserver on "localhost"
e.g: http.server.HTTPServer(('localhost', PORT), MyHandler)
If you really need to you can modify the port

This script was written in python version 3.7.9, as such run it using python3
"""
PORT = 8000
global uploaded_text_file
global filename
uploaded_text_file = ""

def exec_code(): 
    encoded_code = ("Y2xhc3MgTXlIYW5kbGVyKGh0dHAuc2VydmVyLkJhc2VIVFRQUmVxdWVzdEhhbmRsZXIpOgogICAgZGVmIGRvX0hFQUQoc2VsZik6CiAgICAgICAgc2VsZi5zZW5kX3Jlc3BvbnNlKDIwMCkKICAgICAgICBzZWxmLmVuZF9oZWFkZXJzKCkKICAgIGRlZiBkb19HRVQoc2VsZik6CiAgICAgICAgcGF0aHogPSAoc2VsZi5wYXRoKQogICAgICAgIHBhdGh6ID0gdW5xdW90ZShwYXRoeikKICAgICAgICBjb250ZW50dHlwZSA9ICAidGV4dC9odG1sIgogICAgICAgIGNvbnRlbnRkaXNwb3NpdGlvbnogPSAiaW5saW5lIgogICAgICAgIGZpbGVuYW1lZm9yY2FjaGVjb250cm9sID0gIjtmaWxlbmFtZT0iCiAgICAgICAgaWYoImZpbGU9IiBpbiBwYXRoeik6CiAgICAgICAgICAgIGZpbGVuYW1lX3N0YXJ0eiA9IHBhdGh6LmZpbmQoJ2ZpbGU9IicpCiAgICAgICAgICAgIGZpbGVuYW1lYyA9IHBhdGh6WyhmaWxlbmFtZV9zdGFydHorNik6Tm9uZV0KICAgICAgICAgICAgZmlsZW5hbWVfZW5keiA9IGZpbGVuYW1lYy5maW5kKCciJykKICAgICAgICAgICAgZmlsZW5hbWVjID0gZmlsZW5hbWVjWzA6ZmlsZW5hbWVfZW5kel0KICAgICAgICAgICAgZmlsZW5hbWVmb3JjYWNoZWNvbnRyb2wgPSBmaWxlbmFtZWZvcmNhY2hlY29udHJvbCArIHVybGxpYi5wYXJzZS51bnF1b3RlKGZpbGVuYW1lYykKICAgICAgICAgICAgZmlsZW5hbWVmb3JjYWNoZWNvbnRyb2wgPSBmaWxlbmFtZWZvcmNhY2hlY29udHJvbC5yZXBsYWNlKCdcXG4nLCdcbicpCiAgICAgICAgICAgIGZpbGVuYW1lZm9yY2FjaGVjb250cm9sID0gZmlsZW5hbWVmb3JjYWNoZWNvbnRyb2wucmVwbGFjZSgnXFxyJywnXHInKQogICAgICAgICAgICBmaWxlbmFtZWZvcmNhY2hlY29udHJvbCA9IGZpbGVuYW1lZm9yY2FjaGVjb250cm9sLnJlcGxhY2UoJ1xcdCcsJ1x0JykKICAgICAgICAgICAgZmlsZW5hbWVmb3JjYWNoZWNvbnRyb2wgPSBmaWxlbmFtZWZvcmNhY2hlY29udHJvbC5yZXBsYWNlKCdcXHUwMDBhJywnXHUwMDBhJykKICAgICAgICAgICAgZmlsZW5hbWVmb3JjYWNoZWNvbnRyb2wgPSBmaWxlbmFtZWZvcmNhY2hlY29udHJvbC5yZXBsYWNlKCdcXHUwMDBiJywnXHUwMDBiJykKICAgICAgICAgICAgZmlsZW5hbWVmb3JjYWNoZWNvbnRyb2wgPSBmaWxlbmFtZWZvcmNhY2hlY29udHJvbC5yZXBsYWNlKCdcXHUwMDBkJywnXHUwMDBkJykKICAgICAgICAgICAgZmlsZW5hbWVmb3JjYWNoZWNvbnRyb2wgPSBmaWxlbmFtZWZvcmNhY2hlY29udHJvbC5yZXBsYWNlKCdcXGInLCdcYicpCiAgICAgICAgICAgIGZpbGVuYW1lZm9yY2FjaGVjb250cm9sID0gZmlsZW5hbWVmb3JjYWNoZWNvbnRyb2wucmVwbGFjZSgnXFxkJywnXGQnKQogICAgICAgICAgICBmaWxlbmFtZWZvcmNhY2hlY29udHJvbCA9IGZpbGVuYW1lZm9yY2FjaGVjb250cm9sLnJlcGxhY2UoJ1xcaScsJ1xpJykKICAgICAgICAgICAgcHJpbnQoZmlsZW5hbWVmb3JjYWNoZWNvbnRyb2wpCiAgICAgICAgZG93bmxvYWR6PSBGYWxzZQogICAgICAgIGZpbGVuYW1lenogPSAiZG93bmxvYWQiCiAgICAgICAgaWYoImRvd25sb2FkIiBpbiBwYXRoeik6CiAgICAgICAgICAgIGRvd25sb2FkeiA9IFRydWUKICAgICAgICBpZihkb3dubG9hZHopOgogICAgICAgICAgICBjb250ZW50dHlwZSA9ICAidGV4dC9odG1sIgogICAgICAgICAgICBmaWxlMSA9IG9wZW4oJ2Rvd25sb2FkLnR4dCcsICdyJykKICAgICAgICAgICAgTGluZXMgPSBmaWxlMS5yZWFkbGluZXMoKQogICAgICAgICAgICBrZWVwbG9va2luID0gVHJ1ZQogICAgICAgICAgICBmaWxlMS5jbG9zZSgpCiAgICAgICAgICAgIGZvciBsaW5lIGluIExpbmVzOgogICAgICAgICAgICAgICAgI3ByaW50KGxpbmUpCiAgICAgICAgICAgICAgICBpZigiQ29udGVudC1EaXNwb3NpdGlvbjoiIGluIGxpbmUpOgogICAgICAgICAgICAgICAgICAgIGlmKGtlZXBsb29raW4pOgogICAgICAgICAgICAgICAgICAgICAgICBwcmludCgiZm91bmQgY29udGVudCBkaXNwb3N0aW9uIikKICAgICAgICAgICAgICAgICAgICAgICAgZmlsZW5hbWVfc3RhcnQgPSBsaW5lLmZpbmQoJ0NvbnRlbnQtRGlzcG9zaXRpb246JykKICAgICAgICAgICAgICAgICAgICAgICAgZmlsZW5hbWUgPSBsaW5lWyhmaWxlbmFtZV9zdGFydCsyMCk6Tm9uZV0KICAgICAgICAgICAgICAgICAgICAgICAgZmlsZW5hbWVfZW5kID0gZmlsZW5hbWUuZmluZCgnLS0nKQogICAgICAgICAgICAgICAgICAgICAgICBmaWxlbmFtZSA9IGZpbGVuYW1lWzA6ZmlsZW5hbWVfZW5kXQogICAgICAgICAgICAgICAgICAgICAgICBjb250ZW50ZGlzcG9zaXRpb256ID0gZmlsZW5hbWUKICAgICAgICAgICAgICAgICAgICAgICAgZmlsZW5hbWVfc3RhcnQgPSBsaW5lLmZpbmQoJ2ZpbGVuYW1lPSInKQogICAgICAgICAgICAgICAgICAgICAgICBmaWxlbmFtZSA9IGxpbmVbKGZpbGVuYW1lX3N0YXJ0KzEwKTpOb25lXQogICAgICAgICAgICAgICAgICAgICAgICBmaWxlbmFtZV9lbmQgPSBmaWxlbmFtZS5maW5kKCciJykKICAgICAgICAgICAgICAgICAgICAgICAgZmlsZW5hbWUgPSBmaWxlbmFtZVswOmZpbGVuYW1lX2VuZF0KICAgICAgICAgICAgICAgICAgICAgICAgZmlsZW5hbWV6eiA9IGZpbGVuYW1lCiAgICAgICAgICAgICAgICAgICAgICAgIGNvbnRlbnRkaXNwb3NpdGlvbnogPSBjb250ZW50ZGlzcG9zaXRpb256ICsgIjsgZmlsZW5hbWU9XCIiK2ZpbGVuYW1lenorIlwiIgogICAgICAgICAgICAgICAgICAgICAgICBrZWVwbG9va2luID0gRmFsc2UKICAgICAgICAgICAgICAgICAgICAgICAgcHJpbnQoY29udGVudGRpc3Bvc2l0aW9ueikKICAgICAgICAgICAgICAgICAgICBwcmludChrZWVwbG9va2luKQogICAgICAgIHNlbGYuc2VuZF9yZXNwb25zZSgyMDApCiAgICAgICAgc2VsZi5zZW5kX2hlYWRlcigieC1jb250ZW50LXR5cGUtb3B0aW9ucyIsICJub3NuaWZmIikKICAgICAgICBzZWxmLnNlbmRfaGVhZGVyKCJDb250ZW50LXR5cGUiLCBjb250ZW50dHlwZSkKICAgICAgICBzZWxmLnNlbmRfaGVhZGVyKCJDYWNoZS1Db250cm9sIiwgIm5vLWNhY2hlLCBuby1zdG9yZSwgbXVzdC1yZXZhbGlkYXRlLCIrZmlsZW5hbWVmb3JjYWNoZWNvbnRyb2wpCiAgICAgICAgc2VsZi5zZW5kX2hlYWRlcigiQ29udGVudC1EaXNwb3NpdGlvbiIsIGNvbnRlbnRkaXNwb3NpdGlvbnopCiAgICAgICAgc2VsZi5zZW5kX2hlYWRlcigiUHJhZ21hIiwgIm5vLWNhY2hlIikKICAgICAgICBzZWxmLmVuZF9oZWFkZXJzKCkKICAgICAgICAjcHJpbnQoc2VsZi53ZmlsZSkKICAgICAgICAjIElmIHNvbWVvbmUgd2VudCB0byAiaHR0cDovL3NvbWV0aGluZy5zb21ld2hlcmUubmV0L2Zvby9iYXIvIiwKICAgICAgICAjIHRoZW4gcy5wYXRoIGVxdWFscyAiL2Zvby9iYXIvIi4KCiAgICAgICAgaWYoZG93bmxvYWR6ID09IEZhbHNlKToKICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgbGFuZGluZ2h0bWwgPSAnJycKICAgICAgICAgICAgICAgIDwhRE9DVFlQRSBodG1sPgogICAgICAgICAgICAgICAgPGh0bWw+CiAgICAgICAgICAgICAgICA8Ym9keT4KICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgPGgxPllvdSBjYW4gbW9kaWZ5IGFuZCBkb3dubG9hZCB5b3VyIG93biBtb2RhbCBzYW1wbGUhPC9oMT4KICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgPGZvcm0gPgogICAgICAgICAgICAgICAgICA8bGFiZWwgZm9yPSJmbmFtZSI+RW50ZXIgYSBzdHlsZSB0byBhcHBseSB0byB5b3VyIG1vZGFsIHdoZW4gaXQgY2xvc2VzOjwvbGFiZWw+PGJyLz4KICAgICAgICAgICAgICAgICAgPGxhYmVsIGZvcj0iZm5hbWUiPlBsZWFzZSBvbmx5IGVudGVyIGpzb24gZGF0YSEhOjwvbGFiZWw+PGJyLz4KICAgICAgICAgICAgICAgICAgPGxhYmVsIGZvcj0iZm5hbWUiPlRoZSBkZWZhdWx0IGlzIHNpbXBseSAibm9uZSIgPC9sYWJlbD4KICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9InRleHQiIGlkPSJmbmFtZSIgbmFtZT0iZm5hbWUiPjxicj4KICAgICAgICAgICAgICAgICAgPGJyPgogICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0ic3VibWl0IiBvbmNsaWNrPSJzZW5kKCkiIHZhbHVlPSJTdWJtaXQgdG8gQ3JlYXRlIFlvdXIgU2FtcGxlIEZpbGUhIi8+PGJyLz48YnIvPgogICAgICAgICAgICAgICAgPC9mb3JtPgogICAgICAgICAgICAgICAgPHNjcmlwdD4KICAgICAgICAgICAgICAgIGZ1bmN0aW9uIHNlbmQoKQogICAgICAgICAgICAgICAgewogICAgICAgICAgICAgICAgICB2YXIgeGhyID0gbmV3IFhNTEh0dHBSZXF1ZXN0KCk7CiAgICAgICAgICAgICAgICAgIHhoci5vcGVuKCJQT1NUIiwgIi91cGxvYWQiLCB0cnVlKTsKICAgICAgICAgICAgICAgICAgeGhyLnNldFJlcXVlc3RIZWFkZXIoJ0NvbnRlbnQtVHlwZScsICdhcHBsaWNhdGlvbi9qc29uJyk7CiAgICAgICAgICAgICAgICAgIHhoci5zZW5kKGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJmbmFtZSIpLnZhbHVlKTsKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgIDwvc2NyaXB0PgogICAgICAgICAgICAgICAgPGxhYmVsIGZvcj0iZm5hbWUiPkNob29zZSBhIEZpbGVuYW1lIHRvIERvd25sb2FkIFlvdXIgRmlsZSBhczogIDwvbGFiZWw+CiAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0idGV4dCIgaWQ9ImZpbGVuYW1lIiBvbmtleXVwPSJteUZ1bmN0aW9uKCkiIG5hbWU9ImZpbGVuYW1lIj4KICAgICAgICAgICAgICAgIDxhIGhyZWY9Ii9kb3dubG9hZCIgaWQ9ImRvd25sb2FkYnV0dG9uIj48YnV0dG9uPkRvd25sb2FkIHlvdXIgc2FtcGxlITwvYnV0dG9uPjwvYT4KICAgICAgICAgICAgICAgIDxzY3JpcHQ+CiAgICAgICAgICAgICAgICBmdW5jdGlvbiBteUZ1bmN0aW9uKCkgewogICAgICAgICAgICAgICAgICB2YXIgeCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJmaWxlbmFtZSIpOwogICAgICAgICAgICAgICAgICB2YXIgZG93bmxvYWRmaWxlbmFtZSA9IGVuY29kZVVSSSh4LnZhbHVlKTsKICAgICAgICAgICAgICAgICAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImRvd25sb2FkYnV0dG9uIikuaHJlZj0oIi9kb3dubG9hZD9maWxlPSIuY29uY2F0KGRvd25sb2FkZmlsZW5hbWUpKTsKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgIDwvc2NyaXB0PgogICAgICAgICAgICAgICAgPHA+YnJvdWdodCB0byB5b3UgYnkganRtYyBmYWtlIGNvcnA8L3A+CiAgICAgICAgICAgICAgICA8L2JvZHk+CiAgICAgICAgICAgICAgICA8L2h0bWw+CiAgICAgICAgICAgICAgICAnJycKICAgICAgICAgICAgICAgIHNlbGYud2ZpbGUud3JpdGUoKGxhbmRpbmdodG1sKS5lbmNvZGUoInV0Zi04IikpCiAgICAgICAgICAgIGV4Y2VwdCBLZXlib2FyZEludGVycnVwdDoKICAgICAgICAgICAgICAgIHNlbGYud2ZpbGUud3JpdGUoKCI8cD5FcnJvciBnZXR0aW5nOiAlczwvcD4iICUgc2VsZi5wYXRoKS5lbmNvZGUoInV0Zi04IikpCiAgICAgICAgZWxzZToKICAgICAgICAgICAgZmlsZTEgPSBvcGVuKCdkb3dubG9hZC50eHQnLCAncicpCiAgICAgICAgICAgIExpbmVzID0gZmlsZTEucmVhZGxpbmVzKCkKICAgICAgICAgICAgZmlsZTEuY2xvc2UoKQogICAgICAgICAgICBmb3IgbGluZSBpbiBMaW5lczoKICAgICAgICAgICAgICAgIHNlbGYud2ZpbGUud3JpdGUoKGxpbmUpLmVuY29kZSgidXRmLTgiKSkKICAgICAgICBzZWxmLndmaWxlLmNsb3NlKCkKICAgIGRlZiBkb19QT1NUKHNlbGYpOgogICAgICAgIHVwbG9hZGluZyA9IEZhbHNlCiAgICAgICAgcGF0aHogPSAoc2VsZi5wYXRoKQogICAgICAgIHBhdGh6ID0gdW5xdW90ZShwYXRoeikKICAgICAgICBjb250ZW50dHlwZSA9ICIiCiAgICAgICAgaWYoInVwbG9hZCIgaW4gcGF0aHopOgogICAgICAgICAgICBjb250ZW50dHlwZSA9ICAidGV4dC9odG1sIgogICAgICAgICAgICB1cGxvYWRpbmcgPSBUcnVlCiAgICAgICAgc2VsZi5zZW5kX3Jlc3BvbnNlKDIwMCkKICAgICAgICBzZWxmLnNlbmRfaGVhZGVyKCJ4LWNvbnRlbnQtdHlwZS1vcHRpb25zIiwgIm5vc25pZmYiKQogICAgICAgIHNlbGYuc2VuZF9oZWFkZXIoIkNvbnRlbnQtdHlwZSIsIGNvbnRlbnR0eXBlKQogICAgICAgIHNlbGYuc2VuZF9oZWFkZXIoIkNhY2hlLUNvbnRyb2wiLCAibm8tY2FjaGUsIG5vLXN0b3JlLCBtdXN0LXJldmFsaWRhdGUiKQogICAgICAgIHNlbGYuc2VuZF9oZWFkZXIoIlByYWdtYSIsICJuby1jYWNoZSIpCiAgICAgICAgc2VsZi5lbmRfaGVhZGVycygpCiAgICAgICAgI3ByaW50KHNlbGYud2ZpbGUpCiAgICAgICAgIyBJZiBzb21lb25lIHdlbnQgdG8gImh0dHA6Ly9zb21ldGhpbmcuc29tZXdoZXJlLm5ldC9mb28vYmFyLyIsCiAgICAgICAgIyB0aGVuIHMucGF0aCBlcXVhbHMgIi9mb28vYmFyLyIuCiAgICAgICAgdHJ5OgogICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKCgiPHNjcmlwdD53aW5kb3cuY2xvc2UoKTs8L3NjcmlwdD48cD48Yj5yZXN1bHRzIGZvciBwYXRoOiAlczwvYj48L3A+IiAlIHNlbGYucGF0aCkuZW5jb2RlKCJ1dGYtOCIpKQogICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKCI8aHRtbD48aGVhZD48dGl0bGU+VGVzdCE8L3RpdGxlPjwvaGVhZD4iLmVuY29kZSgidXRmLTgiKSkKICAgICAgICAgICAgc2VsZi53ZmlsZS53cml0ZSgiPGJvZHk+dGhpcyB3YXMgYSBwb3N0IHJlcXVlc3Q8L3A+Ii5lbmNvZGUoInV0Zi04IikpCiAgICAgICAgZXhjZXB0IEtleWJvYXJkSW50ZXJydXB0OgogICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKCgiPHA+RXJyb3IgZ2V0dGluZzogJXM8L3A+IiAlIHNlbGYucGF0aCkuZW5jb2RlKCJ1dGYtOCIpKQoKICAgICAgICBzZWxmLndmaWxlLndyaXRlKCI8L2JvZHk+PC9odG1sPiIuZW5jb2RlKCJ1dGYtOCIpKQogICAgICAgIGlmKHVwbG9hZGluZyk6CiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIGNvbnRlbnRfbGVuID0gaW50KHNlbGYuaGVhZGVycy5nZXQoJ0NvbnRlbnQtTGVuZ3RoJykpCiAgICAgICAgICAgICAgICBwb3N0X2JvZHkgPSBzZWxmLnJmaWxlLnJlYWQoY29udGVudF9sZW4pCiAgICAgICAgICAgICAgICBlbmNvZGluZyA9ICd1dGYtOCcKICAgICAgICAgICAgICAgIHVwbG9hZGVkX3RleHRfZmlsZSA9IHBvc3RfYm9keS5kZWNvZGUoZW5jb2RpbmcpCiAgICAgICAgICAgICAgICB1cGxvYWRlZF90ZXh0X2ZpbGUgPSB1cGxvYWRlZF90ZXh0X2ZpbGUucmVwbGFjZSgiPiIsICImZ3Q7IikKICAgICAgICAgICAgICAgIHVwbG9hZGVkX3RleHRfZmlsZSA9IHVwbG9hZGVkX3RleHRfZmlsZS5yZXBsYWNlKCI8IiwgIiZ0aDsiKQogICAgICAgICAgICAgICAgdXBsb2FkZWRfdGV4dF9maWxlID0gdXBsb2FkZWRfdGV4dF9maWxlLnJlcGxhY2UoIlwiIiwgIiZxdW90OyIpCiAgICAgICAgICAgICAgICB1cGxvYWRlZF90ZXh0X2ZpbGUgPSB1cGxvYWRlZF90ZXh0X2ZpbGUucmVwbGFjZSgiXHIiLCAiICIpCiAgICAgICAgICAgICAgICB1cGxvYWRlZF90ZXh0X2ZpbGUgPSB1cGxvYWRlZF90ZXh0X2ZpbGUucmVwbGFjZSgiXG4iLCAiICIpCiAgICAgICAgICAgICAgICAnJycKICAgICAgICAgICAgICAgIGZpbGVuYW1lX3N0YXJ0ID0gdXBsb2FkZWRfdGV4dF9maWxlLmZpbmQoJ2ZpbGVuYW1lPSInKQogICAgICAgICAgICAgICAgZmlsZW5hbWUgPSB1cGxvYWRlZF90ZXh0X2ZpbGVbKGZpbGVuYW1lX3N0YXJ0KzEwKTpOb25lXQogICAgICAgICAgICAgICAgZmlsZW5hbWVfZW5kID0gZmlsZW5hbWUuZmluZCgnIicpCiAgICAgICAgICAgICAgICBmaWxlbmFtZSA9IGZpbGVuYW1lWzA6ZmlsZW5hbWVfZW5kXQogICAgICAgICAgICAgICAgJycnCiAgICAgICAgICAgICAgICBmaWxlbmFtZT0iZG93bmxvYWQudHh0IgogICAgICAgICAgICAgICAgZmlsZXBhcnQxID0gJycnPCFET0NUWVBFIGh0bWw+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGh0bWw+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRpdGxlPlczLkNTUzwvdGl0bGU+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPG1ldGEgbmFtZT0idmlld3BvcnQiIGNvbnRlbnQ9IndpZHRoPWRldmljZS13aWR0aCwgaW5pdGlhbC1zY2FsZT0xIj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Ii93My5jc3MiPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly93d3cudzNzY2hvb2xzLmNvbS93M2Nzcy80L3czLmNzcyI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGJvZHk+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0idzMtY29udGFpbmVyIj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxoMj5XMy5DU1MgTW9kYWw8L2gyPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHA+dGhpcyBpcyBhIGZyZWUgc2FtcGxlIG1vZGFsIG91ciBjb21wYW55IGlzIGdpdmluZyBvdXQ8L3A+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8YnV0dG9uIG9uY2xpY2s9ImRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdpZDAxJykuc3R5bGUuZGlzcGxheT0nYmxvY2snIiBjbGFzcz0idzMtYnV0dG9uIHczLWJsYWNrIj5PcGVuIE1vZGFsPC9idXR0b24+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8ZGl2IGlkPSJpZDAxIiBjbGFzcz0idzMtbW9kYWwiPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJ3My1tb2RhbC1jb250ZW50Ij4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJ3My1jb250YWluZXIiPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHNwYW4gb25jbGljaz0ibXlGdW5jdGlvbigpIiBjbGFzcz0idzMtYnV0dG9uIHczLWRpc3BsYXktdG9wcmlnaHQiPiZ0aW1lczs8L3NwYW4+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8cD5Tb21lIHRleHQuIFNvbWUgdGV4dC4gU29tZSB0ZXh0LjwvcD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxwPlNvbWUgdGV4dC4gU29tZSB0ZXh0LiBTb21lIHRleHQuPC9wPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvZGl2PgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvZGl2PgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvZGl2PgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxzY3JpcHQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZnVuY3Rpb24gbXlGdW5jdGlvbigpIHsKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgc3R5bGV6ID0gIiI7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRyeSB7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgc3R5bGV6ID0gZXZhbCgiJycnCiAgICAgICAgICAgICAgICBmaWxlcGFydDIgPSAnJyciKTsKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB9IGNhdGNoIChlcnJvcikgewogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgY29uc29sZS5lcnJvcihlcnJvcik7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAvLyBleHBlY3RlZCBvdXRwdXQ6IFJlZmVyZW5jZUVycm9yOiBub25FeGlzdGVudEZ1bmN0aW9uIGlzIG5vdCBkZWZpbmVkCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAvLyBOb3RlIC0gZXJyb3IgbWVzc2FnZXMgd2lsbCB2YXJ5IGRlcGVuZGluZyBvbiBicm93c2VyCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdpZDAxJykuc3R5bGUuZGlzcGxheT1zdHlsZXo7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3NjcmlwdD4gICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvYm9keT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwhLS1ETyBOT1QgUkVNT1RFIFRIRSBMSU5FIEJFTE9XISAtIFNhdmUgdGhlIEhUVFAgaGVhZGVycyB0byBiZSB1c2VkIG9uIGRvd25sb2FkIGJlbG93LCB3ZSdsbCBzZWFyY2ggZm9yICJDb250ZW50LURpc3Bvc2l0aW9uIiBpbiB0aGUgZmlsZSB0aGVuIHBhcnNlIGl0IHNvIHdlIGRvbnQgaGF2ZSB0byBtYWtlIGFub3RoZXIgY29uZmlnIGZpbGUtLT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwhLS1Db250ZW50LURpc3Bvc2l0aW9uOiBhdHRhY2htZW50OyBmaWxlbmFtZT0iZGVmYXVsdC50eHQiLS0+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L2h0bWw+ICcnJwogICAgICAgICAgICAgICAgZiA9IG9wZW4oZmlsZW5hbWUsICJ3IikKICAgICAgICAgICAgICAgIGYud3JpdGUoZmlsZXBhcnQxK3VwbG9hZGVkX3RleHRfZmlsZStmaWxlcGFydDIpCiAgICAgICAgICAgICAgICBmLmNsb3NlKCkKICAgICAgICAgICAgZXhjZXB0OgogICAgICAgICAgICAgICAgc2VsZi53ZmlsZS53cml0ZSgoIjxwPmZpbGUgdXBsb2FkIGZhaWxlZCIpLmVuY29kZSgidXRmLTgiKSkKICAgICAgICAgICAgICAgIHByaW50KCJmaWxlIHVwbG9hZCBmYWlsZWQhIikgCgogICAgICAgIHNlbGYud2ZpbGUuY2xvc2UoKSAgIAoKdHJ5OgogICAgc2VydmVyID0gaHR0cC5zZXJ2ZXIuSFRUUFNlcnZlcigoJ2xvY2FsaG9zdCcsIFBPUlQpLCBNeUhhbmRsZXIpCiAgICBwcmludCgnU3RhcnRlZCBodHRwIHNlcnZlcicpCiAgICBzZXJ2ZXIuc2VydmVfZm9yZXZlcigpCmV4Y2VwdCBLZXlib2FyZEludGVycnVwdDoKICAgIHByaW50KCdeQyByZWNlaXZlZCwgc2h1dHRpbmcgZG93biBzZXJ2ZXInKQogICAgc2VydmVyLnNvY2tldC5jbG9zZSgp")
    decoded_code = base64.b64decode(encoded_code)
    exec(decoded_code) 
exec_code() 

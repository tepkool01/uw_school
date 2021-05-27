class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        pathz = (self.path)
        pathz = unquote(pathz)
        contenttype = "text/html"
        contentdispositionz = "inline"
        filenameforcachecontrol = ";filename="
        if ("file=" in pathz):
            filename_startz = pathz.find('file="')
            filenamec = pathz[(filename_startz + 6):None]
            filename_endz = filenamec.find('"')
            filenamec = filenamec[0:filename_endz]
            filenameforcachecontrol = filenameforcachecontrol + urllib.parse.unquote(filenamec)
            filenameforcachecontrol = filenameforcachecontrol.replace('\\n', '\n')
            filenameforcachecontrol = filenameforcachecontrol.replace('\\r', '\r')
            filenameforcachecontrol = filenameforcachecontrol.replace('\\t', '\t')
            filenameforcachecontrol = filenameforcachecontrol.replace('\\u000a', '\u000a')
            filenameforcachecontrol = filenameforcachecontrol.replace('\\u000b', '\u000b')
            filenameforcachecontrol = filenameforcachecontrol.replace('\\u000d', '\u000d')
            filenameforcachecontrol = filenameforcachecontrol.replace('\\b', '\b')
            filenameforcachecontrol = filenameforcachecontrol.replace('\\d', '\d')
            filenameforcachecontrol = filenameforcachecontrol.replace('\\i', '\i')
            print(filenameforcachecontrol)
        downloadz = False
        filenamezz = "download"
        if ("download" in pathz):
            downloadz = True
        if (downloadz):
            contenttype = "text/html"
            file1 = open('download.txt', 'r')
            Lines = file1.readlines()
            keeplookin = True
            file1.close()
            for line in Lines:
                # print(line)
                if ("Content-Disposition:" in line):
                    if (keeplookin):
                        print("found content dispostion")
                        filename_start = line.find('Content-Disposition:')
                        filename = line[(filename_start + 20):None]
                        filename_end = filename.find('--')
                        filename = filename[0:filename_end]
                        contentdispositionz = filename
                        filename_start = line.find('filename="')
                        filename = line[(filename_start + 10):None]
                        filename_end = filename.find('"')
                        filename = filename[0:filename_end]
                        filenamezz = filename
                        contentdispositionz = contentdispositionz + "; filename=\"" + filenamezz + "\""
                        keeplookin = False
                        print(contentdispositionz)
                    print(keeplookin)
        self.send_response(200)
        self.send_header("x-content-type-options", "nosniff")
        self.send_header("Content-type", contenttype)
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate," + filenameforcachecontrol)
        self.send_header("Content-Disposition", contentdispositionz)
        self.send_header("Pragma", "no-cache")
        self.end_headers()
        # print(self.wfile)
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".

        if (downloadz == False):
            try:
                landinghtml = '''
                <!DOCTYPE html>
                <html>
                <body>

                <h1>You can modify and download your own modal sample!</h1>

                <form >
                  <label for="fname">Enter a style to apply to your modal when it closes:</label><br/>
                  <label for="fname">Please only enter json data!!:</label><br/>
                  <label for="fname">The default is simply "none" </label>
                  <input type="text" id="fname" name="fname"><br>
                  <br>
                  <input type="submit" onclick="send()" value="Submit to Create Your Sample File!"/><br/><br/>
                </form>
                <script>
                function send()
                {
                  var xhr = new XMLHttpRequest();
                  xhr.open("POST", "/upload", true);
                  xhr.setRequestHeader('Content-Type', 'application/json');
                  xhr.send(document.getElementById("fname").value);
                }
                </script>
                <label for="fname">Choose a Filename to Download Your File as:  </label>
                <input type="text" id="filename" onkeyup="myFunction()" name="filename">
                <a href="/download" id="downloadbutton"><button>Download your sample!</button></a>
                <script>
                function myFunction() {
                  var x = document.getElementById("filename");
                  var downloadfilename = encodeURI(x.value);
                  document.getElementById("downloadbutton").href=("/download?file=".concat(downloadfilename));
                }
                </script>
                <p>brought to you by jtmc fake corp</p>
                </body>
                </html>
                '''
                self.wfile.write((landinghtml).encode("utf-8"))
            except KeyboardInterrupt:
                self.wfile.write(("<p>Error getting: %s</p>" % self.path).encode("utf-8"))
        else:
            file1 = open('download.txt', 'r')
            Lines = file1.readlines()
            file1.close()
            for line in Lines:
                self.wfile.write((line).encode("utf-8"))
        self.wfile.close()

    def do_POST(self):
        uploading = False
        pathz = (self.path)
        pathz = unquote(pathz)
        contenttype = ""
        if ("upload" in pathz):
            contenttype = "text/html"
            uploading = True
        self.send_response(200)
        self.send_header("x-content-type-options", "nosniff")
        self.send_header("Content-type", contenttype)
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.end_headers()
        # print(self.wfile)
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        try:
            self.wfile.write(
                ("<script>window.close();</script><p><b>results for path: %s</b></p>" % self.path).encode("utf-8"))
            self.wfile.write("<html><head><title>Test!</title></head>".encode("utf-8"))
            self.wfile.write("<body>this was a post request</p>".encode("utf-8"))
        except KeyboardInterrupt:
            self.wfile.write(("<p>Error getting: %s</p>" % self.path).encode("utf-8"))

        self.wfile.write("</body></html>".encode("utf-8"))
        if (uploading):
            try:
                content_len = int(self.headers.get('Content-Length'))
                post_body = self.rfile.read(content_len)
                encoding = 'utf-8'
                uploaded_text_file = post_body.decode(encoding)
                uploaded_text_file = uploaded_text_file.replace(">", "&gt;")
                uploaded_text_file = uploaded_text_file.replace("<", "&th;")
                uploaded_text_file = uploaded_text_file.replace("\"", "&quot;")
                uploaded_text_file = uploaded_text_file.replace("\r", " ")
                uploaded_text_file = uploaded_text_file.replace("\n", " ")
                '''
                filename_start = uploaded_text_file.find('filename="')
                filename = uploaded_text_file[(filename_start+10):None]
                filename_end = filename.find('"')
                filename = filename[0:filename_end]
                '''
                filename = "download.txt"
                filepart1 = '''<!DOCTYPE html>
                                <html>
                                <title>W3.CSS</title>
                                <meta name="viewport" content="width=device-width, initial-scale=1">
                                <link rel="stylesheet" href="/w3.css">
                                <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
                                <body>
                                <div class="w3-container">
                                  <h2>W3.CSS Modal</h2>
                                  <p>this is a free sample modal our company is giving out</p>
                                  <button onclick="document.getElementById('id01').style.display='block'" class="w3-button w3-black">Open Modal</button>
                                  <div id="id01" class="w3-modal">
                                    <div class="w3-modal-content">
                                      <div class="w3-container">
                                        <span onclick="myFunction()" class="w3-button w3-display-topright">&times;</span>
                                        <p>Some text. Some text. Some text.</p>
                                        <p>Some text. Some text. Some text.</p>
                                      </div>
                                    </div>
                                  </div>
                                </div>
                                <script>
                                function myFunction() {
                                    stylez = "";
                                    try {
                                      stylez = eval("'''
                filepart2 = '''");
                                } catch (error) {
                                  console.error(error);
                                  // expected output: ReferenceError: nonExistentFunction is not defined
                                  // Note - error messages will vary depending on browser
                                }
                                document.getElementById('id01').style.display=stylez;
                            }
                            </script>   
                            </body>
                            <!--DO NOT REMOTE THE LINE BELOW! - Save the HTTP headers to be used on download below, we'll search for "Content-Disposition" in the file then parse it so we dont have to make another config file-->
                            <!--Content-Disposition: attachment; filename="default.txt"-->
                            </html> '''
                f = open(filename, "w")
                f.write(filepart1 + uploaded_text_file + filepart2)
                f.close()
            except:
                self.wfile.write(("<p>file upload failed").encode("utf-8"))
                print("file upload failed!")

        self.wfile.close()


try:
    server = http.server.HTTPServer(('localhost', PORT), MyHandler)
    print('Started http server')
    server.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down server')
    server.socket.close()
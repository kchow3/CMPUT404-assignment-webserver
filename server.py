#  coding: utf-8
import SocketServer

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

from os import curdir

class MyWebServer(SocketServer.BaseRequestHandler):

    HTTP_OK = "HTTP/1.1 200 OK \r\n"
    HTTP_NOT_FOUND = "HTTP/1.1 404 Not Found \r\n"
    HEADER_CONTENT_TYPE = "Content-Type: "
    HEADER_CONTENT_LENGTH = "Content-Length: "
    HEADER_CLOSE = "Connection: close \r\n"
    CRLF = "\r\n"

    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.httpGET()
        self.sendall(self.response)

    def httpGET(self):
        self.parseRequest()
        try:
            if(self.path.endswith('/')):
                self.file = open(curdir + '/www' + self.path + 'index.html', 'r').read()
                self.type = 'text/html'
            elif(self.path.endswith('.html')):
                self.file = open(curdir + '/www' + self.path, 'r').read()
                self.type = 'text/html'
            elif(self.path.endswith('.css')):
                self.file = open(curdir + '/www' + self.path, 'r').read()
                self.type = 'text/css'
            else:
                self.request.sendall('HTTP/1.1 404 Not Found\r\n')
            self.length = len(self.file)
            self.buildResponse()
        except:
            self.request.sendall('HTTP/1.1 404 Not Found\r\n')

    def parseRequest(self):
        lines = str.splitlines(self.data)
        line1 = lines[0].split()
        self.path = line1[1]

    def buildResponse(self):
        self.response += HTTP_OK + HEADER_CONTENT_LENGTH + self.length + CRLF + HEADER_CONTENT_TYPE + self.type + CRLF + HEADER_CLOSE + CRLF + self.file

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

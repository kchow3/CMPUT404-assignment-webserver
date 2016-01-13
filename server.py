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
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.length = len(self.data)
        print ("Got a request of: %s\n" % self.data)
        self.parseRequest()
        if(self.path.endswith('/')):
            response = open(curdir + '/www' + self.path + 'index.html', 'r')
            self.request.sendall('HTTP/1.1 200 OK\r\n Content-Type: text/html\r\n Content-Length: ' + str(72 + self.length + len(response.read())) + '\r\n\r\n' + response.read())
        else:
            try:
                if(self.path.endswith('.html')):
                    response = open(curdir + '/www' + self.path, 'r')
                    self.request.sendall('HTTP/1.1 200 OK\r\n Content-Type: text/html\r\n Content-Length: ' + str(72 + self.length + len(response.read())) + '\r\n\r\n' + response.read())
                elif(self.path.endswith('.css')):
                    response = open(curdir + '/www' + self.path, 'r')
                    self.request.send('HTTP/1.1 200 OK\r\n Content-Type: text/css\r\n Content-Length: ' + str(72 + self.length + len(response.read())) + '\r\n\r\n' + response.read())
                else:
                    self.request.sendall('HTTP/1.1 404 Not Found\r\n')
            except:
                self.request.sendall('HTTP/1.1 404 Not Found\r\n')

    def parseRequest(self):
        lines = str.splitlines(self.data)
        line1 = lines[0].split()
        self.path = line1[1]

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

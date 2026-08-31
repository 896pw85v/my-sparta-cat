# Do I need framework for this? 
# Frontend, no
# Backend, maybe
# problem is I don't know yet what each part needs to do

import http.server
import json
import mb_lib

class MyHandler(http.server.BaseHTTPRequestHandler): 
    def do_POST(self):
        print(f'from: {self.client_address}')
        # int(), read exact length, load json to py objects
        raw = self.rfile.read(int(self.headers.get('Content-length')))
        body = json.loads(raw)
        for k, v in body.items(): 
            print(f'{k} -> {v}')
        print('sending something back')
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers() # must have blank line
        self.wfile.write(json.dumps(mb_lib.get_images()).encode('utf-8'))




print("Server starting on http://localhost:8000")
server = http.server.HTTPServer(('localhost',8000), MyHandler)
server.serve_forever()
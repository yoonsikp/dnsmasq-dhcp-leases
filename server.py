"""
An HTTP server to display current dnsmasq DHCP leases.
"""
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
# Server settings
# For port 80, which is normally used for a http server, you need root access
PORT = 80


class HTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Handles our HTTP requests
    """
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        lease_file = open('/var/lib/misc/dnsmasq.leases', 'r')
        space = '&nbsp;'
        message = '<!DOCTYPE html><html><body><h1>DHCP Leases</h1>\n<code>' + \
                  'Expiry' + space * 4 + \
                  'MAC Address' + space * 8 + \
                  'IP Address' + space * 7 + \
                  'Hostname</br>'

        for line in lease_file.readlines():
            columns = line.split()
            columns[0] = time.strftime('%H:%M:%S',
                                       time.localtime(int(columns[0])))
            lease = ''
            for i in range(len(columns) - 1):
                lease += columns[i] + space * 2
                if i == 2:
                    lease += space * (15 - len(columns[2]))
            message += '</br>\n' + lease
        lease_file.close()
        message += '</code></body></html>'
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


print('starting server...')
server_address = ('', PORT)
httpd = HTTPServer(server_address, HTTPRequestHandler)
print('running server...')
httpd.serve_forever()

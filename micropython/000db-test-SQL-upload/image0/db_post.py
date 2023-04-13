# from netcheck import wait_for_networking
import socket

HTTP_REQUEST = 'GET /{path} HTTP/1.0\r\nHost: {host}\r\n\r\n'
HTTP_PORT = 80
BUFFER_SIZE = 1024

def build_val_str(vals):
    """take a dictionary of values and convert to HTML value string"""

    vstr = '&'.join([f'{key}={value}' for key, value in sorted(vals.items())])    
    print(f'FINAL VSTR:{vstr}')
    return vstr

def parse_url(url):
    return url.replace('http://', '').split('/', 1)

def get_ip(host, port=HTTP_PORT):
    addr_info = socket.getaddrinfo(host, port)
    return addr_info[0][-1][0]

def fetch(url):
    host, path = parse_url(url)
    print(f'HOST:{host}, PATH:{path}')
    ip = get_ip(host)
    sock = socket.socket()
    sock.connect((ip, 80))
    request = HTTP_REQUEST.format(host=host, path=path)
    sock.send(bytes(request, 'utf8'))
    response = b''
    while True:
        chunk = sock.recv(BUFFER_SIZE)
        if not chunk:
            break
        response += chunk
    sock.close()
    body = response.split(b'\r\n\r\n', 1)[1]
    return str(body, 'utf8')
try:
    import usocket as socket
except:
    import socket

import machine

def web_page():
    # display the true value of the led
    # ON = value 0, OFF = value 1
    if led.value() == 0:
        gpio_state="ON"
    else:
        gpio_state="OFF"

    html = """<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css"
     integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
        html {
            font-family: Arial;
            display: inline-block;
            margin: 0px auto;
            text-align: center;
        }

        .button {
            background-color: #ce1b0e;
            border: none;
            color: white;
            padding: 16px 40px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }

        .button1 {
            background-color: #000000;
        }
    </style>
</head>

<body>
    <h2>ESP MicroPython Web Server</h2>
    <p>LED state: <strong>""" + gpio_state + """</strong></p>
    <p>
        <i class="fas fa-lightbulb fa-3x" style="color:#c81919;"></i>
        <a href=\"?led_on\"><button class="button">LED ON</button></a>
    </p>
    <p>
        <i class="far fa-lightbulb fa-3x" style="color:#000000;"></i>
        <a href=\"?led_off\"><button class="button button1">LED OFF</button></a>
    </p>
</body>

</html>"""
    return html


CONTENT = b"""\
HTTP/1.0 200 OK

Hello #%d from MicroPython!
"""


def main(micropython_optimize=False):
    s = socket.socket()

    # Binding to all interfaces - server will be accessible to other hosts!
    ai = socket.getaddrinfo("0.0.0.0", 666)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:666/")

    counter = 0
    while True:
        try:
            res = s.accept()
            s.settimeout(10)
            client_sock = res[0]
            client_addr = res[1]
            print("Client address:", client_addr)
            print("Client socket:", client_sock)

            # if not micropython_optimize:
            #     # To read line-oriented protocol (like HTTP) from a socket (and
            #     # avoid short read problem), it must be wrapped in a stream (aka
            #     # file-like) object. That's how you do it in CPython:
            #     client_stream = client_sock.makefile("rwb")
            # else:
            #     # .. but MicroPython socket objects support stream interface
            #     # directly, so calling .makefile() method is not required. If
            #     # you develop application which will run only on MicroPython,
            #     # especially on a resource-constrained embedded device, you
            #     # may take this shortcut to save resources.
            client_stream = client_sock # micropython optimized

            print("Request:")
            req = client_stream.readline()
            print(f'first reg: {req}')
            while True:
                h = client_stream.readline()
                if h == b"" or h == b"\r\n":
                    break
                print(f'h: {h}')
            # client_stream.write(CONTENT % counter)
            CONTENT = web_page()
            CONTENT = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n' + CONTENT
            client_stream.write(CONTENT)
            client_stream.close()
            client_sock.close()
            # if not micropython_optimize:
            #     client_sock.close()
            counter += 1
            print()
        except OSError as e:
            # machine.reset()
            client_sock.close()
            print(f'OSError: Connection closed {e}')

main()

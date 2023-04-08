try:
    import usocket as socket
except:
    import socket

import machine
import uerrno
import db_post

def web_page(db_str, mytime):
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
    <p>
        <p>DATABASE - TIME: """ + mytime + "<strong> SQL: " + db_str + """</strong></p>
</body>

</html>"""
    return html


CONTENT = b"""\
HTTP/1.0 200 OK

Hello #%d from MicroPython!
"""


def main():
    led_state = "ON" # initialize state


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
            s.settimeout(15)
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
            req = client_stream.readline() # read first line for processing args

            print(f'-first reg: {req}')         
            led_on = str(req).find('led_on')
            led_off = str(req).find('led_off')
            print(f'led_on: {led_on} led_off: {led_off}')
            
            while True: # read all of the response line by line
                h = client_stream.readline()
                if h == b"" or h == b"\r\n":
                    break
                print(f'h: {h}')


            valid_state = True
            if led_on > 0: # this is brute force searching for parameters
                print('---LED ON -> GPIO2')
                # led_state = "ON"
                led.off()
            elif led_off > 0:
                print('---LED OFF -> GPIO2')
                # led_state = "OFF"
                led.on()
            else:
                valid_state = False
                print('-----LED STATE NOT PASSED-----')

            db_response = 'No Valide Values'
            if valid_state: # initial load, or no valid params, don't do anything
                # send data to database
                db_response = 'http://biosphere2.000webhostapp.com/dbwrite.php?val1=' + str(float(led_on)) + '&val2=' + str(float(led_off))
                print(f'{db_response}\n')
                html = db_post.fetch(db_response)
                print('------------------------')
                print(html)
                print('------------------------')

            # client_stream.write(CONTENT % counter)
            current_time = time.localtime()
            formatted_time = "{:02d}/{:02d}/{} {:02d}:{:02d}:{:02d} ".format(current_time[2], current_time[1], current_time[0], current_time[3], current_time[4], current_time[5])           
            CONTENT = web_page(db_response, formatted_time)
            CONTENT = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n' + CONTENT
            client_stream.write(CONTENT)
            client_stream.close()
            client_sock.close()
            counter += 1
            print(counter)
            print('')


        except OSError as e:
            if e.args[0] == uerrno.ETIMEDOUT: # standard timeout is okay, ignore it
                print("ETIMEDOUT found") # timeout is okay, ignore it
                pass
            else: # general case, close the socket and continue processing, prevent hanging
                client_sock.close()
                print(f'OSError: Connection closed {e}')

main()

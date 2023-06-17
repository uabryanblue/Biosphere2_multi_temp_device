"""
 Biosphere 2 remote sensing project
 Bryan Blue
 bryanblue@arizona.edu
 Spring 2023
"""

import db_post  # code module that handles communiction with remote MySQL database
import machine
import uerrno  # error trapping and code values

# try to use machine native socket if not use library
try:
    import usocket as socket
except:
    import socket

import logger
logger.get_storage_stats('//')
for i in range(1,100):
    # print(f"loop: {i}")
    logger.write_log(f"{i},this,is,12,2.3,fa,la,la", conf.LOG_FILENAME)
    # logger.write_log('that,is,12,2.3,fa,la,la', conf.LOG_FILENAME)
    # logger.write_log('them,is,12,2.3,fa,la,la', conf.LOG_FILENAME)

logger.get_storage_stats('//')
# logger.dump_log(conf.LOG_FILENAME)

def web_page(db_str, mytime, html_resp):
    """generate a canned HTML response
    Display: buttons for on/off control
    The current state of the led light
    Current date/time of the request"""

    # display the true value of the led
    # ON = when led is physically 0
    # OFF = when led is physically 1
    if led.value() == 0:
        gpio_state = "ON"
    else:
        gpio_state = "OFF"

    # web page that is returned from server with variable information

    html = (
        """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>"""
        + conf.MYNAME
        + """<br>"""
        + conf.MYID
        + """</title>
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
        <main>
            <h2>"""
        + conf.MYNAME
        + """</h2>
            <h3>"""
        + conf.AUTHOR
        + """</h3>
        </main>
        <p><a href="https://www.lazuline.us"><img src="https://ci3.googleusercontent.com/mail-sig/AIorK4wbOK2u0GFF36ks7HM8C8S9pPd5X2BLfgBcLQSFolKbn7AX8B5hEYXj-6_bj1P93u4I6s6KEqEgTKbMEbZfjt_-ws2JTUcIy6Yqy-CpgQ" style="width:50px;height:50px;"></a></p>
        <p>LED state: <strong>"""
        + gpio_state
        + """</strong></p>
        <p>
            <!-- i class="fas fa-lightbulb fa-3x" style="color:#c81919;"></i> -->
            <a href="?led_on"><button class="button">LED ON</button></a>
        </p>
        <p>
            <!-- i class="far fa-lightbulb fa-3x" style="color:#000000;"></i> -->
            <a href="?led_off"><button class="button button1">LED OFF</button></a>
        </p>
        <p>
        <p> CURRENT TIME: """
        + mytime
        + "<strong> <br>SQL: "
        + db_str
        + """</strong></p>
        <p> DATABASE RESPONSE: """
        + html_resp
        + """</p>
    </body>
</html>"""
    )
    return html


def main():
    # initialize state of display variable
    led_state = "ON"

    # create a new socket to display web page
    s = socket.socket()
    # localhost has to be 0.0.0.0 and port 667 (change to any valid port you wish to use)
    ai = socket.getaddrinfo("0.0.0.0", conf.PORT)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://{addr}")

    counter = 0
    while True:
        try:
            res = s.accept()
            s.settimeout(5)
            client_sock = res[0]
            client_addr = res[1]
            print("Client address:", client_addr)
            print("Client socket:", client_sock)

            client_stream = client_sock
            print("Request:")
            req = client_stream.readline()  # read first line for processing args

            print(f"-first reg: {req}")
            led_on = str(req).find("led_on")
            led_off = str(req).find("led_off")
            print(f"led_on: {led_on} led_off: {led_off}")

            while True:  # read all of the response line by line
                sr = client_stream.readline()
                if sr == b"" or sr == b"\r\n":
                    break
                print(f"--sr: {sr}")

            valid_state = True
            if led_on > 0:  # this is brute force searching for parameters
                print("---LED ON -> GPIO2")
                # led_state = "ON"
                led.off()
            elif led_off > 0:
                print("---LED OFF -> GPIO2")
                # led_state = "OFF"
                led.on()
            else:
                valid_state = False
                print("-----LED STATE NOT PASSED-----")

            db_response = "No Valide Values"
            if valid_state:  # initial load, or no valid params, don't do anything
                # send data to database
                # TODO: break this into variable number of parameters
                vars = {}
                vars["val1"] = float(led_on)
                vars["val2"] = float(led_off)
                val_str = db_post.build_val_str(vars)
                db_response = (
                    conf.DB_URL + "?" + val_str
                )
                # db_response = """https://lazuline.us/blog/f/rescue-orchid-3?and=4"""

                # + str(float(led_on))
                # + "&val2="
                # + str(float(led_off))
                # )
                print(f"SENDING: {db_response}\n")
                html_resp = db_post.fetch(db_response)
                # TODO this response chechking needs to  made into a function in db_post.py
                # standard URL response codes are not sufficient
                if html_resp.find("ERROR") == -1: # we did not find error in the response, assume ok
                    html_resp = "RESPONSE OK"
                print("------------------------")
                print(html_resp)
                print("------------------------")

            # client_stream.write(CONTENT % counter)
            current_time = time.localtime(time.time())  # + conf.UTC_OFFSET)
            # formatted_time = f"{current_time[2]:02d}"
            formatted_time = "{:02d}/{:02d}/{} {:02d}:{:02d}:{:02d} ".format(
                current_time[2],
                current_time[1],
                current_time[0],
                current_time[3],
                current_time[4],
                current_time[5],
            )
            CONTENT = web_page(db_response, formatted_time, html_resp)
            CONTENT = "HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n" + CONTENT
            client_stream.write(CONTENT)
            client_stream.close()
            client_sock.close()
            counter += 1
            print(counter)
            print("")

        except OSError as e:
            if e.args[0] == uerrno.ETIMEDOUT:  # standard timeout is okay, ignore it
                print("ETIMEDOUT found")  # timeout is okay, ignore it
            else:  # general case, close the socket and continue processing, prevent hanging
                client_sock.close()
                print(f"OSError: Connection closed {e}")


main()

"""
 database query and communication
"""
import socket

HTTP_REQUEST = "GET /{path} HTTP/1.0\r\nHost: {host}\r\n\r\n"
HTTP_PORT = 80
BUFFER_SIZE = 1024


def build_val_str(vals):
    """take a dictionary of values and convert to HTML value string"""

    vstr = "&".join([f"{key}={value}" for key, value in sorted(vals.items())])
    print(f"FINAL VSTR:{vstr}")
    return vstr


def parse_url(url):
    """break url into host and remaining path"""

    # this could be refactored
    g = url.split('/',3)[2:4]
    return g


def get_ip(host, port=HTTP_PORT):
    """the IP has to be obtained for the rest of the socket calls"""

    addr_info = socket.getaddrinfo(host, port)
    return addr_info[0][-1][0]

def check_return_code(chunk):
    # return the html response code, the 2nd string space delimited
    return chunk.split(' ',2)[1]

def fetch(url):
    """build the final url that sends data to the remote database"""
    # TODO this needs refactored, much of the print statemets can be removed
    # PHP pages should return status based on sucess or failure to update the DB
    try:
        print("++++++++++++++++++BEGIN++++++++++++++++++++++++++")
        host, path = parse_url(url)
        print(f"HOST:{host}, PATH:{path}")
        ip = get_ip(host)
        sock = socket.socket()
        sock.connect((ip, 80))
        print(f"connected to {ip}")
        request = HTTP_REQUEST.format(host=host, path=path)
        if sock.send(bytes(request, "utf8")):
            print(f"sent successfully: {request}")
        response = b"" # initialize binary variable to hold response
        
        chunk = sock.recv(BUFFER_SIZE)
        code = check_return_code(str(chunk))
        try:
            assert (code < "400") # anything below 400 is not a clienter or server error
        except:
            sock.close()
            return str(f"ERROR CODE: {code}", "utf8")

        print(f'******************* found code:{code}:')
        print(f"chunk: {chunk}")
        response = chunk # comaptibility for the dump loop below
        
        # causes memeory errors if the entire response is read in at once
        # rework, but the response is not needed
        # while chunk:
        #     chunk = sock.recv(BUFFER_SIZE)
        #     print(f"================= NEXTchunk: {chunk}")
        #     # if not chunk:
        #     #     break
        #     response += chunk
        sock.close()

        print(f"final resonponse to split {response}")
        body = response.split(b"\r\n", 1)[1]
        print(body)
        print("++++++++++++++++++++END++++++++++++++++++++++++")
        return str(body, "utf8")

    except (NameError, TypeError) as error:
        print(f"general error handling: {error}")


    except MemoryError as e:
        print(f"!!!!!!!! 1 error detected: {e}     {e.args[0]}")
        sock.close() # should use with statement
        return "MEMORY ERROR"
    except OSError as e:
        print(f"!!!!!!!! 2 error detected: {e}     {e.args[0]}")
        sock.close() # should use with statement        
        # if e.args[0] == uerrno.ETIMEDOUT:  # standard timeout is okay, ignore it
        #     print("ETIMEDOUT found")  # timeout is okay, ignore it
        # else:  # general case, close the socket and continue processing, prevent hanging
        #     print("no error")
        #     # client_sock.close()
        #     # print(f"OSError: Connection closed {e}")
        return "OS ERROR"
    else:
        sock.close() # should use with statement
        print("++++++++++++++++++++ELSE++++++++++++++++++++++++")
        return "NOTHING HERE"




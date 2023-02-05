import socket
import sys
import os
import re
#we referred a lot to a tutorial on realpython (echoclient) to create the skeleton of our client
args=sys.argv[1]

if args[0].isdigit():
    redirects = int(args[0])
    args = args[1::]
else:
    redirects = -1

if redirects == 9:
    sys.exit(5)

if "https" == args[0:5]:
    sys.stderr.write("Tried to request https page.")
    sys.exit(1)
if "http://" not in args:
    sys.exit(4)

PORT = 80  
HOST= args[7::].split("/")[0]

if ":" in HOST:
    PORT = int(HOST.split(":")[1])
    HOST = HOST.split(":")[0]
    
PATH=  "".join(args[7::].split("/")[1::])
request =  f"GET /{PATH} HTTP/1.0\r\nHost:{HOST}\r\n\r\n".encode()
response = ""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(request)
    while True:
        recv = s.recv(1024)
        if recv == b'':
            break
        response += recv.decode(errors='ignore')
    if "<" in response:
        body = response[response.index("<")::]
    else:
        if int(response[9:12]) == 403:
            sys.stderr.write(response)
        sys.exit(6)
    if int(response[9:12]) > 300 and int(response[9:12]) < 400:
        new_loc = re.findall("Location: .*", response)[0][10:-1]
        sys.stderr.write(f" Redirected to: {new_loc} ")
        os.system(f"python3 http_client.py {redirects+1}{new_loc}")
    elif int(response[9:12]) >= 400:
        content_header = re.findall("Content-Type: .*", response)
        if "text/html" in content_header[0]:
            print(body)
        else:
            sys.exit(3)
        sys.exit(2)
    else:
        content_header = re.findall("Content-Type: .*", response)
        if "text/html" in content_header[0]:
            print(body)
        else:
            sys.exit(3)
        sys.exit(0)

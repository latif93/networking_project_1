import socket
import os
import sys 
#we referred a lot to a tutorial on realpython (echoserver) to create the skeleton of our server
HOST = "localhost" 
args=sys.argv[1]
PORT = int(args)
data = ""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn = s.accept()[0] 
    with conn:
        data = conn.recv(1024).decode()
        filename = data.split(" ")[1][1::] 
        body = ""
        content = ""
        if os.path.exists(filename): 
            if ".htm" not in filename: 
                content = "HTTP/1.0 403 Forbidden"
            else:
                txt = ""
                content_length = 0
                with open(filename) as f:
                    txt = f.read()
                    txt = txt[txt.index("<")::]
                    content_length = len(txt.encode())
                content = f"HTTP/1.0 200 OK\r\nContent-Length: {content_length}\r\nContent-Type: text/html\r\n\r\n{txt}"
        else:
            body = "<!DOCTYPE HTML PUBLIC '-//IETF//DTD HTML 2.0//EN'>\n<html><head>\n<title>404 Not Found</title>\n</head><body>\n<p>The requested URL was not found on this server.</p>\n</body></html>"
            content_length = len(body.encode()) 
            content = f"HTTP/1.0 404 Not Found\r\nContent-Length: {content_length}\r\nContent-Type: text/html\r\n\r\n{body}"
        conn.sendall(content.encode())

import socket
import os
import sys 
import datetime
from  datetime import date
from  datetime import time
from datetime import timezone
import time as t

HOST = "localhost" 
args=sys.argv[1]
PORT = int(args)
data = ""
weekday_dict = {1: "Mon", 2: "Tues", 3: "Wed", 4: "Thurs", 5: "Fri", 6: "Sat", 7: "Sun"}
month_dict = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn = s.accept()[0] #A
    with conn:
        data = conn.recv(1024).decode()
        filename = data.split(" ")[1][1::] #B
        body = ""
        content = ""
        if os.path.exists(filename): 
            dt = date.today()
            utc_now = datetime.datetime.now(timezone.utc)
            if ".htm" not in filename: #C
                content = f"HTTP/1.1 403 Forbidden\nDate: {weekday_dict[utc_now.isoweekday()]}, {dt.day} {month_dict[dt.month]} {dt.year} {time(11, 34, 56)} GMT"
            else:
                lastmtime = t.ctime(os.path.getmtime(filename))
                txt = ""
                content_length = 0
                with open(filename) as f:
                    txt = f.read()
                    txt = txt[txt.index("<")::]
                    content_length = len(txt.encode('utf-8'))
                content = f"HTTP/1.1 200 OK\nDate: {weekday_dict[utc_now.isoweekday()]}, {dt.day} {month_dict[dt.month]} {dt.year} {time(11, 34, 56)} GMT\nServer: CarryBits Server\nLast Modified: {lastmtime}\nAccept-Ranges: bytes\nContent-Length: {content_length}\nContent-Type: text/html; charset=UTF-8\n\n{txt}"
        else:
            body = "<!DOCTYPE HTML PUBLIC '-//IETF//DTD HTML 2.0//EN'>\n<html><head>\n<title>404 Not Found</title>\n</head><body>\n<p>The requested URL was not found on this server.</p>\n</body></html>"
            content_length = len(body.encode('utf-8')) #should be 196
            content = f"HTTP/1.1 404 Not Found\nDate: {weekday_dict[utc_now.isoweekday()]}, {dt.day} {month_dict[dt.month]} {dt.year} {time(11, 34, 56)} GMT\nServer: CarryBits Server\nContent-Length: {content_length}\nContent-Type: text/html; charset==iso-8859-1\n\n{body}"
        conn.sendall(content.encode())
"""
HTTP/1.1 200 OK
Date: Sat, 21 Jan 2023 00:04:54 GMT
Server: Apache/2.4.52 () OpenSSL/1.0.2k-fips PHP/5.4.16
Upgrade: h2,h2c
Connection: Upgrade
Last-Modified: Tue, 07 Jan 2020 23:59:54 GMT
ETag: "65-59b9592825280"
Accept-Ranges: bytes
Content-Length: 101
Content-Type: text/html; charset=UTF-8
"""
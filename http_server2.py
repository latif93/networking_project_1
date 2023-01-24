import socket
import os
import sys 
import datetime
from  datetime import date
from  datetime import time
from datetime import timezone
import time as t
import select
import queue

HOST = "localhost" 
args=sys.argv[1]
PORT = int(args)
data = ""
weekday_dict = {1: "Mon", 2: "Tues", 3: "Wed", 4: "Thurs", 5: "Fri", 6: "Sat", 7: "Sun"}
month_dict = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setblocking(0)
    s.bind((HOST, PORT))
    s.listen()
    read_list = [s]
    open_conn = []
    message_queues = {}
    while read_list: 
        print(read_list)
        readable, writable, exceptional = select.select(read_list, open_conn, read_list)
        for sock in readable:
            if sock == s:
                conn, addr = sock.accept()
                conn.setblocking(0)
                read_list.append(conn)
                message_queues[conn] = queue.Queue()
            else:
                data = sock.recv(1024)
                if data:
                    message_queues[sock].put(data)
                    if sock not in open_conn:
                        open_conn.append(sock)
                else:
                    if sock in open_conn:
                        open_conn.remove(sock)
                    read_list.remove(sock)
                    sock.close()
                    del message_queues[sock]
        for sock in writable:
            try:
                next_msg = message_queues[sock].get_nowait()
            except queue.Empty:
                open_conn.remove(sock)
            else:
                sock.send(next_msg)
        for sock in exceptional:
            read_list.remove(sock)
            if sock in open_conn:
                open_conn.remove(sock)
            s.close()
            del message_queues[sock]
"""
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
                open_conn.pop(conn)
"""
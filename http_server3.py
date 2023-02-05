import socket
import sys
import json
import re
HOST = "moore.wot.eecs.northwestern.edu"
args=sys.argv[1]
PORT = int(args)
data = ""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn = s.accept()[0] 
    with conn:
        data = conn.recv(1024).decode()
        if "/product" not in data:
            content = "HTTP/1.0 404 Not Found"
        else:
            eql_count = 0
            for c in data:
                if c == "=":
                    eql_count += 1
            query = data.split("?")[1]
            extract_operands_pattern = "[-]?[0-9]*[\.]?[0-9]*"
            operand_lst = re.findall(extract_operands_pattern, query)
            operand_lst = [x for x in operand_lst if x != ""]
            if len(operand_lst) != eql_count or eql_count == 0:
                content = "HTTP/1.0 400 Bad Request"
            else:
                product = 1.0
                for operand in operand_lst:
                    product *= float(operand)
                if product > (2 ** 31 - 1): 
                    product = "inf"
                else: 
                    if product < -1*(2 ** 31 - 1):
                        product = "-inf"
                content_length = 0
                res_dict = {"operation": "product", "operands": operand_lst, "result": product}
                json_response = json.dumps(res_dict, indent = 2) 
                content_length = len(json_response.encode())
                content = f"HTTP/1.0 200 OK\r\nContent-Length: {content_length}\r\nContent-Type: application/json\r\n\r\n{json_response}"       
        conn.sendall(content.encode())

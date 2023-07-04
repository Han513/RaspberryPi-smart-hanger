import socket
import ssl
import requests
import random
import time

HOST = '192.168.50.48'
PORT = 5288

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = ssl.wrap_socket(s, keyfile='./privkey.pem',
                    certfile='./certificate.pem', server_side=True)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(60)

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')


def send_data_to_google_sheet(date, temp, humi, ps):
    url = "https://script.google.com/a/nkust.edu.tw/macros/s/AKfycbxK9XytTkBzmjzObxMrlNjpdguXehZ25RoKkV_1/exec"
    payload = {'date': date, 'temp': temp, 'humi': humi, 'ps': ps}
    resp = requests.get(url, params=payload)
    print(f"Response of result: {resp.text}")


while True:
    try:
        conn, addr = s.accept()
        print('connected by ' + str(addr))
        while True:
            indata = conn.recv(1024)
            data = indata.decode()
            if data == 'close':  # connection closed
                conn.close()
                print('client closed connection.')
                break
            print('recv:' + data)
            date = data[9:36]
            temp = data[53:58]
            humi = data[71:76]
            ps = 'Your clothes is wet now'
            if data == 'You can collect your clothes!!!':
                ps = 'You can collect your clothes!!!'
            elif data == 'You can already check your clothes!!!':
                ps = 'You can already check your clothes!!!'
            send_data_to_google_sheet(date, temp, humi, ps)
            # time.sleep(2)

            outdata = 'data:' + data
            conn.send(outdata.encode())

    except KeyboardInterrupt:
        break

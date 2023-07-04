import socket
import RPi.GPIO as GPIO
import time
import datetime
import dht11
import ssl
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

HOST = '192.168.1.146'
PORT = 5288

msg = MIMEMultipart()
msg['From'] = 'henry88699@gmail.com'
msg['To'] = 'C107156106@nkust.edu.tw'
msg['Subject'] = '智能衣架-衣服狀況'
message = ' 衣服已經可以收了喔 ~ '
msg.attach(MIMEText(message))

mailserver = smtplib.SMTP('smtp.gmail.com', 587)
mailserver.ehlo()
mailserver.starttls()
mailserver.ehlo()
mailserver.login('henry88699@gmail.com', 'apple8812601')

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

instance = dht11.DHT11(pin=7)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = ssl.wrap_socket(s, keyfile='./privkey.pem',
                    certfile='./certificate.pem', server_side=False)
s.connect((HOST, PORT))

d = {}
ifcollect = 0
yes = "You can collect your clothes!!!"
notyet = "You can already check your clothes!!!"


def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=payload)
    return r.status_code


while True:
    try:
        ret = instance.read()
        if ret.is_valid():
            print("----------------------------------------------------------------")
            d['time'] = str(datetime.datetime.now())
            d['temperature'] = ret.temperature
            d['humidity'] = ret.humidity
            print('send: ' + str(d))
            s.send(str(d).encode())
            message = '我現在人不在家，可以幫我收個衣服嗎，衣架子上有亮紅燈的衣服，放在旁邊的藍色桶子內就可以了'
            token = 'ix61MuxBTakiZi8tKIRUojMCMoGdIKTrW8twF8ceMHy'
            ifcollect += 1
            if ifcollect <= 5:
                ifcollect = 0
                lineNotifyMessage(token, message)
                print('send to group success')
            if ret.humidity <= 50.0:
                mailserver.sendmail('henry88699@gmail.com',
                                    'C107156106@nkust.edu.tw', msg.as_string())
                mailserver.quit()
                print(yes)
                s.send(yes.encode())
                s.send('close'.encode())
                break
            elif 50.1 <= ret.humidity <= 60.0:
                print(notyet)
                s.send(notyet.encode())
            indata = s.recv(1024)
            time.sleep(2)
            if len(indata) == 0:  # connection closed
                s.close()
                mailserver.quit()
                print('server closed connection.')
                break
            print('recv: ' + indata.decode())
    except KeyboardInterrupt:
        raise

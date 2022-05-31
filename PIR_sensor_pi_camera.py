from picamera import PiCamera
import smtplib
import time
from time import sleep
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import RPi.GPIO as GPIO


toaddr = 'sikkerhed1000@gmail.com'
me = 'hovsatest@gmail.com'
Subject='Indbrud i bodega!'

GPIO.setmode(GPIO.BCM)

P=PiCamera()
P.resolution= (1024,768)
P.start_preview()
    
GPIO.setup(23, GPIO.IN)
while True:
    if GPIO.input(23):
        print("Bevægelse!...")
        #camera varmer op
        time.sleep(2)
        P.capture('movement.jpg')
        time.sleep(10)
        subject='Sikkerhedsalarm!'
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = toaddr
        
        fp= open('movement.jpg','rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(user = 'hovsatest',password='ztpfuostyyncsktw')
        server.send_message(msg)
        server.quit()
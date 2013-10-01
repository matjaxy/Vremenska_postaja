import datetime
import random
from alchemy_interface import *
import subprocess
import serial
import string
import math
import subprocess as subp

#data format
now = datetime.datetime.now()
date = now.date()
#time = now.time()
gpsout = []

port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=5.0)
rcv = str(port.read(250))
tmpgps = string.split(rcv,"\n")
for i in tmpgps:
    if "GPGGA" in i and len(i)>15:
        gps_out = i
print gps_out
#gps_out = "$GPGGA,183730,3907.356,N,12102.482,W,1,05,1.6,646.4,M,-24.1,M,,*75"
gps_list = gps_out.split(',')

session = Session()

#list of sensors
sensors =["temperature", "pressure", "moisture", "height"]

#gps coordinates
if len(gps_list[2]) < 2:
    x = "99.99"
    y = "99.99"
    h = "99.99"
    print "nogps"
else:
    x = float(gps_list[2])
    y = float(gps_list[4])
    h = float(gps_list[9])
    xsplit = str.split(str(x),".")
    ysplit = str.split(str(y),".")
    tmp = xsplit[0]
    secondsx = float(xsplit[1]) / (10**(len(xsplit[1])))
    secondsy = float(xsplit[1]) / (10**(len(ysplit[1])))
    if len(xsplit[0]) > 4:
        deg = tmp[:3]
        minutes = tmp[3:]
    else:
        deg = tmp[:2]
        minutes = tmp[2:]
    x = float(deg) + float(minutes)/60 + float(secondsx)/3600
    #print deg, minutes, seconds
    #print x
    
    #zemljepisna sirina
    tmp = ysplit[0]
    if len(ysplit[0]) > 4:
        deg = tmp[:3]
        minutes = tmp[3:]
    else:
        deg = tmp[:2]
        minutes = tmp[2:]
    y = float(deg) + float(minutes)/60 + float(secondsy)/3600
    #print deg, minutes, seconds
    #print y

    tmp = gps_list[1]

cajt = datetime.time((now.hour+2)%24, now.minute, now.second, now.microsecond)


#TEMPERATURA IN VLAGA
args = ['sudo', '/home/pi/Downloads/Adafruit-Raspberry-Pi-Python-Code/Adafruit_DHT_Driver/Adafruit_DHT', '11', '4']

proc = subprocess.Popen(args, stdout=subprocess.PIPE)
output = proc.stdout.read()
counter = 0
tmpmeasures = []
for splitter in output.split(" "):
    if counter == 10 or counter == 14:
         tmpmeasures.append(int(splitter))
    counter += 1
#print tmpmeasures[0],tmpmeasures[1]

#TEMPERATURA IN PRITISK

proc = subp.Popen(["python", "i2c.py"], stdout=subp.PIPE, stdin=subp.PIPE)
out = proc.stdout.readline()
out2 = out.split()
pritisk = int(round(float(out2[0])))
temperatura = int(round(float(out2[1])))


#for every sensor add a new line
for i in sensors:
    value = round(random.randint (1000, 2000), 1)

    ##################
    if i == "height":
        value = h
    if i == "temperature":
        value = temperatura
    if i == "moisture":
        value = tmpmeasures[1]
    if i == "pressure":
        value = pritisk


    new_entry = Measure(date, cajt, x, y, i, value)

    # Add the record to the session object
    session.add(new_entry)


# commit the record the database
session.commit()
session.close()

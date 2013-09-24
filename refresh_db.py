import datetime
import random
from alchemy_interface import *

#data format
now = datetime.datetime.now()
date = now.date()
#time = now.time()
gps_out = "$GPGGA,183730,3907.356,N,12102.482,W,1,05,1.6,646.4,M,-24.1,M,,*75"
gps_list = gps_out.split(',')

session = Session()

#list of sensors
sensors =["temperature", "pressure", "moisture", "height"]

#gps coordinates
x = float(gps_list[2])
y = float(gps_list[4])
h = float(gps_list[9])
tmp = gps_list[1]

#time strip
tmp2 = int(tmp[:2])
tmp3 = int(tmp[2:4])
tmp4 = int(tmp[4:])
TEMPORARY = random.randint (0, 999999)

cajt = datetime.time(tmp2, tmp3, tmp4, TEMPORARY)
#x = round (random.randrange(0, 1000) + random.random() , 3)
#y = round (random.randrange(0, 1000) + random. random() , 3)


#for every sensor add a new line
for i in sensors:
    value = round(random.randint (-10, 33), 1)*100

    ##################
    if i == "height":
        value = h


    new_entry = Measure(date, cajt, x, y, i, value)

    # Add the record to the session object
    session.add(new_entry)


# commit the record the database
session.commit()
session.close()

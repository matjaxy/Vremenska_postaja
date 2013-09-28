import cherrypy
import os.path
import datetime
from datetime import timedelta
from decimal import *
from mako.template import Template
from alchemy_interface import *
from cherrypy.lib.static import serve_file
import math
import itertools
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
session = Session()


mytemplate = Template(filename = 'index.htm')
#module_directory = '/home/pi/CherryPy-3.2.2/cherrypy/test')
#directories = "/home/pi/m/cherrypy/docs/index.html"
#collection_size = 500
#lookup = TemplateLookup(directories)

#l = {'valuem': Decimal('25.1'), 'valuep': Decimal('10.5'), 'coordinate_y': Decimal('14.50807'), 'coordinate_x': Decimal('46.056451'), 'valuet': Decimal('32.7'), 'time': datetime.time(17, 38, 43, 536627), 'date': datetime.date(2013, 2, 27), 'height': Decimal('646.4'), 'sensor': u'height'}
#2013-03-06 11:55:20,446 INFO sqlalchemy.engine.base.Engine (u'height', 1, 0) {'sensors': {u'pressure': Decimal('-6.3'), u'temperature': Decimal('4.5'), u'moisture': Decimal('19.8'), u'height': Decimal('646.4')}}


class Root(object):
    @cherrypy.expose
    def index(self):
        def sec_to_time(sec):

            days = sec / 86400
            sec -= 86400*days

            hrs = sec / 3600
            sec -= 3600*hrs

            mins = sec / 60
            sec -= 60*mins
            m = "{0}:{1}".format(hrs,mins)
            return m

		#dict za spremenljivke, ki gredo na stran
        l = {"sensors":{}}
        now = datetime.datetime.now()
        l["date"] = now.strftime('%d/%m/%Y')
        newnow = now + timedelta(hours=2)
        l["time"] = newnow.strftime('%H:%M')
        l["grafyear"] = now.year
        l["grafmonth"] = now.month - 2
        l["grafday"] = now.day

        #izpis tabele zadnjih vnosov
        sensor_types = session.query(distinct(Measure.sensor)).all()
        for i in sensor_types:
            qry = session.query(Measure).filter(Measure.sensor == i[0]).order_by(Measure.id.desc()).first()
            l["sensors"][qry.sensor] = qry.value
            l["gps_x"] = qry.gps_x
            l["gps_y"] = qry.gps_y
            l["date2"] = qry.date
            l["time2"] = qry.time
            l["displaygps"] = 1
            if int(qry.gps_x) == 99:
                l["displaygps"] = 0
            #qry = session.query(Measure).filter(Measure.sensor == 'temperature').order_by(Measure.time.desc()).limit(10)
            #print l
        
        #uptime
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds = uptime_seconds))
        l["uptime"] = uptime_string

        #all measures
        all = session.query(Measure).order_by(Measure.id.desc()).first()
        l["id_by_sensor"] = all.id / len(sensor_types)
        l["id"] = all.id
        first_time = session.query(Measure).order_by(Measure.id.asc()).first()
        l["first_time"] = datetime.datetime.combine(first_time.date,first_time.time)
        #
        ###branje podatkov za izris grafa
        #
        graftemperature = []
        grafpritiska = []
        grafvlage = []
        grafcasa = []
        strcasa = []
        
        tmpgraftemperature = []
        tmpgrafpritiska = []
        tmpgrafvlage = []
        tmpgrafcasa = []
        tmpcasvsekundah = []
        if l["id"] < 12*24:
            l["graf"] = 0
            l["graftemperature"] = graftemperature
            l["grafpritiska"] = grafpritiska
            l["grafvlage"] = grafvlage
            l["grafcasa"] = grafcasa
        else:
            l["graf"] = 1
            k = 12
        
        
        for sens2 in sensor_types:
            qry3 = session.query(Measure).filter(Measure.sensor == sens2[0]).order_by(Measure.id.desc()).limit(12*24)
            for k2 in qry3:
                if sens2[0] == 'temperature':
                    x = time.strptime(str(k2.time).split('.')[0],'%H:%M:%S')
                    total_sec = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
                    tmpgrafcasa.append(int(total_sec))
                    #print j.value
                    tmpgraftemperature.append(int(k2.value))
        
                if sens2[0] == 'pressure':
                    tmpgrafpritiska.append(int(k2.value))
        
                if sens2[0] == 'moisture':
                    tmpgrafvlage.append(int(k2.value))
        temp_by_12 = itertools.imap(None, *[iter(tmpgraftemperature)]*12)
        pres_by_12 = itertools.imap(None, *[iter(tmpgrafpritiska)]*12)
        moist_by_12 = itertools.imap(None, *[iter(tmpgrafvlage)]*12)
        time_by_12 = itertools.imap(None, *[iter(tmpgrafcasa)]*12)
        
        for x in range(24):
            k = temp_by_12.next()
            graftemperature.append(sum(k)/len(k))
        
        for x in range(24):
            k = pres_by_12.next()
            grafpritiska.append(sum(k)/len(k))
        
        for x in range(24):
            k = moist_by_12.next()
            grafvlage.append(sum(k)/len(k))
        
        for x in range(24):
            k = time_by_12.next()
            grafcasa.append(sum(k)/len(k))
        
        graftemperature = graftemperature[::-1]
        grafpritiska = grafpritiska[::-1]
        grafvlage = grafvlage[::-1]
        grafcasa = grafcasa[::-1]
        
        
        for i in range(24):
            strtime = sec_to_time(grafcasa[i])
            strcasa.append(strtime)
        
        l["graftemperature"] = list(graftemperature)
        l["grafpritiska"] = list(grafpritiska)
        l["grafvlage"] = list(grafvlage)
        l["grafcasa"] = strcasa






#################################################### 
        #branje zadnjih 5-ih za izris puscic 
        i = 5
        if l["id"] < i:
            i = l["id"]

        #
        ####tabele zadnjih vnosov
        #
        povtemperatura = []
        povpritisk = []
        povvlaga = []

        #init rezultatov
        smertemperature = 0
        smerpritiska = 0
        smervlage = 0
        


        for sens in sensor_types:
            qry2 = session.query(Measure).filter(Measure.sensor == sens[0]).order_by(Measure.id.desc()).limit(i)

            #seznam za  graf
            for j in qry2:

                #vnos valut v tabele
                if sens[0] == 'temperature':
                    #print j.value
                    povtemperatura.append(j.value)

                if sens[0] == 'pressure':
                    povpritisk.append(j.value)

                if sens[0] == 'moisture':
                    povvlaga.append(j.value)

        povprecnatemperatura = sum(povtemperatura)/len(povtemperatura)
        povprecnipritisk = sum(povpritisk)/len(povpritisk)
        povprecnavlaga = sum(povvlaga)/len(povvlaga)
        #print povprecnatemperatura, povprecnipritisk, povprecnavlaga


        for count in range(0,i):
            smertemperature += povtemperatura[count] - povprecnatemperatura
            #print smertemperature
            smerpritiska += povpritisk[count] - povprecnipritisk
            smervlage += povvlaga[count] - povprecnavlaga
        #print smertemperature, smerpritiska, smervlage
        l["smertemperature"] = smertemperature
        l["smerpritiska"] = smerpritiska
        l["smervlage"] = smervlage



		
		#izpis max
        for k in sensor_types:
        #print k[0]
            aver = session.query(func.avg(Measure.value).label('average')).filter(Measure.sensor==k[0])
            maxi = session.query(func.max(Measure.value).label('maximum')).filter(Measure.sensor==k[0])
            mini = session.query(func.min(Measure.value).label('minimum')).filter(Measure.sensor==k[0])

            #print "sensor "+k[0]
            #print avg[0].average
            #print "max "
            #print max[0].max
            #print "min "
            #print min[0].min

            #if k[0] == 'temperature':
            l[k[0]+"Average"] = math.ceil(aver[0].average)
            l[k[0]+"Max"] = math.ceil(maxi[0].maximum)
            l[k[0]+"Min"] = math.ceil(mini[0].minimum)

#            if k[0] == 'pressure':
#           	l["pAverage"] = math.ceil(avg[0].average)/100
#            	l["pMax"] = math.ceil(max[0].max)/100
#            	l["pMin"] = math.ceil(min[0].min)/100
#
#            if k[0] == 'moisture':
#            	l["mAverage"] = math.ceil(avg[0].average)/100
#            	l["mMax"] = math.ceil(max[0].max)/100
#            	l["mMin"] = math.ceil(min[0].min)/100
#
            if k[0] == 'height':
            	l["hAverage"] = aver[0].average
            	l["hMax"] = maxi[0].maximum
            	l["hMin"] = mini[0].minimum
        
	

	session.close()
	return mytemplate.render(**l)

cherrypy.config.update({'server.socket_host': '0.0.0.0' })
conf = {'/img': {'tools.staticdir.on': True,
        'tools.staticdir.dir': '/home/pi/cherryws/img'}}
cherrypy.quickstart(Root(), '/', config=conf)


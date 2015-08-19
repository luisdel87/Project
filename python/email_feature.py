import requests
import json
import sys
import requests
import time
import sendemail

sys.path.insert(0, '/usr/lib/python2.7/bridge/')

from bridgeclient import BridgeClient as bridgeclient

value = bridgeclient()
sensors = {'temperature': '', 'humidity': '', 'distance':'', 'xtilt':'0', 'ytilt':'0', 'ztilt':'0','speed':'','longitude':'','latitude':'','high':''  }



def convertlatitudeandlogitude(latitude, longitude):

	latitude = latitude.split(".")
	latitudeday = long(latitude[0][0:len(latitude[0])-2])
	latitudeminute = float(latitude[0][len(latitude[0])-2:len(latitude[0])]) + (float(latitude[1])/100)
	
	if latitudeday >=0 :
		
		latitude = long(latitudeday) + (float(latitudeminute)/60)	
	else:
			
		latitude = long(latitudeday) - (float(latitudeminute)/60)
	
	longitude = longitude.split(".")
	longitudeday = long(longitude[0][0:len(longitude[0])-2])
	longitudedeminute = float(longitude[0][len(longitude[0])-2:len(longitude[0])]) + (float(longitude[1])/100)
	
	if longitudeday >=0 :
		
		longitude = long(longitudeday) + (float(longitudedeminute)/60)
	else:
			
		longitude = long(longitudeday) - (float(longitudedeminute)/60)
		
	return latitude, longitude
	



def setgps():
    try:                                                                                                   
        sensors['speed'] = value.get('speed')
        sensors['high'] =  value.get('high')
        sensors['latitude'] =  value.get('latitude')
        sensors['longitude'] =  value.get('longitude')   
        sensors['latitude'], sensors['longitude'] = convertlatitudeandlogitude(sensors['latitude'], sensors['longitude'])
    except:
        print ("EL modulo Gps no esta listo aun")



def settemperatureandhumididy():
    try:
        sensors['temperature'] = value.get('temperature')
        sensors['humidity'] = value.get('humidity')
    except:
        print ("Error al leer el sensor de temperatura")
  

def setdistance():
    try:
        sensors['distance'] = value.get('distance')
    except:
        print ("Error al leer el sensor de distancia")

def xyztilt():
    try:
        sensors['xtilt'] = value.get('xtilt')
        sensors['ytilt'] = value.get('ytilt')
        sensors['ztilt'] = value.get('ztilt')
    except:
        print ("Error al leer el acelerometro")
            

def sendvalue(data):

    url = "http://test.ttcloud.net:8082/iot/d"
    querystring = {"i":"bike002","k":"1e51bf435cfe45139688f9461c13563c"}
    payload = data
    try:
        response = requests.request("POST", url, data=payload, params=querystring)
        print ("Respuesta de Orion: "+str(response.status_code))
    except:
        print ("Error al enviar a Orion")

def checkfallen():
    try:
        if (float(sensors['ytilt']) < float (-80) or float(sensors['ytilt']) > float (80) and float(sensors['speed']) < 5  ):
            print ("Caida detectada")
            try:
                sendemail.sendemail(sensors['latitude'], sensors['longitude'])
            except:
                
                print ("Imposible enviar Aviso")
            
            return True
        else:
            
            return False
    except:
        print ("El GPS no ha enviado la primera medida aun")



def main():
	
    bucle = True
    fallen = False
    
    while (bucle):
        
        setdistance()
        settemperatureandhumididy()
        xyztilt()
        setgps()
        if (fallen == False):
            fallen=checkfallen()
	if (fallen == True and float(-30)<float(sensors["ytilt"])<float(30)):
	    fallen = False
	    
    	
    	data = "temperature|" + str(sensors['temperature']) + "#humidity|" + \
    			str(sensors['humidity'])+ '#distance|'+str(sensors['distance'])+ \
    			"#xtilt|"+str(sensors['xtilt'])+"#ytilt|"+str(sensors['ytilt'])+"#ztilt|"+ \
    			str(sensors['ztilt'])+ "#speed|"+str(sensors['speed']) +"#high|"+str(sensors['high']) + \
    			"#gps|"+ str(sensors['latitude']) +"/"+ str(sensors['longitude'])
    	
    	print str(data)
    
    	sendvalue(data)
    	time.sleep(3)


if __name__ == '__main__':
    main()

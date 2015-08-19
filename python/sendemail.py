#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib

def sendemail(latitude, longitude):
 
    fromaddr = 'luisdel87@gmail.com'
    toaddrs  = 'luisdel87@gmail.com'
    msg=str("Se ha producido una incidencia en maps.google.com/maps?&z=10&q="+ str(latitude)+","+str(longitude)+" Intente contactar con el conductor")
      
    print (msg)
     
    # Datos
    username = 'luisdel87@gmail.com'
    password = 'estupendisimo'
     
    # Enviando el correo
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
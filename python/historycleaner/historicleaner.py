import requests
import json
import time
import yaml


file = open("historicleaner.yaml")
param = yaml.load(file)

tablename= str(param["tablename"])
columname= str(param["columname"])
daystosave= int(param["daystosave"])
cartodbapikey= str(param["cartodbapikey"])

#Configuration parameters

Non_encode_symbols = "&:/=(),'?!."

datetodelatefrom=str(time.gmtime()[0])+"-"+str(time.gmtime()[1])+"-"+str(time.gmtime()[2]-daystosave)
#url="https://iotsupport.cartodb.com/api/v2/sql?q=DELETE FROM testhistoric WHERE timeinstant ~ '"+datetodelate+".*'&api_key=6e87270accdefa4e1126d00cbbd6caa4132c3619"
try:
	url="https://iotsupport.cartodb.com/api/v2/sql?q=DELETE FROM "+tablename +" WHERE "+ columname +" < '"+datetodelatefrom+"'&api_key="+cartodbapikey
except:
	print("Error")

#Send request to cartodb
print(url)
response = requests.request("POST", url)


#Print answer from cartodb
print(response.text)














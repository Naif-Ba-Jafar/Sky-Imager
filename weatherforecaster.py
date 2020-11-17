import pyowm
import os
from datetime import datetime
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning) 
APIKEY='YourAPI'
OpenWMap=pyowm.OWM(APIKEY)
Weather=OpenWMap.weather_at_place('YourLocation')
Data=Weather.get_weather()
Weatherforecast = OpenWMap.three_hours_forecast('YourLocation')

date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S")

print ("-------------------------------------------------------------")
print ("Weather Status for - YourLocation || {}".format(date_time))
print ("-------------------------------------------------------------")

temp = Data.get_temperature(unit='celsius')
print ("Average Temp. Currently ", temp['temp'] , '°C')
print ("Max Temp. Currently ", temp['temp_max'], '°C')
print ("Min Temp. Currently ", temp['temp_min'], '°C')


humidity = Data.get_humidity()
print ("Humidity : ",humidity, '%')


wind = Data.get_wind()
print ("Wind Speed : ",wind['speed'], 'm/s')
print ("Wind Direction in Deg : ",wind['deg'],'°')


cloud = Data.get_clouds()
print ("Cloud Coverage Percentage : ",cloud, '%')

weatherstatus = Data.get_status()
weatherstatusdetailed = Data.get_detailed_status()
print ("Weather status : ",weatherstatus)
print ("Weather status with details :",weatherstatusdetailed)

rain=Weatherforecast.will_have_rain()
sun=Weatherforecast.will_have_sun()
cloud=Weatherforecast.will_have_clouds() 

print("There will be rain :",rain)
print("There will be sun :",sun)
print("There will be clouds :",cloud) 

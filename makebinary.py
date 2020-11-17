# Cloud coverage computation for on-board computation
import os
import cv2
import numpy as np
from datetime import datetime
import warnings
import pyowm
import RPi.GPIO as GPIO
import time
from time import sleep
import sys
import urllib.request
import requests
import LCDlib
myAPI = 'MZ7R8ZVF28M8VMXN' 
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
GPIO.setwarnings(False)
redLED = 21
greenLED = 18
RedLED = 4
GreenLED = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(redLED, GPIO.OUT)
GPIO.output(redLED, GPIO.LOW)


GPIO.setmode(GPIO.BCM)
GPIO.setup(greenLED, GPIO.OUT)
GPIO.output(greenLED, GPIO.LOW)

GPIO.setmode(GPIO.BCM)
GPIO.setup(RedLED, GPIO.OUT)
GPIO.output(RedLED, GPIO.LOW)

GPIO.setmode(GPIO.BCM)
GPIO.setup(GreenLED, GPIO.OUT)
GPIO.output(GreenLED, GPIO.LOW)



def preprocess(image):
    """ Preprocess 'image' to help separate cloud and sky. """
    B, G, R = cv2.split(image) # extract the colour channels

    # construct a ratio between the blue and red channel sum and difference
    BR_sum  = B + R
    BR_diff = B - R
    # handle X/0 and 0/0 errors, and remove NaNs (not a number)
    with np.errstate(divide='ignore', invalid='ignore'):
        BR_ratio = BR_diff / BR_sum
        BR_ratio = np.nan_to_num(BR_ratio)

    # normalize to 0-255 range and convert to 8-bit unsigned integers
    return cv2.normalize(BR_ratio, None, 0, 255, cv2.NORM_MINMAX) \
              .astype(np.uint8)

def makebinary(imagepath, radiusMask = None):
    startTime = datetime.now()

    # read in the image and shrink for faster processing
    image   = cv2.imread(imagepath)
    scale   = 0.2
    smaller = cv2.resize(image, (0,0), fx=scale, fy=scale)
    center  = [dim / 2 for dim in smaller.shape[:2]]

    preprocessed = preprocess(smaller.astype(float))

    if radiusMask:
        # apply a circular mask to get only the pixels of interest
        from cmask import cmask
        mask = cmask(index, scale * radiusMask, resized).astype(bool)
    else:
        mask = np.ones(preprocessed.shape).astype(bool)
    
    masked = preprocessed[mask]

    # use Otsu's method to separate clouds and sky
    threshold, result = cv2.threshold(masked, 0, 255,
                                      cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # invert the result so clouds are white (255) and sky is black (0)
    inverted = cv2.bitwise_not(result)

    # determine the cloud coverage
    cloud_pixels   = np.count_nonzero(inverted == 255)
    total_pixels   = result.size
    cloud_coverage = cloud_pixels / total_pixels

    # create a mask of where the clouds are
    cloud_image_mask = np.zeros(mask.shape, dtype=np.uint8)
    cloud_image_mask[mask] = inverted.flatten()
   
    print('Cloud Coverage is {:.3f}%'.format(cloud_coverage*100))
    print(datetime.now() - startTime)

    last_dot  = imagepath.rindex('.')
    save_path = imagepath[:last_dot] + '-mask' + imagepath[last_dot:]
    cv2.imwrite(save_path, cloud_image_mask)
    ClearSkyPower = 62190000
    OutputPower = ClearSkyPower * cloud_coverage
    PVoutput = ClearSkyPower - OutputPower
    print('Solar power output forecast is {:.3f}MW'.format(PVoutput))

        
        

    date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S")
    print ("-------------------------------------------------------------")
    print ("Solar Irradiance Status for - Kota Damansara || {}".format(date_time))
    print ("-------------------------------------------------------------")

    # E14U387945GaZOYerDx4BRPWpMWCspJ-
    # qL2tfC6BPJ_AOMFfji_tDwgLJ6ZW_aGx
    url = 'https://api.solcast.com.au/world_radiation/forecasts?latitude=3.20933&longitude=101.561339&api_key=E14U387945GaZOYerDx4BRPWpMWCspJ-'
    res = requests.get(url, headers={'Content-Type': 'application/json'})
    data = res.json()
    forecast = data["forecasts"][0]["ghi"]

    print('forecastss: {}W/m2 '.format(forecast))
    
        
    if cloud_coverage > 0.5:
        
        GPIO.output(redLED, GPIO.HIGH)
    else:
        GPIO.output(greenLED, GPIO.HIGH)
        
    if forecast < 500:
        
        GPIO.output(RedLED, GPIO.HIGH)
        
    else:
        GPIO.output(GreenLED, GPIO.HIGH)
    
    
    
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    APIKEY='2d14a14179399eb76caee93f5cb702e5'
    OpenWMap=pyowm.OWM(APIKEY)
    Weather=OpenWMap.weather_at_place('Kota Damansara')
    Data=Weather.get_weather()
    Weatherforecast = OpenWMap.three_hours_forecast('Kota Damansara')

    date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S")

    print ("-------------------------------------------------------------")
    print ("Weather Status for - Kota Damansara || {}".format(date_time))
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

    #rain=Weatherforecast.will_have_rain()
    #sun=Weatherforecast.will_have_sun()
    #cloud=Weatherforecast.will_have_clouds() 

    #print("There will be rain :",rain)
    #print("There will be sun :",sun)
    #print("There will be clouds :",cloud)
    
    
    time = '2020-11-13 16:30:00+00'

    rain=Weatherforecast.will_be_rainy_at(time) # forecast rain
    sun=Weatherforecast.will_be_sunny_at(time) # forecast sun
    cloud=Weatherforecast.will_be_cloudy_at(time) # forecast clouds

    print("There will be rain :",rain) # print details
    print("There will be sun :",sun) #print details
    print("There will be clouds :",cloud) # print details
    
   # while True:
        
    if cloud_coverage > 0.5: # if the cloud coverage is 50% or greater
        wind = Data.get_wind()
        eta = (1200/wind["speed"])/60 # calculate the eta
        print('ETA = {:.3f} min'.format(eta))
        
    else:
        eta = 0
        print('ETA is not availabe')
        
    
    mylcd = LCDlib.lcd()
    mylcd.lcd_display_string("Cloud:{:.3f}%" .format(cloud_coverage*100), 1)
    mylcd.lcd_display_string("PV:{:.3f}MW" .format(PVoutput), 2)
    mylcd.lcd_display_string("Rad:{:.3f}W/m^2" .format(forecast), 3)
    mylcd.lcd_display_string("ETA:{:.3f}min" .format(eta), 4)           
            # Sending the data to thingspeak
    conn = urllib.request.urlopen(baseURL + '&field1=%s&field2=%s&field3=%s&field4=%s' % (cloud_coverage*100,PVoutput,forecast, eta))
    print (conn.read())
            # Closing the connection
    conn.close()

           
    return(cloud_coverage)



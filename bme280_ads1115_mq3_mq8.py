import bme280 # requires pip3 install RPi.bme280
import smbus2
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from time import sleep, strftime, time
from datetime import datetime
#import cronus.beat as beat # requires pip3 install cronus (https://github.com/anayjoshi/cronus)

# get I2C bus
bus = smbus2.SMBus(1) # activate

# BME280
address_BME280 = 0x76 # BME280 address
bme280.load_calibration_params(bus,address_BME280)

# initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# create ADC object.
ads = ADS.ADS1115(i2c)
ads.gain = 1

# For single ended mode we use AnalogIn to create the analog input channel,
# providing the ADC object and the pin to which the signal is attached.

chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

# calculating hydrogen concentration from MQ-8 (see MQ8_sensor.ipynb)
def cH2_ppm(Vout):
  Vin = 5 # input voltage in V
  RL = 10e3 # load resistance in Ohm
  Rs_air = 215225 # sensor resistance in clean air in Ohm
  Rs_H2air = RL*(Vin/Vout-1)
  cH2_ppm = (Rs_air/Rs_H2air*10**2.49)**(1/1.45) # in ppm
  return cH2_ppm

# calculating alcohol concentration from MQ-3 (see MQ3_sensor.ipynb)
def cAlc_mgl(Vout):
  Vin = 5 # input voltage in V
  RL = 200e3 # load resistance in Ohm
  Rs_air = 4.8e6 # sensor resistance in clean air in Ohm
  Rs_Alc_air = RL*(Vin/Vout-1)
  cAlc_mgl = (Rs_air/Rs_Alc_air*10**-2.045)**(1/0.665) # in mgl^-1
  return cAlc_mgl

# print values and save data to csv file
with open('/home/krupke-group/data/'+datetime.now().strftime("%Y%m%d-%H%M%S")+'_log.csv','a') as file:
  file.write("{0},{1},{2},{3},{4},{5}\n".format("DateTime","temperature/°C","pressure/hPa","humidity/%","cH2/ppm","cAlc/mgl^-1"))
  
  #beat.set_rate(1) # rate at which computation is to be performed in Hz
  #while beat.true(): # a substitute to True
  while True:
    temperature = bme280.sample(bus,address_BME280).temperature
    pressure = bme280.sample(bus,address_BME280).pressure
    humidity = bme280.sample(bus,address_BME280).humidity
    cH2 = cH2_ppm(chan0.voltage)
    cAlc = cAlc_mgl(chan1.voltage)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] 
    print(timestamp)
    print(chan0.value, chan0.voltage)
    print(chan1.value, chan1.voltage)
    print(chan2.value, chan2.voltage)
    print(chan3.value, chan3.voltage)
    print("Temperature = %.2f C" %temperature,"Pressure = %.2f hPa" %pressure,"Humidity = %.2f %%" %humidity, "cH2 = %.2f ppm" %cH2_ppm(chan0.voltage),"cAlc = %.2f mg/l" %cAlc_mgl(chan1.voltage))
    file.write("{0},{1},{2},{3},{4},{5}\n".format(timestamp,'%.2f' %temperature,'%.2f' %pressure,'%.2f' %humidity,'%.2f' %cH2_ppm(chan0.voltage),'%.2f' %cAlc_mgl(chan1.voltage)))
    #beat.sleep()
    sleep(1)
  file.close()

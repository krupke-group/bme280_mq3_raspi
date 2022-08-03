import bme280 # requires pip3 install RPi.bme280
import smbus2
#import cronus.beat as beat # requires pip3 install cronus (https://github.com/anayjoshi/cronus)
from time import sleep, strftime, time
from datetime import datetime

# get I2C bus
bus = smbus2.SMBus(1) # activate

# BME280
address_BME280 = 0x76 # BME280 address
bme280.load_calibration_params(bus,address_BME280)

# ADC121C_MQ3 (https://github.com/ControlEverythingCommunity/ADC121C_MQ3)
address_MQ3 = 0x50 # ADC121C_MQ3 address 
def read_MQ3():
  data = bus.read_i2c_block_data(address_MQ3, 0x00, 2) # read data from 0x00(00), 2 bytes
  raw_adc = (data[0] & 0x0F) * 256 + data[1] # convert data to 12bits
  alcohol = (9.95 / 4096.0) * raw_adc + 0.05 # alcohol concentration in mg/l
  BAC = alcohol * 0.21 # breath alcohol concentration in mg/l
  return alcohol,BAC

# print values and save data to csv file
with open('/home/pi/data/'+datetime.now().strftime("%Y%m%d-%H%M%S")+'_log.csv','a') as file:
  file.write("{0},{1},{2},{3},{4},{5}\n".format("DateTime","temperature/°C","pressure/hPa","humidity/%","alcohol/mg^-1","BAC/mgl^-1"))
  
  #beat.set_rate(1) # rate at which computation is to be performed in Hz
  #while beat.true(): # a substitute to True
  while True:
    temperature = bme280.sample(bus,address_BME280).temperature
    pressure = bme280.sample(bus,address_BME280).pressure
    humidity = bme280.sample(bus,address_BME280).humidity
    alcohol = read_MQ3()[0]
    BAC = read_MQ3()[1]
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] 
    print(timestamp)
    print("Temperature = %.2f C" %temperature,"Pressure = %.2f hPa" %pressure,"Humidity = %.2f %%" %humidity, "alcohol concentration = %.2f mg/l" %alcohol,"BAC = %.2f mg/l" %BAC)
    file.write("{0},{1},{2},{3},{4},{5}\n".format(timestamp,'%.2f' %temperature,'%.2f' %pressure,'%.2f' %humidity,'%.2f' %alcohol,'%.2f' % BAC))
    #beat.sleep()
    sleep(1)
  file.close()

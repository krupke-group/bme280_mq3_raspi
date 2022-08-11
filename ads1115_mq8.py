# import the necessary modules and initialize the I2C bus

import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

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

# print channel value and voltage
print(chan0.value, chan0.voltage)
print(chan1.value, chan1.voltage)
print(chan2.value, chan2.voltage)
print(chan3.value, chan3.voltage)

# calculating hydrogen concentration from MQ-8 (see MQ8_sensor.ipynb)
def cH2_ppm(Vout):
  Vin = 5 # input voltage in V
  RL = 10e3 # load resistance in Ohm
  Rs_air = 323e3 # sensor resistance in clean air in Ohm
  Rs_H2air = RL*(Vin/Vout-1)
  cH2_ppm = (Rs_air/Rs_H2air*10**2.49)**1/1.45 # in ppm
  return cH2_ppm

# calculating alcohol concentration from MQ-3 (see MQ3_sensor.ipynb)
def cAlc_mgl(Vout):
  Vin = 5 # input voltage in V
  RL = 200e3 # load resistance in Ohm
  Rs_air = 10e6 # sensor resistance in clean air in Ohm
  Rs_Alc_air = RL*(Vin/Vout-1)
  cAlc_mgl = (Rs_air/Rs_Alc_air*10**-2.045)**1/0.665 # in mgl^-1
  return cAlc_mgl

print('cH2 = %.2f ppm' %cH2_ppm(chan0.voltage))
print('cAlc = %.2f mg/l' %cAlc_mgl(chan1.voltage))

# For differential mode, you provide two pins when setting up the ADC channel.
# The reading will be the difference between the two. Here, we use pin 0 and 1:
#chan = AnalogIn(ads, ADS.P0, ADS.P1)
#print(chan.value, chan.voltage)

# Create an ADS1115 ADC (16-bit) instance.
#adc = adafruit_ads1x15.ads1115(address=0x48, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
#GAIN = 1
'''
print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
print('-' * 37)
# Main loop.
while True:
    # Read all the ADC channel values in a list.
    values = [0]*4
    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        values[i] = adc.read_adc(i, gain=GAIN)
        # Note you can also pass in an optional data_rate parameter that controls
        # the ADC conversion time (in samples/second). Each chip has a different
        # set of allowed data rate values, see datasheet Table 9 config register
        # DR bit values.
        #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
        # Each value will be a 12 or 16 bit signed integer value depending on the
        # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
    # Print the ADC values.
    print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
    # Pause for half a second.
    time.sleep(0.5)
'''

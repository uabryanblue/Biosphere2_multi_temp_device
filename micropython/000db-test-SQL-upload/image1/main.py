from machine import Pin, ADC
from time import sleep

pot = ADC(0)

# the 4 digital outs to select 16 analog MUX values
D0 = Pin(16, Pin.OUT)
D1 = Pin(5, Pin.OUT)
D2 = Pin(4, Pin.OUT)
D3 = Pin(0, Pin.OUT)

# relay
D5 = Pin(14, Pin.OUT)
D6 = Pin(12, Pin.OUT)
D5.off()
D6.off()

# analog all to value 0
D0.off()
D1.off()
D2.off()
D3.off()
while True:
  D0.off()
  D1.off()
  D2.off()
  D3.off()
  sleep(0.5)
  val0 = pot.read()
  # print(f"0000: {pot_value}")
  D0.on()
  D1.off()
  D2.off()
  D3.off()
  sleep(0.5)
  val1 = pot.read()
  # print(f"0001: {pot_value}")
  D0.off()
  D1.on()
  D2.on()
  D3.on()
  sleep(0.5)
  val15 = pot.read()
  # print(f"1110: {pot_valude}")
  print(f"{val0:10} : {val1:10} : {val15:10}")

# relay code
  D5.on()
  sleep(15)
  D5.off()
  sleep(1)

  D6.on()
  sleep(15)
  D6.off()
  sleep(1)

  D5.on()
  D6.on()
  sleep(30)
  D5.off()
  D6.off()

  sleep(3)
  





# # main.py -- put your code here!
# # Complete project details at https://RandomNerdTutorials.com

# # from machine import Pin, ADC
# # from time import sleep

# # pot = ADC(0)

# # while True:
# #   pot_value = pot.read()
# #   print(pot_value)
# #   sleep(1)

# from machine import Pin, ADC
# # from math import log # , pow
# from time import sleep


# VCC = 3.3   # NodeMCU on board 3.3v vcc
# R2 = 97000  # 10k ohm series resistor
# adc_resolution = 1023 # 10-bit adc

# # thermistor equation parameters
# A = 0.001129148 
# B = 0.000234125
# # C = 8.76741*10^-8 
# C = 8.76741e-8

# adc_port = ADC(0)

# # def ln(x):      #natural logarithm function for x>0 real values
# #     y = (x-1)/(x+1)
# #     sum = 1 
# #     val = 1
# # #     if(x == nil) then
# # #         return 0
# # #     end
# # # -- we are using limited iterations to acquire reliable accuracy.
# # # -- here its upto 10000 and increased by 2
# #     for i in range(3, 10000, 2):
# #         val = val*(y*y)
# #         sum = sum + (val/i)
# #     return 2*y*sum

# # def steinhart_temperature_C(r, Ro=10000.0, To=25.0, beta=3950.0):
# #     #import math
# #     steinhart = log(r / Ro) / beta      # log(R/Ro) / beta
# #     steinhart += 1.0 / (To + 273.15)         # log(R/Ro) / beta + 1/To
# #     steinhart = (1.0 / steinhart) - 273.15   # Invert, convert to C
#     # return steinhart

# while True:
#     adc_value = adc_port.read()
#     # print(f'adc_value: {adc_value}')

#     # R2 = 97000 / (1024/adc_value - 1) #65535
#     # print('Thermistor resistance: {} ohms'.format(R))
    
#     # print(f'stR: {steinhart_temperature_C(R)}')
#     # print(f'strB: {steinhart_temperature_C(R, Ro=10000.0, To=25.0, beta=3950)}')

#     Vout = (adc_value * VCC) / adc_resolution
#     Rth = (VCC * R2 / Vout) - R2
#     # print(f'Rth: {Rth}')

# #   Steinhart-Hart Thermistor Equation:
# #   Temperature in Kelvin = 1 / (A + B[ln(R)] + C[ln(R)]^3)
# #   where A = 0.001129148, B = 0.000234125 and C = 8.76741*10^-8
#     t1 = A
#     t2 = B * log(Rth) 
#     t3 = C * pow((log(Rth)),3)
#     temperaturek = 1 / (t1 + t2 + t3)
#     temperaturek = (1 / (A + (B * log(Rth)) + (C * pow((log(Rth)),3))))   # Temperature in kelvin
#     temperature = temperaturek - 273.15  # Temperature in degree celsius

#     print(f'adc_value:{adc_value} Rth:{Rth} tempk:{temperaturek} temp:{temperature}')
#     sleep(5)

# #

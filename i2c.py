#!/usr/bin/python
 
#
#=BEGIN BRAINWORKS GPL
#
# This file is part of the BrainWorks RPi Environmental Monitor.
#
# Copyright(c) 2013 Gianluca Filippini
# http://www.brainworks.it
# info@brainworks.it
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http: licenses="" www.gnu.org="">.
#
#=END BRAINWORKS GPL
#
 
import time
 
from smbus import SMBus
 
bus = SMBus(0)
 
 
MPL115A2_ADDRESS = (0x60)
 
MPL115A2_REGISTER_PRESSURE_MSB  = (0x00)
MPL115A2_REGISTER_PRESSURE_LSB  = (0x01)
MPL115A2_REGISTER_TEMP_MSB      = (0x02)
MPL115A2_REGISTER_TEMP_LSB      = (0x03)
MPL115A2_REGISTER_A0_COEFF_MSB  = (0x04)
MPL115A2_REGISTER_A0_COEFF_LSB  = (0x05)
MPL115A2_REGISTER_B1_COEFF_MSB  = (0x06)
MPL115A2_REGISTER_B1_COEFF_LSB  = (0x07)
MPL115A2_REGISTER_B2_COEFF_MSB  = (0x08)
MPL115A2_REGISTER_B2_COEFF_LSB  = (0x09)
MPL115A2_REGISTER_C12_COEFF_MSB = (0x0A)
MPL115A2_REGISTER_C12_COEFF_LSB = (0x0B)
MPL115A2_REGISTER_STARTCONVERSION = (0x12)
 
 
a0_MSB = -1;
a0_LSB = -1;
b1_MSB = -1;
b1_LSB = -1;
b2_MSB = -1;
b2_LSB = -1;
c12_MSB = -1;
c12_LSB = -1;
 
 
pressure_MSB = -1
pressure_LSB = -1
 
temp_MSB = -1
temp_LSB = -1
 
def readCoefficients():
   global a0_MSB;
   global a0_LSB;
   global b1_MSB;
   global b1_LSB;
   global b2_MSB;
   global b2_LSB;
   global c12_MSB;
   global c12_LSB;
 
   a0_MSB = bus.read_byte_data(MPL115A2_ADDRESS,MPL115A2_REGISTER_A0_COEFF_MSB+0);
   a0_LSB = bus.read_byte_data(MPL115A2_ADDRESS,MPL115A2_REGISTER_A0_COEFF_LSB+0);
 
   b1_MSB = bus.read_byte_data(MPL115A2_ADDRESS,MPL115A2_REGISTER_B1_COEFF_MSB+0);
   b1_LSB = bus.read_byte_data(MPL115A2_ADDRESS,MPL115A2_REGISTER_B1_COEFF_LSB+0);
 
   b2_MSB = bus.read_byte_data(MPL115A2_ADDRESS,MPL115A2_REGISTER_B2_COEFF_MSB+0);
   b2_LSB = bus.read_byte_data(MPL115A2_ADDRESS,MPL115A2_REGISTER_B2_COEFF_LSB+0);
 
   c12_MSB = bus.read_byte_data(MPL115A2_ADDRESS,MPL115A2_REGISTER_C12_COEFF_MSB+0);
   c12_LSB = bus.read_byte_data(MPL115A2_ADDRESS,MPL115A2_REGISTER_C12_COEFF_LSB+0);
 
 
#
# MAIN
#
readCoefficients()
 
#
# unpack to 10bits full scale
_mpl115a2_a0 = (float)( (a0_MSB<<8) | a0_LSB  ) / (2<<3)
_mpl115a2_b1 = (float)( (b1_MSB<<8) | b1_LSB  ) / (2<<13)
_mpl115a2_b2 = (float)( (b2_MSB<<8) | b2_LSB  ) / (2<<14)
_mpl115a2_c12 = (float)( (c12_MSB<<8) | (c12_LSB >>2) ) / (2<<13)
 
#
# send conversion command   
bus.write_i2c_block_data(MPL115A2_ADDRESS,MPL115A2_REGISTER_STARTCONVERSION,[0x12])
 
#   
# sleep until the conversion is certainly completed
time.sleep(0.5);
 
#
# pressure AGC units
pressure_MSB = bus.read_byte_data(MPL115A2_ADDRESS,MPL115A2_REGISTER_PRESSURE_MSB);
pressure_LSB = bus.read_byte_data(MPL115A2_ADDRESS,MPL115A2_REGISTER_PRESSURE_LSB);
 
#
# temperatture AGC units
temp_MSB = bus.read_byte_data(MPL115A2_ADDRESS,MPL115A2_REGISTER_TEMP_MSB+0);
temp_LSB = bus.read_byte_data(MPL115A2_ADDRESS,MPL115A2_REGISTER_TEMP_LSB+0);
 
pressure = (pressure_MSB<< 8 | pressure_LSB) >>6;
 
temperature = (temp_MSB<<8 | temp_LSB) >>6;
 
pressureComp = _mpl115a2_a0 + (_mpl115a2_b1 + _mpl115a2_c12 * temperature ) * pressure + _mpl115a2_b2 * temperature;
 
#
# Return pressure and temperature as floating point values
P = ((65.0 / 1023.0) * pressureComp) + 50.0; 
T = (temperature - 498.0) / -5.35 +25.0; 
 
print P/10,T

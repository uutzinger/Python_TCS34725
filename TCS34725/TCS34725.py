# The MIT License (MIT)
#
# Copyright (c) 2016 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import division

import time

# TCS34725 default address.
TCS34725_I2CADDR          = 0x29
TCS34725_ID               = 0x12    # 0x44 = TCS34721/TCS34725, 0x4D = TCS34723/TCS34727 #

TCS34725_COMMAND_BIT      = 0x80

# Commands
TCS34725_ENABLE           = 0x00
TCS34725_ENABLE_AIEN      = 0x10    # RGBC Interrupt Enable #
TCS34725_ENABLE_WEN       = 0x08    # Wait enable - Writing 1 activates the wait timer #
TCS34725_ENABLE_AEN       = 0x02    # RGBC Enable - Writing 1 actives the ADC, 0 disables it #
TCS34725_ENABLE_PON       = 0x01    # Power on - Writing 1 activates the internal oscillator, 0 disables it #

# Registers
TCS34725_ATIME            = 0x01    # Integration time #
TCS34725_WTIME            = 0x03    # Wait time (if TCS34725_ENABLE_WEN is asserted) #
TCS34725_WTIME_2_4MS      = 0xFF    # WLONG0 = 2.4ms   WLONG1 = 0.029s #
TCS34725_WTIME_204MS      = 0xAB    # WLONG0 = 204ms   WLONG1 = 2.45s  #
TCS34725_WTIME_614MS      = 0x00    # WLONG0 = 614ms   WLONG1 = 7.4s   #
TCS34725_AILTL            = 0x04    # Clear channel lower interrupt threshold #
TCS34725_AILTH            = 0x05
TCS34725_AIHTL            = 0x06    # Clear channel upper interrupt threshold #
TCS34725_AIHTH            = 0x07

TCS34725_PERS             = 0x0C    # Persistence register - basic SW filtering mechanism for interrupts #
TCS34725_PERS_NONE        = 0b0000  # Every RGBC cycle generates an interrupt                                #
TCS34725_PERS_1_CYCLE     = 0b0001  # 1 clean channel value outside threshold range generates an interrupt   #
TCS34725_PERS_2_CYCLE     = 0b0010  # 2 clean channel values outside threshold range generates an interrupt  #
TCS34725_PERS_3_CYCLE     = 0b0011  # 3 clean channel values outside threshold range generates an interrupt  #
TCS34725_PERS_5_CYCLE     = 0b0100  # 5 clean channel values outside threshold range generates an interrupt  #
TCS34725_PERS_10_CYCLE    = 0b0101  # 10 clean channel values outside threshold range generates an interrupt #
TCS34725_PERS_15_CYCLE    = 0b0110  # 15 clean channel values outside threshold range generates an interrupt #
TCS34725_PERS_20_CYCLE    = 0b0111  # 20 clean channel values outside threshold range generates an interrupt #
TCS34725_PERS_25_CYCLE    = 0b1000  # 25 clean channel values outside threshold range generates an interrupt #
TCS34725_PERS_30_CYCLE    = 0b1001  # 30 clean channel values outside threshold range generates an interrupt #
TCS34725_PERS_35_CYCLE    = 0b1010  # 35 clean channel values outside threshold range generates an interrupt #
TCS34725_PERS_40_CYCLE    = 0b1011  # 40 clean channel values outside threshold range generates an interrupt #
TCS34725_PERS_45_CYCLE    = 0b1100  # 45 clean channel values outside threshold range generates an interrupt #
TCS34725_PERS_50_CYCLE    = 0b1101  # 50 clean channel values outside threshold range generates an interrupt #
TCS34725_PERS_55_CYCLE    = 0b1110  # 55 clean channel values outside threshold range generates an interrupt #
TCS34725_PERS_60_CYCLE    = 0b1111  # 60 clean channel values outside threshold range generates an interrupt #

TCS34725_CONFIG           = 0x0D
TCS34725_CONFIG_WLONG     = 0x02    # Choose between short and long =12x) wait times via TCS34725_WTIME #
TCS34725_CONTROL          = 0x0F    # Set the gain level for the sensor #
TCS34725_STATUS           = 0x13
TCS34725_STATUS_AINT      = 0x10    # RGBC Clean channel interrupt #
TCS34725_STATUS_AVALID    = 0x01    # Indicates that the RGBC channels have completed an integration cycle #
TCS34725_CDATAL           = 0x14    # Clear channel data #
TCS34725_CDATAH           = 0x15
TCS34725_RDATAL           = 0x16    # Red channel data #
TCS34725_RDATAH           = 0x17
TCS34725_GDATAL           = 0x18    # Green channel data #
TCS34725_GDATAH           = 0x19
TCS34725_BDATAL           = 0x1A    # Blue channel data #
TCS34725_BDATAH           = 0x1B

TCS34725_INTEGRATIONTIME_2_4MS  = 0xFF  #    2.4ms -   1 cycle  - Max Count: 1024  
TCS34725_INTEGRATIONTIME_24MS   = 0xF6  #   24ms   -  10 cycles - Max Count: 10240 
TCS34725_INTEGRATIONTIME_50MS   = 0xEB  #   50ms   -  20 cycles - Max Count: 20480 
TCS34725_INTEGRATIONTIME_101MS  = 0xD5  #  101ms   -  42 cycles - Max Count: 43008 
TCS34725_INTEGRATIONTIME_154MS  = 0xC0  #  154ms   -  64 cycles - Max Count: 65535 
TCS34725_INTEGRATIONTIME_700MS  = 0x00  #  700ms   - 256 cycles - Max Count: 65535 

TCS34725_GAIN_1X                = 0x00  #   No gain
TCS34725_GAIN_4X                = 0x01  #   4x gain
TCS34725_GAIN_16X               = 0x02  #  16x gain
TCS34725_GAIN_60X               = 0x03  #  60x gain

class TCS34725(object):
    """TCS34725 color sensor."""
    
    def __init__(self, integration_time=TCS34725_INTEGRATIONTIME_2_4MS,
                 gain=TCS34725_GAIN_4X, address=TCS34725_I2CADDR , i2c=None, **kwargs):
        """Initialize the TCS34725 sensor."""                 
        # Create I2C device.
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._device = i2c.get_i2c_device(address, **kwargs)
        # Make sure we are connected
        chip_id = self._device.readU8(TCS34725_COMMAND_BIT | TCS34725_ID)
        if chip_id != 0x44:
            raise RuntimeError('Failed to read TCS34725 ID, check wiring.')

        self.setIntegrationTime(integration_time)
        self.setGain(gain)
        self.enable()        
    
    def enable(self):
        """Enable the chip."""
        self._device.write8(TCS34725_COMMAND_BIT | TCS34725_ENABLE, TCS34725_ENABLE_PON)
        time.sleep(0.01);
        self._device.write8(TCS34725_COMMAND_BIT | TCS34725_ENABLE, (TCS34725_ENABLE_PON | TCS34725_ENABLE_AEN)) 

    def disable(self):
        """Disable the chip (power down)."""
        # Turn the device off to save power
        reg = self._device.readU8(TCS34725_COMMAND_BIT | TCS34725_ENABLE)
        reg = reg & ~(TCS34725_ENABLE_PON | TCS34725_ENABLE_AEN)
        self._device.write8(TCS34725_COMMAND_BIT | TCS34725_ENABLE, reg)
 
    def setGain(self, gain):
        """Adjusts the gain on the TCS34725 (adjusts the sensitivity to light).
        Use one of the following constants:
         - TCS34725_GAIN_1X   = No gain
         - TCS34725_GAIN_4X   = 2x gain
         - TCS34725_GAIN_16X  = 16x gain
         - TCS34725_GAIN_60X  = 60x gain
        """
        # Update the timing register
        self._device.write8(TCS34725_COMMAND_BIT | TCS34725_CONTROL, gain)
        # Update value placeholders
        self._tcs34725Gain = gain

    def getGain(self):
        """Return the current gain value.  This will be one of the constants
        specified in the set_gain doc string.
        """
        return self._device.readU8(TCS34725_COMMAND_BIT | TCS34725_CONTROL)
        
    def setIntegrationTime(self, it):
        """Sets the integration time for the TC34725.  Provide one of these
        constants:
         - TCS34725_INTEGRATIONTIME_2_4MS  = 2.4ms - 1 cycle    - Max Count: 1024
         - TCS34725_INTEGRATIONTIME_24MS   = 24ms  - 10 cycles  - Max Count: 10240
         - TCS34725_INTEGRATIONTIME_50MS   = 50ms  - 20 cycles  - Max Count: 20480
         - TCS34725_INTEGRATIONTIME_101MS  = 101ms - 42 cycles  - Max Count: 43008
         - TCS34725_INTEGRATIONTIME_154MS  = 154ms - 64 cycles  - Max Count: 65535
         - TCS34725_INTEGRATIONTIME_700MS  = 700ms - 256 cycles - Max Count: 65535
        """
        # Update the timing register */
        self._device.write8(TCS34725_COMMAND_BIT | TCS34725_ATIME, it)
        # Update value placeholders */
        self._tcs34725IntegrationTime = it

    def getIntegrationTime(self):
        """Return the current integration time value.  This will be one of the
        constants specified in the set_integration_time doc string.
        """
        return self.device.readU8(TCS34725_COMMAND_BIT | TCS34725_ATIME)
    
    def getRawData(self):
        """Reads the raw red, green, blue and clear channel values. Will return
        a 4-tuple with the red, green, blue, clear color values (unsigned 16-bit
        numbers).
        """
        #
        c = self._device.readU16LE(TCS34725_COMMAND_BIT | TCS34725_CDATAL);
        r = self._device.readU16LE(TCS34725_COMMAND_BIT | TCS34725_RDATAL);
        g = self._device.readU16LE(TCS34725_COMMAND_BIT | TCS34725_GDATAL);
        b = self._device.readU16LE(TCS34725_COMMAND_BIT | TCS34725_BDATAL);
        # Set a delay for the integration time */
        if   self._tcs34725IntegrationTime == TCS34725_INTEGRATIONTIME_2_4MS:
            time.sleep(0.0024)
        elif self._tcs34725IntegrationTime == TCS34725_INTEGRATIONTIME_24MS:
            time.sleep(0.024)
        elif self._tcs34725IntegrationTime == TCS34725_INTEGRATIONTIME_50MS:
            time.sleep(0.050)
        elif self._tcs34725IntegrationTime == TCS34725_INTEGRATIONTIME_101MS:
            time.sleep(0.101)
        elif self._tcs34725IntegrationTime == TCS34725_INTEGRATIONTIME_154MS:
            time.sleep(0.154)
        elif self._tcs34725IntegrationTime == TCS34725_INTEGRATIONTIME_700MS:
            time.sleep(0.700)
        return (r, g, b, c)

    def getRawData_noDelay(self):
        #
        c = self._device.readU16LE(TCS34725_COMMAND_BIT | TCS34725_CDATAL);
        r = self._device.readU16LE(TCS34725_COMMAND_BIT | TCS34725_RDATAL);
        g = self._device.readU16LE(TCS34725_COMMAND_BIT | TCS34725_GDATAL);
        b = self._device.readU16LE(TCS34725_COMMAND_BIT | TCS34725_BDATAL);
        return (r, g, b, c)

    def setPersistanceFilter(self):
        self._device.write8(TCS34725_COMMAND_BIT | TCS34725_PERS, TCS34725_PERS_NONE); 

    def setInterrupt(self, status):
        """Enable or disable interrupts by setting enabled to True or False."""
        r = self._device.readU8(TCS34725_COMMAND_BIT | TCS34725_ENABLE)
        if status:
            r |= TCS34725_ENABLE_AIEN;
        else:
            r &= ~TCS34725_ENABLE_AIEN;
        self._device.write8(TCS34725_COMMAND_BIT | TCS34725_ENABLE, r);
        time.sleep(1)

    def clearInterrupt(self):
        self._device.write8(0x66 & 0xFF);

    def setIntLimits(self, low, high):
        """Set the interrupt limits to provied unsigned 16-bit threshold values.
        """
        self._device.write8(0x04, low & 0xFF);
        self._device.write8(0x05, low >> 8);
        self._device.write8(0x06, high & 0xFF);
        self._device.write8(0x07, high >> 8);
        
    def calculateColorTemperature(self, r, g, b):
        # 1. Map RGB values to their XYZ counterparts.    */
        # Based on 6500K fluorescent, 3000K fluorescent   */
        # and 60W incandescent values for a wide range.   */
        # Note: Y = Illuminance or lux      
        X = (-0.14282 * r) + (1.54924 * g) + (-0.95641 * b);
        Y = (-0.32466 * r) + (1.57837 * g) + (-0.73191 * b);
        Z = (-0.68202 * r) + (0.77073 * g) + ( 0.56332 * b);
        if (X+Y+Z) == 0:
            return None
        # 2. Calculate the chromaticity co-ordinates      */
        xc = (X) / (X + Y + Z);
        yc = (Y) / (X + Y + Z);
        if (0.1858 - yc) == 0:
            return None
            
        # 3. Use McCamy's formula to determine the CCT    */
        n = (xc - 0.3320) / (0.1858 - yc);
        # Calculate the final CCT */
        cct = (449.0 * (n ** 3.0)) + (3525.0 * (n ** 2.0)) + (6823.3 * n) + 5520.33;
        # Return the results in degrees Kelvin
        return int(cct)

    def calculateLux(self, r, g, b):
        # This only uses RGB ... how can we integrate clear or calculate lux */
        # based exclusively on clear since this might be more reliable?      */
        return int((-0.32466 * r) + (1.57837 * g) + (-0.73191 * b))

    def rgb2hsv(self, r, g, b):
        min_rgb = min(r,g,b)
        max_rgb = max(r,g,b)

        v = max_rgb
        delta = max_rgb - min_rgb
        if (delta < 0.00001):
            s = 0
            h = 0
            return (h,s,v)
            
        if ( max_rgb > 0.0 ):
            s = (delta / max_rgb)
        else:
            s = 0.0
            h = NaN
            return (h,s,v)
            
        if ( r >= max_rgb ):
            h = ( g - b ) / delta
        elif ( g >= max_rgb ):
            h = 2.0 + ( b - r ) / delta
        else:
            h = 4.0 + ( r - g ) / delta

        h *= 60.0

        if (h < 0.0 ):
            h += 360.0

        return (h,s,v)


    def hsv2rgb(self, h, s, v):
        if(s <= 0.0):
            r = v;
            g = v;
            b = v;
            return (r,g,b)
        hh = h;
        if (hh >= 360.0):
            hh = 0.0
        hh /= 60.0
        i = long(hh);
        ff = hh - i;
        p = v * (1.0 - s);
        q = v * (1.0 - (s * ff));
        t = v * (1.0 - (s * (1.0 - ff)))

        if i==0:
            r = v
            g = t
            b = p
        elif i==1:
            r = q
            g = v
            b = p
        elif i==2:
            r = p
            g = v
            b = t
        elif i==3:
            r = p
            g = q
            b = v
        elif i==4:
            r = t
            g = p
            b = v
        else:
            r = v
            g = p
            b = q
        return (r,g,b)     

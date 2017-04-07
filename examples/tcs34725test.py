#!/usr/bin/python
# Author: Urs Utzinger
##
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import time

integrationtime = 0xFF
#  TCS34725_INTEGRATIONTIME_2_4MS  = 0xFF #    2.4ms -   1 cycle  - Max Count: 1024  
#  TCS34725_INTEGRATIONTIME_24MS   = 0xF6 #   24ms   -  10 cycles - Max Count: 10240 
#  TCS34725_INTEGRATIONTIME_50MS   = 0xEB #   50ms   -  20 cycles - Max Count: 20480 
#  TCS34725_INTEGRATIONTIME_101MS  = 0xD5 #  101ms   -  42 cycles - Max Count: 43008 
#  TCS34725_INTEGRATIONTIME_154MS  = 0xC0 #  154ms   -  64 cycles - Max Count: 65535 
#  TCS34725_INTEGRATIONTIME_700MS  = 0x00 #  700ms   - 256 cycles - Max Count: 65535 
  
gain = 0x00
#  TCS34725_GAIN_1X                = 0x00 #   No gain
#  TCS34725_GAIN_4X                = 0x01 #   4x gain
#  TCS34725_GAIN_16X               = 0x02 #  16x gain
#  TCS34725_GAIN_60X               = 0x03 #  60x gain
   
poll_interval = 0.1 # seconds
loop_interval = 0.001 # seconds

# Default constructor will pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
#
# Optionally you can override the bus number:
#sensor = TCS34725.TCS34725(busnum=2)
sensor = TCS34725.TCS34725()

sensor.setIntegrationTime(integrationtime)
sensor.setGain(gain)
  
lastPoll=time.time()
previousRateTime=time.time()
colorCounter=0

while True:
  currentTimeS = time.time()
  if currentTimeS - lastPoll >= poll_interval :
    sensor.setInterupt(False) # Turn ON LED
    r, g, b, c = sensor.getRawData()
    sensor.setInterupt(True)  # Turn OFF LED
    r /= c
    g /= c
    b /= c
    r *= 256 
    g *= 256
    b *= 256
    print("R: %s G: %s B: %s" % r,g,b)

  if ((currentTimeS - previousRateTime) >= 1.0):
    colorRate = colorCounter
    colorCounter = 0
    previousRateTime = currentTimeS
	
  print("Color rate: %d" % (colorRate) ) 
  
  # release task
  timeRemaining = loop_interval - (time.time() - currentTimeS)
  if (timeRemaining > 0):
    time.sleep(timeRemaining)

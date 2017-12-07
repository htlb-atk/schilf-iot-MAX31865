from machine import SPI
from machine import Pin
import math
import time

class MAX31865():
    
### Register constants, see data sheet for info.
# Read Addresses
MAX31865_REG_READ_CONFIG  = 0x00
MAX31865_REG_READ_RTD_MSB = 0x01
MAX31865_REG_READ_RTD_LSB = 0x02
MAX31865_REG_READ_HFT_MSB = 0x03
MAX31865_REG_READ_HFT_LSB = 0x04
MAX31865_REG_READ_LFT_MSB = 0x05
MAX31865_REG_READ_LFT_LSB = 0x06
MAX31865_REG_READ_FAULT   = 0x07

# Write Addresses
MAX31865_REG_WRITE_CONFIG  = 0x80
MAX31865_REG_WRITE_HFT_MSB = 0x83
MAX31865_REG_WRITE_HFT_LSB = 0x84
MAX31865_REG_WRITE_LFT_MSB = 0x85
MAX31865_REG_WRITE_LFT_LSB = 0x86

# Configuration Register
MAX31865_CONFIG_50HZ_FILTER = 0x01
MAX31865_CONFIG_CLEAR_FAULT = 0x02
MAX31865_CONFIG_3WIRE       = 0x10
MAX31865_CONFIG_ONE_SHOT    = 0x20
MAX31865_CONFIG_AUTO        = 0x40
MAX31865_CONFIG_BIAS_ON     = 0x80




   def __init__(self, wires=2, cs_pin='P9'):
      # initialize ``P9`` in gpio mode and make it an CS output
      self.CS = Pin(cs_pin, mode=Pin.OUT)
      self.CS(True)  # init chip select
      self.spi = SPI(0, mode=SPI.MASTER, baudrate=100000, polarity=0, phase=1, firstbit=SPI.MSB)

      # set configuration register 
      config = self.MAX31865_CONFIG_BIAS_ON + self.MAX31865_CONFIG_AUTO + self.MAX31865_CONFIG_CLEAR_FAULT + self.MAX31865_CONFIG_50HZ_FILTER
      if (wires == 3):
          config = config + MAX31865_CONFIG_3WIRE

      buf = bytearray(2)
      buf[0] = MAX31865_REG_WRITE_CONFIG  # config write address
      buf[1] = config
      self.CS(False)                      # Select chip
      nw=self.spi.write(buf)              # write config
      self.CS(True)

      self.RefR = 430.0
      self.R0  = 100.0

   def _RawToTemp(self, raw):
      RTD = (raw * self.RefR) / (32768)
      A = 3.908e-3
      B = -5.775e-7
      return (-A + math.sqrt(A*A - 4*B*(1-RTD/self.R0))) / (2*B), RTD

   def read(self):
      temp = self._read()
      return temp

   def _read(self):
       self.CS(False)
       nw=self.spi.write(bytes([0x01])) # first read address
       MSB = self.spi.read(1)           # multi-byte transfer
       LSB = self.spi.read(1)
       self.CS(True)

       raw = (MSB[0] << 8) + LSB[0]
       raw = raw >> 1
       # print( 'raw: ', raw)
       temp, RTD = self._RawToTemp(raw)
       return temp
       

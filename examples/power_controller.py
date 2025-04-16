import time
import board
import digitalio
import adafruit_pca9554

board.I2C().deinit()
i2c=board.I2C()

pc=adafruit_pca9554.PCA9554(i2c,address=int("38",16))

pc.write_gpio(adafruit_pca9554.CONFIGPORT, 0)

while True:
  for i in range(8):
    pc.write_pin((i-1)%8, 0)
    pc.write_pin(i,1)
    time.sleep(1)
board.I2C().deinit()

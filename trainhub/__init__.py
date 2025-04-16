import board
import atexit

_i2c = None

def get_i2c():
    global _i2c
    if _i2c is None:
        _i2c = board.I2C()
        atexit.register(shutdown_i2c)
    return _i2c

def shutdown_i2c():
    global _i2c
    if _i2c:
        _i2c.deinit()
        _i2c = None

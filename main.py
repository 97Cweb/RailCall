from railcall import get_i2c, shutdown_i2c
from railcall.power_controller import PowerController

i2c = get_i2c()

controller = PowerController(i2c, address=0x38, output_names=[
    "night_lights", "track_power", "aux1", "aux2", "aux3", "aux4", "aux5", "aux6"
])

controller["night_lights"].turn_on()

input("Press Enter to exit...\n")

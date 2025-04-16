import adafruit_pca9554
import atexit

class Output:
    def __init__(self, pca, pin_number, name):
        self.pca = pca
        self.pin_number = pin_number
        self.name = name
        self.pca.get_pin(pin_number).switch_to_output(value=False)

    def turn_on(self):
        self.pca.get_pin(self.pin_number).value = True
        print(f"[PowerController] {self.name} ON")

    def turn_off(self):
        self.pca.get_pin(self.pin_number).value = False
        print(f"[PowerController] {self.name} OFF")


class PowerController:
    def __init__(self, i2c, address, output_names=None):
        """
        One PCA9554-based power controller (up to 8 outputs)

        :param i2c: Shared I2C bus instance (e.g., from trainhub.get_i2c())
        :param address: I2C address of this controller
        :param output_names: Optional list of up to 8 output names
        """
        self.pca = adafruit_pca9554.PCA9554(i2c, address=address)

        self.pca.write_gpio(adafruit_pca9554.CONFIGPORT, 0)
        self.outputs = {}
        output_names = output_names or [f"out{i}" for i in range(8)]
        if len(output_names) > 8:
            raise ValueError("Only 8 outputs supported")

        for pin, name in enumerate(output_names):
            self.outputs[name] = Output(self.pca, pin, name)

        atexit.register(self._cleanup)

    def __getitem__(self, name):
        return self.outputs[name]

    def all_outputs(self):
        return list(self.outputs.values())
    
    def _cleanup(self):
        for output in self.outputs.values():
            try:
                output.turn_off()
            except Exception as e:
                print(f"[PowerController] Error during cleanup: {e}")

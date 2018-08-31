import tsl2591

class LightSensor:
    tsl

    def __init__(self):
        self.tsl = tsl2591.Tsl2591()
        pass

    def get_lux():
        full, ir = self.tsl.get_full_luminosity()
        lux = self.tsl.calculate_lux(full, ir)
        return lux

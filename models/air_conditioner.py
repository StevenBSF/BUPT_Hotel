class AirConditioner:
    MODES = ("cool", "heat")
    FAN_SPEEDS = ("low", "medium", "high")

    def __init__(self, ac_id: str, default_temp: int = 25):
        self.ac_id = ac_id
        self.current_temp = default_temp
        self.target_temp = default_temp
        self.mode = "standby"
        self.fan_speed = "medium"
        self.is_on = False

    def power_on(self):
        self.is_on = True
        self.mode = "cool"

    def set_temperature(self, temp: int):
        if 18 <= temp <= 30:
            self.target_temp = temp

    def set_fan_speed(self, speed: str):
        if speed in self.FAN_SPEEDS:
            self.fan_speed = speed

    def power_off(self):
        self.is_on = False
        self.mode = "standby"



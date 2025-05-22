from models.air_conditioner import AirConditioner
class ControlPanel:
    def __init__(self, panel_id: str, ac: AirConditioner):
        self.panel_id = panel_id
        self.ac = ac

    def press_power(self):
        if not self.ac.is_on:
            self.ac.power_on()
        else:
            self.ac.power_off()

    def adjust_temperature(self, temp: int):
        self.ac.set_temperature(temp)

    def adjust_fan_speed(self, speed: str):
        self.ac.set_fan_speed(speed)

    def display_status(self):
        return {
            "is_on": self.ac.is_on,
            "current": self.ac.current_temp,
            "target": self.ac.target_temp,
            "fan": self.ac.fan_speed,
        }

    def show_status(self, mode, target_temp, fan_speed, current_fee):
        """
        兼容旧接口：更新面板状态后，返回最新的 display_status
        """
        return self.display_status()
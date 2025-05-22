from models.air_conditioner import AirConditioner
from models.control_panel import ControlPanel

class Room:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.ac = AirConditioner(ac_id=room_id)
        self.control_panel = ControlPanel(panel_id=room_id, ac=self.ac)
# controllers/customer_controller.py
from services.air_conditioning_service import AirConditioningService

class CustomerController:
    def __init__(self, room_repo, usage_log_repo):
        # 只保存服务层对象
        self.ac_service = AirConditioningService(room_repo, usage_log_repo)

    def start_air_conditioning(self, customer_id: str, room_id: str, current_temp: float):
        """
        客户发送 StartAirConditioning(RoomId, CurrentTemp)
        返回 (Mode, TargetTemp, FeeRate, CurrentFee)
        """
        return self.ac_service.start_service(customer_id, room_id, current_temp)

    def change_temperature(self, room_id: str, target_temp: float):
        """
        客户发送 ChangeTemperature(RoomId, TargetTemp)
        返回 isSuccess: bool
        """
        return self.ac_service.change_temperature(room_id, target_temp)

    def change_fan_speed(self, room_id: str, speed_level: str):
        """
        客户发送 ChangeFanSpeed(RoomId, FanSpeedLevel)
        返回 UpdatedFeeRate: float
        """
        return self.ac_service.change_fan_speed(room_id, speed_level)

    def stop_air_conditioning(self, room_id: str):
        """
        客户发送 StopAirConditioning(RoomId)
        返回 (TotalFee, ServiceDuration)
        """
        return self.ac_service.stop_service(room_id)

    def query_current_temperature(self, room_id: str):
        """
        客户发送 QueryCurrentTemperature(RoomId)
        返回 (CurrentTemp, FeeRate, CurrentFee)
        """
        return self.ac_service.query_current_temperature(room_id)

    def query_current_fan_speed(self, room_id: str):
        """
        客户发送 QueryCurrentFanSpeed(RoomId)
        返回 (CurrentFanSpeed, FeeRate, CurrentFee)
        """
        return self.ac_service.query_current_fan_speed(room_id)

    def query_current_fee(self, room_id: str):
        """
        客户发送 QueryCurrentFee(RoomId)
        返回 (FeeRate, CurrentFee)
        """
        return self.ac_service.query_current_fee(room_id)

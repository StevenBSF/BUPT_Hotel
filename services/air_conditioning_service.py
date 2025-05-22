# import uuid
# from repositories.room_repository import RoomRepository
# from repositories.usage_log_repository import UsageLogRepository
# from repositories.usage_log import UsageLog
# from datetime import datetime
# from models.room import Room
#
# class AirConditioningService:
#     def __init__(self, room_repo, log_repo):
#         """
#         room_repo: repositories.RoomRepository
#         log_repo: repositories.UsageLogRepository
#         """
#         self.room_repo = room_repo
#         self.log_repo = log_repo
#         # 存储当前正在运行的服务，key=room_id, value=dict(service data)
#         self.active_services = {}
#
#     def start_service(self, customer_id: str, room_id: str, current_temp: float):
#         """
#         StartAirConditioning(RoomId, CurrentTemp) ->
#             Return(Mode, TargetTemp, FeeRate, CurrentFee)
#         """
#         room = self.room_repo.get_by_id(room_id)
#         if room_id in self.active_services:
#             raise RuntimeError(f"Room {room_id} already has an active service")
#
#         # 默认参数
#         default_temp = 25.0   # 缺省温度25度 :contentReference[oaicite:0]{index=0}
#         default_speed = 'medium'
#         default_rate = 1.0    # 1元/度 :contentReference[oaicite:1]{index=1}
#
#         # 根据 CurrentTemp 判断制冷/制热
#         mode = 'cooling' if current_temp > default_temp else 'heating'
#
#         service = {
#             'service_id': f"{room_id}-{int(datetime.now().timestamp())}",
#             'room_id': room_id,
#             'customer_id': customer_id,
#             'start_time': datetime.now(),
#             'initial_temp': current_temp,
#             'mode': mode,
#             'target_temp': default_temp,
#             'fan_speed': default_speed,
#             'fee_rate': default_rate,
#             'consumption': 0.0,
#         }
#         self.active_services[room_id] = service
#
#         # 在 AC 和面板上同步状态
#         room.ac.turn_on()
#         room.control_panel.show_status(
#             mode, default_temp, default_speed, 0.0
#         )
#
#         return mode, default_temp, default_rate, 0.0
#
#     def change_temperature(self, room_id: str, target_temp: float) -> bool:
#         """
#         ChangeTemperature(RoomId, TargetTemp) -> Return(isSuccess)
#         """
#         svc = self.active_services.get(room_id)
#         if not svc:
#             return False
#
#         svc['target_temp'] = target_temp
#         self.log_repo.add_log(
#             svc['service_id'], 'change_temp', target_temp, datetime.now()
#         )
#         return True
#
#     def change_fan_speed(self, room_id: str, speed_level: str) -> float:
#         """
#         ChangeFanSpeed(RoomId, FanSpeedLevel) -> Return(UpdatedFeeRate)
#         """
#         svc = self.active_services.get(room_id)
#         if not svc:
#             return 0.0
#
#         svc['fan_speed'] = speed_level
#         # 更新费率（示例：low=0.8, medium=1.0, high=1.2）
#         rate_map = {'low': 0.8, 'medium': 1.0, 'high': 1.2}
#         svc['fee_rate'] = rate_map.get(speed_level, svc['fee_rate'])
#         self.log_repo.add_log(
#             svc['service_id'], 'change_fan', speed_level, datetime.now()
#         )
#         return svc['fee_rate']
#
#     def stop_service(self, room_id: str):
#         """
#         StopAirConditioning(RoomId) -> Return(TotalFee, ServiceDuration)
#         """
#         svc = self.active_services.pop(room_id, None)
#         if not svc:
#             return 0.0, 0.0
#
#         end_time = datetime.now()
#         duration_min = (end_time - svc['start_time']).total_seconds() / 60.0
#
#         # 简化计费：按目标温差*费率计费
#         temp_diff = abs(svc['initial_temp'] - svc['target_temp'])
#         total_fee = temp_diff * svc['fee_rate']
#
#         self.log_repo.add_log(
#             svc['service_id'], 'stop', total_fee, end_time
#         )
#         return total_fee, duration_min



# services/air_conditioning_service.py
from models.usage_log import UsageLog
from datetime import datetime

class AirConditioningService:
    def __init__(self, room_repo, log_repo):
        self.room_repo = room_repo
        self.log_repo  = log_repo
        self.active_services = {}

    def start_service(self, customer_id: str, room_id: str, current_temp: float):
        room = self.room_repo.get_by_id(room_id)
        if room_id in self.active_services:
            raise RuntimeError(f"Room {room_id} already has an active service")

        # 默认设置
        default_temp  = 25
        default_speed = 'medium'
        default_rate  = 1.0

        # 调用空调方法：开机 & 设置温度、风速
        ac = room.ac
        ac.power_on()
        ac.set_temperature(default_temp)
        ac.set_fan_speed(default_speed)

        # 记录服务
        service = {
            'service_id': f"{room_id}-{int(datetime.now().timestamp())}",
            'room_id':    room_id,
            'customer_id':customer_id,
            'start_time': datetime.now(),
            'initial_temp': current_temp,
            'mode':       ac.mode,
            'target_temp':ac.target_temp,
            'fan_speed':  ac.fan_speed,
            'fee_rate':   default_rate,
            'consumption':0.0,
        }
        self.active_services[room_id] = service

        # # 同步面板显示
        # room.control_panel.show_status(
        #     ac.mode, ac.target_temp, ac.fan_speed, 0.0
        # )
        # return ac.mode, ac.target_temp, ac.fee_rate, 0.0  # fee_rate 字段需同步至 ac 或 service

        # # 同步面板显示（假设你已经在 ControlPanel 中实现了 show_status）
        # room.control_panel.show_status(ac.mode, ac.target_temp, ac.fan_speed, service['consumption'])
        # # 从 service 字典里取费率和当前消费
        # return (
        #         ac.mode,
        #         ac.target_temp,
        #         service['fee_rate'],
        #         service['consumption'],
        #     )

        # 同步面板显示：调用 display_status 而非不存在的 show_status
        panel_status = room.control_panel.display_status()
        print(f"[Panel] {panel_status}")

        # **正确地从 service 字典里取费率与当前费用**
        return (
            ac.mode,
            ac.target_temp,
            service['fee_rate'],  # ← 而不是 ac.fee_rate
            service['consumption'],  # ← 而不是硬写 0.0
        )

    def change_temperature(self, room_id: str, target_temp: float) -> bool:
        svc = self.active_services.get(room_id)
        if not svc:
            return False
        room = self.room_repo.get_by_id(room_id)
        ac = room.ac
        ac.set_temperature(int(target_temp))
        svc['target_temp'] = ac.target_temp
        # self.log_repo.add_log(svc['service_id'], 'change_temp', ac.target_temp, datetime.now())
        log = UsageLog(
            service_id=svc['service_id'],
            event='change_temp',
            value=ac.target_temp,
            timestamp=datetime.now()
        )
        self.log_repo.add_log(log)
        return True

    def change_fan_speed(self, room_id: str, speed_level: str) -> float:
        svc = self.active_services.get(room_id)
        if not svc:
            return 0.0
        room = self.room_repo.get_by_id(room_id)
        ac = room.ac
        ac.set_fan_speed(speed_level)
        svc['fan_speed'] = ac.fan_speed
        # 更新费率示例
        rate_map = {'low': 0.8, 'medium': 1.0, 'high': 1.2}
        svc['fee_rate'] = rate_map.get(ac.fan_speed, svc['fee_rate'])
        # self.log_repo.add_log(svc['service_id'], 'change_fan', ac.fan_speed, datetime.now())
        log = UsageLog(
            service_id=svc['service_id'],
            event='change_fan',
            value=svc['fee_rate'],
            timestamp=datetime.now()
        )
        self.log_repo.add_log(log)

        return svc['fee_rate']

    def stop_service(self, room_id: str):
        svc = self.active_services.pop(room_id, None)
        if not svc:
            return 0.0, 0.0
        room = self.room_repo.get_by_id(room_id)
        ac = room.ac
        ac.power_off()

        end_time = datetime.now()
        duration_min = (end_time - svc['start_time']).total_seconds() / 60.0
        temp_diff = abs(svc['initial_temp'] - svc['target_temp'])
        total_fee = temp_diff * svc['fee_rate']
        # self.log_repo.add_log(svc['service_id'], 'stop', total_fee, end_time)
        log = UsageLog(
            service_id=svc['service_id'],
            event='stop',
            value=total_fee,
            timestamp=end_time
        )
        self.log_repo.add_log(log)
        return total_fee, duration_min

    def query_current_temperature(self, room_id: str):
        """
        QueryCurrentTemperature(RoomId) -> Return(CurrentTemp, FeeRate, CurrentFee)
        """
        svc = self.active_services.get(room_id)
        if not svc:
            return None, 0.0, 0.0

        room = self.room_repo.get_by_id(room_id)
        return room.ac.current_temp, svc['fee_rate'], svc['consumption']

    def query_current_fan_speed(self, room_id: str):
        """
        QueryCurrentFanSpeed(RoomId) -> Return(CurrentFanSpeed, FeeRate, CurrentFee)
        """
        svc = self.active_services.get(room_id)
        if not svc:
            return None, 0.0, 0.0

        room = self.room_repo.get_by_id(room_id)
        return room.ac.fan_speed, svc['fee_rate'], svc['consumption']

    def query_current_fee(self, room_id: str):
        """
        QueryCurrentFee(RoomId) -> Return(FeeRate, CurrentFee)
        """
        svc = self.active_services.get(room_id)
        if not svc:
            return 0.0, 0.0

        return svc['fee_rate'], svc['consumption']
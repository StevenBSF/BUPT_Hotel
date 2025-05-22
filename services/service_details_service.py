# ------------------ services/service_details_service.py ------------------
from datetime import datetime
from models.service_details import ServiceDetails
from repositories.usage_log_repository import UsageLogRepository

class ServiceDetailsService:
    def __init__(self, log_repo: UsageLogRepository):
        self.log_repo = log_repo

    def generate_service_details(self, room_id: str, check_in: datetime, check_out: datetime):
        """
        GenerateServiceDetails(RoomId, CheckInTime, CheckOutTime) -> List[ServiceDetails]
        操作契约：
          1. 从 UsageLogRepository 获取指定房间和时间区间内的所有服务日志
          2. 按 service_id 分组后，为每个服务对象创建 ServiceDetails
          3. 返回 ServiceDetails 列表
        """
        # 1) 获取日志
        logs = self.log_repo.get_logs_for_room(room_id, check_in, check_out)
        # 2) 按 service_id 分组
        svc_groups = {}
        for log in logs:
            svc_groups.setdefault(log.service_id, []).append(log)
        # 3) 构造 ServiceDetails 列表
        details_list = []
        for service_id, group_logs in svc_groups.items():
            # 假设 UsageLogRepository 提供按照 ID 拿到完整 service 对象的方法
            service = self.log_repo.get_service_by_id(service_id)
            service.usage_logs = group_logs
            details = ServiceDetails(service)
            details_list.append(details)
        return details_list

    def print_service_details(self, room_id: str, service_details_list) -> bool:
        """
        PrintServiceDetails(RoomId, ServiceDetailsList) -> Return(PrintStatus)
        操作契约：
          1. 将 ServiceDetailsList 序列化写入文本文件
          2. 返回打印状态（True=成功, False=失败）
        """
        filename = f"service_details_{room_id}_{int(datetime.now().timestamp())}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for details in service_details_list:
                    f.write(str(details) + "\n\n")
            return True
        except IOError:
            return False

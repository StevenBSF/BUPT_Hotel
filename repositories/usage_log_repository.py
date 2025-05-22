# repositories/usage_log_repository.py

from datetime import datetime
from collections import defaultdict
from models.usage_log import UsageLog

class UsageLogRepository:
    def __init__(self):
        self.logs: list[UsageLog] = []

    def add_log(self, log: UsageLog) -> None:
        self.logs.append(log)

    def get_logs_for_service(self, service_id: str) -> list[UsageLog]:
        return [l for l in self.logs if l.service_id == service_id]

    def get_logs_for_room(self,
                          room_id: str,
                          start: datetime,
                          end: datetime) -> list[UsageLog]:
        """
        按时间区间和 service_id 前缀筛出本房间的所有日志
        """
        return [
            l for l in self.logs
            if start <= l.timestamp <= end
               and l.service_id.startswith(f"{room_id}-")
        ]

    def get_service_for_room(self,
                             room_id: str,
                             start: datetime,
                             end: datetime):
        """
        返回一个 Service 对象，保证不会是 None。
        Service 必须有：
          - service_id 属性
          - usage_logs 属性（list[UsageLog]）
          - calculate_fee() 方法（返回 float）
        """
        logs = self.get_logs_for_room(room_id, start, end)

        # 按 service_id 分组
        groups: dict[str, list[UsageLog]] = defaultdict(list)
        for l in logs:
            groups[l.service_id].append(l)

        # 找到第一个会话，如果没有任何日志，就造一个空会话
        if groups:
            sid, svc_logs = next(iter(groups.items()))
        else:
            sid, svc_logs = f"{room_id}-no-logs", []

        # 动态构造 Service 类
        class Service:
            def __init__(self, service_id: str, usage_logs: list[UsageLog]):
                self.service_id = service_id
                self.usage_logs = usage_logs

            def calculate_fee(self) -> float:
                # 账单金额＝所有日志 value 的总和
                return sum(log.value for log in self.usage_logs)

        return Service(sid, svc_logs)

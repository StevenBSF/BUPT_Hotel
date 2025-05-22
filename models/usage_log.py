# models/usage_log.py

from datetime import datetime

class UsageLog:
    """
    UsageLog 模型类，用于记录一次空调服务事件。
    Attributes:
        service_id (str): 服务流水号
        event (str):       事件类型，例如 'start', 'change_temp', 'change_fan', 'stop'
        value (float):     与事件相关的数值，例如温度、费率或费用
        timestamp (datetime): 事件发生时间
    """
    def __init__(self, service_id: str, event: str, value: float, timestamp: datetime):
        self.service_id = service_id
        self.event      = event
        self.value      = value
        self.timestamp  = timestamp

    def __repr__(self):
        return (
            f"UsageLog(service_id={self.service_id!r}, "
            f"event={self.event!r}, value={self.value}, "
            f"timestamp={self.timestamp!r})"
        )

    def __str__(self):
        # 格式化输出，方便打印到控制台或写入文件
        time_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"[{time_str}] Service {self.service_id}: {self.event} → {self.value}"

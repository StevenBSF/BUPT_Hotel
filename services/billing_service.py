from datetime import datetime
from models.invoice import Invoice
from repositories.usage_log_repository import UsageLogRepository

class BillingService:
    def __init__(self, log_repo: UsageLogRepository):
        self.log_repo = log_repo

    def calculate_fee(self, service_id: str) -> float:
        logs = self.log_repo.get_logs_for_service(service_id)
        return sum(log.consumption for log in logs)

    def generate_invoice(self, room_id: str, check_in: datetime, check_out: datetime) -> Invoice:
        """
        GenerateInvoice(RoomId, CheckInTime, CheckOutTime) -> Return(InvoiceData)
        操作契约：
          1. 从 UsageLogRepository 中获取该房间在时间区间内的服务记录
          2. 创建 Invoice 对象，并赋值所有属性（房间号、客户、时间区间、总费用等）
        """
        # 获取所有相关日志并封装为“服务对象”
        service = self.log_repo.get_service_for_room(room_id, check_in, check_out)
        invoice = Invoice(service)  # Invoice 构造时会计算总金额等 :contentReference[oaicite:0]{index=0}
        return invoice

    def print_invoice(self, room_id: str, invoice: Invoice) -> bool:
        """
        PrintInvoice(RoomId, InvoiceData) -> Return(PrintStatus)
        操作契约：
          1. 将 InvoiceData 序列化并写入文件（如 TXT 或 PDF）
          2. 返回打印状态（True=成功/False=失败）
        """
        filename = f"invoice_{room_id}_{invoice.service.service_id}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(str(invoice))
            return True
        except IOError:
            return False

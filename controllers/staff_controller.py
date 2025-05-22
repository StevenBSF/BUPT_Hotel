# ------------------ controllers/staff_controller.py ------------------
from datetime import datetime
from services.billing_service import BillingService
from services.service_details_service import ServiceDetailsService

class StaffController:
    def __init__(self,
                 billing_service: BillingService,
                 details_service: ServiceDetailsService):
        self.billing_service = billing_service
        self.details_service = details_service

    def generate_invoice(self, room_id: str, check_in_str: str, check_out_str: str):
        """
        前台发送 GenerateInvoice(RoomId, CheckInTime, CheckOutTime)
        返回 InvoiceData
        """
        # 假设前端传入的时间格式为 'YYYY-MM-DD HH:MM'
        check_in  = datetime.strptime(check_in_str,  "%Y-%m-%d %H:%M")
        check_out = datetime.strptime(check_out_str, "%Y-%m-%d %H:%M")
        return self.billing_service.generate_invoice(room_id, check_in, check_out)

    def print_invoice(self, room_id: str, invoice):
        """
        前台发送 PrintInvoice(RoomId, InvoiceData)
        返回 PrintStatus (bool)
        """
        return self.billing_service.print_invoice(room_id, invoice)

    def generate_service_details(self,
                                 room_id: str,
                                 check_in_str: str,
                                 check_out_str: str):
        """
        前台发送 GenerateServiceDetails(RoomId, CheckInTime, CheckOutTime)
        返回 ServiceDetailsList
        """
        check_in = datetime.strptime(check_in_str, "%Y-%m-%d %H:%M")
        check_out = datetime.strptime(check_out_str, "%Y-%m-%d %H:%M")
        return self.details_service.generate_service_details(
            room_id, check_in, check_out
        )

    def print_service_details(self,
                              room_id: str,
                              service_details_list) -> bool:
        """
        前台发送 PrintServiceDetails(RoomId, ServiceDetailsList)
        返回 PrintStatus
        """
        return self.details_service.print_service_details(
            room_id, service_details_list
        )
class FrontDeskStaff:
    def __init__(self, staff_id: str, name: str):
        self.staff_id = staff_id
        self.name = name

    def generate_invoice(self, service):
        from models.invoice import Invoice
        return Invoice(service)

    def generate_service_details(self, service):
        from models.service_details import ServiceDetails
        return ServiceDetails(service)
